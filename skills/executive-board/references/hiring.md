# Hiring and training sub-agents

Any seat on the board can create sub-agents — a Head of Sales under the CMO, a Head of Project
under the COO, a QA Lead under the CTO — choose their skills, and train them. The sub-agent
then works for that seat, which stays accountable for everything it produces.

A sub-agent is a cost before it is a help: another context to brief, another output to review,
another place for the plan to drift. The steps below exist to make each hire pay for itself.

## Contents

1. [Decide whether to hire](#1-decide-whether-to-hire)
2. [Write the mission](#2-write-the-mission)
3. [Equip: choose its skills](#3-equip-choose-its-skills)
4. [Train: write what you know into the charter](#4-train-write-what-you-know-into-the-charter)
5. [Calibrate: a probation task](#5-calibrate-a-probation-task)
6. [Deploy](#6-deploy)
7. [Manage](#7-manage)
8. [Retire](#8-retire)

## 1. Decide whether to hire

Hire when at least two of these are true:

- The work is a **standing workstream**, not a single deliverable.
- It needs skills or context that would crowd out your own.
- It can run **in parallel** with what you are doing.
- It needs a **different stance** from yours — a reviewer who did not write the code, a critic
  who did not make the design.

Do not hire when:

- It is a one-off task. Dispatch an **ephemeral worker** instead: a generic sub-agent with a
  good one-off brief (use `assets/templates/request.md`), no charter, no row in `ORG.md`.
- You cannot say how you would judge the output. Work that out first; otherwise you will accept
  whatever comes back.
- The work belongs to another seat. Send that seat a request.
- You are at the headcount cap in the charter (default: three reports per seat, two levels
  deep). Retire someone, or ask the COO for a decision to raise it. The cap is there because
  every extra agent adds coordination cost faster than it adds output.

Hiring a standing sub-agent is a COO decision under docket item 9. In practice: propose the
hire in one line; within the cap, the COO's agreement is the row in `ORG.md`.

## 2. Write the mission

Before any persona or title, write:

- **Mission** — the outcome this agent exists to produce, in one or two sentences.
- **Scope and non-goals** — what is its job, and which neighbouring work it must hand back.
- **Decision rights** — what it decides alone, what it proposes to you, what is off-limits.
- **Deliverables** — named files or outputs.

A job title and a personality are not a brief. "You are a world-class sales leader" tells the
agent nothing about this product, this customer, or what you will accept.

Start from the catalog when an archetype fits — it pre-fills mission, deliverables, skills and
a calibration task:

```bash
python <skill-dir>/scripts/board.py hire --archetype head-of-sales --parent cmo
python <skill-dir>/scripts/board.py hire --id pricing-analyst --title "Pricing Analyst" --parent cfo \
    --mission "Own the pricing research and the pricing page experiments."
```

Both write `board/agents/<id>.md` from the charter template and add a `probation` row to
`board/ORG.md`. The catalog is in [sub-agent-catalog.md](sub-agent-catalog.md). Without
scripts, copy `assets/templates/agent-charter.md` and fill it in by hand.

## 3. Equip: choose its skills

1. **Start from the catalog** stack for the archetype, or from the relevant part of your own stack.
2. **Cut it down to what this mission needs** — usually three to six skills the agent will use
   every week. A catalog stack is the full menu, not the order. Each extra skill adds
   instructions that compete for the agent's attention, and two skills that both want to run
   the process will fight. Narrow an archetype by naming the skills to keep:

   ```bash
   python <skill-dir>/scripts/board.py hire --archetype head-of-sales \
       --skills account-research,draft-outreach,call-prep,cold-email,humanizer
   ```
3. **Fill gaps deliberately.** If nothing in the registry covers a need, search for a skill and
   vet it before assigning it — [skill-vetting.md](skill-vetting.md). Never hand a sub-agent a
   skill you have not read.
4. **Install them where the sub-agent runs**, and check that they are there:

   ```bash
   python <skill-dir>/scripts/board.py install head-of-sales          # prints the commands
   python <skill-dir>/scripts/board.py install head-of-sales --run    # runs them
   ```

5. **Say when to use each one.** In the charter's skills table, the "use it when" column is
   yours to write. A bare list of skill names gets ignored; "run `X` before any outbound
   message leaves your folder" gets followed.

## 4. Train: write what you know into the charter

The sub-agent starts with nothing. It has not read the charter, was not at the board meeting,
and does not know what you have learned since. Training is writing that down. Fill these
sections of the charter yourself — this is the part no template can do for you:

- **Context digest.** The ten to twenty lines that bear on its mission: who the customer is,
  what was decided and why, the constraints, the words to use and avoid. Link to files for the
  rest; do not paste whole documents.
- **Procedure.** How you would do this job, step by step, with the skill used at each step.
- **Standards.** How you will judge the output: concrete checks, thresholds, and **one worked
  example** of what good looks like. An example transfers more of your judgment than a page of
  adjectives.
- **Decision rights and stop conditions.** When to proceed, when to come back to you.

The test: could a capable stranger do this job from the charter alone, and would you accept
the result? If not, the missing piece is still in your head.

Keep the charter about **this project**. The skills carry the general method — how to qualify
a lead, how to write a test plan. The charter carries what no skill can know: this customer,
these decisions, your standards. A charter padded with a generic operating manual buries the
ten lines that matter, and a short, specific one is a complete hire.

Write in plain instructions with reasons. A sub-agent that knows *why* a rule exists applies
it sensibly to cases you did not foresee; one that only has the rule follows it off a cliff.

## 5. Calibrate: a probation task

Before real work, give the sub-agent one small, real task that is typical of the job and whose
quality you can judge — the catalog suggests one per archetype.

Review the result against your standards, then:

- **Good** → record it under Calibration in the charter, set the status to `active`.
- **Off** → fix the **charter**, not just the output. The gap is almost always in your brief:
  a missing piece of context, a standard you never stated. Re-run.
- **Still off after two rounds** → the mission is wrong-sized. Split it, narrow it, or do the
  work yourself. Do not keep an agent whose output you have to redo.

## 6. Deploy

The charter in `board/agents/<id>.md` is the source of truth on every platform. Render it into
your runtime's format:

```bash
python <skill-dir>/scripts/board.py deploy head-of-sales     # → .claude/agents/head-of-sales.md
```

Everything above the `MANAGEMENT NOTES` line becomes the agent's system prompt; your
calibration and review notes stay out of its context. Re-run `deploy` whenever you change the
charter. For other runtimes — the Agent SDK, multi-agent platforms, a plain chat — see
[platforms.md](platforms.md).

## 7. Manage

- **You are accountable.** Review its output before it leaves your lane. The board sees your
  name on it.
- **Brief every task** with outcome, context, and what done means. The charter covers the job;
  the brief covers this task. Point to files instead of pasting history — a brief that is
  mostly pasted conversation hides the instruction inside it.
- **Read the status line.** Sub-agents end each task with `DONE`, `DONE_WITH_CONCERNS`,
  `BLOCKED` or `NEEDS_CONTEXT`. The last three are requests for you to act, not noise.
- **One chain of command.** It reports to you. Other seats that want its work ask you.
- **Training continues.** If you correct the same thing twice, the correction belongs in the
  charter. Update it and redeploy.
- **Its own hires.** A sub-agent may hire below itself only if the depth cap allows it and you
  approve; it follows this same file, with you as the approver.
- **Review at every phase gate:** keep, retrain, or retire. Log one line in the charter.

## 8. Retire

When the workstream ends or the agent is not earning its cost:

```bash
python <skill-dir>/scripts/board.py retire head-of-sales
```

This marks it `retired` in the charter and `ORG.md` and removes the runtime file. The charter
stays, so the board keeps what was learned and can rehire from it.
