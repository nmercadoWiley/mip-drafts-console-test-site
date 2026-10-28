# Regression test kit

Run this before every release to confirm that a change didn't alter which manuscripts get flagged, who they go to, or what the emails say. No browser and no real data are needed.

## Run it

You need Node.js 18 or later. From the repo root:

```
node tests/run.js
```

| Result | Meaning | What to do |
|---|---|---|
| `✔ … matches baseline` for all three | Nothing changed | Release |
| `✘ … N difference(s)` | Something changed. Each difference shows the expected text next to the actual text. | If the change was **intended** (for example new template wording or an agreed rule change), run `node tests/run.js --update`, then commit the updated `tests/baseline/*.json` with a CHANGELOG note. If it **wasn't intended**, fix the code. |

## What it checks

`run.js` loads the console's own code from `mip-drafts-console.html`, feeds it the synthetic fixtures, and runs it under three settings configurations:

| Configuration | Grouping | All-overdue → Invite | Health Check rule |
|---|---|---|---|
| `v2-defaults` | per journal | on | off |
| `like-original` | combined | off | off |
| `health-check-rule` | per journal | on | on |

For each configuration it compares:

- the Step 04 summary tiles
- where each manuscript went and why
- the subject and text of every editor, triage, EA and reviewer draft
- the Step 05b delayed-editor list

The run date is fixed at 1 Oct 2026, so day counts never drift.

## Test data

`fixtures/` is **entirely made up**. Each of the 20 MIP rows covers one rule, and the rule is written into the Manuscript Title (for example `[S11 all accepted reviewers overdue]`), so a failure points at the rule that changed.

| Scenario | Rule covered |
|---|---|
| S01, S20 | Author stage excluded |
| S02, S19 | EA-side role excluded |
| S03, S04 | Triage routing |
| S05, S07 | Invite Reviewers: stale, or no dates at all |
| S06 | Held back by the grace period |
| S08, S14 | Decision ready (2+ reviews), V1 and V2 |
| S09 | One review only → Invite |
| S10 | Reviews Pending |
| S11 | All accepted reviewers overdue |
| S12 | Data discrepancy |
| S13 | "On Track" paper (Health Check setting) |
| S15 | Over a year since submission |
| S16 | Stale invites (70 invited) |
| S17 | Data check: no decision and blank task performer |
| S18 | Same editor in a second journal (grouping) |

The reviewer fixture has 5 rows. They cover:

- one overdue reviewer who should get a reminder
- a reviewer who has already submitted
- a pending reviewer who isn't overdue yet
- a reviewer who declined
- an RSS service address

To add a scenario, edit `make_fixtures.py`, then run `python tests/make_fixtures.py` and `node tests/run.js --update`. Commit all three changes together.

## Testing with a real export

Never commit real exports. To test with a real file, or to share it for a bug report, make a masked copy first:

```
pip install openpyxl
python tests/anonymise.py "C:\path\to\export.xlsx"
```

This replaces names, emails, titles, institutions, URLs and manuscript IDs with stable stand-ins, and keeps every count, date, stage and task. On the 29 Sep test export, the masked copy produced the same 42 drafts as the original. Check the output by eye before sharing it.
