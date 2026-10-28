# Plan: load data straight from Power BI

**Status:** proposed, 20 Oct 2026. Nothing is built yet. **Owner:** Nelson.
**Backlog:** B20 (prerequisites), B21 (build). **Decisions:** LD-1, LD-2 in `docs/open-decisions.md`.

## The idea

Users stop exporting the MIP Summary Report and uploading it. Instead, the console has a **Load from Power BI** button. It fetches the same data, as the signed-in user, and everything after that works as it does today.

## How it works

1. The user opens the hosted console and signs in with Wiley SSO, as now.
2. The page asks Microsoft for a Power BI token **for that same user**. It uses MSAL, Microsoft's sign-in library for web pages.
3. The page sends one query (DAX) to the Power BI REST API ("Execute Queries") against the semantic model behind the MIP Summary Report.
4. The rows come back in the same columns as the export. Routing, drafts and workbooks don't change.

**Why "as the signed-in user":** each person gets only the data they can already see in Power BI. The model's row-level security still applies, so vendor EAs can't see each other's journals. No service account is needed, and no data is stored on a server.

**What stays the same:**

- Processing stays in the browser, and nothing is stored.
- **Upload stays** as a fallback, and for anyone opening the file directly.

## What changes

| Area | Today | After |
|---|---|---|
| CLAUDE.md hard rule 6 | No network calls | Calls allowed **only** to Microsoft sign-in and `api.powerbi.com`, and **only** on the hosted copy. Needs decision LD-1. |
| Security policy (`nginx/security-headers.inc`) | `connect-src 'none'` | `connect-src https://login.microsoftonline.com https://api.powerbi.com` |
| Libraries | SheetJS only | Adds MSAL (Microsoft), pinned to one version. Ideally bundled, as in B1. |
| Data handling docs | Data comes from an uploaded file | Data may also come from Power BI under the user's own permissions. Update `data-model.md` and `hosting-and-security.md` (S9). |

## What we know (20 Oct 2026)

