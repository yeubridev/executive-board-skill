"""Tests for scripts/board.py. Standard library only: python -m unittest discover -s tests"""

import io
import json
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "executive-board" / "scripts"))
import board  # noqa: E402


def run(*argv):
    """Run board.py in-process; return (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with redirect_stdout(out), redirect_stderr(err):
        try:
            board.main(list(argv))
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
    return code, out.getvalue(), err.getvalue()


class BoardTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        os.environ.pop("CLAUDECODE", None)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def init(self):
        code, _, err = run("init", "--project", "Acme Notes")
        self.assertEqual(code, 0, err)

    def test_init_scaffolds_boardroom_and_never_overwrites(self):
        self.init()
        for name in ("CHARTER.md", "STATUS.md", "ORG.md", "DECISIONS.md"):
            self.assertTrue((Path("board") / name).exists(), name)
        for folder in ("decisions", "requests", "agents", "ceo", "cto", "cmo", "cfo", "coo", "design"):
            self.assertTrue((Path("board") / folder).is_dir(), folder)
        self.assertIn("Acme Notes", Path("board/CHARTER.md").read_text())
        self.assertNotIn("{{", Path("board/CHARTER.md").read_text())
        Path("board/CHARTER.md").write_text("# Project Charter — Mine\n")
        self.init()
        self.assertEqual(Path("board/CHARTER.md").read_text(), "# Project Charter — Mine\n")

    def test_init_with_agents_copies_six_seats(self):
        run("init", "--project", "X", "--with-agents")
        self.assertEqual(len(list(Path(".claude/agents").glob("*.md"))), 6)

    def test_every_seat_and_archetype_has_a_stack_and_an_install_plan(self):
        reg = board.load_registry()
        for target in list(board.SEATS) + list(reg["archetypes"]):
            code, out, err = run("stack", target)
            self.assertEqual(code, 0, f"{target}: {err}")
            code, out, err = run("install", target, "--tier", "all")
            self.assertEqual(code, 0, f"{target}: {err}")
            self.assertIn("Dry run", out)

    def test_install_leaves_alternatives_out_by_default(self):
        _, out, _ = run("install", "cto", "--tier", "all")
        self.assertNotIn("ecc@ecc", out.split("Alternatives left out")[0])
        self.assertIn("affaan-m/ECC  instead of  obra/superpowers", out)
        _, out, _ = run("install", "cto", "--tier", "all", "--with-alternatives")
        self.assertIn("/plugin install ecc@ecc", out)

    def test_install_via_skills_uses_the_skills_cli_and_agent_flag(self):
        _, out, _ = run("install", "cmo", "--via", "skills", "--agent", "codex")
        self.assertIn("npx -y skills add coreyhaines31/marketingskills --agent codex --yes", out)
        self.assertIn("npx -y skills add blader/humanizer --agent codex --yes", out)

    def test_hire_from_archetype_writes_charter_and_org_row(self):
        self.init()
        code, _, err = run("hire", "--archetype", "head-of-sales")
        self.assertEqual(code, 0, err)
        charter = Path("board/agents/head-of-sales.md").read_text()
        self.assertIn("parent: cmo", charter)
        self.assertIn("`draft-outreach`", charter)
        self.assertNotIn("{{", charter)
        rows = board.org_rows(Path("board"))
        self.assertEqual([(r["id"], r["parent"], r["status"]) for r in rows], [("head-of-sales", "cmo", "probation")])

    def test_headcount_and_depth_caps(self):
        self.init()
        for arch in ("head-of-sales", "head-of-growth", "head-of-content"):
            self.assertEqual(run("hire", "--archetype", arch)[0], 0)
        code, _, err = run("hire", "--id", "pr-lead", "--title", "PR Lead", "--parent", "cmo", "--mission", "Press.")
        self.assertNotEqual(code, 0)
        self.assertIn("cap is 3", err)
        self.assertEqual(run("hire", "--id", "sdr", "--title", "SDR", "--parent", "head-of-sales", "--mission", "Meetings.")[0], 0)
        code, _, err = run("hire", "--id", "sdr-aide", "--title", "Aide", "--parent", "sdr", "--mission", "Help.")
        self.assertNotEqual(code, 0)
        self.assertIn("cap is 2", err)
        self.assertEqual(run("hire", "--id", "pr-lead", "--title", "PR Lead", "--parent", "cmo", "--mission", "Press.", "--force")[0], 0)

    def test_hire_rejects_bad_ids_and_seats(self):
        self.init()
        self.assertNotEqual(run("hire", "--id", "Head Of Sales", "--title", "T", "--parent", "cmo", "--mission", "M")[0], 0)
        self.assertNotEqual(run("hire", "--id", "cto", "--title", "T", "--parent", "ceo", "--mission", "M")[0], 0)
        self.assertNotEqual(run("hire", "--id", "x", "--title", "T", "--parent", "nobody", "--mission", "M")[0], 0)

    def test_deploy_refuses_untrained_charter_then_deploys_trained_one(self):
        self.init()
        run("hire", "--archetype", "qa-lead")
        code, _, err = run("deploy", "qa-lead")
        self.assertEqual(code, 2)
        self.assertIn("Standards", err)
        self.assertFalse(Path(".claude/agents/qa-lead.md").exists())

        path = Path("board/agents/qa-lead.md")
        text = path.read_text()
        text = re.sub(r"<!-- Parent:.*?-->", "Written by the parent.", text, flags=re.DOTALL)
        text = re.sub(r"<!-- (?:e\.g\.|anything).*?-->", "decided with the parent", text)
        path.write_text(text)
        code, out, err = run("deploy", "qa-lead")
        self.assertEqual(code, 0, err)
        agent = Path(".claude/agents/qa-lead.md").read_text()
        self.assertTrue(agent.startswith("---\nname: qa-lead\n"))
        self.assertNotIn("<!--", agent)
        self.assertNotIn("Calibration", agent)  # management notes stay out of the prompt
        meta, _ = board.parse_frontmatter(agent)
        self.assertEqual(meta["name"], "qa-lead")

    def test_retire_keeps_charter_updates_org_and_removes_runtime_file(self):
        self.init()
        run("hire", "--archetype", "tech-lead")
        run("deploy", "tech-lead", "--allow-untrained")
        self.assertTrue(Path(".claude/agents/tech-lead.md").exists())
        self.assertEqual(run("retire", "tech-lead")[0], 0)
        self.assertFalse(Path(".claude/agents/tech-lead.md").exists())
        self.assertIn("status: retired", Path("board/agents/tech-lead.md").read_text())
        self.assertEqual(board.org_rows(Path("board"))[0]["status"], "retired")
        self.assertEqual(run("hire", "--archetype", "tech-lead", "--force")[0], 0)  # can rehire

    def test_registry_is_valid_json_with_all_seats(self):
        reg = json.loads(board.REGISTRY_PATH.read_text())
        self.assertEqual(set(reg["stacks"]), set(board.SEATS))
        for seat, entries in reg["stacks"].items():
            self.assertTrue(any(e["tier"] == "core" for e in entries), seat)


if __name__ == "__main__":
    unittest.main()
