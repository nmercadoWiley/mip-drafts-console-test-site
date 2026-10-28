# Changelog

## Unreleased
- **Plan for loading data straight from Power BI** (`docs/power-bi-live-data-plan.md`): the console would query the MIP report as the signed-in user, with upload kept as a fallback. Adds backlog B20–B21 and decisions LD-1 (network rule change) and LD-2 (keep upload). Draft messages for the Power BI owners, IT and Iris are included. No code changed.
- **Signed-in user in the header:** on the hosted copy, the header shows "Signed in as <email>" above the date. nginx copies the email from the SSO header into a `mip-user` meta tag, and the page shows it only if it is a plain email address. When the file is opened directly there is no user, so nothing is shown. Nothing is stored or sent. Regression tests are unchanged (all 3 configurations pass).
- Docs drift check (19 Oct 2026): `business-rules.md` now says that a manuscript with no last-action date goes to Invite Reviewers with no grace period. No code changed.
- **Real data removed from the console (backlog B2):** the 3 embedded Power BI screenshots, which showed author names, are replaced with text instructions. The example manuscript ID in the lookup boxes is now `1234567`. File size dropped from 970 KB to 404 KB. Regression tests are unchanged (all 3 configurations pass).
- **Deploy repo created:** `wiley/mip-drafts-console-ea` (Partybus system `mipdraftsconsole`) holds the deployable copy, `public-html/index.html`, plus the Dockerfile (nginx-unprivileged, 8080), the nginx config with `/health`, and security headers including `connect-src 'none'`. This repo stays the development home. Release by copying `mip-drafts-console.html` across (see that repo's `AGENTS.md`).
- Tool landscape (15 Oct 2026):
  - `docs/tool-landscape.md` and `docs/prp-tools-matrix.html` compare all five PRP tools from their code: MIP, EDT, v2.2, PRPL Portfolio Insights and Aria 2 / PeerPulse. They cover capabilities, what's redundant, and a 3-layer release plan.
  - `docs/scope-questions.md` holds the 10 questions for Iris and a draft message.
  - `docs/portfolio-insights-merge-plan.md` sets out the v2.3 plan.
  - New product-scope decisions PS-1 to PS-6 in `docs/open-decisions.md`.
  - Backlog B13–B19.
  - The Portfolio Insights and Aria source files are deliberately not added: one is someone else's unconfirmed tool, and the other contains embedded staff and KPI data.
- Docs drift check (13 Oct 2026): `business-rules.md` now lists the "leave out V1 papers" setting (off by default) and gives the Step 12 data check column its full name. `data-model.md` flowchart now shows that the Health Check "On Track" setting also applies to triage rows, and notes the V1 and Reviews Pending settings. `README.md` now says the Editor Delay Tracker was merged in v2.0, not v2.1. No code changed.
- Added the meeting → approval → change loop:
  - `docs/meetings/` holds one record per meeting. The template and the 29 Sep 2026 AI COE session are back-filled.
  - New backlog statuses: Awaiting approval, Ready (approved), Done (awaiting commit).
  - The `mip-meeting-intake` Cowork skill is listed in `CLAUDE.md`.
- Added `CLAUDE.md` (rules for agents), `docs/backlog.md`, and `agent-setup/` (the builder, qa-reviewer and docs-keeper agents, plus permissions; to be moved into `.claude/`).
- Documentation set added under `docs/`, all written from the code:
  - `business-rules.md`: every tab, with 12 ☐ Confirm items for Gayatri / PRP
  - `maintainer-guide.md`
  - `ea-quick-start.md` (draft, with ⚠ items for PRP)
  - `prpl-guide.md`
  - `troubleshooting.md`
  - `hosting-and-security.md`
- Regression test kit added under `tests/`:
  - synthetic fixtures (20 MIP scenarios, 5 reviewer rows, no real data)
  - `run.js`, which compares 3 settings configurations against `tests/baseline/`
  - `anonymise.py`, for masking real exports. On the 29 Sep export, the masked copy produced the same 42 drafts as the original.
- Added `docs/data-model.md`: data flow from Power BI to the outputs, report relationships (joined on Manuscript ID), which report feeds which tab, how a row becomes an email, and known data weak points. Written from the code.
- Added `docs/open-decisions.md`: the decisions still needed before rollout, with the evidence from testing and a column to record each decision. The tool itself is unchanged.
- Updated `docs/open-decisions.md` with outcomes from the *MIP Efficiencies Interface: AI COE Session* (29 Sep 2026):
  - GR-1 resolved: grouping default depends on portfolio type.
  - New items: per-journal grace period (TH-1), rollout through vendor management (Q5), sent tracking and Freshdesk (Q6).
  - New dependencies on Luke Barrett's team (D1–D3).

## v2.2 (1 Oct 2026): editable email templates
- All email wording moved out of the code into `templates/templates.json`, templates v1.0.0. That covers subjects, greetings, paragraphs, summary bullets, section headings and EA notes for all six templates: Handling Editor, Triage Editor, the two EA summaries, reviewer reminder, and section labels. The console carries a copy in an embedded `mipTemplates` block.
- New `admin/template-admin.html` for PRP template owners:
  - edit the wording with a live preview on fictional sample data
  - click-to-insert placeholders, with checks that each placeholder is valid and required lines aren't empty
  - track which fields changed
  - release with a version, approver and change note, which updates `templates.json` and the console file together
- The console footer shows the template version and approver.
- Regression check: all 42 drafts generated from the Adachi test export (37 Handling Editor, 1 Triage, 2 EA summaries and 2 reviewer reminders) have the same text as v2.1. The only change is that the video-guide link now opens in a new tab.
- Template values are escaped before they go into emails. A title or name can't inject markup, and the release can't break the console file's script block.

## v2.1 (29 Sep 2026): fixes from testing
- Chief Editor workbook: the delayed proportion is now stored as a real percentage (0.0%), and every sheet has a header filter.
- Chief Editor inclusion reason now names only the criteria the selected mode uses. Before this fix, count-only mode could say "count and proportion". The bug came from the Editor Delay Tracker.
- "Copy plain text" button on every Handling Editor and Triage Editor draft.
- Step 05b manuscript view shows the Required task and Task performer columns.
- Step 12 help text now lists the "Task Performer Differs from Handling Editor?" column, and the colour key includes "Health Check On Track".

## v2.0 (29 Sep 2026): Editor Delay Tracker merged in
- New **Step 05b: Delayed editors & Chief Editor escalation**:
  - delayed proportion for each editor and journal
  - a Needs action / No action needed / All manuscripts view
  - a Chief Editor workbook, with editors included by count, proportion or either
- Handling Editor emails greet by surname and include the Reviewer Invitation Queue video tip under "Invite Reviewers".
- New Step 03 settings:
  - papers where every accepted reviewer is overdue go to "Invite Reviewers" (on by default)
  - optional Health Check "On Track" exclusion (off by default)
- Default grouping is now one email per editor, per journal.
- CSV uploads are accepted, and Power BI "Applied filters" footer rows are skipped.
- The draft status export adds a "Task Performer Differs from Handling Editor?" column and a "Skipped - Health Check On Track" category.

## v1 (before Sep 2026)
- MIP Drafts Console "Final" (Gayatri). See `archive/mip-drafts-console-original.html`.
- Editor Delay Tracker Portable V36 (Daniel). See `archive/editor-delay-tracker-v36.html`.
