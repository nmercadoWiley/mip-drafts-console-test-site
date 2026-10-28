# Meeting records

There's one file per meeting, named `YYYY-MM-DD-short-title.md`. Each file records the changes requested in the meeting and what the business owners approved. It's how a change in the code traces back to the conversation and the approval behind it.

The records are written by the **mip-meeting-intake** skill in Cowork. Drop in a transcript and say "process this meeting". You can also write them by hand.

**Never paste the transcript here.** Transcripts stay in the TranscriptSync archive. Records may name Wiley staff and roles, but **never** external editors, reviewers, authors, manuscript IDs or titles.

## The loop

```
transcript ──► meeting record + backlog items ("Awaiting approval") + approval drafts
                                   │
                    Nelson sends drafts to the approver(s)
                                   │
reply pasted back ──► Approvals section filled in · backlog → "Ready (approved)" · decision log updated
                                   │
"implement" ──► code + tests + CHANGELOG ──► Nelson reviews in GitHub Desktop and commits
```

## Template

```markdown
# <Meeting name> (<YYYY-MM-DD>)

**Source:** <transcript file name> · **Attendees:** <Wiley staff + roles> · **Processed:** <date>

## Summary
<2–4 sentences: what the meeting was about and what changed in our understanding>

## Items

| # | Type | Item | Raised by (time) | Maps to | Approver | Effort / risk |
|---|---|---|---|---|---|---|
| 1 | Change requested | <plain-language change> | <name> (<mm:ss>) | <B#/decision ID or new> | <name> | <S/M/L, risk> |
| 2 | Decision made | … | | | | |
| 3 | Question | … | | | | |
| 4 | Action item | <who will do what> | | | — | — |
| 5 | Context | … | | | — | — |

## Approval requests sent
- <date> to <approver>: items <#, #>

## Approvals
| # | Approver | Answer | Date |
|---|---|---|---|
| 1 | | Approve / Change: … / Reject | |

## Implemented
| # | Backlog | Commit summary | Date |
|---|---|---|---|
```
