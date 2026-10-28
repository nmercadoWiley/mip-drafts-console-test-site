# Plan: fold PRPL Portfolio Insights into the console (v2.3)

**Status:** plan, not started · **Last updated:** 15 Oct 2026 · **Blocked on:** decisions PS-1 to PS-5 (`docs/open-decisions.md`)

PRPL Portfolio Insights reads the same MIP report as the console. It adds a PRPL oversight view: portfolio summary, journal pages, most-overdue list, editor workload, trends between uploads, KPI benchmarking, and bottleneck recommendations. It's about 3,500 lines of logic, roughly **2–3 times the size of the Editor Delay Tracker merge**.

## Step 0: decisions (Iris, plus the tool's author)

| ID | Decision | Why it blocks the build |
|---|---|---|
| PS-1 | Portfolio Insights is in scope, and its author agrees to the merge | It's someone else's work. The author isn't stated in the file. |
| PS-2 | Which measure of "overdue" is the standard: Health Check, or "needs action"? | Portfolio Insights is built on Health Check, and v2.2 isn't |
| PS-3 | Its AI features: drop them, or route them through an approved Wiley AI service? | They send manuscript IDs and editor names to the Anthropic API, and only work inside Claude.ai. The console's rule is no network calls. |
| PS-4 | One stage-definition list | The tools define E1, E4A and other stages differently |
| PS-5 | Which editor-performance view to keep | v2.2's Tab 5, or Portfolio Insights' version with benchmarks and targets |

## Step 1: compare (no approval needed; backlog B13)

- **Rule map:** every calculation in Portfolio Insights against v2.2, marked same, conflicting, Portfolio Insights only, or v2.2 only.
- **Side-by-side run:** both tools on the same export (masked with `tests/anonymise.py`). What each says is overdue, per journal and per editor, and why they differ.

## Step 2: build Tab 6, Portfolio Oversight (backlog B14)

| Portfolio Insights feature | Plan |
|---|---|
| Upload and parsing | **Reuse Tab 1's upload**, so there's no second upload. Add Article Type, Article Display Type, Days Since Original Submission, Date of entering Stage and Last Handling Editor Full Name to `COLUMN_ALIASES`. |
| Portfolio Summary, journal pages, Most Overdue, editor workload, exclude-S2 toggle | Port them into Tab 6. Show **both** Health Check and "needs action" until PS-2 is decided. |
| Bottleneck recommendations | Move the wording into `templates/templates.json`, so it's approved and editable in the admin page |
| Trends | Replace the Claude.ai artifact storage with **"upload last week's export too"**. The console stores nothing. |
| KPI benchmarking (Journal Performance export, Full Manuscript Listing, predicted targets, editor performance file) | Port it. Share the Full Manuscript Listing upload with Tab 5, then merge the two editor-performance views (PS-5). |
| AI digests and journal overviews | **Remove the API calls.** Keep the data-driven summaries it already uses as its fallback. Any AI comes later, through an approved service only. |
| AI editor email drafter | **Drop it.** Point users to the Step 06 drafts. |
| The 3-CDN library loader | Replace it with the bundled library (backlog B1) |
| Embedded screenshots | Check them. Replace them with synthetic images or text. |
| Sidebar layout and styling | Restyle into the console's tabs and cards |

## Step 3: test (backlog B15)

- Add synthetic fixtures: a Journal Performance export, a Full Manuscript Listing, and a "last week" MIP export. Snapshot the Tab 6 outputs in `tests/run.js`.
- Run a parity test plan like Runs 1–3. Each Portfolio Insights feature is marked same, replaced or dropped, and checked against the original on the same data.
- Get a browser check from the tool's author and one PRPL.

## Step 4: document and release (backlog B16)

- Update `business-rules.md` (Tab 6), `data-model.md` (new inputs), `prpl-guide.md`, `tool-landscape.md` and the matrix page.
- Release **v2.3**, which replaces the separate Portfolio Insights file.

## Notes

- The console grows to about 1.3 MB and roughly 10,500 lines. Consider splitting it into modules at hosting time, using the test kit as a safety net.
- **Lighter alternative:** host Portfolio Insights as a separate page on the same site and SSO, with a link to the console. It's less work, but it means two uploads, two "overdue" answers, the AI calls kept, and duplicated features. Use it only as a stopgap.
