# Business rules: every tab

**Version:** console v2.2 · **Last updated:** 1 Oct 2026 · **Status:** written from the code. **Needs SME confirmation.**

This page describes what the tool *does* today, rule by rule. It covers all five tabs. Where a rule is a judgement call rather than a fact about the data, it's marked **☐ Confirm**, with the person who should confirm it.

- The **editor-reminder rules** (Tab 1, Steps 03–08) and their open decisions are owned on the Confluence page *MIP Drafts Console: Business Rules & Decision Log*. They're summarised here only so this page is complete.
- How the reports connect is in `docs/data-model.md`.

Stage codes such as S1 and E3 follow Wiley's official stage list. The full definitions are built into Tab 3 and Tab 4.

---

## Tab 1: Editor, Triage & EA Drafts

### Steps 03–08: editor and triage reminders (summary)

| Rule | What the tool does | Settings |
|---|---|---|
| Excluded rows | Task Performer or Required Task mentions "author", or Task Performer is Submission Checker, Quality Checker, Material Checker, Screener, Revision Checker or Editorial Assistant | — |
| Triage | Required Task mentions "invite handling editor" or "review handling editor decision". It goes straight into the Triage Editor's draft, with no grace period. | — |
| Invite Reviewers | No accepted reviewers and no reports, and the editor's last action is older than the grace period (or there is no last-action date at all, in which case there's no grace period). Also used when there's only 1 unique review, or when every accepted reviewer is overdue (setting on by default). | Grace period: 10 days |
| Make Recommendation / Decision | Everyone who accepted has submitted, and there are at least 2 unique reviews | — |
| Reviews Pending | Accepted reviewers still owe a report. The EA chases them. | Can be moved to a separate sheet |
| Discrepancy | Invited and Accepted are both blank, but a report exists | — |
| Version 1 papers | Can be left out of Handling Editor emails. They still appear in Reviewer Invitation Monitoring. Rows that go to the Triage Editor are not affected. | Off by default |
| Health Check | Shown for context only. It only decides anything if the "On Track" setting is ticked. | Off by default |
| Recipient | Handling Editor. If there isn't one, the Triage Editor. | — |
| Grouping | One email per editor per journal (default), or one combined email per editor | Step 03 |

### Step 05: Stalled queues (PRPL oversight)

| Rule | What the tool does | ☐ Confirm |
|---|---|---|
| Who appears | Editors with at least one manuscript in Invite Reviewers, Make Decision, Triage: invite HE, or Triage: review decision, where the **days since the last editor action ≥ the threshold** | Gayatri |
| Threshold | **30 days** by default. Separate from the Step 03 grace period. | Gayatri / PRP |
| Not counted | Reviews Pending, discrepancies, and manuscripts with no last-action date at all | Gayatri: should "no date at all" count as stalled? |

### Step 05b: Delayed editors and Chief Editor escalation (from Daniel's tool)

| Rule | What the tool does | ☐ Confirm |
|---|---|---|
| Needs action | The manuscript is in an editor or triage draft under Invite Reviewers, Make Decision or either triage section | Daniel (Q3: should Reviews Pending count?) |
| Current manuscripts | Every manuscript routed to that editor in that journal, excluding author-stage and EA-side rows | Daniel |
| Delayed proportion | Needs action ÷ current manuscripts. Shown in red at 50% or more. | Daniel |
| Chief Editor inclusion | By count (default **≥ 1**), by proportion (default **≥ 50%**), or either | Daniel (Q2: he demoed ≥ 2) |

### Step 09: Reviewer Invitation Monitoring (EA summaries)

| Summary | Rule | ☐ Confirm |
|---|---|---|
| #1 V1 status | Every **Version 1** manuscript that isn't in stage S2, split into: no Handling Editor · HE assigned but no invites · invited, none accepted · at least one accepted | Gayatri: why is S2 excluded? |
| #2 Stale invites | Manuscripts with **more than 60** reviewers invited (adjustable), 0 accepted and 0 reports | Gayatri / PRP: is 60 right for every journal? |
| Recipient | The EA email address typed into Step 03 | — |