- **Report:** MIP Summary Report, report ID `6ad4f746-165d-4092-b890-cce4018d7507` (the link in the console's Step 01).
- **Semantic model:** *Manuscripts in Process*, in the workspace *Data and Publishing Insights*. Owner: Xige Huang. **Dataset ID:** `fd19bc42-455e-4f8a-ad79-2d68dfd37562`. Workspace ID: ☐ (the OneLake page opens from "me", so it doesn't show; Xige can confirm it, or the API's Get Dataset call returns it).
- **Refresh:** daily, around 05:00.
- **API tests (20 Oct 2026, Nelson's account, Microsoft "Try It"):** Get Report returns 200 (a normal `PowerBIReport` on dataset `fd19bc42-…`). Get Dataset and Execute Queries both return 404 (`ItemNotFound` / `PowerBIEntityNotFound`). So the API works, but access to the dataset comes only through the report. Build permission (P3) is the blocker.
- **Access:** Nelson can view the model but has no Build permission. The API query needs Build, so every user of the feature needs it, ideally through a security group.
- **Report owners' guidance:** the report says not to use Export or Subscribe, and to use "Export data" on the table instead. Querying through the API is a new use, so the owner should agree to it.
- **The model has helper tables** (Stage Definitions, Health Check Order, Journal Buckets, Journal Contacts and others). The DAX query should reproduce the report's main table, not read raw tables.

## Prerequisites (B20)

| # | Needed | From | Status |
|---|---|---|---|
| P1 | Which **workspace and semantic model** (dataset) the MIP Summary Report uses, and their IDs | Power BI owners (Luke Barrett's team) | Names and dataset ID found (above). Workspace ID ☐ |
| P2 | Whether **row-level security** limits each EA and PRPL to their own journals. How is the vendor → journal mapping applied? (ties to D3) | Power BI owners | ☐ |
| P3 | **Build permission** on the model for PRPLs and EAs (Nelson currently has view only), ideally through a security group | Model owner (Xige Huang) | ☐ |
| P4 | A **DAX query** that returns the same columns as today's export. Drafted with the Power BI owners and tested in DAX Studio or Power BI Desktop. | Power BI owners + Nelson | ☐ |
| P5 | An **Entra app registration** of type single-page app, with the redirect URI of the hosted console, the delegated Power BI permission `Dataset.Read.All`, and admin consent | IT / Entra admins | ☐ |
| P6 | The tenant setting that allows the "Execute Queries" REST API on this model | Power BI admins | ☐ |
| P7 | Approval of decision **LD-1** (network rule change) and **LD-2** (upload stays) | Iris; InfoSec review | ☐ |

## Known limits

- The query API returns at most about **100,000 rows** per call. A portfolio export is far smaller.
- Data is only as fresh as the model's **refresh schedule**, often daily. Emails should keep their "data may be up to X hours old" line.
- Each user needs a Power BI licence or access that allows querying the model. ☐ Confirm with P3.

## Build (B21, after B20 and LD-1)

On a `feature/power-bi-load` branch:

1. MSAL sign-in, reusing the session the user already has, so no second login in most cases.
2. Run the DAX query, then map the result columns to the export's column names.
3. A **Load from Power BI** button in Step 01, keeping upload as it is.
4. Clear errors for "no access", "no data" and "token expired".
5. Tests: a synthetic API response in `tests/fixtures/` must produce the same drafts as the matching synthetic export.
6. Update the security policy, the docs and the CHANGELOG.

## Draft messages

### To the Power BI owners (P1–P4, P6)

> Hi Xige (cc Luke),
>
> The MIP Drafts Console is now hosted on Partybus with Wiley SSO. We'd like it to read the **MIP Summary Report** data straight from Power BI, so PRPLs and EAs no longer export and upload it. It would query as the **signed-in user**, so they only see what they can already see in Power BI.
>
> It would query your **Manuscripts in Process** semantic model (Data and Publishing Insights). Before we build anything, I'd like to check you're happy with that, given the report's guidance on exports. Could you help with:
>
> 1. Are you OK with the console querying the model through the REST API ("Execute Queries"), read-only, as the signed-in user?
> 2. Is there **row-level security** that limits EAs and PRPLs to their own journals? How is the vendor → journal mapping applied?
> 3. The API needs **Build permission** on the model. Could PRPLs and EAs get it through a security group? I currently have view only.
> 4. Could someone help write a **DAX query** that returns the same columns as the export?
> 5. Is the "Execute Queries" REST API enabled in the tenant for this workspace?
>
> Happy to walk through it in 20 minutes.
>
> Thanks,
> Nelson

### To IT / Entra admins (P5)

> Hi,
>
> Could you create an **Entra app registration** for the MIP Drafts Console (Partybus app `mip-drafts-console-ea`, AppCat APP-12859)?
>
> - **Type:** single-page application (SPA)
> - **Redirect URI:** `https://mip-drafts-console-ea.dev.private.partybus.wiley.tools/` (prod URL to follow)
> - **API permission:** Power BI Service, delegated `Dataset.Read.All`, with admin consent
> - **Purpose:** the page reads Power BI data as the signed-in user. There's no client secret and no server-side access.
>
> Thanks,
> Nelson

### Approval request to Iris (P7)

> Hi Iris,
>
> We'd like the console to load the MIP report straight from Power BI instead of users exporting and uploading it each time. It would only fetch data the user can already see in Power BI, it would keep processing in the browser, and it would store nothing. Upload stays as a fallback.
>
> This changes one of the tool's rules ("no network calls"), so I need your approval for:
>
> - **LD-1:** allow the hosted console to call only Microsoft sign-in and the Power BI API.
> - **LD-2:** keep file upload as a fallback.
>
> InfoSec will review it before it goes live. OK to proceed?
>
> Thanks,
> Nelson
