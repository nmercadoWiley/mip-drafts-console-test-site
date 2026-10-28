# PRPL guide: oversight and escalation with MIP Drafts Console

**For:** Peer Review Performance Leads · **Tool version:** v2.2 · **Status: DRAFT.** Daniel and Gayatri to review.

PRPLs use the same tool as EAs, but mostly for **oversight**: how EAs and editors are performing across your portfolio, and who needs escalating. Upload your **portfolio-wide** export from Power BI (filtered to your name). A single-journal file only shows that one journal.

## Weekly routine

⚠ *The frequency is a suggestion. Agree it with PRP.*

| What | Where | What to look for |
|---|---|---|
| **1. Which editors are behind** | Tab 1, **Step 05b: Delayed editors** | Editors with a high **delayed proportion** (red means 50% or more). A high count with a low proportion usually means a busy editor who's otherwise on top of things. |
| **2. Stalled queues** | Tab 1, **Step 05** (threshold 30 days) | Editors who haven't acted at all for 30+ days. That's a stronger signal than "delayed". |
| **3. EA turnaround** | **Tab 3: EA Overdues** | Manuscripts sitting in EA stages longer than the benchmark. ⚠ Set the per-stage thresholds; the default is 1 day. |
| **4. Author delays** | **Tab 4: Author Tasks** | Revisions past their window. ⚠ Set realistic thresholds; the default is 1 day. |
| **5. Old manuscripts** | Tab 1, **Step 11** (365 days) | Tick the stage groups you care about. None are ticked to start with. |
| **6. Data problems** | Tab 1, **Step 04** data check tile and **Tab 3, section 03** | No decision and no named task performer: check these in ReX. |

## Escalating an unresponsive editor

1. **Confirm it.** In Step 05b, click **Open manuscripts** on the editor. Check the **Needs action** list against ReX, and look at "Days since last editor action".
2. **Check the reminder history** with the EA. The tool doesn't track sent reminders yet (wish list item 1).
3. **Escalate to the Chief Editor.** At the bottom of Step 05b, under Chief Editor workbook:
   - pick the **journal**
   - choose **Include editors based on** (count, proportion, or either; ⚠ PRP default to be agreed)
   - check the preview, then click **Download Chief Editor workbook**
   - the Overview sheet lists each included editor and why, and each editor has their own sheet of manuscripts
4. **Send the workbook to the Chief Editor** with your own covering note. The tool doesn't draft this email.
5. ⚠ **What happens next** (performance discussion, reassignment) follows the PRP process. To be defined (wish list item 2).

## Portfolio reporting

**Tab 5, Editor Performance**, uses a different export, the **Full Manuscript Listing** (choose "Data with current layout"). It shows:

- workload
- accept rate
- days to first and final decision
- the 15 slowest editors (only those with 5 or more decided papers)
- decisions by whether reviewer reports exist

Click any number to see the manuscripts behind it.

**Worth checking:** "Accepted, no reviewer reports" and "Accepted, exactly 1 unique reviewer report". These may need an integrity look (⚠ business rules question #12).

## Reviewer health

On **Tab 2, Reviewer Reminders**, upload the Reviewer Performance Report.

- **Step 05, Awaiting reviewer reports:** lists accepted-but-not-submitted reviewers by acceptance date, so you can spot reviewers who've gone quiet for months. Consider revoking those invitations and asking the editor to invite others.
- **Step 07:** shows **specialized reviewer** usage and **RSS service** invitations that are pending or declined.

## Wiley Forward portfolios

If your journals have **internal editors**, set Step 03's **"For editors who work across multiple journals"** to **one combined email per editor**. Editors then get one email covering all their journals. Use **Step 08, per-journal workbooks** when editors want a spreadsheet with every editor on it.
