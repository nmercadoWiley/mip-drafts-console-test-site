# Data model: how Power BI data powers the MIP Drafts Console

**Version:** console v2.2 · **Last updated:** 1 Oct 2026 · **Written from:** the code in `mip-drafts-console.html`, not from screenshots or memory

The console has no database and no live connection. Users export reports from Power BI, or receive them by subscription, and upload the Excel or CSV files. Everything is joined and calculated in the browser, and nothing is kept after the tab closes.

## 1. Data flow

```mermaid
flowchart LR
  subgraph PBI["Power BI (Luke Barrett's team)"]
    MIP["MIP Summary Report<br/>or paginated MIP report"]
    ACT["Activity Tracker<br/>(one journal at a time)"]
    RPR["Reviewer Performance Report"]
    FML["Full Manuscript Listing"]
  end

  subgraph GET["How users get the files"]
    SUB["Subscription email to the<br/>editorial office inbox (EAs)"]
    EXP["Manual export<br/>(PRPLs only)"]
  end

  MIP --> SUB
  MIP --> EXP
  ACT --> EXP
  RPR --> EXP
  FML --> EXP

  subgraph APP["MIP Drafts Console (runs in the browser)"]
    T1["Tab 1: Editor, Triage & EA Drafts<br/>Steps 01–12, incl. 05b Delayed editors"]
    T2["Tab 2: Reviewer Reminders<br/>+ RSS & Specialized Reviewers"]
    T3["Tab 3: EA Overdues"]
    T4["Tab 4: Author Tasks"]
    T5["Tab 5: Editor Performance"]
    TPL[("Embedded templates<br/>templates.json")]
  end

  SUB -->|upload| T1
  EXP -->|upload| T1
  EXP -->|optional upload| T1
  EXP -->|upload| T2
  EXP -->|upload| T5
  T1 -->|reuses MIP data| T2
  T1 -->|reuses MIP data| T3
  T1 -->|reuses MIP data| T4
  TPL --> T1
  TPL --> T2

  subgraph OUT["Outputs (saved to the user's laptop)"]
    EML["Email drafts<br/>copy HTML / plain text / .eml"]
    XLS["Workbooks<br/>per-journal, Chief Editor, stalled queue, overdues"]
    AUD["Draft status export<br/>original report + 9 audit columns"]
  end

  T1 --> EML
  T1 --> XLS
  T1 --> AUD
  T2 --> EML
  T2 --> XLS
  T3 --> XLS
  T4 --> XLS
  T5 --> XLS
  EML -->|EA sends from Outlook or Freshdesk| ED["Editors · Reviewers · Chief Editors"]
```

The Activity Tracker arrow into Tab 1 is optional. Without it, the tool estimates the last editor action from four MIP date columns (see section 3).

## 2. How the reports relate

The **only join key is Manuscript ID**, compared as trimmed text. The tool identifies editors by their **name and email as text**, because the reports carry no editor ID.

```mermaid
erDiagram
  JOURNAL ||--o{ MIP_ROW : "Journal Code"
  MIP_ROW ||--o| ACTIVITY_ROW : "Manuscript ID (optional)"
  MIP_ROW ||--o{ REVIEWER_ROW : "Manuscript ID"
  EDITOR ||--o{ MIP_ROW : "Handling / Triage Editor name"
  MIP_ROW ||--o| AUDIT_ROW : "one per uploaded row"
  EDITOR ||--o{ DRAFT : "one per editor (per journal)"
  DRAFT }o--o{ MIP_ROW : "lists rows needing action"
  LISTING_ROW }o--|| JOURNAL : "Journal Code (Tab 5 only, not joined)"

  MIP_ROW {
    string manuscript_id PK "Manuscript ID"
    string journal_code "Journal Code"
    string stage "Stage (S1, E3, R1…)"
    number version "Version Number"
    string required_task "Required Task"
    string task_performer "Task Performer (role)"
    string task_performer_name "Task Performer Name"
    string health_check "Health Check"
    string he_name_email "Handling Editor Full Name / Email"
    string te_name_email "Triage Editor Full Name / Email"
    number invited "Invited Reviewers"
    number accepted "Accepted Reviewers"
    number submitted "Version Review Reports Submitted"
    number unique_submitted "Unique Reviewers Submitted"
    number overdue "Review Report Overdue Count"
    number days_since_invite "Days Since Last Reviewer Invited"
    date proxy_dates "Last reviewer invited / decision / recommendation / HE invited"
    string rex_url "ReX Review URL"
  }
  ACTIVITY_ROW {
    string manuscript_id FK "Manuscript ID"
    date last_editor_action "Last Editor Action Date"
    number days_since_action "Days Since Last Editor Action Date"
  }
  REVIEWER_ROW {
    string manuscript_id FK "Manuscript ID (many per manuscript)"
    string reviewer_name_email "Reviewer Name / Email"
    string response "Reviewer Response to Invitation"
    string status "Reviewer Action After Initial Agreement"
    date accepted_submitted "Reviewer Accepted / Submitted Date"
    date report_overdue "Report Overdue Date"
    string specialized "Specialized Reviewer"
  }
  LISTING_ROW {
    string manuscript_id "Manuscript ID"
    string editors "Handling / Triage Editor"
    date dates "Submission, first and final decision"
    string final_category "Final Decision Category"
    number reports "Reviewer Reports Submitted"
  }
  EDITOR {
    string name "Full name (text)"
    string email "Email (text)"
  }
  DRAFT {
    string recipient "Editor"
    string sections "Decision, Invite, Pending, Triage…"
    string wording "From templates.json"
  }
  AUDIT_ROW {
    string in_draft "In Email Draft?"
    string drafted_to "Email Drafted To"
    string action "Email Drafted Action"
    string reason "Not-Drafted Reason"
    string category "Row Highlight Category"
  }
```

