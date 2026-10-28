# Hosting and security record

**Status: DRAFT. Not decided.** · **Last updated:** 1 Oct 2026 · **Owner:** Nelson Mercado (AICOE)

This records the facts that InfoSec, Privacy and Platform Engineering need for a hosting decision. Fill in the **Decision** fields as they're made.

## 1. What the tool is, technically

| Item | Today (v2.2) |
|---|---|
| Form | One static HTML file (≈970 KB) plus a static admin page. No server-side code. |
| Where data is processed | **Only in the user's browser.** Uploaded files are read in memory. |
| Storage | **None.** The console uses no localStorage, cookies or IndexedDB. The admin page keeps only template wording in localStorage. |
| Network calls | One: the SheetJS library from `cdnjs.cloudflare.com`. No data is sent anywhere. |
| Outputs | Files the user downloads: .eml, .xlsx, .zip. Clipboard copies. |
| Identity | None. Anyone with the file can use every tab. |
| Code | `nmercadoWiley/mip-drafts-console` (private, personal account). It needs to move to the `wiley` org. |

## 2. Data handled

| Data | Source | Contains personal data |
|---|---|---|
| MIP Summary Report / paginated report | Power BI (Luke Barrett's team) | Author names and emails, editor names and emails, EA names |
| Activity Tracker | Power BI | Minimal (dates per manuscript) |
| Reviewer Performance Report | Power BI | Reviewer names and emails |
| Full Manuscript Listing | Power BI | Editor and author names |
| Embedded screenshots in the tool | Built by the SME | **Removed 15 Oct 2026** and replaced with text instructions (backlog B2) |

Users: about 100 vendor EAs across 3 vendor partners, who **can't see each other's journals**, plus internal PRPLs and PRP management.

## 3. Hosting options

| Option | How updates reach users | Access control | Fit |
|---|---|---|---|
| **A. Keep as a downloaded file** (today) | They don't, until users get a new copy | Whoever holds the file | Pilot only |
| **B. GitHub Pages, private** | Every commit | GitHub org membership. **Vendor EAs would need org accounts.** | Only if private Pages is enabled for the `wiley` org |
| **C. Partybus, Private (Wiley network)** | Every commit, about 10 minutes (ArgoCD) | Wiley network only | Internal users (PRPLs) first |
| **D. Partybus, Public + Istio SSO** | Every commit | Wiley Entra sign-in in front of the site | **Likely target**, if vendor EAs have Entra accounts or guest access |

**On Partybus:**
- The tool would be a *container + Dockerfile* app (unprivileged nginx serving the static files, `/health` route, smallest size), with no infrastructure dependencies.
- There would be a prod approval gate.
- **Prerequisites:** the repo in the `wiley` org, and an AICOE (or Research Publishing) Partybus **System**.
- See the Partybus "Onboard an app" guide.

**Decision:** ☐ Option ___ · Decided by ___ · Date ___

## 4. Security and privacy questions to close

| # | Question | Owner | Answer |
|---|---|---|---|
| S1 | Do vendor EAs have Wiley Entra accounts or guest access? | IT / vendor management | |
| S2 | Is a public URL behind SSO acceptable, given that processing is browser-only and nothing is stored? | InfoSec | |
| S3 | Do the vendor agreements cover EAs handling these exports and the downloaded outputs? | Legal / vendor management | |
| S4 | What's the retention rule for downloaded drafts, workbooks and audit exports on EA laptops? | Privacy | |
| S5 | What review is required for AI-generated code before hosting? | InfoSec / AICOE | |
| S6 | Bundle SheetJS instead of loading it from a CDN (licence Apache-2.0) | AICOE | Planned |
| S7 | Remove the 3 embedded screenshots | AICOE | **Done** 15 Oct 2026 |
| S8 | Should tabs be restricted by role (e.g. Editor Performance for PRPLs only)? | PRP | |
| S9 | Live data: an Entra app registration (SPA, delegated Power BI read) and row-level security on the model (dependency D3). Plan: `docs/power-bi-live-data-plan.md`. | Luke Barrett's team / IT | Planned (B20) |
| S10 | Sent and replied tracking later: Microsoft Graph `Mail.ReadWrite`, and `Mail.Read.Shared` for shared inboxes. Freshdesk journals aren't covered. | IT | Future |

## 5. Operations once hosted

| Item | Partybus provides | Still needs an owner |
|---|---|---|
| Monitoring and alerts | Observability tab (events, pods, logs) | Who responds if it's down on a send day |
| Releases | CI/CD with a uat/prod approval gate | Who approves (see the RACI on Confluence) |
| Rollback | One click on the Deployments tab | — |
| Support | — | **Day-to-day support owner. Not named.** |
