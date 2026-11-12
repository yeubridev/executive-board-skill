#!/usr/bin/env python3
"""board.py — helper for the executive-board skill.

Scaffolds the boardroom, shows and installs curated skill stacks, and manages the
sub-agent lifecycle (hire -> deploy -> retire). Standard library only.

    board.py init     --project "Acme" [--depth standard] [--with-agents]
    board.py stack    <seat|archetype> [--tier core|recommended|optional|all] [--json]
    board.py install  <seat|archetype> [--tier core] [--via auto|skills|plugin] [--run]
    board.py catalog
    board.py hire     --archetype head-of-sales [--parent cmo] | --id X --title T --parent P --mission M
    board.py deploy   <agent-id> [--out .claude/agents]
    board.py retire   <agent-id>

Nothing is installed or executed unless --run is given.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_DIR / "assets" / "registry.json"
TEMPLATES = SKILL_DIR / "assets" / "templates"
AGENT_DEFS = SKILL_DIR / "assets" / "agents"

SEATS = {
    "ceo": ("CEO", "ceo"),
    "cto": ("CTO", "cto"),
    "cmo": ("CMO", "cmo"),
    "cfo": ("CFO", "cfo"),
    "coo": ("COO", "coo"),
    "head-of-design": ("Head of Design", "design"),
}
TIERS = ("core", "recommended", "optional")
MGMT_MARKER = "<!-- MANAGEMENT NOTES"
ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
DEFAULT_MAX_REPORTS, DEFAULT_MAX_DEPTH = 3, 2


# ----------------------------------------------------------------------------- utilities


def die(msg: str, code: int = 1) -> "None":
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def today() -> str:
    return _dt.date.today().isoformat()


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        die(f"registry not found at {REGISTRY_PATH}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def board_dir(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    for name in ("board", ".board"):
        if (Path(name) / "CHARTER.md").exists():
            return Path(name)
    return Path("board")


def require_board(arg: str | None) -> Path:
    d = board_dir(arg)
    if not (d / "ORG.md").exists():
        die(f"no boardroom at ./{d} — run `board.py init` first (or pass --dir)")
    return d


def fill(text: str, values: dict[str, str]) -> str:
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", val)
    return text


def project_name(bdir: Path) -> str:
    charter = bdir / "CHARTER.md"
    if charter.exists():
        first = charter.read_text(encoding="utf-8").splitlines()[0:1]
        if first and "—" in first[0]:
            return first[0].split("—", 1)[1].strip()
    return Path.cwd().name


def headcount_caps(bdir: Path) -> tuple[int, int]:
    charter = bdir / "CHARTER.md"
    if charter.exists():
        m = re.search(r"Headcount cap:\D*(\d+)\D+(\d+)", charter.read_text(encoding="utf-8"))
        if m:
            return int(m.group(1)), int(m.group(2))
    return DEFAULT_MAX_REPORTS, DEFAULT_MAX_DEPTH


# ----------------------------------------------------------------------------- ORG.md table


def _split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def org_rows(bdir: Path) -> list[dict]:
    """Rows of the Sub-agents table in ORG.md."""
    rows, in_table = [], False
    for line in (bdir / "ORG.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| Agent id"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                if line.strip():
                    in_table = False
                continue
            cells = _split_row(line)
            if set(cells[0]) <= {"-", ":", " "} or len(cells) < 8:
                continue
            rows.append(
                dict(id=cells[0], title=cells[1], parent=cells[2], mission=cells[3],
                     skills=cells[4], status=cells[5], since=cells[6], charter=cells[7])
            )
    return rows


def org_add_row(bdir: Path, row: dict) -> None:
    path = bdir / "ORG.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    new = "| {id} | {title} | {parent} | {mission} | {skills} | {status} | {since} | {charter} |".format(**row)
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("| Agent id"):
            insert_at = i + 2  # after header and separator
            while insert_at < len(lines) and lines[insert_at].startswith("|"):
                insert_at += 1
            break
    if insert_at is None:
        die("ORG.md has no Sub-agents table (a row starting with '| Agent id')")
    lines.insert(insert_at, new)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def org_set_status(bdir: Path, agent_id: str, status: str) -> bool:
    path = bdir / "ORG.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    changed, in_table = False, False
    for i, line in enumerate(lines):
        if line.startswith("| Agent id"):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            cells = _split_row(line)
            if cells and cells[0] == agent_id and len(cells) >= 8:
                cells[5] = status
                lines[i] = "| " + " | ".join(cells) + " |"
                changed = True
    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def depth_of(parent: str, rows: list[dict]) -> int:
    """Depth a new agent would have under `parent` (1 = direct report of a seat)."""
    by_id = {r["id"]: r for r in rows}
    depth, cur, seen = 1, parent, set()
    while cur not in SEATS:
        if cur in seen or cur not in by_id:
            die(f"parent '{parent}' is not a seat and has no row in ORG.md")
        seen.add(cur)
        cur = by_id[cur]["parent"]
        depth += 1
    return depth


# ----------------------------------------------------------------------------- charter files


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta: dict = {}
    for line in text[3:end].strip().splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, val = line.split(":", 1)
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            meta[key.strip()] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            meta[key.strip()] = val.strip("'\"")
    body = text[end + 4:].lstrip("\n")
    return meta, body


def set_frontmatter_value(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    end = text.find("\n---", 3)
    head, rest = text[:end], text[end:]
    if pattern.search(head):
        head = pattern.sub(f"{key}: {value}", head, count=1)
    else:
        head += f"\n{key}: {value}"
    return head + rest


def untrained_parts(prompt: str) -> list[str]:
    """Parts of a charter prompt the parent still has to write (empty sections and labels)."""
    label = re.compile(r"^\*\*([^*\n]+?):?\*\*(?: \([^)\n]*\))?:?[ \t]*$")
    inline = re.compile(r"^- \*\*([^*\n]+?):?\*\*[ \t]*$")
    missing: list[str] = []
    current, has_content, is_heading = None, True, False

    def close() -> None:
        if current and not has_content:
            missing.append(current)

    for line in prompt.splitlines():
        heading = re.match(r"^## +(.+)$", line)
        lab = label.match(line)
        if heading or lab:
            if lab and is_heading:
                has_content = True  # a section that holds labelled parts is not empty
            close()
            current, has_content, is_heading = (heading or lab).group(1).strip(), False, bool(heading)
            continue
        m = inline.match(line)
        if m:
            missing.append(m.group(1).strip())
            has_content = True
        elif line.strip():
            has_content = True
    close()
    return missing


# ----------------------------------------------------------------------------- stacks


def resolve_stack(reg: dict, target: str) -> tuple[str, list[dict]]:
    if target in reg.get("stacks", {}):
        return SEATS.get(target, (target,))[0], reg["stacks"][target]
    if target in reg.get("archetypes", {}):
        arch = reg["archetypes"][target]
        return arch["title"], [dict(e, tier=e.get("tier", "core")) for e in arch.get("stack", [])]
    known = sorted(list(reg.get("stacks", {})) + list(reg.get("archetypes", {})))
    die(f"unknown seat or archetype '{target}'. Known: {', '.join(known)}")
    return "", []


def filter_tier(entries: list[dict], tier: str) -> list[dict]:
    if tier == "all":
        return entries
    wanted = TIERS[: TIERS.index(tier) + 1]
    return [e for e in entries if e.get("tier", "core") in wanted]


def install_plan(reg: dict, entries: list[dict], via: str, scope_global: bool, agent: str | None) -> list[dict]:
    """One step per stack entry: {'source', 'kind', 'shell': [...], 'session': [...], 'note'}."""
    steps, seen_market, seen_cmd = [], set(), set()
    for e in entries:
        src = reg["sources"][e["source"]]
        inst = src.get("install", {})
        prefer = inst.get("prefer", "skills")
        order = {"auto": [prefer, "skills", "plugin", "manual"], "skills": ["skills", "plugin", "manual"],
                 "plugin": ["plugin", "skills", "manual"]}[via]
        plugins = e.get("plugins") or inst.get("plugins") or []
        market = inst.get("marketplace")
        step = dict(source=e["source"], kind=None, shell=[], session=[], note=inst.get("note", ""))
        for kind in order:
            if kind == "skills" and inst.get("skills_cli"):
                cmd = ["npx", "-y", "skills", "add", inst["skills_cli"]]
                names = [] if e.get("whole_repo") else [n for n in e.get("skills", []) if not n.startswith("/")]
                if names:
                    cmd += ["--skill"] + names
                if agent:
                    cmd += ["--agent", agent]
                if scope_global:
                    cmd += ["--global"]
                cmd += ["--yes"]
                step.update(kind="skills", shell=[cmd])
                break
            if kind == "plugin" and (plugins or market):
                if market and market not in seen_market:
                    step["shell"].append(["claude", "plugin", "marketplace", "add", market])
                    step["session"].append(f"/plugin marketplace add {market}")
                    seen_market.add(market)
                for pl in plugins:
                    if pl in seen_cmd:
                        continue
                    seen_cmd.add(pl)
                    step["shell"].append(["claude", "plugin", "install", pl])
                    step["session"].append(f"/plugin install {pl}")
                if not plugins:
                    step["session"].append("/plugin    (then choose: " + ", ".join(e.get("skills", [])) + ")")
                step["kind"] = "plugin"
                break
            if kind == "manual" and inst.get("manual"):
                step.update(kind="manual", session=list(inst["manual"]))
                break
        if step["kind"] is None:
            step.update(kind="manual", session=[f"see {src['url']}"])
        steps.append(step)
    return steps


# ----------------------------------------------------------------------------- commands


def cmd_init(args: argparse.Namespace) -> None:
    bdir = Path(args.dir or "board")
    name = args.project or Path.cwd().name
    values = {
        "PROJECT_NAME": name, "DATE": today(), "DEPTH": args.depth, "SEAT": "board.py",
        "MAX_REPORTS": str(args.max_reports), "MAX_DEPTH": str(args.max_depth),
    }
    created = []
    bdir.mkdir(parents=True, exist_ok=True)
    for sub in ["decisions", "requests", "agents"] + [folder for _, folder in SEATS.values()]:
        (bdir / sub).mkdir(exist_ok=True)
        keep = bdir / sub / ".gitkeep"
        if not any((bdir / sub).iterdir()):
            keep.touch()
    for tpl in ("CHARTER.md", "STATUS.md", "ORG.md"):
        dest = bdir / tpl
        if dest.exists():
            continue
        dest.write_text(fill((TEMPLATES / tpl).read_text(encoding="utf-8"), values), encoding="utf-8")
        created.append(str(dest))
    index = bdir / "DECISIONS.md"
    if not index.exists():
        index.write_text(
            f"# Decision Log — {name}\n\n> Owner: CEO. One line per decision, newest first. "
            "Full records live in `decisions/`.\n\n"
            "| # | Date | Decision | Decides | Door | Status |\n|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
        created.append(str(index))
    out = Path(".claude/agents")
    in_claude_code = bool(os.environ.get("CLAUDECODE")) or Path(".claude").is_dir()
    if args.with_agents or in_claude_code:
        fresh_dir = not out.exists()
        out.mkdir(parents=True, exist_ok=True)
        if args.with_agents:
            for src in sorted(AGENT_DEFS.glob("*.md")):
                dest = out / src.name
                if not dest.exists():
                    shutil.copyfile(src, dest)
                    created.append(str(dest))
        if fresh_dir:
            print("note: .claude/agents/ was just created. Claude Code only watches agent folders that existed "
                  "when the session started — restart the session once so new agents load on their own.")
    print(f"Boardroom ready at ./{bdir} ({len(created)} file(s) created).")
    for c in created:
        print(f"  + {c}")
    print("Next: interview the founder and fill CHARTER.md (references/kickoff.md, Phase 0).")


def cmd_stack(args: argparse.Namespace) -> None:
    reg = load_registry()
    title, entries = resolve_stack(reg, args.target)
    entries = filter_tier(entries, args.tier)
    if args.json:
        out = [dict(e, **{"source_info": reg["sources"][e["source"]]}) for e in entries]
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return
    print(f"{title} — skill stack (registry checked {reg.get('verified_on', '?')})\n")
    for tier in TIERS:
        group = [e for e in entries if e.get("tier", "core") == tier]
        if not group:
            continue
        print(tier.upper())
        for e in group:
            src = reg["sources"][e["source"]]
            skills = ", ".join(e.get("skills", [])) or "(whole pack)"
            alt = f"  (alternative to {e['alternative_to']})" if e.get("alternative_to") else ""
            print(f"  {e['source']}  [{src.get('license', '?')}]{alt}")
            print(f"      skills: {skills}")
            if e.get("phase"):
                print(f"      phase:  {e['phase']}")
            print(f"      use:    {e.get('use', src.get('summary', ''))}")
        print()
    print(f"Install: board.py install {args.target} [--tier all] [--run]")


def cmd_install(args: argparse.Namespace) -> None:
    reg = load_registry()
    title, entries = resolve_stack(reg, args.target)
    entries = filter_tier(entries, args.tier)
    alternatives = [e for e in entries if e.get("alternative_to")]
    if not args.with_alternatives:
        entries = [e for e in entries if not e.get("alternative_to")]
    steps = install_plan(reg, entries, args.via, args.scope_global, args.agent)
    print(f"Install plan — {title}, tier: {args.tier} ({len(steps)} step(s))")
    print("Curated, not audited: read a skill before you rely on it (references/skill-vetting.md).\n")
    for s in steps:
        print(f"# {s['source']}  ({s['kind']})")
        if s["kind"] == "skills":
            for c in s["shell"]:
                print("  " + shlex.join(c))
        elif s["kind"] == "plugin":
            for line in s["session"]:
                print("  " + line)
            print("  (shell equivalent: " + " && ".join(shlex.join(c) for c in s["shell"]) + ")")
        else:
            for line in s["session"]:
                print("  " + line + "    [manual]")
        if s["note"]:
            print(f"  note: {s['note']}")
        print()
    if alternatives and not args.with_alternatives:
        print("Alternatives left out (they replace another entry; installing both makes them fight):")
        for e in alternatives:
            print(f"  {e['source']}  instead of  {e['alternative_to']}")
        print("  Include them with --with-alternatives only if you are dropping the entry they replace.\n")
    if not args.run:
        print("Dry run. Re-run with --run to execute the skills-CLI and plugin commands.")
        return
    failures = 0
    for s in steps:
        if s["kind"] == "manual":
            print(f"skip (manual): {s['source']}")
            continue
        for c in s["shell"]:
            if shutil.which(c[0]) is None:
                print(f"skip ({c[0]} not on PATH): {shlex.join(c)}")
                failures += 1
                continue
            print(f"$ {shlex.join(c)}")
            rc = subprocess.run(c).returncode
            if rc != 0:
                print(f"  -> exit {rc}")
                failures += 1
    print("Done." if not failures else f"Done with {failures} failed or skipped command(s).")
    sys.exit(1 if failures else 0)


def cmd_catalog(_: argparse.Namespace) -> None:
    reg = load_registry()
    by_parent: dict[str, list] = {}
    for aid, a in reg.get("archetypes", {}).items():
        by_parent.setdefault(a["parent"], []).append((aid, a))
    for seat, (title, _) in SEATS.items():
        if seat not in by_parent:
            continue
        print(f"{title}")
        for aid, a in by_parent[seat]:
            print(f"  {aid:<24} {a['title']} — {a['mission']}")
        print()


def cmd_hire(args: argparse.Namespace) -> None:
    bdir = require_board(args.dir)
    reg = load_registry()
    arch = None
    if args.archetype:
        arch = reg.get("archetypes", {}).get(args.archetype)
        if not arch:
            die(f"unknown archetype '{args.archetype}'. Run `board.py catalog`.")
    agent_id = args.id or args.archetype
    title = args.title or (arch and arch["title"])
    parent = args.parent or (arch and arch["parent"])
    mission = args.mission or (arch and arch["mission"])
    if not (agent_id and title and parent and mission):
        die("need --archetype, or all of --id, --title, --parent, --mission")
    if not ID_RE.match(agent_id) or len(agent_id) > 48:
        die("agent id must be lowercase letters, digits and single hyphens (e.g. head-of-sales)")
    if agent_id in SEATS:
        die(f"'{agent_id}' is a board seat, not a sub-agent")

    rows = org_rows(bdir)
    live = [r for r in rows if r["status"] in ("probation", "active")]
    if any(r["id"] == agent_id for r in live):
        die(f"'{agent_id}' already exists in ORG.md")
    max_reports, max_depth = headcount_caps(bdir)
    depth = depth_of(parent, live)
    reports = sum(1 for r in live if r["parent"] == parent)
    problems = []
    if reports >= max_reports:
        problems.append(f"'{parent}' already has {reports} report(s); the cap is {max_reports}")
    if depth > max_depth:
        problems.append(f"this hire would sit {depth} levels below the board; the cap is {max_depth}")
    if problems and not args.force:
        die("; ".join(problems) + ". Retire an agent, or get a COO decision and re-run with --force.")

    if arch and not args.skills:
        stack = arch.get("stack", [])
    else:
        stack = []
        for item in (args.skills or "").split(","):
            item = item.strip()
            if not item:
                continue
            source, _, skill = item.partition(":")
            stack.append({"source": source, "skills": [skill] if skill else [], "use": ""})
    table = ["| Skills | Source | Use them when |", "|---|---|---|"]
    skill_names = []
    for e in stack:
        names = e.get("skills") or []
        use = e.get("use") or "<!-- parent: say when -->"
        cell = ", ".join(f"`{n}`" for n in names) or "(whole pack)"
        table.append(f"| {cell} | {e['source']} | {use} |")
        skill_names += names
    if len(table) == 2:
        table.append("| <!-- none yet --> | | |")

    parent_title = SEATS[parent][0] if parent in SEATS else next(
        (r["title"] for r in rows if r["id"] == parent), parent)
    deliverables = "\n".join(f"- {d}" for d in (arch or {}).get("deliverables", [])) or "- <!-- parent: list the deliverables -->"
    description = args.description or f"{title}, reporting to the {parent_title}. {mission}"
    values = {
        "AGENT_ID": agent_id, "TITLE": title, "PARENT": parent, "PARENT_TITLE": parent_title,
        "DATE": today(), "DESCRIPTION": description.replace("\n", " "),
        "PROJECT_NAME": project_name(bdir), "MISSION": mission, "DELIVERABLES": deliverables,
        "SKILLS_TABLE": "\n".join(table),
        "CALIBRATION": (arch or {}).get("calibration", "<!-- parent: one small, real, typical task -->"),
    }
    charter = bdir / "agents" / f"{agent_id}.md"
    if charter.exists() and not args.force:
        die(f"{charter} already exists (use --force to overwrite)")
    charter.parent.mkdir(parents=True, exist_ok=True)
    charter.write_text(fill((TEMPLATES / "agent-charter.md").read_text(encoding="utf-8"), values), encoding="utf-8")
    (bdir / "agents" / agent_id).mkdir(exist_ok=True)
    org_add_row(bdir, dict(
        id=agent_id, title=title, parent=parent, mission=mission.replace("|", "/"),
        skills=(", ".join(skill_names[:6]) + (f" +{len(skill_names) - 6} more" if len(skill_names) > 6 else "")) or "—",
        status="probation", since=today(),
        charter=f"agents/{agent_id}.md",
    ))
    print(f"Hired {title} ({agent_id}) under {parent} — status: probation.")
    print(f"  charter: {charter}")
    print("Next, as the parent (references/hiring.md):")
    print("  1. Fill the charter: context digest, procedure, standards, 'use it when' for each skill.")
    print(f"  2. Install its skills:  board.py install {args.archetype or '<seat>'} [--run]" if arch else
          "  2. Install its skills (see references/skill-vetting.md).")
    print(f"  3. Deploy it:           board.py deploy {agent_id}")
    print("  4. Run the calibration task, review, then set status to active.")


def cmd_deploy(args: argparse.Namespace) -> None:
    bdir = require_board(args.dir)
    charter = bdir / "agents" / f"{args.agent_id}.md"
    if not charter.exists():
        die(f"no charter at {charter}")
    meta, body = parse_frontmatter(charter.read_text(encoding="utf-8"))
    if meta.get("status") == "retired":
        die(f"'{args.agent_id}' is retired")
    prompt = body.split(MGMT_MARKER, 1)[0].rstrip() + "\n"
    prompt = re.sub(r"^[ \t]*<!--.*?-->[ \t]*\n", "", prompt, flags=re.DOTALL | re.MULTILINE)
    prompt = re.sub(r"[ \t]*<!--.*?-->", "", prompt, flags=re.DOTALL)
    prompt = re.sub(r"\n{3,}", "\n\n", prompt)
    unfilled = untrained_parts(prompt)
    if unfilled and not args.allow_untrained:
        print(f"Not deployed: the parent has not written these parts of {charter}:", file=sys.stderr)
        for part in unfilled:
            print(f"  - {part}", file=sys.stderr)
        print("An agent deployed without them will guess. Fill them in (references/hiring.md, step 4), "
              "or pass --allow-untrained.", file=sys.stderr)
        sys.exit(2)
    fm = ["---", f"name: {meta.get('id', args.agent_id)}",
          "description: " + json.dumps(meta.get("description", meta.get("title", args.agent_id)), ensure_ascii=False)]
    model = meta.get("model", "inherit")
    if model:
        fm.append(f"model: {model}")
    if meta.get("tools"):
        fm.append(f"tools: {meta['tools']}")
    preload = meta.get("preload_skills") or []
    if isinstance(preload, str):
        preload = [preload]
    if preload:
        fm.append("skills:")
        fm += [f"  - {s}" for s in preload]
    fm.append("---")
    out_dir = Path(args.out)
    fresh_dir = not out_dir.exists()
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{args.agent_id}.md"
    dest.write_text("\n".join(fm) + "\n\n" + prompt, encoding="utf-8")
    print(f"Deployed {args.agent_id} -> {dest}")
    if unfilled:
        print(f"warning: deployed with {len(unfilled)} part(s) unwritten: {'; '.join(unfilled)}")
    if fresh_dir:
        print(f"note: {out_dir}/ was just created — restart the Claude Code session so it is picked up. "
              "After that, new and edited agent files load within seconds.")


def cmd_retire(args: argparse.Namespace) -> None:
    bdir = require_board(args.dir)
    charter = bdir / "agents" / f"{args.agent_id}.md"
    if not charter.exists():
        die(f"no charter at {charter}")
    charter.write_text(set_frontmatter_value(charter.read_text(encoding="utf-8"), "status", "retired"), encoding="utf-8")
    in_org = org_set_status(bdir, args.agent_id, "retired")
    runtime = Path(args.out) / f"{args.agent_id}.md"
    removed = False
    if runtime.exists():
        runtime.unlink()
        removed = True
    print(f"Retired {args.agent_id}: charter kept at {charter}"
          f"{', ORG.md updated' if in_org else ', no ORG.md row found'}"
          f"{', runtime file removed' if removed else ''}.")
    reports = [r["id"] for r in org_rows(bdir) if r["parent"] == args.agent_id and r["status"] != "retired"]
    if reports:
        print(f"warning: these agents still report to it: {', '.join(reports)} — reassign or retire them.")


# ----------------------------------------------------------------------------- cli


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="board.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("init", help="create the board/ folder in the current project")
    s.add_argument("--project", help="project name (default: current folder name)")
    s.add_argument("--dir", help="boardroom folder (default: board)")
    s.add_argument("--depth", choices=("sprint", "standard", "deep"), default="standard")
    s.add_argument("--max-reports", type=int, default=DEFAULT_MAX_REPORTS)
    s.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH)
    s.add_argument("--with-agents", action="store_true",
                   help="also copy the six executive agent definitions into .claude/agents/")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("stack", help="show the curated skill stack of a seat or archetype")
    s.add_argument("target")
    s.add_argument("--tier", choices=TIERS + ("all",), default="all")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_stack)

    s = sub.add_parser("install", help="print (or with --run, execute) the install commands for a stack")
    s.add_argument("target")
    s.add_argument("--tier", choices=TIERS + ("all",), default="core")
    s.add_argument("--via", choices=("auto", "skills", "plugin"), default="auto",
                   help="auto = each source's preferred method; skills = force the skills CLI (any agent)")
    s.add_argument("--agent", help="target agent for the skills CLI (e.g. claude-code, codex, cursor)")
    s.add_argument("--global", dest="scope_global", action="store_true", help="install for the user, not the project")
    s.add_argument("--with-alternatives", action="store_true",
                   help="also install entries marked as an alternative to another one")
    s.add_argument("--run", action="store_true", help="execute instead of printing")
    s.set_defaults(func=cmd_install)

    s = sub.add_parser("catalog", help="list sub-agent archetypes by parent seat")
    s.set_defaults(func=cmd_catalog)

    s = sub.add_parser("hire", help="create a sub-agent charter and its ORG.md row")
    s.add_argument("--archetype", help="start from a catalog archetype")
    s.add_argument("--id", help="agent id, kebab-case")
    s.add_argument("--title")
    s.add_argument("--parent", help="seat or agent id it reports to")
    s.add_argument("--mission")
    s.add_argument("--description", help="one line used to route work to this agent")
    s.add_argument("--skills", help="comma-separated source:skill pairs, e.g. owner/repo:skill-name")
    s.add_argument("--dir")
    s.add_argument("--force", action="store_true", help="override headcount caps or overwrite a charter")
    s.set_defaults(func=cmd_hire)

    s = sub.add_parser("deploy", help="render a charter into a runtime agent file")
    s.add_argument("agent_id")
    s.add_argument("--out", default=".claude/agents")
    s.add_argument("--dir")
    s.add_argument("--allow-untrained", action="store_true",
                   help="deploy even if the parent has not written every section of the charter")
    s.set_defaults(func=cmd_deploy)

    s = sub.add_parser("retire", help="retire a sub-agent (charter is kept)")
    s.add_argument("agent_id")
    s.add_argument("--out", default=".claude/agents")
    s.add_argument("--dir")
    s.set_defaults(func=cmd_retire)

    args = p.parse_args(argv)
    try:
        args.func(args)
    except BrokenPipeError:  # output piped into head, less, ...
        sys.stderr.close()


if __name__ == "__main__":
    main()