### Step 10: Late-stage revision monitoring

| Rule | What the tool does | ☐ Confirm |
|---|---|---|
| In scope | Version **2 or above**, excluding author-stage and EA-side rows | Gayatri |
| "All V2+" list | Only rows with **2 or more unique reviews** | Gayatri: the heading says "All V2+", but V2+ papers with fewer than 2 reviews are left out |
| Decision-ready list | Also: accepted > 0 and reports = accepted | Gayatri |
| Version filter | Every version is ticked by default | — |

### Step 11: Manuscripts over a year since submission

| Rule | What the tool does | ☐ Confirm |
|---|---|---|
| Age | Days since **Submission Date Original**, more than **365 days** (adjustable) | Gayatri |
| Stages | **None are ticked to start with.** The user picks stage groups: Author, EA, Editor, Reviewer, Quality Control, Decision delays, Reviewer delays. A stage can be in more than one group. | Gayatri: should some be ticked by default? |
| Filters | Follows Step 02's journal, health and editor filters | — |

### Step 12: Draft status export

The original upload, plus 9 columns:

- EA Reminder Sent On
- In Email Draft?
- Email Drafted On
- Email Drafted To
- Email Drafted Action
- Not-Drafted Reason
- Data Check: No Decision & Blank Task Performer Name
- Task Performer Differs from Handling Editor?
- Row Highlight Category

Rows are colour-coded by category. The data check flag takes priority over every other colour.

**Data check:**
- **Checks for:** manuscripts with no Latest Decision Type and a blank Task Performer Name.
- **Stages covered:** E0, E1, E2, E3, R1, E4A, E4, E5, A1, E6, R2, E7A, E7, E8 and R2R.
- **Confirm with Gayatri:** is that the right list of stages?

---

## Tab 2: Reviewer Reminders

**Inputs:**

- **MIP Summary Report.** By default it's reused from Tab 1. It supplies the overdue count, title and journal.
- **Reviewer Performance Report** (required). It has one row per reviewer per manuscript, and it's joined to the MIP report on Manuscript ID.

### Step 04: Overdue reviewer reminders

The tool drafts a reminder for a reviewer only when **all** of these are true:

1. The manuscript's **Review Report Overdue Count** in the MIP report is **above 0**.
2. The reviewer's **Report Overdue Date (Extension NOT captured)** is filled in. This is MIP's own "confirmed overdue, no extension" signal.
3. **Reviewer Response to Invitation** is exactly **"Agreed"**.
4. **Reviewer Action After Initial Agreement** is exactly **"Pending"**. Submitted, Declined, Expired and similar values all mean the slot is closed.
5. The reviewer has an email address.

Then:

- **If the accepted and submitted date columns exist:** every reviewer who accepted and hasn't submitted gets a reminder, oldest acceptance first.
- **Otherwise:** the tool falls back to a status containing "overdue" or "failed to submit". If there's no status column either, every reviewer that passes the checks above gets a reminder.
- **Latest Decision Type is deliberately not checked.** A minor or major revision decision doesn't cancel a reviewer's pending report.
- **There's one draft per reviewer per manuscript.** The wording comes from the `reviewerReminder` template.

☐ **Confirm (Gayatri):** should a reviewer get a reminder for an earlier version after a revision decision?

### Step 05: Awaiting reviewer reports

- **Rule:** reviewers who accepted, haven't submitted, and whose manuscript has **no Final Decision Date**. The response and status checks are the same as in Step 04.
- **No overdue flag needed:** a reviewer doesn't have to be marked overdue to appear here. This list is for visibility before a reminder is due.
- **Grouping:** by **acceptance date**, oldest first, with the days elapsed. Drafts can be generated for one group at a time.

### Step 07: RSS and specialized reviewers

- **Specialized reviewers:** rows where **Specialized Reviewer = "Yes"**. Each manuscript counts once per reviewer, across all versions. A manuscript counts as decided when Final Decision Type is filled in.
- **RSS service:** reviewer emails ending in **rss@wiley.com**. They're detected automatically, and the user can untick any. They're split by Reviewer Response into **Pending** and **Declined**, and broken down by journal.

