# Backlog

**Status key:**

- **Ready** = agreed, and an agent can start.
- **Awaiting approval** = raised in a meeting, with an approval request sent. See `docs/meetings/`.
- **Ready (approved)** = approved by the named business owner.
- **Blocked** = waiting on a decision or another team.
- **Done (awaiting commit)** = implemented, waiting for Nelson to commit.
- **Rejected**.

Move items to GitHub Issues when the repo moves to the `wiley` org. Give each issue a `ready` or `blocked` label, plus `approved` once a decision is recorded.

| # | Item | Status | Agent | Waiting on | Notes |
|---|---|---|---|---|---|
| B1 | **Bundle SheetJS into the console** so no CDN is needed | Ready | builder | — | Readiness #7 / hosting S6. Licence Apache-2.0. CSV and Excel then work offline. |
| B2 | **Replace the 3 embedded Power BI screenshots** with synthetic images, or with text instructions | Done (awaiting commit) | builder | — | 15 Oct 2026: replaced with text instructions. The console dropped from 970 KB to 404 KB. The example manuscript ID in the lookup boxes is now `1234567`. |
| B3 | **Hosted mode:** when served over http(s), load `templates.json` from the site, falling back to the embedded copy | Ready | builder | — | Needed before hosting. Then a wording release is a single-file commit. |
| B4 | **Partybus prep:** Dockerfile (unprivileged nginx), nginx config, `/health` route | Done (awaiting commit) | builder | Local Docker smoke test; then the v4 wizard | 15 Oct 2026: done in the deploy repo `wiley/mip-drafts-console-ea` (system `mipdraftsconsole`). Next: `docker build` smoke test, then run `partybus-new-app-v4` against that repo. |
| B5 | **Daniel's short reminder template** as a second template, with a "Reminder style" choice in Step 03 | Blocked | builder | Decision EM-1 / EM-7 | Template text is in the archive (EDT V36) |
| B6 | **Per-journal grace period** table with PRP-set defaults | Blocked | builder | Decision TH-1 | — |
| B7 | **Save EA and Author stage thresholds** between sessions, with PRP defaults | Blocked | builder | Business rules #9 (benchmark values) | Needs a storage decision. The console currently stores nothing. |
| B8 | **"Mark as sent" button** that adds a "Sent on" column to the Step 12 export | Blocked | builder | Wish list 1 scope | A step towards tracking. Works for Freshdesk too. |
| B9 | **Answers to the 12 ☐ Confirm items** in `business-rules.md` | Blocked | docs-keeper | Gayatri / PRP | Record the answers, then add backlog items for any code changes |
| B10 | **Periodic drift check:** documentation against code | Ready | docs-keeper | — | Run after every merge |
| B11 | **Fill the ⚠ items in `ea-quick-start.md`** | Blocked | docs-keeper | PRP | — |
| B12 | **Extend test fixtures:** Tab 3/4 overdues, Step 10/11 lists, Tab 5 KPIs, RSS | Ready | qa-reviewer → builder | — | `tests/run.js` doesn't yet snapshot these tabs |
| B13 | **Portfolio Insights comparison:** a rule map against v2.2, and a side-by-side run on a masked export | Ready | builder → docs-keeper | — | Step 1 of `docs/portfolio-insights-merge-plan.md`. Keep the Portfolio Insights source out of the repo until PS-1 is decided. |
| B14 | **Fold Portfolio Insights into the console as Tab 6** (v2.3) | Blocked | builder | PS-1 to PS-5 | Step 2 of the merge plan |
| B15 | **Tests for Tab 6:** synthetic Journal Performance, Full Manuscript Listing and "last week" fixtures; a parity test plan | Blocked | qa-reviewer → builder | B14 | Step 3 of the merge plan |
| B16 | **Docs for v2.3:** business rules (Tab 6), data model, PRPL guide, tool landscape, matrix page | Blocked | docs-keeper | B14 | Step 4 of the merge plan |
| B17 | **Single stage-definition list** used by every view | Blocked | builder | PS-4 | Three different lists exist today |
| B18 | **Retire the old tools:** MIP original, EDT V36, the Excel macro. Communicate this through vendor management. | Blocked | — (Nelson / PRP) | v2.2 released | `docs/tool-landscape.md`, "What's redundant" |
| B19 | **Send the scope questions to Iris** and record the answers | Ready | — (Nelson), then docs-keeper | — | `docs/scope-questions.md`. The answers unblock B14 and B17. |
| B20 | **Power BI live data, prerequisites:** dataset IDs, row-level security, access, the DAX query, the Entra app registration, the tenant setting | Blocked | — (Nelson) | Luke Barrett's team, IT, decision LD-1 | `docs/power-bi-live-data-plan.md`, P1–P7. Draft messages are in the plan. |
| B21 | **Load from Power BI** button: MSAL sign-in, then Execute Queries, then map to export columns. Upload stays. | Blocked | builder | B20, LD-1, LD-2 | Changes CLAUDE.md hard rule 6 and the security policy. Tests use a synthetic API response. |
