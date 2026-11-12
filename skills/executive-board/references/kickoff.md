# Kickoff: from idea to launched product

This is the board's operating sequence for a new project. It exists so that the expensive
decisions get made once, in the right order, by the seat that should own them — and so that
any agent arriving cold can find out where the project stands from files alone.

## Contents

1. [Pick the depth](#1-pick-the-depth) — including [sprint in one sitting](#sprint-in-one-sitting)
2. [The boardroom](#2-the-boardroom)
3. [Phase 0 — Intake](#phase-0--intake)
4. [Phase 1 — Discovery](#phase-1--discovery)
5. [Phase 2 — Founding decisions](#phase-2--founding-decisions)
6. [Phase 3 — Definition](#phase-3--definition)
7. [Phase 4 — Build](#phase-4--build)
8. [Phase 5 — Launch](#phase-5--launch)
9. [Phase 6 — Operate and grow](#phase-6--operate-and-grow)
10. [Resuming or joining midway](#resuming-or-joining-midway)

## 1. Pick the depth

Ceremony should match the stakes. Ask the founder which depth they want; if they do not say,
infer it from the charter and state your choice.

| Depth | For | What changes |
|---|---|---|
| **sprint** | Prototype, weekend project, internal tool | One agent, one sitting, a few pages in total. No seat dispatch, no discovery memos, no sub-agents. See [Sprint in one sitting](#sprint-in-one-sitting). |
| **standard** | A real product with real users | Everything below as written. |
| **deep** | Funded, regulated, or hard to reverse | Standard, plus: claims in discovery need a source or are marked as untested; a red-team pass on every one-way-door decision; a financial model with scenarios; a threat model; founder sign-off at every gate. |

Going deeper later is cheap. Starting deep on a prototype wastes the founder's attention
and a great many tokens: six seats dispatched in parallel cost roughly six times one agent,
and each will write as much as it is allowed to.

### Sprint in one sitting

One agent facilitates and speaks for the seats itself; it does not dispatch them.

1. **Charter** — short. Ask only what you cannot infer; tag what you inferred as an assumption.
2. **Walk the docket once** (the table in Phase 2). For each item, read the owning seat's
   judgment calls in its role file, then write that seat's decision in two or three lines. Add
   one line from another seat only where it would object. Skip items that do not apply.
3. **Log it.** One line per decision in `board/DECISIONS.md`; the reasoning for all of them in
   a single `board/decisions/D-0001-sprint-kickoff.md`. Write a separate full record only for
   a one-way door.
4. **Plan.** A short build plan in `board/cto/plan.md`: milestones, the riskiest assumption
   first, what is out of scope.
5. **Hand over.** Update `STATUS.md` and give the founder one list: decisions taken on their
   behalf, assumptions to confirm, and the one-way doors waiting for their approval.

If an item turns out to be contested or hard to reverse, that single item gets a proper
board meeting. The rest stays light.

## 2. The boardroom

All shared state lives in a `board/` folder at the project root (use `.board/` if `board/`
already means something else in this project). Create it with:

```bash
python <skill-dir>/scripts/board.py init --project "<name>" --depth standard
```

or, where scripts cannot run, copy the files from `assets/templates/` by hand.

```
board/
├── CHARTER.md        the brief everyone works from            owner: CEO
├── STATUS.md         phase, gate, who is waiting on what      owner: COO
├── ORG.md            every seat and sub-agent                 owner: COO
├── DECISIONS.md      one line per decision, newest first      owner: CEO
├── decisions/        full decision records (D-0001-….md)
├── requests/         cross-seat asks, when no native channel exists
├── agents/           sub-agent charters
└── ceo/ cto/ cmo/ cfo/ coo/ design/     each seat's own work
```

Two rules keep parallel agents from undoing each other's work:

- **Lanes.** A seat writes in its own folder. Shared files are edited by their owner; everyone
  else proposes a change to the owner or appends to a clearly shared section (the `STATUS.md` log).
- **Files over chat.** If it is not in `board/`, the next agent will not know it. Conclusions go
  in files; conversations are scratch.

## Phase 0 — Intake

**Lead:** CEO (or whoever is facilitating). **Output:** `board/CHARTER.md`, approved.

Interview the founder. Ask only what the charter template needs and what you cannot infer from
what they already gave you; batch the questions in one message rather than drip-feeding them.
The questions that matter most, because every later decision leans on them:

1. Who exactly is this for, and what do they do today instead?
2. What would make you call this a success in 90 days? What would make you stop?
3. What is fixed — budget, deadline, stack, things you refuse to do?
4. How much do you want to be asked? (Fill the autonomy section explicitly.)

If the founder says "you decide", decide, write it in the charter as an assumption, and move on.

If the founder is not available and has said to go ahead, mark the charter `provisional`,
tag every inferred line as an assumption, and proceed on two-way doors only. Prepare the
one-way doors to the point where approval takes a minute, and queue them in `STATUS.md`
under "Waiting on the founder".

**Gate:** the founder has approved the charter, or has explicitly told the board to proceed
on a provisional one. Nothing else starts before this, because a discovery phase run against
the wrong brief is pure waste.

## Phase 1 — Discovery

**Lead:** each seat for its own lens, in parallel. **Output:** `board/<seat>/discovery.md`.

Each seat writes **one page — a real limit, not a figure of speech — without reading the
other seats' pages**. Independence is the point: six memos that have converged in advance
tell the board nothing. Each seat covers its own question below, not the whole docket.

| Seat | The question it answers | Must contain |
|---|---|---|
| CEO | Is this worth building, and where is the opening? | Market and alternatives, 3–5 closest competitors and their weak spot, the wedge, business-model options |
| CMO | Can we reach these people and will they care? | ICP, the words customers use for the problem, 2–3 reachable channels, demand signals |
| CTO | Can we build it, and what is hard? | Feasibility, build-vs-buy, 2 candidate stacks with trade-offs, the riskiest technical assumption, rough effort |
| CFO | Can this make money? | Cost to build and run, pricing hypotheses, unit economics sketch, what it costs to find out |
| COO | Can we actually run this? | Timeline shape, legal and compliance exposure, dependencies, the sub-agents likely needed |
| Head of Design | What should it feel like? | How the best existing products handle this job, 2–3 distinct directions (not variations), the one interaction that must be great |

Label every claim **[fact — source]**, **[assumption]**, or **[guess]**. The board will bet on
these pages; it needs to know which lines can bear weight. In `deep` mode an unlabelled or
unsourced market claim does not count.

**Gate:** all invited seats have filed; the CEO has listed the disagreements between memos —
those disagreements are the agenda for Phase 2.

## Phase 2 — Founding decisions

**Lead:** CEO chairs. **Output:** one decision record per docket item, founder-approved where needed.

Run each item with the protocol in [board-meeting.md](board-meeting.md). Take them in this
order — later items depend on earlier ones, and reopening an early one invalidates the rest.

| # | Decision | Decides | Consulted | Door |
|---|---|---|---|---|
| 1 | Customer and problem we commit to | CEO | CMO, Design | one-way-ish |
| 2 | Positioning and the promise we make | CMO | CEO, Design | two-way |
| 3 | Business model and pricing | CFO | CEO, CMO | two-way early, one-way after launch |
| 4 | MVP scope: in, out, later | CEO | all | two-way |
| 5 | Stack and architecture | CTO | CFO, COO | one-way |
| 6 | Experience and brand direction | Head of Design | CMO, CTO | two-way early |
| 7 | Go-to-market motion and launch shape | CMO | CEO, CFO | two-way |
| 8 | Budget, timeline, milestones | CFO + COO | CTO | two-way |
| 9 | Org: which sub-agents to hire now | COO | each parent seat | two-way |
| 10 | Success metrics and kill criteria | CEO | CFO | two-way |
| 11 | Legal, compliance and risk posture | COO | CTO, CFO | one-way |

Items 5 and 6 can run in parallel once 4 is settled. Skip an item only by writing one line
saying why it does not apply.

**Gate:** every item decided or explicitly deferred with an owner and a date; the founder has
approved the one-way doors. Present those to the founder as a single batch, five lines each
(decision, why, what was rejected, cost to reverse, what happens next) — one interruption, not eleven.

## Phase 3 — Definition

**Lead:** each seat. **Output:** the documents the build will be held to.

| Seat | Deliverable | It is good enough when |
|---|---|---|
| CEO | `ceo/prd.md` — users, jobs, scope in/out, stories with acceptance criteria, non-goals | An engineer could build and a tester could test from it without asking you anything |
| Head of Design | `design/direction.md`, `design/design-system.md`, key flows | Every story in the PRD has its screens and states, including empty, loading and error |
| CTO | `cto/architecture.md`, `cto/plan.md` — milestones, tasks, environments, quality gates | Every story maps to tasks; the riskiest assumption is scheduled first |
| CMO | `cmo/positioning.md`, `cmo/gtm.md` — messaging, channels, launch plan | Someone else could write the landing page from it and you would sign it |
| CFO | `cfo/model.xlsx`, `cfo/budget.md`, `cfo/pricing.md` | Every number traces to a stated assumption; the budget covers the plan |
| COO | `coo/operating-plan.md`, `coo/risk-register.md`, legal checklist | Every milestone has an owner and a date; every top risk has a trigger |

Seats hire sub-agents here if decision 9 approved them — see [hiring.md](hiring.md). Before a
seat starts, it equips itself from the stack in its role file; a seat that skips this ends up
improvising work a vetted skill already does well.

**Gate — definition of ready.** The COO checks consistency across documents, because each was
written in isolation: nothing contradicts a decision record; the architecture and the design
both cover every story; the budget covers the plan; the launch plan promises nothing the MVP
scope excludes. Conflicts go back to Phase 2 as a new decision, not as a quiet edit.

## Phase 4 — Build

**Lead:** CTO. **Cadence:** short cycles, each ending in something demonstrable.

- **CTO** runs each cycle as plan → build → review → demo, using the process skills in its stack.
- **Head of Design** reviews every user-facing change before it counts as done. Design debt
  found at launch is ten times the price of design debt found in review.
- **CMO** builds launch assets in parallel — landing page, waitlist, content — so launch does
  not wait on marketing.
- **CFO** compares spend to budget each cycle and raises a decision if the trend breaks it.
- **COO** keeps `STATUS.md` true and chases anything waiting on the founder.
- **CEO** owns scope. Any change to what is in or out is a decision record. Scope that changes
  by drift is how projects miss their date without anyone having decided to.

End each cycle with a short board sync, written into the `STATUS.md` log: shipped versus
planned, decisions needed, risks that moved. Three lines per seat is plenty.

**Gate:** every MVP story meets its acceptance criteria, demonstrated, not asserted.

## Phase 5 — Launch

**Lead:** CEO calls it; every seat signs its own line.

| Seat | Signs off that |
|---|---|
| CTO | Tests pass; security review done; monitoring, backups and rollback exist and were tried |
| Head of Design | Polish and accessibility pass done on real screens; responsive; no placeholder states |
| CMO | Site says what the positioning says; analytics events fire; launch assets scheduled |
| CFO | Pricing and payment work end to end with a real transaction; cost alerts set |
| COO | Terms and privacy published; support channel staffed; incident runbook written |
| CEO | Go / no-go recorded as a decision |

A public launch is a one-way door: the founder approves it. A seat that cannot sign says what
is missing; "probably fine" is a no.

## Phase 6 — Operate and grow

- **Weekly:** the CEO reviews the north-star metric and the kill criteria against reality; the
  CFO updates actuals; the CMO reports what the channels did.
- **Per cycle:** a short retro — one thing to keep, one to change, written into `STATUS.md`.
- **Per gate:** every parent reviews its sub-agents: keep, retrain, or retire.
- **When a kill criterion trips:** convene the board. That is what the criterion was for.

## Resuming or joining midway

Read, in order: `board/STATUS.md` → `board/CHARTER.md` → `board/DECISIONS.md` → your own
folder. Then say what phase the project is in and what you intend to do next before doing it.
If `STATUS.md` is stale, fixing it is the first task.
