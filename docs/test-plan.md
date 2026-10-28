# Editor Reminder Tools: Test Plan

**Purpose:** confirm that MIP Drafts Console v2 does everything the two original tools do, and that it gives the expected results on the same test data.

| Tool | Owner | File |
|---|---|---|
| Editor Delay Tracker (EDT) | Daniel | `Editor_Delay_Tracker_Portable_V36.html` |
| MIP Drafts Console (original) | Gayatri | `MIP_Drafts_Console_Final 1 (1).html` |
| MIP Drafts Console v2 (merged) | — | `MIP_Drafts_Console_v2.html` |

**Test data:** `data.xlsx`. This is the MIP Summary Report for PRP Lead Ayaka Adachi: 279 manuscripts (JDE 200, HEPR 79) plus a Power BI "Applied filters" footer row.
**Also used in one negative test only:** `data (1).xlsx`, an Activity Tracker export for HEPR.

---

## Instructions for the AI compiling results

You will receive a tester's observations for each test ID below. For each test:

1. Compare the observation with **Expected**.
2. Give it one status:
   - **PASS**: matches exactly.
   - **PASS (date drift)**: differs only in counts that depend on today's date. This applies only where a test says "date-dependent".
   - **PARTIAL**: the feature exists but behaves or looks different from expected.
   - **FAIL**: missing, wrong, or produces an error.
   - **NOT RUN**
3. Quote the tester's actual values. Don't round or paraphrase numbers.
4. If the tester reports something that no test covers, add it under "Unplanned observations".

Produce the output in exactly this structure:

```
## Summary
- Tests run: X of Y | PASS: n | PASS (date drift): n | PARTIAL: n | FAIL: n | NOT RUN: n
- Blocking issues (FAIL on anything in Run 2/3A regression or Run 1 core logic): bullet list or "None"
- EDT features missing or degraded in v2: bullet list, from the Parity checks, or "None"

## Results
| Test ID | Status | Expected (short) | Actual (as reported) | Notes |
|---|---|---|---|---|
| ... one row per test ID, in order ... |

## Parity matrix (EDT → v2)
| EDT feature | EDT result | v2 result | Parity status (Same / Intentional difference / Gap) |

## Unplanned observations
- ...

## Environment
Test date, browser, OS, and whether files were opened directly or inside Claude web
```

---

## General setup (tester)

- Open each HTML file **directly in Chrome or Edge** by double-clicking it, not as a preview inside Claude. A browser agent (Claude in Chrome / Claude web) can drive that tab, but **you do every file upload and every check outside the browser** (Outlook, Notepad, Excel). The prompts below set this up.
- Do **all runs on the same day**. The MIP console counts days from today, so its counts are date-dependent. EDT's counts come from the file and don't change with the date.
- Don't change settings unless a step says so.
- Record the test date and browser.

---

# Running the tests with a browser agent

The browser agent can click, read the page and reload it. It **can't** pick files from your PC, open Excel, or see Outlook and Notepad. So each run is split between the two of you:

| Who | Does what |
|---|---|
| **You (tester)** | Open the HTML file in Chrome or Edge. Do every file upload when the agent pauses and asks. Dismiss browser alert boxes and read their text out. Paste into Outlook or Notepad and describe the result. Open downloaded .xlsx and .eml files and describe them. |
| **Agent** | Everything else: clicks, reading values, reloads, filters, tooltips, window resizing. It records the results and writes the report. |

**Known snags, and how to handle them:**

- **Alert boxes.** EDT uses browser alerts ("Rich email copied…", "Generate a draft first.", "Select a journal with eligible editors."). The agent may freeze on one. Click **OK** yourself and tell the agent the exact message, because that message is the result it needs to record.
- **Copy buttons.** Copying to the clipboard can fail when the agent does the clicking, because the page isn't the active window. If a paste comes up empty, click the button yourself and paste again. Tell the agent which of you made it work.
- **Reloads.** EDT keeps uploaded data after a reload. **Both MIP versions don't**, so after every reload you have to upload data.xlsx again.
- **Same day.** Do all three runs on the same day. The MIP counts depend on today's date.

Give the agent **this whole document** plus the prompt for the run. Each prompt below is self-contained. Use one per run, in a fresh conversation if you like.

---

## Prompt: Run 1 (Editor Delay Tracker, Daniel)

