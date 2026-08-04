# PROJECT_STATE — Premier Law (premier.law redesign)

_Last updated: 2026-08-04_

## What this is
Derek Carrillo's business-law site (telecom + real estate). Repo: `mike32snake/premier-law-site`,
deployed to https://mike32snake.github.io/premier-law-site/. NOTE: the live premier.law domain is
served by a DIFFERENT GitHub Pages repo (not under mike32snake or mikeGenhealth; last modified
May 17, 2026, still shows old estate-planning content). Whoever launched the original site controls
that DNS/repo. Going live means either pointing premier.law DNS at this repo (add CNAME file) or
getting access to the old repo.

## 2026-08-04 session — Derek's edits (deployed, commit 47b9d90)
- Attorneys Key Title → **Title Insights** everywhere (About "Trusted Title Partner" section,
  real-estate page, FAQ schema, meta). No hyperlink yet — Derek owes us the URL.
- Removed "HOA and condo board telecom policy drafting and governance" bullet (telecom page).
- Removed the Title-services sentence from the home real-estate card.
- "Founder & CEO" → Principal Attorney (labels, JSON-LD, alt text).
- Bar admissions each on their own line (About credentials).
- Removed em-dashes from copy; justified all copy blocks (see "JUSTIFIED COPY" block at end of styles.css).
- estate-planning.html now redirects to https://pep.law (estate planning lives on PEP).
- styles.css cache-buster bumped to ?v=20260804.

## Preview site (nav restructure for Derek's approval)
- Dir: `/Users/mmaseda/Desktop/Derek Websites/Premier Law Preview`
- Repo: `mike32snake/premier-law-preview` → https://mike32snake.github.io/premier-law-preview/
- Built by `build_preview.py` (idempotent; edit content dicts there, re-run, commit).
- Nav dropdowns: Telecom → MDU & Broadband / Wireless Infrastructure; Real Estate → Purchase & Sale,
  Leases, Landlord Rep & Evictions, Land Trusts, Surplus Funds. Plus Resources hub + 2 articles.
- Title Insights section moved from About → purchase-sale.html (per Derek's transcript).
- All pages noindex + PREVIEW badge.
- Custom domain preview.premier.law NOT enabled yet — do not add the CNAME until DNS exists, or the
  github.io URL breaks. When Derek adds DNS record `preview CNAME mike32snake.github.io.`, run:
  `gh api repos/mike32snake/premier-law-preview/pages -X PUT -f cname=preview.premier.law`
  and commit a CNAME file containing `preview.premier.law`.

## Open items
- Title Insights URL from Derek → hyperlink the name on about/real-estate/purchase-sale.
- Derek to fact-check drafted subpage content (MDU bulk/retail/access, wireless, surplus funds).
- 4 resources cards are "coming soon" placeholders; write articles if Derek approves the format.
- About page still says "11+ Years" (PEP now says 12) — confirm with Derek.
- Once preview approved: merge preview structure into premier-law-site and sort out the premier.law DNS/repo.

## Deploy
gh auth switch --user mike32snake; git push origin main; poll pages/builds/latest.
