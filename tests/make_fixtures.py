"""Build the synthetic test data for the regression kit.

Every row is invented. There are no real manuscripts, editors, reviewers or authors, so the
fixtures are safe to commit. Each row covers one routing rule; the scenario is written into
the Manuscript Title so a failing test points straight at the rule that changed.

Run from the repo root:  python tests/make_fixtures.py
"""
import datetime as dt
import json
from pathlib import Path

RUN_DATE = dt.date(2026, 10, 1)          # must match RUN_DATE in tests/run.js
EPOCH = dt.date(1899, 12, 30)


def serial(days_ago):
    """Excel date serial for a date N days before the run date (how Excel uploads arrive)."""
    if days_ago is None:
        return None
    return (RUN_DATE - dt.timedelta(days=days_ago) - EPOCH).days


EDITORS = {
    "ALPHA": ("Dr. Alex Alpha", "alex.alpha@example.org"),
    "BRAVO": ("Bea Bravo", "bea.bravo@example.org"),
    "CHARLIE": ("Chris Charlie", "chris.charlie@example.org"),
}
TRIAGE = ("Tara Triage", "tara.triage@example.org")
EA_NAME = "Tja Editorial Office"

BASE = {
    "Journal Name": "Test Journal A", "Version Number": 1, "Health Check": "Overdue",
    "Days in Stage": 20, "Task Performer": "Handling Editor", "Required Task": "Handling Editor to Invite Reviewers",
    "Task Performer Name": "", "Handling Editor Full Name": "", "Handling Editor Email": "",
    "Triage Editor Full Name": "", "Triage Editor Email": "",
    "Invited Reviewers": None, "Accepted Reviewers": None, "Version Review Reports Submitted": None,
    "Unique Reviewers Submitted": None, "Days Since Last Reviewer Invited": None,
    "Review Report Overdue Count (Extension NOT Captured)": None,
    "Editorial Assistant Full Name": EA_NAME, "Submission Date Original": serial(60),
    "Last Version Reviewer Invited Date": None, "Latest Decision Date": None,
    "Latest Recommendation Date": None, "Last Handling Editor Invited Date": None,
    "Latest Decision Type": "",
}

