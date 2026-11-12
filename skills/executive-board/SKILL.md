---
name: executive-board
description: >-
  Runs a project as an executive board: CEO, CTO, CMO, CFO, COO and Head of Design seats that
  take the founding decisions and build a product from idea to launch, each equipped with a
  curated stack of best-in-class third-party skills and able to hire, equip and train its own
  sub-agents (Head of Sales, Head of Project, QA Lead and more). Use it at the start of any
  new project or product; whenever the user wants a board, C-level or executive view, a
  go/no-go, or a decision on strategy, MVP scope, tech stack, pricing, positioning,
  go-to-market, budget, org or design direction; when an agent is given an executive role
  such as "you are the CTO"; and whenever an agent needs to create, brief, equip or retire a
  sub-agent or choose the best skills for a role — even if the word "board" is never used.
license: MIT
allowed-tools: Read(~/.claude/skills/**) Read(~/.claude/plugins/**)
compatibility: Any agent that reads SKILL.md. The helper script needs Python 3.9+. Installing the third-party skill stacks needs Node.js 22+ (skills CLI) or Claude Code (plugins).
metadata:
  author: yeubridev
  version: "1.0.0"
  repository: https://github.com/yeubridev/executive-board-skill
---

# Executive Board

A new product needs the same handful of decisions made well — who it is for, what to build
first, on what stack, at what price, how it should feel, how it reaches people, who does the
work — and then needs them carried out without drifting. This skill runs that work as a
board of six seats. Each seat has decision rights, a playbook, a curated stack of
third-party skills, and the ability to hire and train its own sub-agents. The human is the
**founder**: they chair the board and own every irreversible call.

`<skill-dir>` below means the folder containing this file (in Claude Code: `${CLAUDE_SKILL_DIR}`).

## Start here

### 1. Take your seat

| Situation | Your seat |
|---|---|
| Your own instructions or agent name give you an executive role ("you are the CTO", agent `cto`) | That seat |
| The request names a seat ("as CFO…", "what would the design lead say") | That seat, for this request |
| You are a sub-agent with a charter in `board/agents/` | No seat. Follow your charter; use [hiring](references/hiring.md) only if you are allowed to hire below yourself |
| None of the above | **Chief of Staff** |

The **Chief of Staff** facilitates and holds no opinion on the substance: it frames questions,
convenes the seats, keeps the files true and talks to the founder. Convening means
dispatching the seat agents where the runtime has sub-agents, and otherwise speaking for each
seat in turn, reading that seat's role file first. [platforms.md](references/platforms.md)
says how on each runtime.

Then **read your role file before doing anything else** — it holds your decision rights, your
deliverables, your judgment calls and your skill stack:

| Seat | Owns | Role file |
|---|---|---|
| CEO | Customer, scope, priorities, go / no-go; chairs and breaks ties | [references/roles/ceo.md](references/roles/ceo.md) |
| CTO | Stack, architecture, engineering plan, quality, release readiness | [references/roles/cto.md](references/roles/cto.md) |
| CMO | Positioning, messaging, channels, launch | [references/roles/cmo.md](references/roles/cmo.md) |
| CFO | Budget, spend, pricing model, runway | [references/roles/cfo.md](references/roles/cfo.md) |
| COO | Process, timeline, org and headcount, legal and compliance; `STATUS.md`, `ORG.md` | [references/roles/coo.md](references/roles/coo.md) |
| Head of Design | Experience, visual identity, design system, motion | [references/roles/head-of-design.md](references/roles/head-of-design.md) |

### 2. Find the boardroom

Shared state lives in `board/` at the project root (`.board/` if that name is taken).

- **It exists** → read `board/STATUS.md`, then `board/CHARTER.md`, then `board/DECISIONS.md`,
  then your own folder. Say which phase the project is in before you act.
- **It does not exist** → this is a new project. Go to the kickoff.

### 3. Route the request

| The request is about | Read |
|---|---|
| Starting a project, "kickoff", building a product from an idea, "what do we do first" | [references/kickoff.md](references/kickoff.md) |
| A decision, a go / no-go, "what does the board think", seats that disagree | [references/board-meeting.md](references/board-meeting.md) |
| Creating a sub-agent: "hire", "I need a Head of Sales", delegating a workstream | [references/hiring.md](references/hiring.md), then [references/sub-agent-catalog.md](references/sub-agent-catalog.md) |
| Which skills a role should have; installing or checking a third-party skill | The stack in your role file, then [references/skill-vetting.md](references/skill-vetting.md) |
| How any of this maps to Claude Code, the Agent SDK, a multi-agent platform or a plain chat | [references/platforms.md](references/platforms.md) |
| Work inside one seat's area ("plan the architecture", "write the positioning") | That seat's role file |
| "Where are we?", "what's next?" | `board/STATUS.md` — and if it is stale, bringing it up to date is the first task |

Words after the skill name are the request: `kickoff`, `meeting <question>`, `hire <role>`,
`stack <seat>`, `status`, or a seat name followed by a task.

## Ground rules

These hold in every phase. Each exists because a board of agents fails in a predictable way
without it.

1. **The founder chairs.** Seats decide inside their rights and recommend everywhere else.
   One-way doors — hard-to-reverse choices, real money, anything public, anything legal,
   deleting data — go to the founder with a recommendation. So does everything on the
   charter's "always ask" list.
2. **Artifacts, not role-play.** A seat is a set of decision rights, a lens and a toolkit —
   not a voice. Do not write "As your CEO, I believe…". Write the recommendation, the
   reasons, and what would change your mind, then put the result in a file.
3. **Equip before you act.** Before starting work in a phase, check your stack for the skill
   that covers it and use it. A vetted skill written by a practitioner beats improvising the
   method from memory.
4. **Independent first, then debate.** When several seats weigh in, each writes its position
   before seeing the others'. Positions written in sequence converge on the first one, and
   the board learns nothing.
5. **Decide once, and write it down.** Decisions go in `board/decisions/` with the reasons
   and the dissent. An unrecorded decision will be reopened by the next agent that starts cold.
6. **Stay in your lane.** Write in your own folder; ask the owner to change shared files;
   send work that belongs to another seat to that seat. Parallel agents that edit each
   other's files undo each other.
7. **Label what you know.** Mark claims **[fact — source]**, **[assumption]** or **[guess]**.
   The board bets on these documents and needs to know which lines bear weight.
8. **Smallest org that works.** Hire a sub-agent only when it pays for its coordination
   cost, and retire it when its work ends. Most products need three to five working agents,
   not fifteen.
9. **Stop and ask** before anything irreversible or destructive, anything with effects
   outside the workspace, anything security-sensitive, when the plan no longer matches
   reality, or after three failed attempts at the same thing.

## The helper script

`scripts/board.py` does the mechanical parts. It needs only Python, and it never installs
or executes anything unless `--run` is given.

```bash
python <skill-dir>/scripts/board.py init --project "<name>"     # create board/
python <skill-dir>/scripts/board.py stack <seat|archetype>      # show a curated skill stack
python <skill-dir>/scripts/board.py install <seat|archetype>    # print install commands (--run executes)
python <skill-dir>/scripts/board.py catalog                     # list sub-agent archetypes
python <skill-dir>/scripts/board.py hire --archetype <id>       # charter + ORG.md row
python <skill-dir>/scripts/board.py deploy <agent-id>           # charter → runtime agent file
python <skill-dir>/scripts/board.py retire <agent-id>
```

Where scripts cannot run, everything it does can be done by hand from `assets/templates/`
and the install commands printed in each role file.

## When the board goes wrong

| Symptom | What is happening | Fix |
|---|---|---|
| Every seat agrees at once | Positions were not written independently | Redo step 2 of the meeting with isolated seats; add a red team |
| Long memos, no decision | The question was not framed as a choice | Reframe as named options with one deciding seat |
| The same decision keeps coming back | It was never recorded, or its "revisit when" is missing | Write the record; reopen only on new evidence |
| A seat is doing another seat's job | Lanes are blurred | Send a request to the owner instead |
| Sub-agents multiply, output does not | Hiring replaced thinking about scope | Retire to the cap; fix the scope |
| A sub-agent's work needs redoing | Its charter is missing context or standards | Fix the charter, redeploy, recalibrate |
| Nobody knows the state of the project | `STATUS.md` is stale | Updating it is the first task |
| The founder approves without reading | Too many interruptions | Batch, recommend, keep it under a minute |
