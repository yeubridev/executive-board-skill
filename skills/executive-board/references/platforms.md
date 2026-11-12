# Running the board on your runtime

The skill is the same everywhere: the seats, the files in `board/`, the protocols. What
changes is how a seat becomes an agent and how a charter becomes a sub-agent. Find your
runtime below. Platform details were checked in November 2026; these products move fast, so
when something here disagrees with your runtime's current documentation, trust the documentation.

## Contents

1. [Claude Code](#claude-code)
2. [Claude Agent SDK and other programmatic runtimes](#claude-agent-sdk-and-other-programmatic-runtimes)
3. [Multi-agent platforms](#multi-agent-platforms)
4. [A single chat with no sub-agents](#a-single-chat-with-no-sub-agents)
5. [Other coding agents](#other-coding-agents)

## Claude Code

**Getting the seats.** Installed as a plugin, the six seats exist as subagents named
`executive-board:ceo`, `executive-board:cto`, and so on, each with this skill preloaded.
Installed as a plain skill, create them once per project:

```bash
python <skill-dir>/scripts/board.py init --project "<name>" --with-agents   # writes .claude/agents/ceo.md …
```

**Two ways to run.**

- *One session facilitates.* The main session is the Chief of Staff. It dispatches the seat
  subagents with the Agent tool — in parallel for discovery memos and board-meeting
  positions, which also keeps them independent — and talks to the founder.
- *One session per seat.* Start a session as a seat with `claude --agent cto` (or
  `claude --agent executive-board:cto`). That session holds the seat for its whole life and
  coordinates with the others through `board/`.

**Sub-agents hired at runtime.** `board.py deploy <id>` writes `.claude/agents/<id>.md`.
Things to know:

- Subagents can spawn subagents, by default up to three layers below the main conversation.
  Main session → seat → head → specialist fits exactly, which is why the default headcount
  cap is two levels below a seat.
- New and edited files in `.claude/agents/` are picked up within seconds — **except** when
  the folder did not exist at session start; then the session must be restarted once.
  `board.py init` creates the folder early for this reason.
- Until a new file is picked up, the parent can still use the sub-agent: dispatch a
  general-purpose subagent and tell it to read `.claude/agents/<id>.md` and act as that agent.
- The `skills:` field in an agent file preloads the **full text** of those skills into the
  sub-agent's context at start. Use it sparingly — set `preload_skills` in the charter only
  for a skill the agent needs on every task. Everything else it can invoke on demand, as
  long as the skill is installed at project or user scope.
- Agent files shipped inside a plugin ignore `hooks`, `mcpServers` and `permissionMode`.
  Agents that need those must live in `.claude/agents/`.
- A sub-agent does not see what its parent has in context. That is what the charter and the
  task brief are for.

**Agent teams** (experimental, off by default). Teammates can use these agent definitions,
but the `skills:` field is not applied to teammates; tell each teammate to load the
`executive-board` skill in its first instruction. Teammates cannot spawn teammates.

**Reading the skill's own files.** A seat has to open its role file, which lives in the
skill's folder. Installed in the project (`.claude/skills/`), that is inside the working
directory and needs no permission. Installed for the user or as a plugin, the skill
pre-approves reads under `~/.claude/skills/` and `~/.claude/plugins/` — nothing else. If the
skill lives anywhere else (a custom config directory, a local marketplace path) an
interactive session asks once; a headless run needs `--add-dir <that folder>`.

**Installing the stacks.** `board.py install <seat>` prints each source's preferred route:
plugin commands (`/plugin marketplace add …`, `/plugin install …`) or the skills CLI
(`npx skills add …`). With `--run` it executes the shell equivalents. In web and remote
sessions where `/plugin` is unavailable, use `--via skills`.

## Claude Agent SDK and other programmatic runtimes

Define each seat as an agent whose system prompt is the body of
`assets/agents/<seat>.md`, with this skill available to it. Define each hired sub-agent from
its charter: everything above the `MANAGEMENT NOTES` line in `board/agents/<id>.md` is its
system prompt, and the description in the charter's front matter is what the orchestrator
uses to route work to it. Give sub-agents only the tools their charter needs.

Keep `board/` on a filesystem every agent can read and write. It is the only shared memory
the protocol assumes.

## Multi-agent platforms

On platforms where agents are long-lived, have an org chart and are assigned skills
(Paperclip and similar):

- **Assign this skill to each executive agent** and state its seat in that agent's own
  instructions ("You hold the CTO seat on the executive board"). Step 1 of the skill does the rest.
- **Shared state:** put `board/` in the workspace or repository all the agents share. Use the
  platform's tickets or messages for requests between seats; fall back to `board/requests/`.
- **Hiring:** use the platform's own hire flow, and keep its approval gate — it is the
  founder's control over headcount. Map the charter onto it: title and reporting line from
  the charter's front matter, the skill list as the hire's requested skills, and the charter
  body as the new agent's instructions. Installing a skill in the company library and
  attaching it to an agent are usually two separate steps; do both.
- **Budgets:** if the platform enforces spend limits per agent, set them from the CFO's
  budget, and treat 80% of a limit as the moment to tell the parent seat.
- Still record every hire in `board/ORG.md`, so the board's view and the platform's agree.

## A single chat with no sub-agents

One agent plays the Chief of Staff and speaks for each seat in turn.

- Before speaking for a seat, read its role file. Write that seat's contribution completely
  before starting the next, and do not go back to harmonise them — the differences are the point.
- Independence is weaker when one mind holds every seat. Compensate: always run the red-team
  step in board meetings, and tell the founder plainly that one agent simulated the board.
- "Hiring" produces a charter the founder can paste into a new chat or project as its
  instructions. The charter is written to stand alone for exactly this reason.
- If files cannot be written, keep the boardroom as documents in the conversation and give
  the founder the current `STATUS`, `CHARTER` and `DECISIONS` to save at the end of each session.
- Scripts may not run. Use the templates in `assets/templates/` and the install commands
  printed in each role file; the founder runs the installs.

## Other coding agents

Install with the skills CLI and name the agent:

```bash
npx skills add yeubridev/executive-board-skill --agent <agent-name>
python <skill-dir>/scripts/board.py install cto --via skills --agent <agent-name>
```

Sub-agents take whatever form the agent supports — a custom agent file, a mode, a separate
session. In every case the system prompt is the charter above the `MANAGEMENT NOTES` line.
Where the agent has no sub-agent mechanism at all, follow the single-chat section.