# (id, journal, editor, scenario, overrides)
SCENARIOS = [
    ("9000001", "TJA", "ALPHA", "S01 author stage, excluded",
     {"Stage": "S2", "Task Performer": "Author", "Required Task": "Author to Resubmit Manuscript"}),
    ("9000002", "TJA", "ALPHA", "S02 EA-side role, excluded",
     {"Stage": "S1", "Task Performer": "Submission Checker", "Required Task": "Submission Checker to Make Decision"}),
    ("9000003", "TJA", None, "S03 triage invite handling editor",
     {"Stage": "E1", "Task Performer": "Triage Editor", "Required Task": "Triage Editor to Invite Handling Editor"}),
    ("9000004", "TJA", "BRAVO", "S04 triage review handling editor decision",
     {"Stage": "E5", "Task Performer": "Triage Editor", "Required Task": "Triage Editor to Review Handling Editor Decision"}),
    ("9000005", "TJA", "ALPHA", "S05 invite, no reviewers, last invite 40d ago",
     {"Stage": "E3", "Invited Reviewers": 0, "Accepted Reviewers": 0, "Version Review Reports Submitted": 0,
      "Unique Reviewers Submitted": 0, "Last Version Reviewer Invited Date": serial(40), "Days Since Last Reviewer Invited": 40}),
    ("9000006", "TJA", "ALPHA", "S06 invite, within grace (invited 5d ago)",
     {"Stage": "R1", "Invited Reviewers": 3, "Accepted Reviewers": 0, "Version Review Reports Submitted": 0,
      "Unique Reviewers Submitted": 0, "Last Version Reviewer Invited Date": serial(5), "Days Since Last Reviewer Invited": 5}),
    ("9000007", "TJA", "ALPHA", "S07 invite, no activity dates at all",
     {"Stage": "E3", "Invited Reviewers": 0, "Accepted Reviewers": 0, "Version Review Reports Submitted": 0,
      "Unique Reviewers Submitted": 0}),
    ("9000008", "TJA", "ALPHA", "S08 decision ready, 2 unique reviews",
     {"Stage": "E4", "Required Task": "Handling Editor to Make Recommendation / Decision", "Invited Reviewers": 4,
      "Accepted Reviewers": 2, "Version Review Reports Submitted": 2, "Unique Reviewers Submitted": 2,
      "Last Version Reviewer Invited Date": serial(50)}),
    ("9000009", "TJA", "BRAVO", "S09 one review only, back to invite",
     {"Stage": "E4A", "Required Task": "Handling Editor to Make Recommendation / Decision", "Invited Reviewers": 3,
      "Accepted Reviewers": 1, "Version Review Reports Submitted": 1, "Unique Reviewers Submitted": 1,
      "Last Version Reviewer Invited Date": serial(30)}),
    ("9000010", "TJA", "BRAVO", "S10 reviews pending",
     {"Stage": "R1", "Task Performer": "Reviewer/Handling Editor",
      "Required Task": "Reviewers to Submit Review Report / Handling Editor to Invite Reviewers", "Invited Reviewers": 5,
      "Accepted Reviewers": 2, "Version Review Reports Submitted": 1, "Unique Reviewers Submitted": 1,
      "Review Report Overdue Count (Extension NOT Captured)": 0, "Last Version Reviewer Invited Date": serial(25)}),
    ("9000011", "TJA", "BRAVO", "S11 all accepted reviewers overdue",
     {"Stage": "R1", "Task Performer": "Reviewer/Handling Editor",
      "Required Task": "Reviewers to Submit Review Report / Handling Editor to Invite Reviewers", "Invited Reviewers": 9,
      "Accepted Reviewers": 1, "Version Review Reports Submitted": 0, "Unique Reviewers Submitted": 0,
      "Review Report Overdue Count (Extension NOT Captured)": 1, "Last Version Reviewer Invited Date": serial(45)}),
    ("9000012", "TJA", "BRAVO", "S12 data discrepancy, report but blank counts",
     {"Stage": "E4", "Required Task": "Handling Editor to Make Recommendation / Decision", "Version Review Reports Submitted": 1,
      "Unique Reviewers Submitted": 1}),
    ("9000013", "TJA", "CHARLIE", "S13 decision ready but On Track",
     {"Stage": "E4", "Health Check": "On Track", "Required Task": "Handling Editor to Make Recommendation / Decision",
      "Invited Reviewers": 2, "Accepted Reviewers": 2, "Version Review Reports Submitted": 2, "Unique Reviewers Submitted": 2,
      "Last Version Reviewer Invited Date": serial(15)}),
    ("9000014", "TJA", "CHARLIE", "S14 version 2 decision ready",
     {"Stage": "E7", "Version Number": 2, "Required Task": "Handling Editor to Make Recommendation / Decision",
      "Invited Reviewers": 2, "Accepted Reviewers": 2, "Version Review Reports Submitted": 2, "Unique Reviewers Submitted": 2,
      "Last Version Reviewer Invited Date": serial(20)}),
    ("9000015", "TJA", "CHARLIE", "S15 over a year since submission",
     {"Stage": "E3", "Submission Date Original": serial(400), "Invited Reviewers": 0, "Accepted Reviewers": 0,
      "Version Review Reports Submitted": 0, "Unique Reviewers Submitted": 0, "Last Version Reviewer Invited Date": serial(90)}),
    ("9000016", "TJA", "CHARLIE", "S16 stale invites, 70 invited none accepted",
     {"Stage": "R1", "Invited Reviewers": 70, "Accepted Reviewers": 0, "Version Review Reports Submitted": 0,
      "Unique Reviewers Submitted": 0, "Last Version Reviewer Invited Date": serial(12)}),
    ("9000017", "TJA", None, "S17 data check, no decision and blank task performer",
     {"Stage": "E3", "Task Performer": "", "Required Task": ""}),
    ("9000018", "TJB", "ALPHA", "S18 same editor, second journal",
     {"Journal Name": "Test Journal B", "Stage": "E3", "Invited Reviewers": 0, "Accepted Reviewers": 0,
      "Version Review Reports Submitted": 0, "Unique Reviewers Submitted": 0, "Last Version Reviewer Invited Date": serial(35)}),
    ("9000019", "TJA", "ALPHA", "S19 EA stage over threshold (Q1, 4 days)",
     {"Stage": "Q1", "Task Performer": "Quality Checker", "Required Task": "Quality Checker to Make Decision", "Days in Stage": 4}),
    ("9000020", "TJA", "ALPHA", "S20 author revision overdue (A1, 30 days)",
     {"Stage": "A1", "Version Number": 1, "Task Performer": "Author", "Required Task": "Author to Submit Revised Manuscript",
      "Days in Stage": 30}),
]