```
You are testing a local HTML tool in the browser tab I have open: Editor_Delay_Tracker_Portable_V36.html
(Editor Delay Tracker, "EDT"). The attached document "Editor Reminder Tools: Test Plan" is the source of
truth. Run every Run 1 test (EDT-01 to EDT-43) and compare each result with its Expected column.

How we split the work:
- I do ALL file uploads. When a test needs a file, STOP, tell me exactly which file and which control
  ("Upload raw MIP" file input), and wait until I reply "done". Don't try to upload files yourself.
- I handle anything outside the browser: pasting into Outlook or Notepad, the default mail app, and
  opening downloaded .xlsx files. At those steps, click the button, then STOP and ask me to describe
  what I see.
- If a browser alert or confirm box appears, or the page seems frozen, STOP and ask me to click OK and
  read you the message. Record the message text as the result.
- If a copy button seems to do nothing, ask me to click it myself and paste. Note who made it work.

Run in exactly this order (it avoids extra uploads):
1. EDT-01 (initial load), then EDT-02 (Clear local data → zero state).
2. PAUSE: I upload data.xlsx. Then EDT-03 and EDT-04.
3. EDT-05: reload the page (F5); the data should still be there.
4. Sections B to F in order, EDT-10 to EDT-41.
   - EDT-28, EDT-29, EDT-30: click, then PAUSE for my description.
   - EDT-39 / EDT-40: click Generate, then PAUSE. I'll open the workbook and describe the sheets,
     % formatting, autofilter and column widths.
   - Run EDT-32 straight after EDT-41: reload the page, then click "Copy rich email" before drafting.
5. EDT-42 (every "i" tooltip, 7 in total) and EDT-43 (narrow the window to about 400 px).
6. Negative tests, each with a PAUSE for my upload:
   - EDT-08: I upload data (1).xlsx (an Activity Tracker export, the wrong file). Record the numbers exactly.
   - EDT-09: I try to upload a .txt file.
   - EDT-07 (optional): I upload a CSV copy of data.xlsx.
7. EDT-06 last of all: Clear local data, reload, confirm the zero state.

Recording rules:
- Put exact numbers and text in the Actual column. Don't round or paraphrase.
- Mark anything I report as "tester-observed". Mark what you saw yourself as "agent-observed".
- Status per test: PASS / PARTIAL / FAIL / NOT RUN. Mark NOT RUN only if neither of us could do it,
  and say why.
- For EDT-15, copy the full Delayed editors table as it appears. Row order matters (a different order
  with the same rows = PARTIAL).
- For EDT-26, copy the full plain-text draft.

When you finish, output ONLY this:

## Run 1 summary
- Tests: X of 43 run | PASS n | PARTIAL n | FAIL n | NOT RUN n
- Core-logic failures (any non-PASS in EDT-03, 04, 15, 18, 20, 21, 26, 34-36, 40): list or "None"

## Run 1 results
| Test ID | Status | Expected (short) | Actual | Observed by | Notes |
(one row per test, EDT-01 to EDT-43, in order)

## EDT feature inventory
List every button, control, section, column and message you saw in the tool, including anything the
test plan doesn't mention. Mark each as "covered by EDT-xx" or "NOT IN TEST PLAN".

## Unplanned observations
## Environment (date, browser, OS)
```

---

## Prompt: Run 2 (MIP Drafts Console, original, Gayatri)

