#!/usr/bin/env python3
"""Regenerate everything derived from the registry, and validate the skill.

    python tools/build.py           # write generated files
    python tools/build.py --check   # exit 1 if anything is stale or invalid (CI)

Generated from skills/executive-board/assets/registry.json:
  - the STACK block inside each references/roles/<seat>.md
  - references/sub-agent-catalog.md
  - STACKS.md (repository root) and the CORE / ARCHETYPES tables in README.md
  - agents/*.md (plugin copies of assets/agents/*.md)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "executive-board"
sys.path.insert(0, str(SKILL / "scripts"))
import board  # noqa: E402

START = "<!-- STACK:START"
END = "<!-- STACK:END -->"
TIER_TITLES = {
    "core": "Core — install at kickoff",
    "recommended": "Recommended — install when its phase starts",
    "optional": "Optional — only in the situation named",
}
ALLOWED_FRONTMATTER = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def source_link(reg: dict, sid: str) -> str:
    return f"[{sid}]({reg['sources'][sid]['url']})"


def skills_cell(entry: dict) -> str:
    return ", ".join(f"`{s}`" for s in entry.get("skills", [])) or "(whole pack)"


def install_block(reg: dict, entries: list[dict]) -> list[str]:
    lines = ["```text"]
    for step in board.install_plan(reg, entries, "auto", False, None):
        lines.append(f"# {step['source']}")
        if step["kind"] == "skills":
            lines += [" ".join(c) for c in step["shell"]]
        else:
            lines += step["session"]
    lines.append("```")
    return lines


def stack_block(reg: dict, seat: str) -> str:
    entries = reg["stacks"][seat]
    out = [
        f"{START} — generated from assets/registry.json by tools/build.py; edit the registry, not this block -->",
        "",
        f"Registry checked {reg['verified_on']}. Curated, not audited — read "
        "[skill-vetting.md](../skill-vetting.md) before the first install.",
        "",
    ]
    for tier in board.TIERS:
        group = [e for e in entries if e.get("tier", "core") == tier]
        if not group:
            continue
        out += [f"**{TIER_TITLES[tier]}**", "", "| Skills | From | Phase | Use it for |", "|---|---|---|---|"]
        for e in group:
            lic = reg["sources"][e["source"]].get("license", "")
            use = e.get("use", "")
            if e.get("alternative_to"):
                use = f"*Alternative to {e['alternative_to']} — install one, not both.* {use}"
            out.append(f"| {skills_cell(e)} | {source_link(reg, e['source'])} · {lic} | {e.get('phase', '')} | {use} |")
        out.append("")
    out += [
        "**Install**",
        "",
        f"`python <skill-dir>/scripts/board.py install {seat}` prints the core tier; add `--tier all` for "
        "everything, `--run` to execute, `--via skills --agent <name>` for agents other than Claude Code. "
        "The same commands, for runtimes without scripts:",
        "",
    ]
    for tier in board.TIERS:
        group = [e for e in entries if e.get("tier", "core") == tier and not e.get("alternative_to")]
        if group:
            out += [f"*{tier.capitalize()}*", ""] + install_block(reg, group) + [""]
    alts = [e for e in entries if e.get("alternative_to")]
    if alts:
        out += ["*Alternatives (instead of the entry they replace)*", ""] + install_block(reg, alts) + [""]
    notes = []
    for sid in dict.fromkeys(e["source"] for e in entries):
        note = reg["sources"][sid].get("install", {}).get("note")
        if note:
            notes.append(f"- **{sid}** — {note}")
    if notes:
        out += ["**Notes**", ""] + notes + [""]
    out.append(END)
    return "\n".join(out)


def render_role(reg: dict, seat: str, text: str) -> str:
    if START not in text or END not in text:
        raise SystemExit(f"roles/{seat}.md has no STACK markers")
    head = text[: text.index(START)]
    tail = text[text.index(END) + len(END):]
    return head + stack_block(reg, seat) + tail


def render_catalog(reg: dict) -> str:
    out = [
        "# Sub-agent catalog",
        "",
        "<!-- Generated from assets/registry.json by tools/build.py. Edit the registry, not this file. -->",
        "",
        "Ready-made archetypes for the sub-agents a seat most often hires: mission, deliverables, a",
        "pre-selected skill stack, and a calibration task. An archetype is a starting point. The parent",
        "still writes the context digest, the procedure and the standards — see [hiring.md](hiring.md).",
        "",
        "```bash",
        "python <skill-dir>/scripts/board.py hire --archetype <id>      # charter + ORG.md row",
        "python <skill-dir>/scripts/board.py install <id> [--run]       # its skills",
        "python <skill-dir>/scripts/board.py deploy <id>                # runtime agent file",
        "```",
        "",
        "Nothing here fits? Hire from scratch with `--id --title --parent --mission`, pick skills from",
        "your own stack, and vet anything new with [skill-vetting.md](skill-vetting.md).",
        "",
        "## Contents",
        "",
    ]
    by_parent: dict[str, list] = {}
    for aid, a in reg["archetypes"].items():
        by_parent.setdefault(a["parent"], []).append((aid, a))
    for seat, (title, _) in board.SEATS.items():
        if seat in by_parent:
            names = ", ".join(f"[{a['title']}](#{aid})" for aid, a in by_parent[seat])
            out.append(f"- **{title}:** {names}")
    out.append("")
    for seat, (title, _) in board.SEATS.items():
        if seat not in by_parent:
            continue
        out += [f"## Reporting to the {title}", ""]
        for aid, a in by_parent[seat]:
            out += [f"### {aid}", "", f"**{a['title']}** — {a['mission']}", "", "Delivers:", ""]
            out += [f"- {d}" for d in a["deliverables"]]
            out += ["", "| Skills | From | Use them when |", "|---|---|---|"]
            for e in a["stack"]:
                out.append(f"| {skills_cell(e)} | {source_link(reg, e['source'])} | {e.get('use', '')} |")
            out += ["", f"Calibration task: {a['calibration']}", ""]
    return "\n".join(out).rstrip() + "\n"


def render_stacks_md(reg: dict) -> str:
    out = [
        "# Skill stacks",
        "",
        "<!-- Generated from skills/executive-board/assets/registry.json by tools/build.py. -->",
        "",
        f"Every third-party skill the executive board recommends, by seat. Checked {reg['verified_on']}:",
        "repository, licence, skill names and install commands were read from each repository on that",
        "date. **Curated, not audited** — these projects change, and a skill runs with your agent's",
        "permissions. Read what you install.",
        "",
        "Tiers: **core** (install at kickoff) · **recommended** (install when its phase starts) ·",
        "**optional** (only in the situation named).",
        "",
    ]
    for seat, (title, _) in board.SEATS.items():
        out += [f"## {title}", "", "| Tier | Skills | From | Use it for |", "|---|---|---|---|"]
        for e in reg["stacks"][seat]:
            use = e.get("use", "")
            if e.get("alternative_to"):
                use = f"*Alternative to {e['alternative_to']}.* {use}"
            out.append(f"| {e.get('tier', 'core')} | {skills_cell(e)} | {source_link(reg, e['source'])} | {use} |")
        out.append("")
    out += ["## Sub-agent archetypes", "", "| Archetype | Reports to | Skills from |", "|---|---|---|"]
    for aid, a in reg["archetypes"].items():
        srcs = ", ".join(source_link(reg, e["source"]) for e in a["stack"])
        out.append(f"| {a['title']} (`{aid}`) | {board.SEATS[a['parent']][0]} | {srcs} |")
    out += ["", "## Sources", "", "| Repository | Licence | Stars | What it is |", "|---|---|---|---|"]
    for sid, s in sorted(reg["sources"].items(), key=lambda kv: kv[0].lower()):
        out.append(f"| {source_link(reg, sid)} | {s.get('license', '')} | {s.get('stars', '')} | {s['summary']} |")
    out.append("")
    return "\n".join(out)


def replace_block(text: str, name: str, body: str) -> str:
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    if start not in text or end not in text:
        raise SystemExit(f"README.md has no {name} markers")
    return text[: text.index(start) + len(start)] + "\n" + body + "\n" + text[text.index(end):]


def render_readme(reg: dict, text: str) -> str:
    core = ["| Seat | Core stack |", "|---|---|"]
    for seat, (title, _) in board.SEATS.items():
        cells = []
        for e in (e for e in reg["stacks"][seat] if e.get("tier") == "core"):
            names = e.get("skills", [])
            shown = ", ".join(f"`{n}`" for n in names[:3]) + (" …" if len(names) > 3 else "")
            cells.append(f"{source_link(reg, e['source'])} — {shown}")
        core.append(f"| **{title}** | {'<br/>'.join(cells)} |")
    text = replace_block(text, "CORE", "\n".join(core))
    arch = ["| Reports to | Archetype | Mission |", "|---|---|---|"]
    for seat, (title, _) in board.SEATS.items():
        for aid, a in reg["archetypes"].items():
            if a["parent"] == seat:
                arch.append(f"| {title} | {a['title']} (`{aid}`) | {a['mission']} |")
    return replace_block(text, "ARCHETYPES", "\n".join(arch))


def plugin_agent(text: str) -> str:
    """Plugin copies load the skill by its namespaced name."""
    return text.replace("  - executive-board\n", "  - executive-board:executive-board\n")


# ----------------------------------------------------------------------------- validation


def validate(reg: dict) -> list[str]:
    errors = []
    srcs = reg["sources"]
    for seat in board.SEATS:
        if seat not in reg["stacks"]:
            errors.append(f"registry: no stack for seat '{seat}'")
        if not (SKILL / "references" / "roles" / f"{seat}.md").exists():
            errors.append(f"missing role file for '{seat}'")
        if not (SKILL / "assets" / "agents" / f"{seat}.md").exists():
            errors.append(f"missing agent definition for '{seat}'")
    for where, entries in [(f"stacks.{k}", v) for k, v in reg["stacks"].items()] + [
        (f"archetypes.{k}", a["stack"]) for k, a in reg["archetypes"].items()
    ]:
        for e in entries:
            if e["source"] not in srcs:
                errors.append(f"{where}: unknown source {e['source']}")
            if e.get("tier", "core") not in board.TIERS:
                errors.append(f"{where}: bad tier {e.get('tier')}")
            if e.get("alternative_to") and e["alternative_to"] not in srcs:
                errors.append(f"{where}: alternative_to unknown source {e['alternative_to']}")
    for aid, a in reg["archetypes"].items():
        if a["parent"] not in board.SEATS:
            errors.append(f"archetype {aid}: parent {a['parent']} is not a seat")
        if not board.ID_RE.match(aid):
            errors.append(f"archetype {aid}: bad id")
        for key in ("title", "mission", "deliverables", "calibration", "stack"):
            if not a.get(key):
                errors.append(f"archetype {aid}: missing {key}")
    for where, entries in [(f"stacks.{k}", v) for k, v in reg["stacks"].items()] + [
        (f"archetypes.{k}", a["stack"]) for k, a in reg["archetypes"].items()
    ]:
        for e in entries:
            inst = srcs.get(e["source"], {}).get("install", {})
            if not (inst.get("skills_cli") or e.get("plugins") or inst.get("plugins")
                    or inst.get("marketplace") or inst.get("manual")):
                errors.append(f"{where}: {e['source']} has no install route")
    for sid, s in srcs.items():
        for key in ("url", "summary", "license"):
            if not s.get(key):
                errors.append(f"source {sid}: missing {key}")

    skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    meta, body = board.parse_frontmatter(skill_md)
    fm_keys = set(re.findall(r"^([A-Za-z_-]+):", skill_md.split("\n---", 1)[0], re.MULTILINE))
    extra = fm_keys - ALLOWED_FRONTMATTER
    if extra:
        errors.append(f"SKILL.md: frontmatter keys outside the portable set: {sorted(extra)}")
    if meta.get("name") != SKILL.name:
        errors.append("SKILL.md: name must match the folder name")
    desc = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", skill_md.split("\n---", 1)[0], re.MULTILINE | re.DOTALL)
    desc_text = " ".join(desc.group(1).replace(">-", "").replace(">", "").split()) if desc else ""
    if not 50 <= len(desc_text) <= 1024:
        errors.append(f"SKILL.md: description is {len(desc_text)} characters (must be 50-1024)")
    if len(skill_md.splitlines()) > 500:
        errors.append("SKILL.md: over 500 lines")

    link_re = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
    for md in list(SKILL.rglob("*.md")):
        if "templates" in md.parts:
            continue
        for target in link_re.findall(md.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("mailto:"):
                continue
            if not (md.parent / target).resolve().exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link {target}")
    for ref in sorted((SKILL / "references").rglob("*.md")):
        rel = ref.relative_to(SKILL).as_posix()
        if rel not in skill_md:
            errors.append(f"SKILL.md does not link {rel} (every reference must be one hop away)")
    return errors


# ----------------------------------------------------------------------------- main


def main() -> int:
    check = "--check" in sys.argv[1:]
    reg = board.load_registry()
    targets: dict[Path, str] = {}
    for seat in board.SEATS:
        path = SKILL / "references" / "roles" / f"{seat}.md"
        if path.exists():
            targets[path] = render_role(reg, seat, path.read_text(encoding="utf-8"))
    targets[SKILL / "references" / "sub-agent-catalog.md"] = render_catalog(reg)
    targets[ROOT / "STACKS.md"] = render_stacks_md(reg)
    readme = ROOT / "README.md"
    if readme.exists():
        targets[readme] = render_readme(reg, readme.read_text(encoding="utf-8"))
    for src in sorted((SKILL / "assets" / "agents").glob("*.md")):
        targets[ROOT / "agents" / src.name] = plugin_agent(src.read_text(encoding="utf-8"))

    stale = [p for p, text in targets.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
    if not check:
        for p in stale:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(targets[p], encoding="utf-8")
            print(f"wrote {p.relative_to(ROOT)}")
    errors = validate(reg)
    if check and stale:
        errors += [f"stale generated file: {p.relative_to(ROOT)} (run python tools/build.py)" for p in stale]
    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(f"ok — {len(targets)} generated file(s) current, registry and skill valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
