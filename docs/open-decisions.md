# Open decisions

These decisions are needed before MIP Drafts Console v2.1 replaces the Editor Delay Tracker. The defaults below are what v2.1 does today. Rule IDs refer to `docs/rule-map.html`.

The evidence comes from two sources:

- **Testing:** the side-by-side test runs on 29 Sep 2026, written up in `docs/test-report.html`.
- **Meeting:** *MIP Efficiencies Interface: AI COE Session*, 29 Sep 2026. Present: Iris Poesse, Gayatri Allamsetty, Daniel Liste Plicio, Madison Enis, Nelson Mercado, Shipra Verma.

## Direction confirmed in the meeting

- **One unified, standard tool.** Iris wants a single "stamped, vetted" way of doing manuscript management that every EA at every vendor partner follows, instead of people picking and choosing tools. She named Daniel's Chief Editor escalation as a feature that must carry over.
- **The main users are vendor EAs.** There are about 100 EAs across 3 vendor partners. They have no Power BI access and can't see other vendors' journals. They receive a journal-level "paginated" MIP report by email subscription and upload it to the HTML tool. The tool must keep working on single-journal files.

## Needs a decision (blocks rollout)

| Rule | Question | v2.1 default | Evidence | Decided by | Decision |
|---|---|---|---|---|---|
| CL-5 | Should Health Check "On Track" stop a paper from being flagged? | No. Available as an optional setting in Step 03. | **Testing:** this one rule changes the result from 33 flagged papers to 12. In 15 of the 17 papers only MIP flagged, Health Check was "On Track". **Meeting:** Daniel said Health Check is based purely on how long a paper has been in a stage, so an active editor can still show as overdue. Iris said the benchmarks have "serious limitations". **Leaning:** keep the v2.1 default. Daniel to confirm he's happy dropping the rule. | PRP, with Daniel | |
| TH-1 *(new)* | Should the invite grace period be set **per journal**? | One setting for all journals (10 days) | **Meeting:** Gayatri uses 21 days, and other journals use 10 or 30. She called this the only real difference between the two tools. Daniel warned that EAs work to fixed written instructions, so too much configuration can backfire. **Proposal:** a per-journal threshold table with defaults set by PRP, which EAs don't change. | PRP (Iris) | |
| EM-1 / EM-7 | Which email template: Daniel's "Papers Pending Your Action" or Gayatri's "Action summary"? Which subject line and styling? | Gayatri's template | **Testing:** Daniel's template isn't in v2.1. **Meeting:** not discussed. | PRP, Daniel, Gayatri | |
| EM-4 | Should internal EA notes and the "Reviews Pending – EA follow-up" section appear in editor emails? | Yes | **Testing:** that text is written for staff. A setting already moves Reviews Pending to a separate sheet. **Meeting:** not discussed. | PRP | |

## Resolved by the meeting

| Rule | Outcome | Evidence |
|---|---|---|
| GR-1 | **Keep both grouping modes.** The default depends on portfolio type, not a single global setting: *one email per editor, per journal* for journals with external editors, and *one combined email per editor across all journals* for Wiley Forward journals with internal editors. | Gayatri demoed Manisha's Wiley Forward portfolio (about 40 journals, internal editors). Those editors want one combined email and per-journal workbooks with every editor in the To: field. |

## Confirm only (testing supports the default)

| Rule | Default | Evidence | Confirmed by | Confirmed |
|---|---|---|---|---|
| IN-1 | The source report is the MIP Summary Report / paginated MIP subscription | **Testing:** worked in both tools. **Meeting:** Daniel and Gayatri both use the MIP report. Daniel said the paginated version is "essentially the same". | Daniel | |
| SC-1 | MIP's eligibility rules (author and EA-side rows excluded) | **Testing:** same 78 editor rows as EDT's allow-list. | Gayatri, Daniel | |
| SC-2 | The email goes to the assigned Handling Editor | **Testing:** the recipient matched Task Performer Name on 67 of 67 papers. | PRP | |
| CL-6 | If every accepted reviewer is overdue → "Invite Reviewers" | **Testing:** one real case (3771449). **Meeting:** Gayatri described EAs asking editors to invite more reviewers when a reviewer has gone quiet for months. | PRP | |
| AU-3 | No manuscript data kept in the browser | **Testing:** EDT kept it; v2.1 doesn't. **Meeting:** vendors can't see each other's journals, which supports not keeping data. | InfoSec | |