```
You are testing a local HTML tool in the browser tab I have open: MIP_Drafts_Console_Final 1 (1).html
(the original MIP Drafts Console). The attached document "Editor Reminder Tools: Test Plan" is the source
of truth. Run every Run 2 test (MIP-01 to MIP-06) and compare each result with its Expected column.
These results are the BASELINE that v2 must match later, so record them precisely.

How we split the work:
- I do ALL file uploads. When a test needs a file, STOP, tell me exactly which file and which drop zone,
  and wait until I reply "done". Don't try to upload files yourself.
- This tool does NOT keep data after a reload. If you reload for any reason, STOP and ask me to upload
  data.xlsx again.
- I open anything outside the browser (.xlsx downloads). At those steps, click the button, then STOP and
  ask me to describe the file.
- If an alert box appears or the page seems frozen, STOP and ask me to click OK and read you the message.

Setup rules:
- Stay on the "Editor, Triage & EA Drafts" tab.
- Leave EVERY setting in Step 03 at its default. Grouping must be "One combined email per editor".
  Don't tick any checkbox.
- Do NOT upload an Activity Tracker. Leave that drop zone empty.

Run in this order:
1. PAUSE: I upload data.xlsx into Step 01 "MIP Summary Report" (the first, required drop zone).
   Then MIP-01: read the file pill and check that there is no missing-column warning.
2. Click "Generate all drafts". MIP-02: record EVERY tile in "04 Analysis summary", with its label
   and value exactly as shown.
3. MIP-03: expand "05 Stalled queues", leave the threshold at 30, and record the editor count and the
   top 3 rows with every column value.
4. MIP-04: in Step 01 "Double-check a manuscript's data", look up 3771449 and record what it shows.
   Then expand "06 Handling Editor drafts", find the draft that contains 3771449, and record the
   section heading it appears under.
5. MIP-05: open any Handling Editor draft. Record the To line, the Subject, the greeting line, the
   section headings, and whether a "Reviewer Invitation Queue" paragraph appears. Also record the
   total number of drafts shown in 06 and 07.
6. MIP-06: click "Download draft status export (.xlsx)", then PAUSE. I'll open it and describe the
   added columns and row colours.

Recording rules:
- Put exact numbers and text in the Actual column. Don't round or paraphrase.
- Mark anything I report as "tester-observed". Mark what you saw yourself as "agent-observed".
- Status per test: PASS / PASS (date drift) / PARTIAL / FAIL / NOT RUN. "Date drift" applies only to
  the grace-period and flagged-invite counts. The test plan marks these as date-dependent.

When you finish, output ONLY this:

## Run 2 summary
- Tests: X of 6 run | PASS n | PASS (date drift) n | PARTIAL n | FAIL n | NOT RUN n

## Run 2 results
| Test ID | Status | Expected (short) | Actual | Observed by | Notes |

## Baseline values for Run 3 comparison
- 04 tiles (label: value, one per line, every tile):
- 05 Stalled queues: editor count + top 3 rows:
- 06 draft count / 07 draft count:
- 3771449 section:
- Example Subject line / greeting:

## Unplanned observations
## Environment (date, browser, OS)
```

---

## Prompt: Run 3 (MIP Drafts Console v2, merged)

```
You are testing a local HTML tool in the browser tab I have open: MIP_Drafts_Console_v2.html
(MIP Drafts Console v2, which merges the Editor Delay Tracker into the MIP Drafts Console). The attached
document "Editor Reminder Tools: Test Plan" is the source of truth. Run every Run 3 test (V2-01 to V2-22)
and compare each result with its Expected column. If I give you the Run 2 baseline values, use them for
V2-02 to V2-04. Any difference there is a BLOCKING FAIL.

How we split the work:
- I do ALL file uploads. When a test needs a file, STOP, tell me exactly which file and which drop zone,
  and wait until I reply "done". Don't try to upload files yourself.
- This tool does NOT keep data after a reload. Every time you reload (3A → 3B → 3C), STOP and ask me
  to upload data.xlsx again into Step 01 "MIP Summary Report".
- I handle anything outside the browser: Outlook paste, opening .eml files, and opening .xlsx downloads.
  At those steps, click the button, then STOP and ask me to describe what I see.
- If an alert box appears or the page seems frozen, STOP and ask me to click OK and read you the message.
- If a copy button seems to do nothing, ask me to click it myself and paste. Note who made it work.
- Do NOT upload an Activity Tracker in any part of this run.

Part 3A: Regression (v2 set to behave like the original)
1. V2-01: check the page title shows "v2", there is a "What's new in v2" note, and the left overview
   lists "05b".
2. PAUSE: I upload data.xlsx.
3. In Step 03: UNTICK "If every accepted reviewer… is overdue…", leave "Don't draft manuscripts whose
   Health Check is 'On Track'" UNTICKED, and set the grouping to "One combined email per editor".
   Click "Generate all drafts".
4. V2-02: record EVERY tile in 04 Analysis summary. V2-03: 05 Stalled queues (threshold 30), editor
   count + top 3 rows. V2-04: the 06 section heading for 3771449.

Part 3B: v2 defaults
5. Reload the page. PAUSE: I upload data.xlsx again. Change NOTHING in Step 03. Click Generate.
6. Run V2-05 to V2-19 in order.
   - V2-14: click the Chief Editor download, then PAUSE. I'll describe the sheets, whether the
     proportion is a % number or text, and whether there's an autofilter.
   - V2-16: click Copy HTML and Download .eml, then PAUSE for my Outlook and .eml description.
   - V2-17: click the draft status download, then PAUSE for my description.
   - V2-18 (optional) and V2-19: PAUSE for my uploads (a CSV copy of data.xlsx, then data (1).xlsx).
     After V2-19, ask me to upload data.xlsx again before continuing.

Part 3C: Health Check rule
7. Reload the page. PAUSE: I upload data.xlsx again. In Step 03, TICK "Don't draft manuscripts whose
   Health Check is 'On Track'" and leave everything else at its default. Click Generate.
8. Run V2-20 and V2-21. V2-22: click the draft status download, then PAUSE for my description.

Recording rules:
- Put exact numbers and text in the Actual column. Don't round or paraphrase.
- Mark anything I report as "tester-observed". Mark what you saw yourself as "agent-observed".
- Status per test: PASS / PASS (date drift) / PARTIAL / FAIL / NOT RUN. "Date drift" applies only to
  counts marked "≈" or date-dependent in the test plan.
- For V2-08, copy the whole 05b table, not just the top 5.

Then complete the Parity checks section (P1 to P20). Use the Run 1 results if I've given them to you;
otherwise, fill in the v2 side only.

When you finish, output ONLY this:

## Run 3 summary
- Tests: X of 22 run | PASS n | PASS (date drift) n | PARTIAL n | FAIL n | NOT RUN n
- Blocking: does 3A match the Run 2 baseline exactly? Yes / No (list every difference)
- EDT features missing or degraded in v2: list

## Run 3 results
| Test ID | Status | Expected (short) | Actual | Observed by | Notes |

## 3A vs 3B vs 3C comparison
| Measure | 3A | 3B | 3C |
(every 04 tile, the 05b editor count, the 05b notes, the 3771449 section)

## Parity matrix (EDT → v2)
| # | EDT feature | EDT result | v2 result | Parity status (Same / v2 better / Intentional difference / Gap) |

## Unplanned observations
## Environment (date, browser, OS)
```

