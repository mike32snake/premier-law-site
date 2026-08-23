# PROJECT_STATE — Premier Law (premier.law)

_Last updated: 2026-08-23_

## What this is
Derek Carrillo's business-law site (telecom + real estate). Estate planning moved to pep.law.

## THREE repos, and which one the public sees

| Repo | URL | Role |
|---|---|---|
| `loki-mamv/premier-law-site` | **https://premier.law** (CNAME in repo) | **THE LIVE PUBLIC SITE.** Push here or the public sees nothing. |
| `mike32snake/premier-law-site` | https://mike32snake.github.io/premier-law-site/ | Staging mirror. Same content. |
| `mike32snake/premier-law-preview` | https://mike32snake.github.io/premier-law-preview/ | Derek's review copy. noindex + PREVIEW badge. |

`www.premier.law` CNAMEs to `loki-mamv.github.io`. Use `gh auth token --user loki-mamv` to push there.

## Source of truth: the preview repo
All three now carry identical content. Edit in
`/Users/mmaseda/Desktop/Derek Websites/Premier Law Preview`, then:

```
cd "/Users/mmaseda/Desktop/Derek Websites/Premier Law Preview"
python3 build_preview.py                    # regenerate the preview
python3 promote_to_live.py                  # -> ../Premier Law  (mike32snake)
python3 promote_to_live.py <loki-checkout>  # -> premier.law
```

`promote_to_live.py` strips the preview-only artifacts (noindex meta, PREVIEW
badge CSS, `?v=preview1`) and bumps the stylesheet cache-buster to today's date.
It keeps the intentional noindex on `estate-planning.html` and
`privacy-policy.html`, and never touches the live repo's `CNAME`.

## 2026-08-23 session
Promoted the approved preview to both live repos, plus Derek's new notes:
- Home: hero scroll indicator removed; practice cards 3 -> 2 columns, centered,
  card links pinned to the bottom so they align.
- Purchase & Sale: no "What is Title Insights?" question in the FAQ (the Title
  Insights section above it stays). Matching FAQPage JSON-LD entry removed from
  real-estate.html so structured data matches the visible FAQ.
- About: keeps the real education credential and every prior edit.

Also merged in the edits that only existed on the loki-mamv fork and would
otherwise have been lost: favicons, privacy-policy.html, the four-paragraph
footer legal disclaimer, the FormSubmit contact form (required phone, practice
area, and Important Notice checkbox), "First Contact" / "Initial Consultation*"
copy, Barry University education, 11+ years, no EV charging, no photo on the
home about teaser.

## Open items
- Title Insights URL from Derek, to hyperlink the name on real-estate and purchase-sale.
- Derek to fact-check the drafted subpages (MDU bulk/retail/access, wireless, surplus funds).
- 4 Resources cards are "coming soon" placeholders.
- About says "11+ Years"; PEP says 12. Confirm with Derek.
- `preview.premier.law` DNS does not exist. `build_preview.py` no longer writes a
  CNAME. When Derek adds `preview CNAME mike32snake.github.io.`, run
  `gh api repos/mike32snake/premier-law-preview/pages -X PUT -f cname=preview.premier.law`
  and commit a CNAME file.

## Deploy
```
gh auth switch --user mike32snake
git -C "/Users/mmaseda/Desktop/Derek Websites/Premier Law Preview" push origin main
git -C "/Users/mmaseda/Desktop/Derek Websites/Premier Law" push origin main
# premier.law:
GH_TOKEN=$(gh auth token --user loki-mamv) git -C <loki-checkout> push origin main
gh api repos/<owner>/premier-law-site/pages/builds/latest --jq '.status'
```
Commit author must be `mike32snake <mike32snake@users.noreply.github.com>`; a
hook blocks `mike@genhealth.ai` on these repos.
