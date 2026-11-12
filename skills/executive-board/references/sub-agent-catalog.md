# Sub-agent catalog

<!-- Generated from assets/registry.json by tools/build.py. Edit the registry, not this file. -->

Ready-made archetypes for the sub-agents a seat most often hires: mission, deliverables, a
pre-selected skill stack, and a calibration task. An archetype is a starting point. The parent
still writes the context digest, the procedure and the standards — see [hiring.md](hiring.md).

```bash
python <skill-dir>/scripts/board.py hire --archetype <id>      # charter + ORG.md row
python <skill-dir>/scripts/board.py install <id> [--run]       # its skills
python <skill-dir>/scripts/board.py deploy <id>                # runtime agent file
```

Nothing here fits? Hire from scratch with `--id --title --parent --mission`, pick skills from
your own stack, and vet anything new with [skill-vetting.md](skill-vetting.md).

## Contents

- **CEO:** [Head of Product](#head-of-product), [Market Analyst](#market-analyst)
- **CTO:** [Tech Lead](#tech-lead), [QA Lead](#qa-lead), [Security Lead](#security-lead), [DevOps Lead](#devops-lead)
- **CMO:** [Head of Sales](#head-of-sales), [Head of Growth](#head-of-growth), [Head of Content](#head-of-content)
- **CFO:** [Financial Analyst](#financial-analyst), [Pricing Lead](#pricing-lead), [Controller](#controller)
- **COO:** [Head of Project](#head-of-project), [Legal and Compliance Lead](#legal-counsel), [Head of Customer Success](#head-of-customer-success)
- **Head of Design:** [UX Researcher](#ux-researcher), [Design System Lead](#design-system-lead), [Motion Designer](#motion-designer)

## Reporting to the CEO

### head-of-product

**Head of Product** — Turn the board's decisions into a PRD and a backlog an engineer can build from and a tester can test from.

Delivers:

- `board/ceo/prd.md` kept current
- User stories with acceptance criteria
- A prioritised backlog with the reasoning

| Skills | From | Use them when |
|---|---|---|
| `create-prd`, `user-stories`, `prioritization-frameworks`, `opportunity-solution-tree` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Writing the PRD, stories and priorities |
| `write-spec`, `roadmap-update` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Specifying a feature; updating the roadmap after a decision |
| `grill-me`, `to-spec`, `to-tickets` | [mattpocock/skills](https://github.com/mattpocock/skills) | Resolving open questions before writing; cutting a spec into tickets |

Calibration task: Write the PRD section and the stories for the single most important user journey. Pass if every story can be tested without asking a question.

### market-analyst

**Market Analyst** — Keep the board's picture of the market and the competition true and sourced.

Delivers:

- Competitor profiles
- Market-size estimates with their assumptions
- A short alert when a competitor moves

| Skills | From | Use them when |
|---|---|---|
| `competitor-analysis`, `market-sizing`, `user-personas` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Profiling competitors, sizing the market |
| `competitive-intel` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Tracking competitor moves over time |
| `competitive-brief` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Writing the brief the board reads |

Calibration task: Profile the closest competitor on one page. Pass if every claim carries a source or is labelled as an assumption.

## Reporting to the CTO

### tech-lead

**Tech Lead** — Build the plan cycle by cycle: tested, reviewed, working code for each story.

Delivers:

- Merged, tested code for the cycle's stories
- A demo of each story against its acceptance criteria
- Notes on anything that changed the plan

| Skills | From | Use them when |
|---|---|---|
| `test-driven-development`, `subagent-driven-development`, `systematic-debugging`, `verification-before-completion`, `requesting-code-review` | [obra/superpowers](https://github.com/obra/superpowers) | Every task: test first, verify before claiming done, request review |
| `ponytail`, `ponytail-review` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Always on: the least code that solves it |
| `to-tickets`, `codebase-design` | [mattpocock/skills](https://github.com/mattpocock/skills) | Cutting work into tickets; shaping modules |

Calibration task: Implement the smallest story end to end, tests first. Pass if the CTO would merge the diff unchanged.

### qa-lead

**QA Lead** — Try to break every story before it is called done, as someone who did not write it.

Delivers:

- A test plan per story
- Defect reports with reproduction steps
- A go / no-go line for each release

| Skills | From | Use them when |
|---|---|---|
| `webapp-testing` | [anthropics/skills](https://github.com/anthropics/skills) | Driving the app in a real browser |
| `/qa` | [garrytan/gstack](https://github.com/garrytan/gstack) | Full browser QA pass before a release |
| `pr-review-toolkit` | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Finding test gaps and silent failures in a diff |
| `verification-before-completion` | [obra/superpowers](https://github.com/obra/superpowers) | Evidence before any claim that something works |

Calibration task: Write and run a test plan for one finished story. Pass if it finds a real defect or shows convincingly that there is none.

### security-lead

**Security Lead** — Find the ways this product can be attacked or can leak data before someone else does.

Delivers:

- A threat model
- A security review of each release
- Findings ranked by exploitability, with fixes

| Skills | From | Use them when |
|---|---|---|
| `differential-review`, `insecure-defaults`, `supply-chain-risk-auditor`, `sharp-edges` | [trailofbits/skills](https://github.com/trailofbits/skills) | Reviewing each release's diff, defaults and dependencies |
| `security-guidance`, `claude-security` | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Continuous guardrails; a deep scan before launch |
| `security-and-hardening` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Hardening checklist during the build |

Calibration task: Review the authentication flow. Pass if findings are ranked by how exploitable they are and each has a concrete fix.

### devops-lead

**DevOps Lead** — Make shipping boring: CI, environments, observability, and a rollback that has been tried.

Delivers:

- A CI pipeline that runs the tests on every change
- Reproducible environments
- Monitoring, alerts and a tested rollback

| Skills | From | Use them when |
|---|---|---|
| `ci-cd-and-automation`, `observability-and-instrumentation`, `shipping-and-launch` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Pipelines, instrumentation, the launch checklist |
| `cicd-automation`, `deployment-strategies`, `observability-monitoring` | [wshobson/agents](https://github.com/wshobson/agents) | Deployment strategy and monitoring on larger infrastructure |
| `/ship`, `/canary` | [garrytan/gstack](https://github.com/garrytan/gstack) | Release and canary checks |

Calibration task: Set up CI on every push and a one-command rollback. Pass if both are demonstrated, not described.

## Reporting to the CMO

### head-of-sales

**Head of Sales** — Turn the positioning into a pipeline: find the right accounts, start conversations, and learn why deals are won or lost.

Delivers:

- A target-account list with the reason for each
- Outreach sequences and call preparation
- Battlecards and objection handling
- A weekly pipeline review

| Skills | From | Use them when |
|---|---|---|
| `account-research`, `lead-triage`, `draft-outreach`, `call-prep`, `handle-objection`, `close-plan`, `pipeline-review`, `forecast` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | The daily sales loop, from research to pipeline review |
| `prospecting`, `cold-email`, `sales-enablement`, `revops` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Outbound sequences and sales collateral, in the product-marketing context |
| `competitive-battlecard`, `ideal-customer-profile` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Battlecards; checking an account against the ICP |
| `predictable-revenue`, `influence-psychology`, `negotiation` | [wondelai/skills](https://github.com/wondelai/skills) | Outbound method and negotiation |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) | Before any message leaves your folder |

Calibration task: Build a list of ten target accounts with a one-line reason each and draft the first message to one of them. Nothing is sent. Pass if the CMO would send that message.

### head-of-growth

**Head of Growth** — Find what moves acquisition and activation, by running small measured experiments.

Delivers:

- A funnel audit
- An experiment backlog ranked by expected impact and cost
- A readout of each experiment

| Skills | From | Use them when |
|---|---|---|
| `cro`, `signup`, `onboarding`, `ab-testing`, `analytics`, `conversion-tracking`, `attribution` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Funnel audits, experiments and measurement |
| `cro-methodology` | [wondelai/skills](https://github.com/wondelai/skills) | Structuring an experiment |
| `performance-report` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | The readout the CMO takes to the board |

Calibration task: Audit the signup funnel and propose three experiments. Pass if each names its metric, its expected effect, and what it costs to run.

### head-of-content

**Head of Content** — Earn attention with content people search for and want to read, in the brand's voice.

Delivers:

- A content plan tied to search demand
- Finished articles and social posts
- An SEO audit after each release of the site

| Skills | From | Use them when |
|---|---|---|
| `content-strategy`, `copywriting`, `copy-editing`, `seo-audit`, `ai-seo`, `programmatic-seo`, `schema`, `social` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Planning, writing and optimising content |
| `seo-content-brief`, `seo-cluster`, `seo-technical`, `seo-geo` | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | Content briefs, topic clusters, technical and AI-search audits |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) | Last pass on every piece |

Calibration task: Produce the first month's content plan and one finished article. Pass if the article reads as written by a person who knows the customer.

## Reporting to the CFO

### financial-analyst

**Financial Analyst** — Build and maintain the financial model, and report actuals against it.

Delivers:

- `board/cfo/model.xlsx` with an assumptions sheet
- Three scenarios
- A monthly budget-versus-actual note

| Skills | From | Use them when |
|---|---|---|
| `xlsx` | [anthropics/skills](https://github.com/anthropics/skills) | Every model is a real spreadsheet with formulas |
| `3-statement-model`, `audit-xls` | [anthropics/financial-services](https://github.com/anthropics/financial-services) | Building the model; auditing it before the CFO sees it |
| `financial-analyst`, `saas-metrics-coach` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Ratios, SaaS metrics and their benchmarks |
| `startup-financial-modeling`, `startup-metrics-framework` | [wshobson/agents](https://github.com/wshobson/agents) | Startup-shaped projections |

Calibration task: Build the twelve-month model from the charter's assumptions with three scenarios. Pass if every output traces to an assumption cell and the model survives an audit.

### pricing-lead

**Pricing Lead** — Find the price and packaging that customers accept and the model needs.

Delivers:

- Pricing options with the reasoning for each
- A pricing-page brief for the CMO and Head of Design
- A plan to test the price

| Skills | From | Use them when |
|---|---|---|
| `pricing-strategy`, `monetization-strategy` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Generating and comparing pricing options |
| `pricing` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Packaging and the pricing page |
| `pricing-strategist`, `commercial-forecaster` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Price tests and their revenue effect |

Calibration task: Propose three pricing structures. Pass if each states the customer it favours, the metric it optimises, and its effect on the model.

### controller

**Controller** — Keep the books true once money moves: cash, invoices, reconciliation, month-end.

Delivers:

- A monthly cash-flow snapshot
- Reconciled accounts
- A list of overdue invoices and what was done about each

| Skills | From | Use them when |
|---|---|---|
| `reconciliation`, `journal-entry`, `close-management`, `financial-statements`, `cash-flow-snapshot`, `invoice-chase`, `tax-prep` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | The monthly close and the cash position |
| `xlsx` | [anthropics/skills](https://github.com/anthropics/skills) | Workpapers |

Calibration task: Produce this month's cash-flow snapshot and list every unreconciled item. Pass if the CFO can tie it to the bank balance.

## Reporting to the COO

### head-of-project

**Head of Project** — Keep the plan true: who does what by when, what depends on what, and which date is at risk first.

Delivers:

- A milestone roadmap with owners and dependencies
- `board/STATUS.md` kept current
- A weekly status report and a risk register

| Skills | From | Use them when |
|---|---|---|
| `outcome-roadmap`, `sprint-plan`, `pre-mortem`, `stakeholder-map`, `retro` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Roadmap, sprint plans, pre-mortems and retros |
| `to-tickets`, `triage`, `wayfinder`, `handoff` | [mattpocock/skills](https://github.com/mattpocock/skills) | Cutting work into tickets, triaging incoming work, handing off between sessions |
| `status-report`, `risk-assessment`, `task-management`, `sprint-planning`, `stakeholder-update` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Status reports, the risk register, task tracking |
| `senior-pm`, `scrum-master` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Portfolio and sprint health checks |

Calibration task: Turn the approved plan into a milestone roadmap with owners, dependencies and the critical path. Pass if it names the first date at risk and why.

### legal-counsel

**Legal and Compliance Lead** — Spot legal and compliance exposure early and prepare drafts for a qualified lawyer to review. Never the final word on a legal question.

Delivers:

- A list of the legal documents the product needs before launch
- First drafts for lawyer review
- A compliance checklist with open items

| Skills | From | Use them when |
|---|---|---|
| `review-contract`, `triage-nda`, `compliance-check`, `legal-risk-assessment` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Triage of contracts and compliance questions |
| `vendor-agreement-review`, `saas-msa-review`, `dpa-review`, `pia-generation` | [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal) | Vendor agreements, data-processing agreements, privacy impact assessments |
| `privacy-policy`, `draft-nda` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | First drafts |

Calibration task: List the legal documents this product needs before launch and outline the privacy policy. Pass if each item says why it applies to this product.

### head-of-customer-success

**Head of Customer Success** — Make sure customers get an answer and get value, and bring what they say back to the board.

Delivers:

- A help centre
- Reply drafts for incoming tickets
- A monthly summary of what customers ask for and complain about

| Skills | From | Use them when |
|---|---|---|
| `ticket-triage`, `draft-response`, `customer-escalation`, `kb-article` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | The support loop |
| `customer-success-manager` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Health scores and churn risk |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) | Before any reply goes to a customer |

Calibration task: Write one help-centre article and draft replies to three realistic tickets. Pass if the COO would send them as written.

## Reporting to the Head of Design

### ux-researcher

**UX Researcher** — Replace the board's assumptions about users with evidence.

Delivers:

- Interview guides and usability test plans
- Syntheses of what users said, as themes with quotes
- A list of assumptions that the evidence contradicts

| Skills | From | Use them when |
|---|---|---|
| `user-research`, `research-synthesis` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Planning research and synthesising it |
| `interview-script`, `opportunity-solution-tree` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Interview scripts; mapping findings to opportunities |
| `mom-test` | [wondelai/skills](https://github.com/wondelai/skills) | Asking questions people cannot answer politely |

Calibration task: Write an interview guide for the target user and synthesise three existing sources of feedback into themes. Pass if no question in the guide leads the witness.

### design-system-lead

**Design System Lead** — Build and guard the design system: tokens and components that make every screen consistent by default.

Delivers:

- `board/design/design-system.md` and the tokens in code
- Core components with all their states
- An audit of each new screen against the system

| Skills | From | Use them when |
|---|---|---|
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Documenting the system; auditing and polishing components |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Looking up palettes, pairings and rules when defining tokens |
| `better-typography`, `better-colors`, `better-layout`, `better-accessibility` | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | Tuning the type scale, the colour system and spacing |
| `design-system`, `design-handoff` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Auditing for hard-coded values; handoff specs |

Calibration task: Build the tokens and three core components. Pass if they clear the audit with no blocking finding.

### motion-designer

**Motion Designer** — Give the product motion that explains and delights without slowing anyone down.

Delivers:

- Motion principles for the product
- The key interactions, animated
- A motion review of each release

| Skills | From | Use them when |
|---|---|---|
| `emil-design-eng`, `animate`, `choreograph`, `review-animations`, `animation-performance`, `gestures` | [emilkowalski/skills](https://github.com/emilkowalski/skills) | Deciding what to animate, building it, reviewing it |
| `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-performance` | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | Timelines and scroll scenes when GSAP is the library |
| `remotion-best-practices` | [remotion-dev/skills](https://github.com/remotion-dev/skills) | Video: launch films and explainers |

Calibration task: Animate the product's key interaction. Pass if it holds 60 fps on a mid-range phone and respects reduced-motion.