def mip_rows():
    rows = []
    for mid, journal, editor, scenario, over in SCENARIOS:
        r = dict(BASE)
        r.update({"Journal Code": journal, "Manuscript ID": mid, "Manuscript Title": f"[{scenario}]",
                  "ReX Review URL": f"https://review.example.org/details/{mid}"})
        if editor:
            name, email = EDITORS[editor]
            r.update({"Handling Editor Full Name": name, "Handling Editor Email": email, "Task Performer Name": name})
        r.update({"Triage Editor Full Name": TRIAGE[0], "Triage Editor Email": TRIAGE[1]})
        r.update(over)
        if r.get("Task Performer") == "Triage Editor":
            r["Task Performer Name"] = TRIAGE[0]
        if scenario.startswith("S17"):
            r["Task Performer Name"] = ""
        rows.append(r)
    return rows


def reviewer_rows():
    """Reviewer Performance Report rows for the Reviewer Reminders tab."""
    def rv(mid, name, email, response, status, accepted_ago, submitted_ago, overdue_ago, final_ago=None):
        return {"Manuscript ID": mid, "Manuscript Title": f"[{mid} reviewer test]", "Journal Code": "TJA",
                "Journal Name": "Test Journal A", "Reviewer Name": name, "Reviewer Email": email,
                "Reviewer Response to Invitation": response, "Reviewer Action After Initial Agreement": status,
                "Reviewer Accepted Date": serial(accepted_ago), "Reviewer Submitted Date": serial(submitted_ago),
                "Report Overdue Date (Extension NOT Captured)": serial(overdue_ago), "Final Decision Date": serial(final_ago),
                "Specialized Reviewer": "No"}
    return [
        rv("9000011", "Rita Overdue", "rita.overdue@example.org", "Agreed", "Pending", 40, None, 10),   # reminder
        rv("9000011", "Sam Submitted", "sam.done@example.org", "Agreed", "Submitted", 40, 20, None),   # closed
        rv("9000010", "Paula Pending", "paula.pending@example.org", "Agreed", "Pending", 12, None, None),  # awaiting list only
        rv("9000010", "Dan Declined", "dan.declined@example.org", "Declined", "", None, None, None),     # never
        dict(rv("9000016", "Tja Rss", "tja.rss@wiley.com", "Pending", "", None, None, None), **{"Specialized Reviewer": "Yes"}),
    ]


if __name__ == "__main__":
    out = Path(__file__).parent / "fixtures"
    out.mkdir(exist_ok=True)
    (out / "synthetic-mip.json").write_text(json.dumps(mip_rows(), indent=1) + "\n", encoding="utf-8")
    (out / "synthetic-reviewers.json").write_text(json.dumps(reviewer_rows(), indent=1) + "\n", encoding="utf-8")
    print(f"Wrote {len(SCENARIOS)} MIP rows and {len(reviewer_rows())} reviewer rows to {out}")