## 3. Which report feeds which feature

| Feature | MIP Summary | Activity Tracker | Reviewer Performance | Full Manuscript Listing |
|---|:---:|:---:|:---:|:---:|
| Tab 1: editor and triage drafts, 05b delayed editors, Chief Editor workbook, stalled queues, V2+ and over-a-year lists, audit export | **Required** | Optional: exact last-editor-action date | | |
| Tab 2: overdue reviewer reminders and awaiting-reports list | Required (overdue count, title, journal; reused from Tab 1) | | **Required** | |
| Tab 2: RSS and specialized reviewers | | | **Required** | |
| Tab 3: EA Overdues | **Required** (reused from Tab 1) | | | |
| Tab 4: Author Tasks | **Required** (reused from Tab 1) | | | |
| Tab 5: Editor Performance | | | | **Required** (its own upload, not shared) |

**Last editor action:**

- If the Activity Tracker is uploaded, its date is used.
- Otherwise the tool uses the most recent of four MIP dates: *Last Version Reviewer Invited*, *Latest Decision*, *Latest Recommendation* and *Last Handling Editor Invited*. This estimate matched the Activity Tracker exactly on two test journals (153/153 and 567/567 rows).

## 4. How a MIP row becomes an email

```mermaid
flowchart TD
  R["MIP row"] --> F{"Step 02 filters<br/>journal · health check · editor"}
  F -->|filtered out| X0["Audit: excluded by filter"]
  F --> A{"Author-stage or<br/>EA-side role?"}
  A -->|yes| X1["Audit: excluded"]
  A -->|no| TR{"Triage task?"}
  TR -->|yes| HCT{"Health Check setting on<br/>and paper On Track?"}
  HCT -->|yes| X3
  HCT -->|no| TD["Triage Editor draft"]
  TR -->|no| B{"Reviewer progress<br/>(invited / accepted / reports)"}
  B -->|"none accepted, editor acted<br/>within grace period"| X2["Audit: within grace period"]
  B -->|"none accepted · 1 review only ·<br/>all accepted reviewers overdue"| INV["Invite Reviewers"]
  B -->|"all accepted have reported,<br/>2+ unique reviews"| DEC["Make Recommendation / Decision"]
  B -->|"reports still owed"| PEN["Reviews Pending (EA chases)"]
  B -->|"invited and accepted blank,<br/>report exists"| DIS["EA to Review Discrepancies"]
  INV --> HC{"Health Check setting on<br/>and paper On Track?"}
  DEC --> HC
  HC -->|yes| X3["Audit: skipped, Health Check"]
  HC -->|no| HD["Handling Editor draft"]
  PEN --> HD
  DIS --> HD
  HD --> W["Wording from templates.json<br/>+ tables generated by the tool"]
  TD --> W
```

Two more Step 03 settings act just before a row reaches the Handling Editor draft. Both are off by default. One leaves Version 1 papers out. The other moves Reviews Pending papers to a separate spreadsheet. Neither affects rows that go to the Triage Editor.

The full rules and the decisions still open are on the Confluence page *MIP Drafts Console: Business Rules & Decision Log*.

## 5. Known weak points in the data

| Weak point | Effect | Fix |
|---|---|---|
| Editors are matched by **name text**, not an ID | The same person spelled two ways gets two drafts. Two people with the same name get merged into one. | Ask for an editor ID column in the MIP report (Luke Barrett's team) |
| Columns are matched by **exact header name** | A renamed column in Power BI silently switches features off. The tool warns only for Invited, Accepted and Version. | Agree a fixed column list (dependency D4) |
| The Activity Tracker covers **one journal at a time** | Portfolio runs fall back to the estimated last action | Add the fields to the MIP Summary Report (D1) |
| **EAs can't get the Reviewer Performance Report** | EAs can't use Tab 2 | Set up an EA subscription (D2) |
| Data is only as fresh as the **last export** | Emails warn that data may be 24–48 hours old | A live feed. See the wish list and the Power BI REST API notes. |
