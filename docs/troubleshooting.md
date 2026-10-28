# Troubleshooting and known limitations

**Tool version:** v2.2 · Add new problems here as they're reported, especially during the pilot.

## Common problems

| Symptom | Likely cause | Fix |
|---|---|---|
| Yellow **"Heads up"** box after uploading | The file is missing Invited Reviewers, Accepted Reviewers or Version Number. Usually it's the wrong export, for example an Activity Tracker loaded as the Summary Report. | Upload the **MIP Summary Report** or the paginated MIP report. The Activity Tracker goes in the *second* box. |
| Nothing happens when a file is dropped | The file type isn't supported, or the Excel library failed to load (no internet, or a blocked network) | Use .xlsx, .xls or .csv. Check the internet connection. The tool needs the library to read *any* file, CSV included, so on a network that blocks cdnjs.cloudflare.com it can't work until the library is bundled in (planned, see hosting record S6). |
| "Accounted for" numbers don't match | A row went through a path that isn't counted | Download the Step 12 export, filter "In Email Draft?" = No, and read "Not-Drafted Reason". Report it to the maintainer, with a masked copy (`tests/anonymise.py`). |
| A paper I know is finished is in a draft | The export is older than the latest action. The data can be 24–48 hours behind. | Use a fresh export. Remove that paper by hand before sending. |
| An editor gets two separate drafts | Their name is spelled differently on different rows, or they work on several journals and grouping is "per journal" | Check the spelling in the export. For multi-journal editors, that's the grouping setting working as intended. |
| Two different editors got merged into one draft | They have exactly the same name. The tool identifies editors by name. | Split the draft by hand. A known limitation (see below). |
| A paper the EA expected isn't in any draft | It's within the grace period, author- or EA-stage, outside the Step 02 filters, or skipped by the Health Check setting | Look it up in **Step 01 → Double-check a manuscript's data**, then check its "Not-Drafted Reason" in the Step 12 export |
| Formatting is lost when pasting | The destination strips HTML (some Freshdesk setups) | Use **Download .eml** for Outlook, or **Copy plain text** |
| "Copy" doesn't seem to work | The browser blocked clipboard access | Click the button again with the tool window active. If it still fails, select the draft text and copy it manually. |
| The footer shows an old template version | You have an old copy of the file | Get the current file from the published location |
| Reviewer reminders: "No Reviewer Match" | The Summary Report says the paper is overdue, but no reviewer passed the checks (Agreed + Pending + Report Overdue Date filled) | Use Tab 2, **Double-check which reviewers this tool matched** to see each reviewer's values |
| Tab 5 shows nothing useful | The wrong export was used | Use the **Full Manuscript Listing**, choosing "Data with current layout" |

## Known limitations

| Limitation | Why | Planned fix |
|---|---|---|
| Doesn't know if a reminder was sent or answered | Drafts leave the tool through Outlook or Freshdesk | Wish list 1: hosted version + Microsoft Graph, or "mark as sent" |
| Data is only as fresh as the last export | No live connection to Power BI | Wish list 4: scheduled feed through the Power BI REST API |
| Editors are identified by name, not ID | The reports don't have an editor ID | Request an ID column from Luke Barrett's team |
| Last editor action is estimated without the Activity Tracker | The Activity Tracker covers one journal at a time | Dependency D1: add the fields to the MIP Summary Report |
| EAs can't use reviewer reminders | No access to the Reviewer Performance Report | Dependency D2 |
| Tab 3 and 4 thresholds reset every session, and default to 1 day | Settings aren't saved | PRP to set benchmark values. Save them once the tool is hosted. |
| Copies don't update themselves | It's a downloaded file | Hosting: one URL, updated on every commit |
| Shows any journal in the uploaded file | Vendor separation relies on each EA getting only their own journal's report | Must be designed into any hosted or live-data version (NFR-1) |