## New questions

| # | Question | v2.1 default | Source | Decision |
|---|---|---|---|---|
| Q1 | How many unique reviews are needed before a paper is "ready for decision"? Is it the same for every journal? | 2 | Testing | |
| Q2 | Chief Editor escalation defaults | ≥ 1 paper needing action, or ≥ 50% of an editor's papers | Testing. In the meeting, Daniel demoed "a minimum of 2 delays". | |
| Q3 | Should "Reviews Pending" count toward an editor's delayed proportion (Step 05b)? | No | Testing | |
| Q4 | Who owns v2.1, where is it hosted, and who handles support? | Nelson and Gayatri (named in the guide) | Meeting: Nelson is meeting the internal hosting team this week. Tools are currently shared through the PRP team's tools hub. | |
| Q5 | How is the tool rolled out to EAs? | Not decided | Meeting: Daniel said tools can't simply be passed from EA to EA. Rollout has to go through the vendor management team. | |
| Q6 | Should "sent" tracking (and later "replied") be built? | Not built: the tool shows "drafted" only | Meeting: on Iris's wish list. Some journals now send from **Freshdesk** instead of Outlook, so tracking built on Microsoft Graph wouldn't cover them. | |

## Product scope (added 15 Oct 2026)

These come from mapping the five PRP tools (`docs/tool-landscape.md`). They're asked in `docs/scope-questions.md`.

| ID | Question | Current assumption | Evidence | Decided by | Decision |
|---|---|---|---|---|---|
| PS-1 | Is PRPL Portfolio Insights in scope? Who built it, and do they agree to a merge? | Release 2 (merge plan drafted) | The tool reads the same MIP report. It adds trends, KPI benchmarking and bottleneck advice. Its author isn't stated in the file. | Iris | |
| PS-2 | Which "overdue" is the standard across every view: Health Check, or "needs action"? | "Needs action" (v2.2) | Portfolio Insights and Aria use Health Check. The console doesn't (see CL-5). | Iris | |
| PS-3 | Portfolio Insights' AI features: drop them, or route them through an approved Wiley AI service? | Drop them | They send manuscript IDs and editor names to the Anthropic API, and only work inside Claude.ai | Iris / InfoSec | |
| PS-4 | One stage-definition list for every view | The console's official list | The three tools define E1, E4A and other stages differently | Iris | |
| PS-5 | Which editor-performance view to keep | Portfolio Insights' version (benchmarks and targets) | v2.2 Tab 5 and Portfolio Insights both use the Full Manuscript Listing | Iris, with Gayatri | |
| PS-6 | How does Aria / PeerPulse relate to this work: merge, replace, or a separate product we link to? | A separate analytics product, linked from the tool | Aria covers 12-month journal KPIs and the team hierarchy, and its data is a frozen snapshot | Iris | |

## Live data (added 20 Oct 2026)

| # | Question | Proposed | Why | Decides | Decision |
|---|---|---|---|---|---|
| LD-1 | Can the **hosted** console call Microsoft sign-in and the Power BI API to load the MIP report as the signed-in user? This changes CLAUDE.md hard rule 6 ("no network"). | Yes, limited to `login.microsoftonline.com` and `api.powerbi.com`, hosted copy only | Users stop exporting and uploading. The data is limited to what the user can already see in Power BI. Nothing is stored. See `docs/power-bi-live-data-plan.md`. | Iris; InfoSec review | |
| LD-2 | Keep file upload when live data arrives? | Yes, as a fallback and for the standalone file | Covers outages, users without Power BI access, and offline use | Iris | |

## Dependencies outside this team

These need Luke Barrett's team (Power BI subscriptions).

| # | Request | Why it matters |
|---|---|---|
| D1 | Add **Last Editor Action Date** / **Days Since Last Editor Action** to the MIP Summary Report | Today these fields are only in the Activity Tracker, one journal at a time. Adding them would make the grace period exact instead of estimated. Gayatri has already asked for this. |
| D2 | A **Reviewer Performance Report** subscription for EAs, or an equivalent | EAs can't get this report, so reviewer reminders take them hours. The Reviewer Reminders tab needs it. |
| D3 | Explain how subscription reports are mapped to each editorial office inbox | Needed for any future live data feed. Nobody in the meeting knew where the mapping is maintained. |

## Waiting on

- Gayatri: the manuscript lifecycle map/deck. Nelson has a copy.
- Iris: the wish list notes.
