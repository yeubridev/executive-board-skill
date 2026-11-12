# Skill stacks

<!-- Generated from skills/executive-board/assets/registry.json by tools/build.py. -->

Every third-party skill the executive board recommends, by seat. Checked 2026-11-12:
repository, licence, skill names and install commands were read from each repository on that
date. **Curated, not audited** — these projects change, and a skill runs with your agent's
permissions. Read what you install.

Tiers: **core** (install at kickoff) · **recommended** (install when its phase starts) ·
**optional** (only in the situation named).

## CEO

| Tier | Skills | From | Use it for |
|---|---|---|---|
| core | `product-strategy`, `product-vision`, `startup-canvas`, `lean-canvas`, `business-model`, `value-proposition`, `market-sizing`, `competitor-analysis` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Strategy canvases, market sizing and competitor analysis behind the first three docket items. |
| core | `ceo-advisor`, `scenario-war-room`, `competitive-intel`, `board-deck-builder` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | CEO decision frameworks, scenario planning, competitive intelligence, board decks. |
| core | `write-spec`, `competitive-brief`, `metrics-review`, `stakeholder-update`, `product-brainstorming` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Write the PRD, review metrics, update the founder. |
| recommended | `/office-hours`, `/plan-ceo-review` | [garrytan/gstack](https://github.com/garrytan/gstack) | Pressure-test the idea before the charter and the plan before the build, the way a demanding investor would. |
| recommended | `grill-me`, `to-spec` | [mattpocock/skills](https://github.com/mattpocock/skills) | Get interrogated on the plan until every open branch is resolved; turn the result into a spec. |
| recommended | `defining-product-strategy`, `high-stakes-decisions`, `evaluating-startup-ideas`, `measuring-pmf` | [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) | Practitioner judgment on strategy, one-way-door decisions and product-market fit. |
| recommended | `pptx`, `docx` | [anthropics/skills](https://github.com/anthropics/skills) | Decks and memos for the founder or outside readers. |
| optional | `deck-review`, `ic-sim`, `competitive-positioning`, `market-sizing` | [lool-ventures/founder-skills](https://github.com/lool-ventures/founder-skills) | When raising money: deck review and a simulated investment committee. |

## CTO

| Tier | Skills | From | Use it for |
|---|---|---|---|
| core | `brainstorming`, `writing-plans`, `test-driven-development`, `subagent-driven-development`, `systematic-debugging`, `verification-before-completion`, `requesting-code-review`, `using-git-worktrees`, `finishing-a-development-branch` | [obra/superpowers](https://github.com/obra/superpowers) | The process layer: how work moves from idea to merged, tested code. Exactly one process layer should be always-on. |
| core | `setup-matt-pocock-skills`, `grill-with-docs`, `to-spec`, `to-tickets`, `wayfinder`, `codebase-design`, `domain-modeling`, `improve-codebase-architecture`, `prototype` | [mattpocock/skills](https://github.com/mattpocock/skills) | Requirement interrogation, specs, tickets, and architecture: deep modules, a shared domain language. |
| core | `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Always-on restraint: build the least code that solves it. Review diffs with ponytail-review; audit debt periodically. |
| core | `code-review`, `security-guidance` | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Independent multi-agent review of every pull request; security hooks on edits and commits. |
| recommended | `differential-review`, `insecure-defaults`, `supply-chain-risk-auditor`, `sharp-edges` | [trailofbits/skills](https://github.com/trailofbits/skills) | Security review of each release's diff, defaults and dependencies. |
| recommended | `api-and-interface-design`, `documentation-and-adrs`, `security-and-hardening`, `ci-cd-and-automation`, `observability-and-instrumentation`, `shipping-and-launch` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Interface design, architecture decision records, CI/CD, observability and the launch checklist. |
| recommended | `tdd-workflow`, `verification-loop`, `security-review`, `e2e-testing`, `deployment-patterns`, `docker-patterns`, `postgres-patterns` | [affaan-m/ECC](https://github.com/affaan-m/ECC) | *Alternative to obra/superpowers.* The all-in-one alternative to superpowers: one harness with agents, hooks, rules and stack patterns. |
| recommended | `/qa`, `/review`, `/cso`, `/ship`, `/canary` | [garrytan/gstack](https://github.com/garrytan/gstack) | Real-browser QA and release engineering, called by name. |
| recommended | `pr-review-toolkit`, `claude-security` | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Specialised review agents (silent failures, test gaps, types) and a verified deep security scan before launch. |
| recommended | `webapp-testing`, `mcp-builder` | [anthropics/skills](https://github.com/anthropics/skills) | Browser-driven testing of web apps; building MCP servers. |
| optional | `security-audit` | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Whole-repository audit with a coverage ledger. Use this or claude-security as the pre-launch audit, not both. |
| optional | `cicd-automation`, `deployment-strategies`, `observability-monitoring`, `incident-response`, `database-migrations`, `kubernetes-operations`, `cloud-infrastructure` | [wshobson/agents](https://github.com/wshobson/agents) | When the infrastructure is more than a managed platform: Kubernetes, multi-cloud, on-call. |
| optional | `ce-brainstorm`, `ce-plan`, `ce-work`, `ce-code-review`, `ce-compound` | [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) | *Alternative to obra/superpowers.* Alternative process layer for long-lived products where capturing lessons each cycle matters most. |
| optional | `vercel-react-best-practices`, `vercel-composition-patterns` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | When the stack is React or Next.js. |
| optional | `supabase`, `supabase-postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | When the stack uses Supabase or Postgres. |
| optional | `terraform` | [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) | When infrastructure is managed with Terraform. |
| optional | `cloudflare` | [cloudflare/skills](https://github.com/cloudflare/skills) | When deploying on Cloudflare. |

## CMO

| Tier | Skills | From | Use it for |
|---|---|---|---|
| core | `product-marketing`, `customer-research`, `competitor-profiling`, `copywriting`, `copy-editing`, `content-strategy`, `seo-audit`, `ai-seo`, `programmatic-seo`, `schema`, `social`, `launch`, `directory-submissions`, `ads`, `ad-creative`, `emails`, `onboarding`, `churn-prevention`, `cro`, `signup`, `ab-testing`, `analytics`, `conversion-tracking`, `attribution`, `pricing` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | The marketing backbone. Run product-marketing first: it writes the shared context every other skill reads. |
| core | `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) | Last pass on anything a customer will read. |
| recommended | `ideal-customer-profile`, `beachhead-segment`, `gtm-strategy`, `competitive-battlecard`, `positioning-ideas`, `value-prop-statements`, `north-star-metric` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | ICP, beachhead, go-to-market motion, positioning options and battlecards for docket items 2 and 7. |
| recommended | `campaign-plan`, `brand-review`, `competitive-brief`, `performance-report`, `email-sequence`, `discover-brand`, `guideline-generation`, `brand-voice-enforcement` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Campaign briefs, performance reports, and a brand voice that is discovered, written down and enforced. |
| recommended | `seo-audit`, `seo-technical`, `seo-geo`, `seo-schema`, `seo-content-brief`, `seo-cluster` | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | Deep technical SEO and AI-search audits once there is a site. Strategy stays in marketingskills; audits happen here. |
| recommended | `obviously-awesome`, `storybrand-messaging`, `cro-methodology`, `hundred-million-offers`, `made-to-stick` | [wondelai/skills](https://github.com/wondelai/skills) | Named frameworks for positioning, messaging and offers. Feed the results into the product-marketing context. |
| optional | `ads-audit`, `ads-google`, `ads-meta`, `ads-linkedin`, `ads-creative`, `ads-budget` | [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | When paid spend is live: audit the accounts. |
| optional | `remotion-best-practices`, `remotion-create`, `remotion-render`, `remotion-captions` | [remotion-dev/skills](https://github.com/remotion-dev/skills) | When marketing needs video, in React. Use this or hyperframes. |
| optional | `hyperframes` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | *Alternative to remotion-dev/skills.* When marketing needs video, from HTML. |

## CFO

| Tier | Skills | From | Use it for |
|---|---|---|---|
| core | `cfo-advisor`, `financial-analyst`, `saas-metrics-coach` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Unit economics, SaaS metrics, runway and scenario maths with script-backed calculators. |
| core | `xlsx` | [anthropics/skills](https://github.com/anthropics/skills) | Build the model as a real spreadsheet with formulas, not a table in prose. |
| core | `pricing-strategy`, `monetization-strategy`, `business-model` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Pricing and monetisation options for docket item 3. |
| recommended | `3-statement-model`, `dcf-model`, `comps-analysis`, `audit-xls` | [anthropics/financial-services](https://github.com/anthropics/financial-services) | A full three-statement model, valuation, and an audit of the spreadsheet before anyone relies on it. |
| recommended | `financial-statements`, `variance-analysis`, `close-management`, `reconciliation`, `journal-entry`, `cash-flow-snapshot`, `invoice-chase`, `tax-prep` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | After launch: statements, budget versus actual, month-end close, cash and invoices. |
| recommended | `startup-financial-modeling`, `startup-metrics-framework`, `market-sizing-analysis` | [wshobson/agents](https://github.com/wshobson/agents) | Startup-shaped projections and business cases. |
| recommended | `pricing-strategist`, `commercial-forecaster` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Price testing and revenue forecasting. |
| recommended | `pricing` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Packaging and the pricing page, with the CMO. |
| optional | `financial-model-review`, `cap-table` | [lool-ventures/founder-skills](https://github.com/lool-ventures/founder-skills) | When raising money: model review and cap-table scenarios. |
| optional | `charlie` | [EveryInc/charlie-cfo-skill](https://github.com/EveryInc/charlie-cfo-skill) | For a bootstrapped company: runway and thirteen-week cash flow. |

## COO

| Tier | Skills | From | Use it for |
|---|---|---|---|
| core | `process-doc`, `runbook`, `status-report`, `risk-assessment`, `compliance-tracking`, `vendor-review`, `capacity-plan`, `change-request`, `task-management`, `memory-management` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Process documents, runbooks, status reports, the risk register, task tracking. |
| core | `coo-advisor`, `company-os`, `change-management`, `process-mapper`, `knowledge-ops`, `capacity-planner`, `vendor-management` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Operating cadence, process mapping, capacity and vendor management. |
| core | `outcome-roadmap`, `brainstorm-okrs`, `sprint-plan`, `pre-mortem`, `stakeholder-map`, `prioritization-frameworks`, `retro` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Roadmap, OKRs, sprint plans, pre-mortems and retros. |
| recommended | `review-contract`, `triage-nda`, `compliance-check`, `legal-risk-assessment`, `recruiting-pipeline`, `onboarding`, `org-planning`, `ticket-triage`, `draft-response`, `kb-article` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Contract and compliance triage, hiring, and the support desk. |
| recommended | `goal-setting-okrs`, `planning-cadence`, `org-design`, `running-meetings` | [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) | Practitioner judgment on goals, planning rhythm and org design. |
| recommended | `internal-comms`, `doc-coauthoring`, `docx`, `pdf` | [anthropics/skills](https://github.com/anthropics/skills) | Status updates, co-written documents, and documents for outside parties. |
| optional | `vendor-agreement-review`, `nda-review`, `saas-msa-review`, `dpa-review`, `pia-generation` | [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal) | Once real contracts or personal data exist. Output is a draft for a qualified lawyer, never legal advice. |
| optional | `privacy-policy`, `draft-nda` | [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | First drafts of the privacy policy and NDAs for lawyer review. |

## Head of Design

| Tier | Skills | From | Use it for |
|---|---|---|---|
| core | `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | The primary aesthetic layer: init and shape the direction, then critique, audit and polish every surface. |
| core | `frontend-design`, `canvas-design`, `theme-factory` | [anthropics/skills](https://github.com/anthropics/skills) | Baseline for distinctive frontend work; boards and visual explorations; themes for artifacts. |
| core | `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Reference database for the design system: styles, palettes, font pairings, industry rules. Look things up here, then shape them. |
| core | `emil-design-eng`, `animate`, `review-animations`, `improve-animations`, `choreograph`, `animation-performance`, `gestures` | [emilkowalski/skills](https://github.com/emilkowalski/skills) | Motion judgment: whether to animate, how, and a review of what was built. |
| core | `web-design-guidelines` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Cheap rule audit on every user-facing change: accessibility, focus, forms, motion, typography. |
| recommended | `hallmark` | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | New landing pages with a hard quality floor, and audits of existing ones. One pipeline per page: this or taste skill. |
| recommended | `design-taste-frontend` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Showcase and marketing sites where motion carries the brand. One pipeline per page: this or hallmark. |
| recommended | `better-typography`, `better-colors`, `better-layout`, `better-accessibility`, `interface-review` | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | Specialists for tuning type, colour and layout, and for reviewing interface changes. |
| recommended | `user-research`, `research-synthesis`, `design-critique`, `design-system`, `accessibility-review`, `ux-copy`, `design-handoff` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | User research and synthesis, structured critique, UX copy, and handoff specs for engineering. |
| recommended | `accessibility`, `core-web-vitals` | [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) | The measured accessibility and performance gate before launch. |
| optional | `figma-use`, `figma-design-to-code`, `figma-generate-design`, `figma-generate-library`, `figma-code-connect` | [figma/mcp-server-guide](https://github.com/figma/mcp-server-guide) | When the team works in Figma. |
| optional | `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-react`, `gsap-performance` | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | When motion is built with GSAP: timelines and scroll scenes done correctly. |
| optional | `remotion-best-practices` | [remotion-dev/skills](https://github.com/remotion-dev/skills) | When the product needs video: launch films, animated explainers. |
| optional | `shadcn` | [shadcn/ui](https://github.com/shadcn-ui/ui) | When the component layer is shadcn/ui. |
| optional | `brandkit`, `imagegen-frontend-web`, `image-to-code` | [Leonxlnx/imagegen-skills](https://github.com/Leonxlnx/imagegen-skills) | When the agent can generate images: brand kits and visual comps before code. |

## Sub-agent archetypes

| Archetype | Reports to | Skills from |
|---|---|---|
| Head of Product (`head-of-product`) | CEO | [phuryn/pm-skills](https://github.com/phuryn/pm-skills), [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [mattpocock/skills](https://github.com/mattpocock/skills) |
| Market Analyst (`market-analyst`) | CEO | [phuryn/pm-skills](https://github.com/phuryn/pm-skills), [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills), [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) |
| Tech Lead (`tech-lead`) | CTO | [obra/superpowers](https://github.com/obra/superpowers), [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), [mattpocock/skills](https://github.com/mattpocock/skills) |
| QA Lead (`qa-lead`) | CTO | [anthropics/skills](https://github.com/anthropics/skills), [garrytan/gstack](https://github.com/garrytan/gstack), [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), [obra/superpowers](https://github.com/obra/superpowers) |
| Security Lead (`security-lead`) | CTO | [trailofbits/skills](https://github.com/trailofbits/skills), [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| DevOps Lead (`devops-lead`) | CTO | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), [wshobson/agents](https://github.com/wshobson/agents), [garrytan/gstack](https://github.com/garrytan/gstack) |
| Head of Sales (`head-of-sales`) | CMO | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), [phuryn/pm-skills](https://github.com/phuryn/pm-skills), [wondelai/skills](https://github.com/wondelai/skills), [blader/humanizer](https://github.com/blader/humanizer) |
| Head of Growth (`head-of-growth`) | CMO | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), [wondelai/skills](https://github.com/wondelai/skills), [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) |
| Head of Content (`head-of-content`) | CMO | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo), [blader/humanizer](https://github.com/blader/humanizer) |
| Financial Analyst (`financial-analyst`) | CFO | [anthropics/skills](https://github.com/anthropics/skills), [anthropics/financial-services](https://github.com/anthropics/financial-services), [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills), [wshobson/agents](https://github.com/wshobson/agents) |
| Pricing Lead (`pricing-lead`) | CFO | [phuryn/pm-skills](https://github.com/phuryn/pm-skills), [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) |
| Controller (`controller`) | CFO | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [anthropics/skills](https://github.com/anthropics/skills) |
| Head of Project (`head-of-project`) | COO | [phuryn/pm-skills](https://github.com/phuryn/pm-skills), [mattpocock/skills](https://github.com/mattpocock/skills), [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) |
| Legal and Compliance Lead (`legal-counsel`) | COO | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal), [phuryn/pm-skills](https://github.com/phuryn/pm-skills) |
| Head of Customer Success (`head-of-customer-success`) | COO | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills), [blader/humanizer](https://github.com/blader/humanizer) |
| UX Researcher (`ux-researcher`) | Head of Design | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), [phuryn/pm-skills](https://github.com/phuryn/pm-skills), [wondelai/skills](https://github.com/wondelai/skills) |
| Design System Lead (`design-system-lead`) | Head of Design | [pbakaus/impeccable](https://github.com/pbakaus/impeccable), [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), [jakubkrehel/skills](https://github.com/jakubkrehel/skills), [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) |
| Motion Designer (`motion-designer`) | Head of Design | [emilkowalski/skills](https://github.com/emilkowalski/skills), [greensock/gsap-skills](https://github.com/greensock/gsap-skills), [remotion-dev/skills](https://github.com/remotion-dev/skills) |

## Sources

| Repository | Licence | Stars | What it is |
|---|---|---|---|
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT | ~116k | Lifecycle engineering skills with strong shipping and operations coverage. |
| [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) | MIT | ~3k | Measured web quality: accessibility (WCAG 2.2), Core Web Vitals, performance. |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | MIT | ~302k | ECC (formerly everything-claude-code): an all-in-one harness of agents, skills, hooks and rules. |
| [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | MIT | ~11k | Audits of paid-ad accounts across platforms; read-only, proposes changes as drafts. |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | MIT | ~28k | Deep SEO and AI-search audits: technical, schema, content briefs, clusters. |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | MIT | ~30k | Largest business-role skill library, with script-backed calculators: C-level advisors, finance, operations, product and project management. |
| [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal) | Apache-2.0 | ~10k | Legal practice plugins: commercial contracts, privacy, employment, product counsel. |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Apache-2.0 (per-plugin licences vary) | ~47k | Anthropic's official Claude Code plugin marketplace: first-party review and security plugins, plus vetted third-party ones. |
| [anthropics/financial-services](https://github.com/anthropics/financial-services) | Apache-2.0 | ~41k | Institutional-grade spreadsheet modelling: three-statement, DCF, comparables, model audit. |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Apache-2.0 | ~36k | Anthropic's role plugins for knowledge work, with connectors: operations, finance, legal, HR, support, sales, marketing, product, design. |
| [anthropics/skills](https://github.com/anthropics/skills) | Apache-2.0 | ~193k | Anthropic's reference skills: office documents, frontend design, web-app testing, MCP building, skill authoring. |
| [blader/humanizer](https://github.com/blader/humanizer) | MIT | ~68k | Removes the tells of machine-written prose and matches a voice sample. |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | MIT | ~71k | Phased whole-repository security audit with a coverage ledger and independent verification. |
| [cloudflare/skills](https://github.com/cloudflare/skills) | Apache-2.0 | ~3k | Cloudflare platform skills from the vendor. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | ~60k | Broadest maintained marketing pack: positioning, copy, SEO, launch, ads, email, CRO, analytics and sales enablement around one shared product-context document. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT | ~189k | Write-less-code discipline: is it needed, can it be reused, does the platform already do it. Never trades away validation, security or accessibility. |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT | ~56k | Motion and interaction craft from a design engineer: when and how to animate, review, performance, gestures. |
| [EveryInc/charlie-cfo-skill](https://github.com/EveryInc/charlie-cfo-skill) | MIT | <1k | Bootstrapped-company CFO: runway and thirteen-week cash flow. |
| [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) | MIT | ~26k | Plan, work, review, and capture what was learned so each cycle makes the next one easier. |
| [figma/mcp-server-guide](https://github.com/figma/mcp-server-guide) | Figma Developer Terms (no open-source licence file) | ~2k | Figma's official plugin and skills: design to code, code to design, libraries, Code Connect, specs. |
| [garrytan/gstack](https://github.com/garrytan/gstack) | MIT | ~141k | Role-based sprint commands from a YC partner: founder-style idea and plan review, real-browser QA, release engineering. |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | MIT | ~18k | Official GSAP skills: core, timelines, ScrollTrigger, React, performance. |
| [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) | MPL-2.0 | ~1k | Terraform and Packer skills from the vendor. |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | ~83k | Programmatic video from HTML to MP4. |
| [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | MIT | ~12k | Craft specialists: typography, colour, layout, accessibility, interface review. |
| [Leonxlnx/imagegen-skills](https://github.com/Leonxlnx/imagegen-skills) | MIT | <1k | Brand kits and image-based design comps for agents that can generate images. |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | MIT | ~114k | Taste skill: high-end marketing and showcase sites with motion, checked in a real browser. |
| [lool-ventures/founder-skills](https://github.com/lool-ventures/founder-skills) | Apache-2.0 | <1k | Fundraising review written by a venture fund: deck, financial model, cap table, investment-committee simulation. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | ~322k | Small composable engineering skills that do not try to own the process: requirement interrogation, specs, tickets, architecture. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | ~148k | UI UX Pro Max: a searchable reference of styles, palettes, font pairings and UX guidelines, with a design-system generator. |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | MIT | ~54k | Hallmark: themed page builds, redesigns and audits with a browser lint and hard quality gates. |
| [obra/superpowers](https://github.com/obra/superpowers) | MIT | ~316k | Engineering methodology that triggers on its own: brainstorm, plan, test-first build, sub-agent execution, review, finish. |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Apache-2.0 | ~109k | Design vocabulary, commands and a deterministic detector for generic machine-made UI: shape, critique, audit, polish. |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | MIT | ~28k | Product-management frameworks as skills: strategy, market research, go-to-market, execution, pricing. |
| [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) | MIT | ~1.5k | Product and company-building judgment distilled from Lenny's Podcast and Newsletter. |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | No licence file in the skills repository; Remotion itself has its own licence terms | ~7k | Programmatic video in React, from the Remotion team. |
| [shadcn/ui](https://github.com/shadcn-ui/ui) | MIT | n/a | Project-aware shadcn/ui knowledge from the maintainers. |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | MIT | ~3k | Supabase and Postgres best practices from the vendor. |
| [trailofbits/skills](https://github.com/trailofbits/skills) | CC-BY-SA-4.0 | ~8k | Security-audit workflows from a professional security firm. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | MIT | ~34k | Vercel's rule sets: interface guidelines, React performance, composition patterns. |
| [wondelai/skills](https://github.com/wondelai/skills) | MIT | ~3k | Well-known business books turned into skills: positioning, messaging, offers, CRO, sales. |
| [wshobson/agents](https://github.com/wshobson/agents) | MIT | ~42k | Large marketplace of granular plugins; widest DevOps and infrastructure coverage, plus startup finance. |
