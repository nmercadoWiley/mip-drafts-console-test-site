# PRP tool landscape

**Last updated:** 15 Oct 2026 · **Status:** analysis, for scoping with Iris Poesse · **Source:** read from each tool's own code

The PRP team has five manuscript and portfolio tools. This page records what each one does, where they overlap, what's redundant, and the proposed release plan. A formatted version of the matrix is in `docs/prp-tools-matrix.html`.

The source files for **PRPL Portfolio Insights** and **Aria 2** are **not** in this repo:
- PRPL Portfolio Insights is someone else's work, and contains 3 unchecked screenshots.
- Aria 2 contains a built-in snapshot of KPIs and PRP staff names for about 1,200–1,600 journals.

Add either one only once Iris confirms it's in scope and its data has been checked.

## Three jobs, not five versions of one tool

| Layer | Question it answers | Users | Tools |
|---|---|---|---|
| **Action** | Who needs chasing today, and what's the email? | Vendor EAs (about 100), PRPLs | MIP Drafts Console + Editor Delay Tracker → **v2.2** (this repo) |
| **Oversight** | How is my portfolio doing this week? | PRPLs | PRPL Portfolio Insights |
| **Analytics** | How are journals, leads and managers performing over 12 months? | PRP managers, leads, director | Aria 2 / PeerPulse Intelligence ("Iris Poesse Team", Rishabh's proof of concept) |

## The five tools

| | MIP Drafts Console (original) | Editor Delay Tracker V36 | **MIP Drafts Console v2.2** | PRPL Portfolio Insights | Aria 2 / PeerPulse |
|---|---|---|---|---|---|
| Built by | Gayatri Allamsetty | Daniel Liste Plicio | AICOE merge of the two | Not stated in the file | Rishabh (proof of concept) |
| Looks at | Manuscripts | Manuscripts | Manuscripts | Manuscripts + journal KPIs | Journal KPIs (1,199 in Iris's portfolio, up to 1,630) + optional pipeline |
| Built as | One HTML file | One HTML file | One HTML file + admin page + tests | One HTML file, written as a Claude.ai artifact | React bundle (4.5 MB) with the data built in |
| Status | In use (Gayatri's EAs) | In use (Daniel's EAs) | Tested, not released | Unknown | Proof of concept |

## Capability matrix

● does it · ◐ partly · — doesn't

| Capability | MIP orig. | EDT | **v2.2** | Portfolio Insights | Aria 2 |
|---|:---:|:---:|:---:|:---:|:---:|
| **Data in** | | | | | |
| MIP report (Summary or paginated) | ● | ● | ● | ● | ◐ CSV only (Pipeline tab) |
| Activity Tracker | ● opt. | — | ● opt. | — | — |
| Reviewer Performance Report | ● | — | ● | — | — |
| Full Manuscript Listing | ● | — | ● | ● | — |
| Journal Performance export, KPI targets | — | — | — | ● | ● built-in snapshot (May 2025 – Apr 2026) |
| Keeps data after closing | — | ● browser | — by design | ◐ inside Claude.ai only | ● data ships in the file |
| **Action** | | | | | |
| "Needs action" logic beyond Health Check | ● | ◐ includes Health Check | ● | — Health Check only | — Health Check + days |
| Handling Editor reminder drafts | ● bulk | ● one at a time | ● bulk, approved wording | ◐ one, AI-written | — |
| Triage Editor drafts | ● | — | ● | — | — |
| Reviewer reminder drafts | ● | — | ● | — | — |
| EA summaries (V1, stale invites) | ● | — | ● | — | — |
| Delayed proportion per editor | — | ● | ● | — | — |
| Chief Editor escalation workbook | — | ● | ● | — | — |
| "Unblock today" queues | ◐ | — | ◐ | — | ● |
| Audit of what was drafted and why | ● | — | ● | — | — |
| Approved, editable templates | — | — | ● | — | — |
| **Oversight and analytics** | | | | | |
| EA-stage and author-stage overdues | ● | — | ● | ◐ | ◐ |
| Stalled editor queues / HE backlogs | ● | — | ● | ◐ | ● |
| Portfolio health summary | ◐ | — | ◐ | ● | ● health score and tier |
| Journal KPIs (TAT, accept, triage, withdrawal…) | — | — | — | ◐ | ● 40+ metrics, monthly |
| Editor performance | ● | — | ● | ● against benchmarks and targets | ◐ |
| Trends over time | — | — | — | ● against last upload | ● 12 months |
| Integrity flags | ◐ | — | ◐ | — | ● |
| Recommendations, action plans, briefs | — | — | — | ● rule-based | ● rule-based |
| Team view (director → manager → lead) | — | — | — | — | ● |
| Plain-English questions | — | — | — | ◐ AI summaries | ● keyword-based, not an AI model |
| **Data handling** | | | | | |
| Sends data outside the browser | No | No | No | **Yes:** Anthropic API (manuscript IDs, stages, editor names), and only inside Claude.ai | No |
| Real data inside the file | 3 screenshots with author names | None | Same 3 screenshots (backlog B2) | 3 screenshots, unchecked | Full KPI snapshot + PRP staff names |
| Refresh | Each upload | Each upload | Each upload | Each upload | KPIs need a rebuild |
| "Overdue" means | Needs action | Needs action + Health Check | Needs action (Health Check optional) | Health Check | Health Check |

## What's redundant

**Truly redundant: one version should go**

| What | Duplicated in | Keep | Retire |
|---|---|---|---|
| The whole MIP and EDT tools | MIP original, EDT V36, v2.2 | **v2.2** | Both originals, plus Gayatri's old Excel macro, once v2.2 is released. The one gap is Daniel's email template (decision EM-1). |
| Editor reminder emails | v2.2, Portfolio Insights (AI-written) | **v2.2** | Portfolio Insights' email drafter |
| Pipeline-by-stage from the MIP export | v2.2, Portfolio Insights (Most Overdue, workload), Aria (Pipeline tab) | **v2.2's "needs action" logic**, shared by all views | Aria's Pipeline tab, and Portfolio Insights' separate overdue calculation |
| Stage definitions | Three different lists | **One PRP-owned list** | The other two |
| Rule-based advice | Portfolio Insights (bottleneck fixes), Aria (action plans) | **One rule set**, decided by PRP | Whichever loses |

**Overlapping but different: keep both, link them**

| What | Where | Why it isn't redundant |
|---|---|---|
| Editor performance | v2.2 Tab 5, Portfolio Insights | Same input. Portfolio Insights adds benchmarks and targets. **Pick one home**: the oversight view. |
| Portfolio health | Portfolio Insights, Aria | This week's manuscripts against 12-month journal KPIs |
| Trends | Portfolio Insights, Aria | Week against week, versus month by month |
| Integrity checks | v2.2 Tab 5, Aria | Aria's set is broader. Fold v2.2's check into it eventually. |

## Proposed release plan

1. **Release 1, Action:** host v2.2 (MIP + EDT) with Wiley SSO for PRPLs and one pilot vendor. Sign off the open rules. Retire the MIP and EDT originals and the Excel macro.
2. **Release 2, Oversight:** fold Portfolio Insights into v2.2 as a PRPL tab (v2.3). See `docs/portfolio-insights-merge-plan.md`.
3. **Separate track, Analytics:** keep Aria / PeerPulse as the managers' analytics product, aligned with the Research Publishing data-layer work. The hosted tool links to it.

The open questions for Iris are in `docs/scope-questions.md`. The matching decisions (PS-1 to PS-6) are in `docs/open-decisions.md`.