### Step 06: Draft status export

- **Summary Report sheet:** the Summary Report with three added columns: Reminder Status, Reminder Recipients and Reminder Created On.
- **Reminder Status values:**
  - Generated – Overdue
  - Generated – Pending Follow-up
  - No Reviewer Match
  - Not Overdue
- **Reviewer Reminder Log sheet:** one row per drafted reminder.

---

## Tab 3: EA Overdues

| Rule | What the tool does | ☐ Confirm |
|---|---|---|
| Stages | **E0, E1, Q1, Q2, Q3, RC1, RC3, S1, S3**, all ticked by default | Gayatri: E0 and E1 are editor-assignment stages. Are they EA-owned in every journal? |
| Overdue | **Days in Stage > the stage's threshold** | — |
| Default threshold | **1 day for every stage**, editable per stage. The thresholds are not saved. | Gayatri / PRP: what are the benchmark values per stage? |
| Grouping | By journal, sorted by the longest delay | — |
| Data check | The same "no decision and blank task performer" check as Step 12, grouped by journal | — |
| Source | The Tab 1 upload, or its own upload covering a whole portfolio | — |

## Tab 4: Author Tasks

| Rule | What the tool does | ☐ Confirm |
|---|---|---|
| Stages | **A1, S2, RC2, Q2** | Gayatri: Q2 is in both the EA and the Author lists |
| Overdue | **Days in Stage > the stage's threshold**. The default is **1 day** per stage. | Gayatri / PRP: authors usually get weeks (for example, a 90-day revision window). Is 1 day a placeholder? |
| Output | A list grouped by journal, and an .xlsx download. **No author email drafts.** | Gayatri: are author reminders needed? |

## Tab 5: Editor Performance

**Input:** the **Full Manuscript Listing** export ("Data with current layout"). It's a separate upload and isn't shared with the other tabs.

| Measure | Definition |
|---|---|
| Decided | Final Decision Category is filled in and isn't "No Final Decision" |
| Current workload | Total minus decided |
| Accept rate | "Formally Accepted" ÷ decided |
| Days to final decision | Submission Date Original → Final Decision Date (decided papers only, negative values ignored). Shown as an average and a median. |
| Days to first decision | Submission → First Decision Date |
| First → final, recommendation → final | Between those dates, decided papers only |
| Zero-reviewer share | Papers with no unique reviewer reports ÷ total |
| Slowest-editor chart | The 15 slowest by average days to final decision, **only editors with 5 or more decided papers** |
| Workload chart | The top 15 by current workload |
| Decision breakdown | Rejected or accepted, with or without reviewer reports. Accepted papers with exactly 1 versus 2 or more unique reports. |
| Grouping | By Handling Editor, Triage Editor or journal. Journal rows expand to show their editors. |

☐ **Confirm (Gayatri / Iris):**
- Should "Accepted with no reviewer reports" and "Accepted with exactly 1 report" be flagged as integrity checks?
- Is 5 decided papers the right minimum for the slowest-editor chart?

---

## Summary of what needs confirming

| # | Question | Owner |
|---|---|---|
| 1 | Do manuscripts with no editor-action date count as stalled (Step 05)? | Gayatri |
| 2 | Why is stage S2 excluded from EA summary #1? | Gayatri |
| 3 | Is the 60-invite stale threshold right for every journal? | Gayatri / PRP |
| 4 | "All V2+" leaves out V2+ papers with fewer than 2 reviews. Rename it, or change the rule? | Gayatri |
| 5 | Should Step 11 tick any stages by default? | Gayatri |
| 6 | Are the stages covered by the data check correct? | Gayatri |
| 7 | Reviewer reminders after a revision decision | Gayatri |
| 8 | Are E0 and E1 EA-owned? | Gayatri |
| 9 | What should the stage thresholds be for EA (1 day today) and authors (1 day today)? | Gayatri / PRP |
| 10 | Q2 appears in both the EA and Author lists | Gayatri |
| 11 | Are author reminder emails needed? | Gayatri / Iris |
| 12 | Editor Performance: integrity flags and the 5-paper minimum | Gayatri / Iris |
