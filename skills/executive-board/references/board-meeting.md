# Board meetings: how decisions get made

A board of agents fails in one of two ways: it holds a six-seat ceremony over a choice one
seat could have made in a minute, or it "debates" and every seat agrees with whoever spoke
first. This protocol is built against both.

## Contents

1. [Triage: does this need a meeting?](#1-triage-does-this-need-a-meeting)
2. [Decision rights](#2-decision-rights)
3. [The full meeting](#3-the-full-meeting)
4. [Running it on your runtime](#4-running-it-on-your-runtime)
5. [Taking a decision to the founder](#5-taking-a-decision-to-the-founder)
6. [Reopening a decision](#6-reopening-a-decision)

## 1. Triage: does this need a meeting?

Ask two things: who owns this, and how hard is it to undo?

| Situation | What to do |
|---|---|
| Two-way door, inside one seat's rights | The owner decides and adds one line to `board/DECISIONS.md`. No meeting. |
| Two-way door that costs another seat something | The owner asks the affected seats for three lines each, decides, logs a short record. |
| One-way door, or seats disagree, or it is a docket item | Full meeting (section 3) and a decision record. Founder approval if it is a one-way door. |

**One-way doors** are choices that are expensive or impossible to reverse: the customer you
commit to, the core stack, anything public, anything legal, anything that spends real money,
anything that deletes data. When unsure, treat it as one-way — the cost of an unneeded
question is a minute of the founder's time; the cost of the opposite mistake is not bounded.

## 2. Decision rights

The owner decides. Other seats are consulted, not polled: a board that votes produces the
average of six opinions, which is rarely anyone's best idea.

| Area | Decides | Must consult |
|---|---|---|
| Vision, target customer, product scope, priorities | CEO | all seats |
| Positioning, messaging, channels, launch | CMO | CEO, Design |
| Stack, architecture, engineering plan, release readiness | CTO | CFO on cost, COO on timeline |
| Budget, spend, pricing model | CFO | CEO, CMO |
| Process, timeline, headcount, legal and compliance | COO | affected seats |
| UX, visual identity, design system, motion | Head of Design | CMO on brand, CTO on feasibility |
| Tie between seats | CEO | — |
| Any one-way door; anything in the charter's "always ask" list | Founder | the board's recommendation |

**Blocks.** Four seats can stop something inside a narrow remit, because these are the
failures that cannot be patched afterwards:

- CTO — a release with a known security or data-loss risk.
- CFO — spend outside the approved budget.
- COO — anything with unresolved legal or compliance exposure.
- Head of Design — shipping a user-facing surface below the agreed quality bar.

A block is not a veto on the project. It goes to the CEO, who either resolves it or overrides
it with a decision record that names the risk being accepted; overriding a CTO, CFO or COO
block needs the founder.

## 3. The full meeting

### Step 1 — Frame

The convening seat writes the question so that it can be answered:

- the decision as a choice between **named options** (include "do nothing" when it is real),
- the deciding seat, the door type, the deadline,
- the constraints from the charter and earlier decisions that bind it,
- which seats are invited — only those whose area is affected. Empty chairs are fine, and
  every seat you add costs a full agent's worth of tokens.

A vague question ("what should our strategy be?") produces six essays. If you cannot name the
options, you are still in discovery; go do that first.

The framing is the first half of the decision record. Create
`board/decisions/D-NNNN-<slug>.md` now from `assets/templates/decision-record.md`, with status
`proposed` and the context and options filled in, and send that file to the seats. Number it
one above the highest in `board/DECISIONS.md`.

### Step 2 — Positions, written independently

Each invited seat writes a position using `assets/templates/position-memo.md`: recommendation,
confidence, three reasons, what worries it, what would change its mind. It goes in the seat's
own folder, as `board/<seat>/positions/D-NNNN.md`, so that every seat writes only in its lane.

Each seat writes **before seeing any other seat's position**. This is the step that makes the
meeting worth holding. A model shown an existing opinion tends to elaborate on it rather than
test it, so positions written in sequence collapse into agreement and the board learns nothing.

### Step 3 — Challenge, one round

- Every seat reads the others and answers the strongest point against its own position: concede
  it or rebut it, in a few lines. Changing your mind for a stated reason is a good outcome;
  changing it to end the discussion is not.
- One seat acts as **red team** — by default the seat with the least at stake in this decision.
  It writes a short pre-mortem on the leading option: "Six months on, this failed. What
  happened?" In `deep` mode this is required for every one-way door.

One round only. A second round rarely adds information; it adds words.

### Step 4 — Decide

The deciding seat decides and says why. If two seats with decision rights collide, the CEO
breaks the tie. Seats that disagreed have their dissent recorded in their own words and then
commit — the record lets the board find out later who was right.

### Step 5 — Record

- Check `board/DECISIONS.md` for an earlier decision this one contradicts. If there is one,
  the new record supersedes it explicitly — two live decisions that disagree is how a board
  ends up building two products.
- Complete the record started in step 1 — decision, reasons, dissent, consequences, revisit
  condition — and link the position memos from it.
- Add one line at the top of `board/DECISIONS.md`: `D-NNNN · date · decision · owner · door`.
- Put follow-ups in `board/STATUS.md` with owners and dates.
- If founder approval is needed, the status is `proposed` until it is given.

A decision that is not recorded will be re-litigated by the next agent that arrives cold.

## 4. Running it on your runtime

**Each seat is a separate agent** (Claude Code subagents, a multi-agent platform, several
sessions): the convener sends every invited seat the same framing and nothing else, collects
the memos, then circulates all of them for the challenge round. Dispatch the positions in
parallel — it is faster, and it enforces independence for free.

**One agent plays every seat** (a single chat, no sub-agents): write the positions one at a
time. For each, re-read only the framing and that seat's role file and folder, write the memo,
and do not go back to edit earlier ones. Then run the challenge round. It is less independent
than separate agents, so lean harder on the red-team step and tell the founder the board was
simulated by one agent.

**The founder is in the room:** show the framing first and ask whether they want to state a
view before or after the board does. A founder who speaks first anchors everyone.

## 5. Taking a decision to the founder

One message, readable in under a minute:

1. **The decision** the board recommends, in one sentence.
2. **Why** — the two or three reasons that carried it.
3. **What was rejected**, and the best argument for it (include the dissent).
4. **Cost to reverse** if this turns out wrong.
5. **What happens next** on approval.

Batch decisions that are ready together. While waiting, keep working on everything that does
not depend on the answer, and list what is blocked in `STATUS.md` under "Waiting on the founder".

## 6. Reopening a decision

Decisions stand until their "revisit when" condition is met or new evidence appears — not
because a seat that lost the argument has thought of another way to make it. To reopen, write
what has changed since the record was made. The new record supersedes the old one; the old one
is marked `superseded by D-NNNN` and kept.
