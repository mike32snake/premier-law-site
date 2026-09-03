# PROJECT_STATE — Premier Law (premier.law)

_Last updated: 2026-09-03_

## What this is
Derek Carrillo's business-law site: telecommunications and real estate.
Estate planning moved to pep.law; `estate-planning.html` redirects there.

## One repo, one site
`mike32snake/premier-law-site` -> **https://premier.law**

The `CNAME` file in this repo owns the domain. `www.premier.law` resolves too,
GitHub redirects it to the apex. `https://mike32snake.github.io/premier-law-site/`
301s to premier.law, so there is no duplicate copy to keep in sync.

DNS is at GoDaddy (`ns75/ns76.domaincontrol.com`): apex A records point at
GitHub's Pages IPs `185.199.108-111.153`, and `www` is a CNAME to
`loki-mamv.github.io`. That www record is stale but harmless, GitHub routes by
Host header, not by the CNAME target. Repoint it to `mike32snake.github.io`
whenever someone is in GoDaddy anyway.

### Retired 2026-08-23, do not use
- `loki-mamv/premier-law-site` — a fork of this repo that held the domain from
  Feb to Aug 2026. Archived, Pages deleted, everything merged back here first.
- `mike32snake/premier-law-preview` — Derek's review copy for the Aug nav
  restructure. Approved and shipped. Archived, Pages deleted.

Both carry a `RETIRED.md` explaining the move.

## Editing the site
```
cd "/Users/mmaseda/Desktop/Derek Websites/Premier Law"
python3 tools/build.py
git add -A && git commit && git push origin main
gh api repos/mike32snake/premier-law-site/pages/builds/latest --jq '.status'
```

`tools/build.py` is the generator. It rewrites the nav, mobile menu, and footer
on the six hand-written pages (`index`, `telecommunications`, `real-estate`,
`about`, `contact`, `privacy-policy`) and regenerates the ten subpages from the
content dicts inside it. Copy for those subpages lives in the script, not in the
HTML: edit there or the next build overwrites you. It is idempotent, and it
bumps the stylesheet cache-buster to the build date on every run.

Hand-edit only the six pages above, and only outside the nav/menu/footer blocks.

**about.html is pinned to its 2026-08-04 version (commit 47b9d90) as of
2026-09-03.** Mike asked to revert it after the Aug 23 changes. It has the
flat nav (no dropdowns, no Resources link), the Title Insights section, the
short disclaimer, and "J.D., Accredited Law School". Running `tools/build.py`
will rewrite its nav and footer and move Title Insights to purchase-sale.html
again. Do not run the build until Mike says which about.html he wants long
term; if you must build, run `git checkout HEAD -- about.html` afterwards.

Commit author must be `mike32snake <mike32snake@users.noreply.github.com>`.
A hook blocks `mike@genhealth.ai` on these repos.

## Site structure
- Telecommunications -> MDU & Broadband, Wireless Infrastructure
- Real Estate -> Purchase & Sale, Leases, Landlord Rep & Evictions, Land Trusts,
  Surplus Funds
- Resources hub + 2 articles (bulk agreements, surplus funds)
- About, Contact, Privacy Policy

Contact form posts to FormSubmit -> info@premier.law. Name, phone, email,
practice area, message, and the Important Notice checkbox are all required;
`main.js` validates them and `?submitted=true` shows the success state.

## Open items for Derek
- Title Insights URL, to hyperlink the name on real-estate and purchase-sale.
- Fact-check the drafted subpages: MDU bulk/retail/access, wireless, surplus funds.
- 4 Resources cards are "coming soon" placeholders with no target.
- About and the home trust bar say "11+ Years"; pep.law says 12.
