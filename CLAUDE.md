# MIP Drafts Console: instructions for Claude agents

Read this first in every session. It applies to every agent working in this repo.

## What this is

A single-file browser tool, `mip-drafts-console.html`, for Wiley's Peer Review Performance team. EAs and PRPLs upload Power BI exports, and the tool drafts reminder emails, flags delayed editors and builds escalation workbooks. Everything runs in the browser, and nothing is stored or sent.

- **Code map and how to change things:** `docs/maintainer-guide.md`. Read it before you touch the code.
- **What every rule does:** `docs/business-rules.md`
- **How the data connects:** `docs/data-model.md`
- **Decisions:** the live decision log is on Confluence, *MIP Drafts Console: Business Rules & Decision Log* (AICOE space). `docs/open-decisions.md` is a copy.

## Hard rules

1. **Never change a business rule or default setting that hasn't been approved.** If an issue asks for a rule change, check that it's marked approved (the `approved` label, or a link to the decision). If it isn't, stop and comment instead of coding.
2. **Never put real data in the repo.** That means no Power BI exports, no real names, emails, manuscript IDs or titles, and no screenshots of reports. Use `tests/fixtures/`, which is synthetic, or `tests/anonymise.py`.
3. **Run `node tests/run.js` before every commit.**
   - If it fails and the change wasn't meant to alter behaviour, fix the code.
   - If the change *was* meant to (approved), run `node tests/run.js --update`, and describe the intended difference in `CHANGELOG.md` and the PR.
4. **Email wording lives in `templates/templates.json`.** Don't hard-code wording in the console. If you add a template field, update the admin page's `META` too.
5. **Keep both copies of the template engine identical:** `tplHtml` and `tplText` in the console and in `admin/template-admin.html`.
6. **No storage, no network** in the console. That means no localStorage, cookies or fetch to third parties. The only exception is SheetJS, until it's bundled.
7. **Escape every value from a report** before it goes into HTML. Keep the order in `tplHtml`: formatting first, then placeholders.
8. **Work on a branch and open a pull request.** Never push to `main`. A person reviews and merges.
9. **Every PR updates `CHANGELOG.md`**, and also updates `docs/business-rules.md` / `docs/data-model.md` if rules or data handling changed.
10. **Don't edit `archive/`.** It holds the original tools as a reference.

## Style

- **Code:** plain JavaScript in the single file. No frameworks or build step. Match the existing banner-comment sections.
- **Docs:** plain English for non-technical readers (PRP, EAs). Short sentences. Facts from the code, not guesses. Mark anything unconfirmed **☐ Confirm** with an owner.
- **Commit and PR titles:** `vX.Y: what changed` for releases, `area: what changed` otherwise.

## Agents in this repo

| Agent | Use it for |
|---|---|
| `builder` | Implementing an approved backlog item |
| `qa-reviewer` | Reviewing a branch or PR: tests, safety rules, rule compliance |
| `docs-keeper` | Keeping docs, the changelog and the decision copy in step with the code |
| `mip-meeting-intake` (Cowork skill) | Turning a meeting transcript into backlog items and approval drafts, recording approvals, then implementing approved items |

The backlog is in `docs/backlog.md` until it moves to GitHub Issues. Meeting records are in `docs/meetings/`. Every behaviour change should trace back to a meeting record or decision, plus an approval.