---

## Prompt: Final compilation (optional, after all three runs)

```
Attached are the test plan "Editor Reminder Tools: Test Plan" and the outputs from Run 1 (EDT), Run 2
(MIP original) and Run 3 (MIP v2). Compile them into one report, using the structure in the test plan's
section "Instructions for the AI compiling results": Summary, Results, Parity matrix, Unplanned
observations, Environment. Don't re-judge a test unless the run outputs contradict each other; if they
do, flag the contradiction. Finish with a short list of "Fixes needed in v2", ordered by severity:
blocking regressions, then EDT features missing from v2, then cosmetic issues.
```

---

# Run 1: Editor Delay Tracker (Daniel). Full feature test

EDT counts only rows where **Task Performer** is `Handling Editor`, `Reviewer/Handling Editor` or `Triage Editor`. A paper is **delayed** when all three of these are true:

- no reviewer was invited in the last 10 days (from `Days Since Last Reviewer Invited`, since this file doesn't have the Yes/No column)
- the non-delayed reviewer count is 0 (Accepted − Submitted − Overdue)
- Health Check is not "On Track"

Editors are identified by **Task Performer Name**, per journal.

### A. Loading and data handling

| ID | Steps | Expected |
|---|---|---|
| EDT-01 | Open the file. | The page loads with the title "Editor Delay Tracker Portable V36", the note about V36, and 6 cards: Upload raw MIP, Filters, Summary metrics, Delayed editors, Chief Editor Sharing Centre, Reminder email draft. The Editor Paper Navigator is hidden. No error banner. |
| EDT-02 | Click **Clear local data**. | Metrics show 0 / 0 / 0 / 0. The Delayed editors table says "No delayed editors." |
| EDT-03 | Upload `data.xlsx`. | The diagnostic box says **"Import successful"**, **Rows included: 78**, **Rows ignored: 201**. No red error banner. (The "Applied filters" footer and blank rows are skipped without being counted.) |
| EDT-04 | Look at the **Summary metrics** card, with no filters. | Included rows **78**, Ignored rows **201**, Editors **37**, Delayed papers **9**. |
| EDT-05 | **Reload** the browser page (F5) without uploading again. | The data is still loaded from browser storage and the metrics are unchanged (78 / 201 / 37 / 9). |
| EDT-06 | Click **Clear local data**, then reload. | Everything is back to 0. Then upload `data.xlsx` again before continuing. |
| EDT-07 | *(Optional)* In Excel, save `data.xlsx` as CSV and upload the CSV. | Same results as EDT-03 and EDT-04 (78 / 201 / 37 / 9). Re-upload `data.xlsx` afterwards. |
| EDT-08 | **Negative test.** Upload `data (1).xlsx` (the Activity Tracker). | It imports without an error: **Rows included: 2**, **Rows ignored: 77**, **Delayed papers: 0**. **This is a known risk:** EDT accepts a file that is missing the reviewer columns and gives no warning. Record exactly what's shown, then re-upload `data.xlsx`. |
| EDT-09 | **Negative test.** Upload a non-spreadsheet file (e.g. a .txt or .html). | The file picker may not allow it. If it does, a red banner says "Unsupported file type". |

### B. Filters

| ID | Steps | Expected |
|---|---|---|
| EDT-10 | Look at the journal buttons under **Filters**. | Two buttons, **HEPR** and **JDE**, in alphabetical order. |
| EDT-11 | Click **HEPR** only. | Editors **2**, Delayed papers **0**. The table says "No delayed editors." |
| EDT-12 | Click **JDE** as well, so both are selected. | Editors **37**, Delayed papers **9**. Both journal buttons are highlighted. |
| EDT-13 | Clear both journals, then type `Kadono` in **Search editor**. | Editors **1**, Delayed papers **3**. The table shows only Takafumi Kadono. |
| EDT-14 | Click **Clear search**. | Back to 37 / 9. |

### C. Delayed editors table

| ID | Steps | Expected |
|---|---|---|
| EDT-15 | Read every row of **Delayed editors**, with no filters. | **7 rows**, all JDE, in this order: |

| Editor | Journal | Delayed | Current task-performer papers | Delayed proportion |
|---|---|---|---|---|
| Takafumi Kadono | JDE | 3 | 3 | 100% |
| Kenshi Yamasaki | JDE | 1 | 4 | 25% |
| Tomomitsu Miyagaki | JDE | 1 | 3 | 33.3% |
| Toshiyuki Yamamoto | JDE | 1 | 3 | 33.3% |
| Shinichi Moriwaki | JDE | 1 | 2 | 50% |
| Yumi Aoyama | JDE | 1 | 4 | 25% |
| Shin Morizane | JDE | 1 | 1 | 100% |

The row order among the editors with 1 delayed paper follows the file order. If the rows are the same but the order differs, mark it PARTIAL, not FAIL.

| ID | Steps | Expected |
|---|---|---|
| EDT-16 | Check the proportion formatting. | Whole numbers show without decimals ("25%", "100%"). Fractions show one decimal ("33.3%"). |

### D. Editor Paper Navigator

| ID | Steps | Expected |
|---|---|---|
| EDT-17 | Click **Open papers** on Takafumi Kadono. | The navigator opens with the title **"Takafumi Kadono \| JDE"** and the summary **"3 delayed, 0 not delayed, 3 current task-performer papers"**. **Delayed only** is active. |
| EDT-18 | Read the Delayed only rows. | 3 rows, all with a red "Delayed" pill: **4959091** (Invite Reviewers, Longstanding), **5966577** (Triage Editor to Invite Handling Editors, Overdue), **8586549** (Invite Reviewers, Longstanding). Columns: Status, Manuscript ID, Title, Journal, Required Task, Health Check, Task Performer, Reviewer invited ≤10 days?, Non-delayed reviewers, Link. "Reviewer invited ≤10 days?" = No and Non-delayed reviewers = 0 on all 3. |
| EDT-19 | Click **Not delayed**. | 0 rows. |
| EDT-20 | Click **Close**, then **Open papers** on **Kenshi Yamasaki**. | Summary: **"1 delayed, 3 not delayed, 4 current task-performer papers"**. Delayed only: **3771449** (Health Check Longstanding, Non-delayed reviewers 0). |
| EDT-21 | Click **Not delayed**. | 3 rows with green pills: **1811749** (Overdue, Non-delayed reviewers 2), **5914563** (On Track), **9218171** (On Track). |
| EDT-22 | Click **All task-performer papers**. | All 4 rows, with red rows for delayed papers and green rows for the rest. |
| EDT-23 | Click **Link → Open** on any row. | The ReX page (review.wiley.com/details/…) opens in a new tab. |
| EDT-24 | Click **Close**. | The navigator hides. |

### E. Reminder email

| ID | Steps | Expected |
|---|---|---|
| EDT-25 | Open papers for Kadono → **Draft reminder email**. | The page scrolls to the draft. Meta line: **"Draft for Takafumi Kadono \| JDE \| 3 delayed paper(s)"**. |
| EDT-26 | Read the plain-text draft. | Subject: **"Papers Pending Your Action - JDE"**. Body: "Dear Dr Kadono," / "I hope you are well." / "For your convenience, below is a list of the papers that are pending your action as editor." Then a tab-separated table (Manuscript ID, Link to Paper, Manuscript Title) with 3 rows, then the **Reviewer Invitation Queue** paragraph, then "Thank you,". There's no sender name. |
| EDT-27 | Read the rich preview. | Same content, with a 3-column table that has a blue header row. "video guide" is a link. |
| EDT-28 | Click **Copy rich email** and paste into a new Outlook message. | The confirmation says "Rich email copied…". Outlook keeps the blue-header table and the link. The subject line appears as the first line of the body, not in the Subject field. |
| EDT-29 | Click **Copy plain text** and paste into Notepad. | The plain text from EDT-26, including "Subject: …" as the first line. |
| EDT-30 | Click **Open in mail client**. | A new mail window opens with the subject filled in, a plain-text body and **no To: address**. (If nothing opens, record that. It depends on the PC's default mail app.) |
| EDT-31 | Open papers for **Toshiyuki Yamamoto** → Draft reminder email. | "Dear Dr Yamamoto," with 1 row (**5671278**). **No** Reviewer Invitation Queue paragraph, because his task is "Make Recommendation / Decision". |
| EDT-32 | Reload the page (the data stays loaded), then click **Copy rich email** before drafting anything. | A message: "Generate a draft first." |

### F. Chief Editor Sharing Centre

| ID | Steps | Expected |
|---|---|---|
| EDT-33 | Open the journal dropdown. | Options: Select journal, HEPR, JDE. |
| EDT-34 | Journal **JDE**, mode **Delayed-paper count**, min **1** → **Preview editors**. | **7 editors**, each like "Takafumi Kadono — 3 of 3 current task-performer papers delayed (100%) — count". |
| EDT-35 | Change the mode to **Delayed proportion**. | The count box hides and the proportion box (default 50) shows. The preview updates on its own to **3 editors**: Kadono (100%), Moriwaki (50%), Morizane (100%). |
| EDT-36 | Mode **Either threshold** (min count 1, min 50%). | Both boxes show. **7 editors**. The reason is "count and proportion" for Kadono, Moriwaki and Morizane, and "count" for the other 4. |
| EDT-37 | Min count **2**, mode **Delayed-paper count**. | **1 editor** (Kadono). |
| EDT-38 | Journal **HEPR** → Preview. | "No editors meet the selected criteria." |
| EDT-39 | JDE, Either, count 1, 50% → **Generate Chief Editor workbook**. | Downloads **"JDE - Chief Editor Delayed Papers.xlsx"**. |
| EDT-40 | Open the workbook. | **8 sheets**: *Overview*, plus one per editor named after them (7). Overview columns: Editor, Delayed papers, Current task-performer papers, Delayed proportion, Inclusion reason. **Delayed proportion is formatted as a percentage** (e.g. 100.0%), there's an **autofilter** on the header row, and the columns are sized. Each editor sheet has Manuscript ID, Title, Required Task, Health Check, Link, with their delayed papers only (Kadono: 3 rows). |
| EDT-41 | Select no journal → Generate. | A message: "Select a journal with eligible editors." |

### G. Help and interface

| ID | Steps | Expected |
|---|---|---|
| EDT-42 | Hover or click each **i** icon (7 in total: Upload, Filters, Summary metrics, Delayed editors, Navigator, Chief Editor Sharing Centre, Reminder email). | Each shows a tooltip. The Navigator tip states the 3-part delay rule. Clicking elsewhere closes open tips. |
| EDT-43 | Narrow the window to phone width (about 400 px). | The layout still works and the tooltips reposition. Note any clipping. |

---

# Run 2: MIP Drafts Console, original (Gayatri). Baseline

Settings: all defaults. Grouping is "One combined email per editor". Results are **date-dependent**.

| ID | Steps | Expected |
|---|---|---|
| MIP-01 | Tab "Editor, Triage & EA Drafts" → Step 01 → upload `data.xlsx` as the Summary Report. Leave the Activity Tracker empty. | The file pill shows **279 manuscript rows**. No missing-column warning. |
| MIP-02 | Step 03 → **Generate all drafts**. Record every tile in **04 Analysis summary**. | Author-stage **187**, EA-side **14**, V1 excluded **0**, In grace period **≈4** (date-dependent), Flagged invite stale **≈25** (date-dependent), Editor drafts **36**, Triage drafts **1**, Accounted for **279 / 279**, Data check **0**. |
| MIP-03 | **05 Stalled queues**, threshold 30. | Record the editor count and the top 3 rows. (No fixed expectation. This is a baseline for MIP-R03.) |
| MIP-04 | Look up **3771449** (Step 01 lookup), then find it in the **06** drafts. | It appears under **"Reviews Pending – EA follow-up only"**. |
| MIP-05 | Open any Handling Editor draft in 06. | The greeting is "Dear Dr. {full name}". There's **no** Reviewer Invitation Queue paragraph. Record the subject line. |
| MIP-06 | Download **12 Draft status export**. | It opens in Excel with 8 added columns and colored rows. |

---

# Run 3: MIP Drafts Console v2 (merged)

Load `data.xlsx` as in MIP-01. Then generate three times, changing only the Step 03 settings listed.

### 3A. Regression (v2 set to behave like the original)

Settings: **untick** "every accepted reviewer… overdue", leave "Health Check On Track" **unticked**, set grouping to **"One combined email per editor"**.

| ID | Steps | Expected |
|---|---|---|
| V2-01 | The page loads. | The title shows "v2". There's a "What's new in v2" note, and a **05b** item in the left overview. |
| V2-02 | Upload + Generate. Record the 04 tiles. | **Identical to MIP-02**, including 279 / 279. Any difference is a **FAIL (blocking)**. |
| V2-03 | Compare 05 Stalled queues with MIP-03. | Identical. |
| V2-04 | 3771449 section. | "Reviews Pending – EA follow-up only" (same as MIP-04). |

### 3B. v2 defaults

Reload the page, upload `data.xlsx`, and generate **without changing anything**. Defaults: overdue re-route **on**, Health Check filter **off**, grouping **per journal**.

| ID | Steps | Expected |
|---|---|---|
| V2-05 | 04 tiles. | Same as MIP-02, except **Flagged invite stale is 1 higher (≈26)**. Still 279 / 279. |
| V2-06 | 3771449 section. | **"Handling Editor to Invite Reviewers"**, with the EA observation "Escalate: all accepted reviewers overdue". |
| V2-07 | **05b** card: badge and note. | Badge **≈23 editors**. The note says "**1** manuscript(s) moved from "Reviews Pending" to "Invite Reviewers"…". |
| V2-08 | 05b table, top 5 rows. | Columns: Editor, Journal, Needs action, Current manuscripts, Delayed proportion, Open manuscripts. Sorted by Needs action, highest first. Expected top rows (date-dependent): Takafumi Kadono JDE 3/3 (100%), Kenshi Yamasaki JDE 3/4 (75%), then several with 2. Ties are broken by the higher proportion. Proportions of 50% or more show in red. |
| V2-09 | Type `Kadono` in the 05b search box, then clear it. Pick **HEPR** in the 05b journal dropdown. | The search narrows to Kadono. HEPR shows "No editors have manuscripts needing their action…". |
| V2-10 | **Open manuscripts** on Kadono → **Needs action**. | It includes **4959091**, **5966577** and **8586549**. Columns: Status, ID, Title, Ver, Stage, Section / reason, Days since last editor action, Health, ReX. |
| V2-11 | **Open manuscripts** on Yamasaki → **No action needed**, then **All current manuscripts**. | The views switch correctly and the counts add up to the summary line. |
| V2-12 | Chief Editor: JDE, **Either**, count 1, 50%. | The preview lists **≈23 editors** with reasons. Changing the mode shows and hides the right boxes, as in EDT-35 and EDT-36. |
| V2-13 | Chief Editor: mode **Delayed proportion**, 50%. | Record the count. It should be fewer than 23. |
| V2-14 | Download the Chief Editor workbook (JDE / Either / 1 / 50%). | **"JDE - Chief Editor Delayed Manuscripts.xlsx"**. Overview + one sheet per editor (**≈24 sheets**). Overview columns: Editor, Editor Email, Manuscripts Needing Action, Current Manuscripts, Delayed Proportion, Inclusion Reason. Record whether the proportion is a **percentage number or text**, and whether there's an **autofilter**. |
| V2-15 | Open any Handling Editor draft in 06. | The greeting is "**Dear Dr. {surname}**". The subject is "{JC} - Action summary for your manuscripts". If the draft has an "Invite Reviewers" section, the **Reviewer Invitation Queue** paragraph with a video link appears under it. |
| V2-16 | **Copy HTML** on a draft and paste into Outlook. **Download .eml** and open it. | The table formatting survives in both. The .eml opens as an editable draft with the **To: address filled in**. |
| V2-17 | Download the **12 Draft status export**. | It opens in Excel and has the new column **"Task Performer Differs from Handling Editor?"** (Yes / No / blank). Record how many rows say Yes. |
| V2-18 | Upload a **CSV** copy of `data.xlsx` (optional). | Same results as V2-05. |
| V2-19 | **Negative test.** Upload `data (1).xlsx` as the Summary Report. | A yellow "Heads up" warning appears about missing Invited/Accepted/Version columns. Compare this with EDT-08, where EDT gave no warning. |

### 3C. Health Check rule (Daniel's behaviour)

Same as 3B, but **tick** "Don't draft manuscripts whose Health Check is 'On Track'", then Generate.

| ID | Steps | Expected |
|---|---|---|
| V2-20 | 04 tiles. | Flagged invite stale **≈11**, Editor drafts **≈34**. Still **279 / 279** accounted for. |
| V2-21 | 05b badge and note. | **≈10 editors**. The note says "**≈21** manuscript(s) not drafted because Health Check is On Track". |
| V2-22 | Draft status export. | Affected rows show the category "Skipped - Health Check On Track" in a pale amber color. |

---

# Parity checks: every EDT feature in v2

The compiler fills this table from the Run 1 and Run 3 results. "Expected parity" is what the merge intended.

| # | EDT feature (Run 1 test) | Where it is in v2 (Run 3 test) | Expected parity |
|---|---|---|---|
| P1 | Upload XLSX / CSV (EDT-03, 07) | Step 01 (V2-05, 18) | Same |
| P2 | Skips "Applied filters" row (EDT-03) | Step 01 (V2-05: 279 rows, not 280) | Same |
| P3 | Warns on the wrong file (EDT-08) | Step 01 warning (V2-19) | **v2 better**: EDT gives no warning |
| P4 | Data survives page reload (EDT-05) | Not carried over | **Intentional difference** (rule AU-3: no manuscript data kept in the browser) |
| P5 | Multi-select journal filter (EDT-10–12) | Step 02 journal filter (multi-select) + 05b single-journal dropdown | **Check**: is a single journal dropdown enough in 05b? |
| P6 | Editor search (EDT-13) | 05b search (V2-09) | Same |
| P7 | Summary metrics (EDT-04) | 04 tiles + 05b badge | Same intent, different numbers (different delay rule) |
| P8 | Delayed editors table with proportion (EDT-15, 16) | 05b table (V2-08) | Same columns. Counts differ by design. |
| P9 | Navigator: Delayed / Not delayed / All (EDT-17–22) | 05b Open manuscripts (V2-10, 11) | Same |
| P10 | Navigator columns: Required Task, Task Performer, "Reviewer invited ≤10 days?", Non-delayed reviewers | 05b navigator shows Section / reason, Days since last editor action, Health | **Known gap**. Decide whether Required Task and Task Performer are needed. |
| P11 | Draft email from inside the navigator (EDT-25) | Drafts are in Step 06, not in 05b | **Intentional difference**: one draft per editor, generated in bulk |
| P12 | Surname greeting (EDT-26) | 06 drafts (V2-15) | Same, with "Dr." punctuation |
| P13 | Reviewer Invitation Queue tip (EDT-26, 31) | Under the Invite Reviewers section (V2-15) | Same |
| P14 | Copy rich email → Outlook (EDT-28) | Copy HTML (V2-16) | Same |
| P15 | Copy plain text (EDT-29) | Not available | **Known gap**. Decide whether it's needed. |
| P16 | Open in mail client, mailto with no To: (EDT-30) | Download .eml, To: filled in (V2-16) | **v2 better** |
| P17 | Chief Editor: 3 modes + thresholds + preview (EDT-34–38) | 05b Chief Editor (V2-12, 13) | Same |
| P18 | Chief Editor workbook: Overview + sheet per editor (EDT-39, 40) | 05b download (V2-14) | Same structure. **Check** the % formatting and autofilter (EDT has both). |
| P19 | Tooltips (EDT-42) | Section descriptions (no tooltips) | Intentional difference |
| P20 | Delay rule = Health Check ≠ On Track (EDT-15) | Optional setting (V2-20, 21) | Same when the setting is ticked. The counts won't match EDT exactly, because v2 also uses its own buckets and editor-activity dates. |

---

## Tester result template

Copy this, fill it in and give it to the AI compiler with this document.

```
Environment: date | browser | opened directly or in Claude web

EDT-01:
EDT-02:
...
EDT-43:
MIP-01:
...
MIP-06:
V2-01:
...
V2-22:

Unplanned observations:
```

For every test, give the numbers and text you actually saw. Paste screenshots or copied text where you can, especially for EDT-15, EDT-26, EDT-40, MIP-02, V2-02, V2-08 and V2-14.
