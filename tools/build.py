#!/usr/bin/env python3
"""Build the premier.law site: nav, footers, and the practice subpages.

Run from anywhere:  python3 tools/build.py

Idempotent. It rewrites the nav, mobile menu, and footer on the six hand-written
pages, and regenerates the ten subpages from the content dicts below. Edit the
content here, re-run, commit, push. GitHub Pages deploys from main.
"""
import re, sys, os, datetime

CACHE = datetime.date.today().strftime('%Y%m%d')

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
CARET = '<svg class="nav-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'

TELECOM_SUBS = [
    ('mdu-broadband.html', 'MDU &amp; Broadband Transactions'),
    ('wireless-infrastructure.html', 'Wireless Infrastructure Transactions'),
]
RE_SUBS = [
    ('purchase-sale.html', 'Purchase &amp; Sale Transactions'),
    ('leases.html', 'Commercial &amp; Residential Leases'),
    ('landlord-evictions.html', 'Landlord Representation &amp; Evictions'),
    ('land-trusts.html', 'Land Trusts'),
    ('surplus-funds.html', 'Surplus Funds Recovery'),
]

def nav_html(active):
    """active: index | telecom | realestate | resources | about | contact
    or a subpage filename (marks its parent group active)."""
    def cls(key):
        return ' class="active"' if active == key else ''
    tel_active = active in ('telecom',) or active in [f for f, _ in TELECOM_SUBS]
    re_active = active in ('realestate',) or active in [f for f, _ in RE_SUBS]
    tel_dd = '\n'.join(f'          <a href="{f}"{" class=" + chr(34) + "active" + chr(34) if active == f else ""}>{label}</a>' for f, label in TELECOM_SUBS)
    re_dd = '\n'.join(f'          <a href="{f}"{" class=" + chr(34) + "active" + chr(34) if active == f else ""}>{label}</a>' for f, label in RE_SUBS)
    return f'''<nav class="nav-links" aria-label="Main navigation">
      <a href="index.html"{cls('index')}>Home</a>
      <div class="nav-item">
        <a href="telecommunications.html"{' class="active"' if tel_active else ''}>Telecommunications{CARET}</a>
        <div class="nav-dropdown">
{tel_dd}
        </div>
      </div>
      <div class="nav-item">
        <a href="real-estate.html"{' class="active"' if re_active else ''}>Real Estate{CARET}</a>
        <div class="nav-dropdown">
{re_dd}
        </div>
      </div>
      <a href="resources.html"{cls('resources')}>Resources</a>
      <a href="about.html"{cls('about')}>About</a>
      <a href="contact.html"{cls('contact')}>Contact</a>
    </nav>'''

MOBILE_MENU = '''<div class="mobile-menu" id="mobileMenu" aria-hidden="true">
  <a href="index.html">Home</a>
  <a href="telecommunications.html">Telecommunications</a>
  <a href="mdu-broadband.html" class="mobile-sub">MDU &amp; Broadband Transactions</a>
  <a href="wireless-infrastructure.html" class="mobile-sub">Wireless Infrastructure Transactions</a>
  <a href="real-estate.html">Real Estate</a>
  <a href="purchase-sale.html" class="mobile-sub">Purchase &amp; Sale Transactions</a>
  <a href="leases.html" class="mobile-sub">Commercial &amp; Residential Leases</a>
  <a href="landlord-evictions.html" class="mobile-sub">Landlord Representation &amp; Evictions</a>
  <a href="land-trusts.html" class="mobile-sub">Land Trusts</a>
  <a href="surplus-funds.html" class="mobile-sub">Surplus Funds Recovery</a>
  <a href="resources.html">Resources</a>
  <a href="about.html">About</a>
  <a href="contact.html">Contact</a>
  <a href="tel:8133300697" class="mobile-phone">813.330.0697</a>
  <a href="contact.html" class="btn btn-primary" style="margin-top: 8px;">Schedule a Consultation</a>
</div>'''

HEADER_TMPL = '''<header class="header" id="header">
  <div class="header-inner">
    <a href="index.html" class="header-logo" aria-label="Premier Law Home">
      <img src="assets/premier-law-lockup-white.png" alt="Premier Law" width="140" height="48" class="logo-white"><img src="assets/premier-law-lockup-dark.png" alt="Premier Law" width="140" height="48" class="logo-dark">
    </a>
    {NAV}
    <div class="header-cta">
      <a href="tel:8133300697" class="header-phone" aria-label="Call 813-330-0697">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        813.330.0697
      </a>
      <a href="contact.html" class="btn btn-primary">Consultation</a>
    </div>
    <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
</header>'''

FAVICON_LINKS = '''<link rel="icon" type="image/x-icon" href="assets/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
'''

FOOTER = '''<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="assets/premier-law-lockup-white.png" alt="Premier Law" width="130" height="44" loading="lazy">
        <p>A boutique Tampa law firm delivering strategic legal counsel in real estate and telecommunications. More than $1 billion in closed transactions.</p>
      </div>
      <div class="footer-col">
        <h4>Practice Areas</h4>
        <a href="telecommunications.html">Telecommunications</a>
        <a href="real-estate.html">Real Estate</a>
      </div>
      <div class="footer-col">
        <h4>Quick Links</h4>
        <a href="index.html">Home</a>
        <a href="resources.html">Resources</a>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
        <a href="privacy-policy.html">Privacy Policy</a>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <a href="tel:8133300697">813.330.0697</a>
        <a href="mailto:info@premier.law">info@premier.law</a>
        <a href="https://premier.law" target="_blank" rel="noopener">premier.law</a>
        <a>Tampa, Florida</a>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2026 Premier Law. All rights reserved.</p>
      <p>Tampa, Florida</p>
    </div>

    <div class="footer-disclaimer">
      <p class="footer-disclaimer-title">Legal Disclaimer</p>
      <p>The hiring of a lawyer is an important decision and should not be based solely on advertisements. Before you decide, you may request free written information about our attorneys&rsquo; qualifications and experience.</p>
      <p>This website is provided for informational purposes only and does not constitute legal advice. The information here is not a substitute for consulting with an attorney and does not create an attorney-client relationship. You should always seek professional legal counsel for advice regarding your specific situation.</p>
      <p>Because laws change frequently and some content relies on external sources, we do not warrant or guarantee the accuracy, completeness, or availability of the information provided on this site or any linked third-party websites. Links to other sites are offered solely as a convenience and do not imply endorsement.</p>
      <p>You should never delay seeking legal advice, disregard professional guidance, or start or stop any legal action based solely on information from this website. Always consult a qualified attorney for advice tailored to your circumstances.</p>
    </div>
  </div>
</footer>'''

CTA_BAND = '''<section class="cta-band">
  <div class="container">
    <div class="cta-band-content reveal">
      <h2>{cta_h}</h2>
      <p>{cta_p}</p>
      <a href="contact.html" class="btn btn-primary">Schedule a Consultation</a>
    </div>
  </div>
</section>'''

PAGE_TMPL = '''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/x-icon" href="assets/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={cache}">
<noscript><style>.reveal {{ opacity: 1; transform: none; }}</style></noscript>
</head>

<body>
<script>document.documentElement.classList.remove('no-js');</script>

{header}

{mobile}

<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a>
      <span class="sep">/</span>
      {crumb_mid}<span class="current">{crumb}</span>
    </nav>
    <h1>{h1}</h1>
    <p class="hero-subtitle">{subtitle}</p>
  </div>
</section>

{body}

{cta}

{footer}

<script src="main.js"></script>
</body>
</html>
'''

def svc_list(title, items, light=True):
    variant = 'light' if light else 'dark'
    rows = '\n'.join(
        f'''          <div class="service-item">
            {CHECK}
            <span class="service-item--{variant}">{it}</span>
          </div>''' for it in items)
    return f'''        <div class="services-list services-list--{variant}">
          <h4>{title}</h4>
{rows}
        </div>'''

def faq_section(heading, faqs):
    items = '\n'.join(f'''
      <div class="faq-item">
        <button class="faq-question" aria-expanded="false">
          {q}
          <svg class="faq-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        </button>
        <div class="faq-answer" aria-hidden="true">
          <div class="faq-answer-inner">{a}</div>
        </div>
      </div>''' for q, a in faqs)
    return f'''<section class="faq-section">
  <div class="container">
    <h2 class="section-heading reveal">{heading}</h2>
    <div class="faq-list reveal reveal-delay-1">
{items}

    </div>
  </div>
</section>'''

def dark_section(h2, paras, label=None, extra=''):
    ps = '\n'.join(f'      <p>{p}</p>' for p in paras)
    lbl = f'      <p class="section-label">{label}</p>\n' if label else ''
    return f'''<section class="content-section content-section--dark">
  <div class="container">
    <div class="content-text content-text--dark reveal">
{lbl}      <h2>{h2}</h2>
{ps}
    </div>
{extra}
  </div>
</section>'''

def light_section(h2, paras, label=None, extra=''):
    ps = '\n'.join(f'      <p>{p}</p>' for p in paras)
    lbl = f'      <p class="section-label" style="color: var(--crimson);">{label}</p>\n' if label else ''
    return f'''<section class="content-section content-section--light">
  <div class="container">
    <div class="content-text content-text--light reveal">
{lbl}      <h2>{h2}</h2>
{ps}
    </div>
{extra}
  </div>
</section>'''

def grid_wrap(inner_left, inner_right):
    return f'''    <div class="content-grid reveal reveal-delay-1" style="margin-top: 32px;">
      <div>
{inner_left}
      </div>
      <div>
{inner_right}
      </div>
    </div>'''

def feature_box(icon_kind, h4, text, light=True):
    txt_cls = 'feature-box-text--light' if light else 'feature-box-text--dark'
    icon = 'feature-icon--crimson' if light else 'feature-icon--gold'
    return f'''        <div class="detail-feature-box" style="margin-bottom: 24px;">
          <div class="feature-icon {icon}">
            {icon_kind}
          </div>
          <h4>{h4}</h4>
          <p class="{txt_cls}">{text}</p>
        </div>'''

ICO_USERS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
ICO_DOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
ICO_LAYERS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>'
ICO_KEY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>'
ICO_TREND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'


# ============================================================
# PAGE CONTENT
# ============================================================

PAGES = {}

# ---------- TELECOM: MDU & BROADBAND ----------
PAGES['mdu-broadband.html'] = dict(
    title='MDU &amp; Broadband Transactions | Telecommunications | Premier Law',
    desc='Florida attorney for MDU broadband transactions: bulk agreements, retail marketing agreements (exclusive and non-exclusive), and access-only agreements for communities and property owners.',
    parent=('telecommunications.html', 'Telecommunications'),
    crumb='MDU &amp; Broadband Transactions',
    h1='MDU &amp; Broadband Transactions',
    subtitle='Bulk, retail, and access agreements for multifamily properties and community associations. The core of our telecom practice, with $1B+ in closed deals.',
    cta_h='Reviewing a Provider Agreement?',
    cta_p='Send us the draft before you sign. We will tell you what is missing and what it is worth.',
    body_fn=lambda: '\n\n'.join([
        dark_section(
            'Broadband Deals for Multifamily Properties and Communities',
            [
                'A multi-dwelling unit (MDU) is any property where multiple households share one building or community: apartment complexes, condominiums, HOA neighborhoods, and mixed-use developments. When a broadband or cable provider wants to serve an MDU, the terms of that relationship are set by contract, and those contracts decide who controls the infrastructure, who gets paid, and what residents pay for service.',
                'Premier Law represents MDU owners, developers, community associations, and property management companies in these negotiations. Provider agreements come in three basic shapes: bulk agreements, retail agreements, and access-only agreements. Which structure fits depends on your property, your residents, and your goals, and the differences between them are worth real money.',
            ],
        ),
        light_section(
            'Bulk Agreements',
            [
                'In a bulk agreement, the property or association purchases broadband (and sometimes video) service for every unit at a deeply discounted wholesale rate, and the cost is built into rent or assessments. Residents get service at a fraction of the retail price, the provider gets guaranteed penetration, and the property gets a marketable amenity and often a revenue share.',
                'Bulk deals are long-term commitments, commonly five to ten years, so the details carry: rate escalators, service-level commitments, technology refresh obligations, transfer rights when the property sells, and what happens at renewal. We negotiate each of these terms so the deal still looks good in year eight, not just at signing.',
            ],
            label='Structure One',
            extra=grid_wrap(
                svc_list('What We Negotiate in Bulk Deals', [
                    'Wholesale per-unit rates and multi-year escalator caps',
                    'Service levels, outage credits, and support commitments',
                    'Technology refresh and upgrade obligations over the term',
                    'Door fees, revenue sharing, and construction contributions',
                    'Assignment and transfer rights on a sale of the property',
                    'Renewal, expiration, and end-of-term transition planning',
                ], light=True),
                feature_box(ICO_USERS, 'Community Association Experience',
                    'We work extensively with HOA and condo boards. Community associations (the umbrella term for HOAs, condominium associations, and cooperatives) face governance requirements, budgeting rules, and disclosure obligations that shape how a bulk deal must be structured. We handle both the provider negotiation and the association-side mechanics.', light=True)
                + feature_box(ICO_TREND, 'Leverage You May Not Know You Have',
                    'Providers compete hard for MDU penetration. Communities that bid their contract competitively, rather than renewing by default, routinely improve rates, service levels, and compensation.', light=True),
            ),
        ),
        dark_section(
            'Retail Agreements',
            [
                'In a retail structure, the provider sells directly to your residents at its retail rates, and your agreement with the provider governs what the provider gets in exchange for compensation to the property. Retail agreements generally take one of three forms, and knowing which one you are signing matters.',
            ],
            label='Structure Two',
            extra=grid_wrap(
                feature_box(ICO_DOC, 'Exclusive Marketing Agreements',
                    'The provider pays for the exclusive right to market its services to your residents: move-in packets, onsite events, community channels. Exclusivity applies to marketing only. Under FCC rules, providers cannot lock competitors out of serving residents, but exclusive marketing rights still command real compensation.', light=False)
                + feature_box(ICO_LAYERS, 'Non-Exclusive Marketing Agreements',
                    'Multiple providers may market on the property, each under its own agreement. Compensation per provider is lower than in an exclusive deal, but residents get choice and the property keeps future flexibility. Often the right fit for larger communities.', light=False),
                feature_box(ICO_KEY, 'Access-Only Agreements',
                    'The narrowest form: the provider receives the right to enter the property, install facilities, and serve residents who sign up, with no marketing rights at all. Even here, the terms matter: insurance, indemnification, damage repair, equipment removal at termination, and whether the provider pays for the access it receives.', light=False)
                + feature_box(ICO_TREND, 'Choosing the Right Structure',
                    'Bulk, exclusive marketing, non-exclusive marketing, or access-only: each trades control, revenue, and resident experience differently. We model the options for your specific property before you commit to one.', light=False),
            ),
        ),
        faq_section('MDU &amp; Broadband Questions', [
            ('What is the difference between a bulk agreement and a retail agreement?',
             'In a bulk agreement, the property or association buys service for all units at a wholesale rate and residents receive it as an amenity. In a retail agreement, the provider sells directly to residents at retail rates and the property is compensated for marketing rights or access. Bulk deals deliver lower per-unit pricing and stronger amenity value; retail deals preserve resident choice and involve less financial commitment by the association.'),
            ('What is an access-only agreement?',
             'An access-only agreement gives a provider the right to enter the property and install the facilities needed to serve residents who choose to subscribe, without any marketing rights. It is the minimum agreement a provider needs to lawfully operate on private property, and it should still address insurance, indemnification, construction standards, damage repair, and removal of equipment when the agreement ends.'),
            ('Can a provider get exclusive rights to serve our community?',
             'Not to serve it. FCC rules prohibit agreements that give one provider the exclusive right to provide service to an MDU. What can be sold is exclusive marketing: the sole right to promote services to residents through the property’s channels. That distinction is frequently misunderstood, and it changes what an exclusivity clause is actually worth.'),
            ('Is HOA and condo work different from apartment MDU work?',
             'The provider side looks similar, but community associations answer to boards, budgets, governing documents, and statutory requirements that apartment owners do not. A bulk assessment has to fit the association’s budgeting and disclosure process, and board approval has to be documented properly. We handle both sides of that equation.'),
            ('Our contract auto-renews soon. Is it too late to negotiate?',
             'Usually not, but timing matters. Most agreements have a renewal notice window, and leverage is highest before it closes. If your agreement is approaching renewal, have it reviewed now so you can either renegotiate or run a competitive process before the window passes.'),
        ]),
    ]),
)

# ---------- TELECOM: WIRELESS INFRASTRUCTURE ----------
PAGES['wireless-infrastructure.html'] = dict(
    title='Wireless Infrastructure Transactions | Telecommunications | Premier Law',
    desc='Florida attorney for wireless infrastructure: rooftop antenna leases, cell tower ground leases, and perpetual easements with carriers and tower companies.',
    parent=('telecommunications.html', 'Telecommunications'),
    crumb='Wireless Infrastructure Transactions',
    h1='Wireless Infrastructure Transactions',
    subtitle='Rooftop leases, cell tower leases, and easements, negotiated with the carriers and tower companies on the other side of the table.',
    cta_h='Received a Lease Offer From a Carrier?',
    cta_p='First offers are rarely best offers. Have it reviewed before you respond.',
    body_fn=lambda: '\n\n'.join([
        dark_section(
            'When a Carrier Wants Your Property',
            [
                'Wireless carriers and tower companies lease building rooftops, ground space, and easement rights to place the antennas and equipment their networks depend on. For a property owner, these agreements can produce decades of reliable income. They can also encumber the property for just as long, so the terms deserve the same scrutiny as any other long-term real estate deal.',
                'Premier Law represents property owners, associations, and developers in wireless infrastructure transactions. Our telecom industry background means we know how carriers and tower companies structure these deals internally, where their walk-away points really are, and which "standard" terms are actually negotiable.',
            ],
        ),
        light_section(
            'Rooftop Leases',
            [
                'Rooftop antenna leases let a carrier mount antennas and equipment on your building in exchange for monthly rent. The economics are attractive, but rooftop deals raise issues that ground leases do not: structural loading, roof warranty preservation, access for maintenance, interference with building systems, and coordination with roof replacement cycles.',
                'We negotiate rent and escalators alongside the operational terms that protect the building: defined equipment areas, engineering review rights, restoration obligations, and relocation rights when the roof needs work.',
            ],
            label='Rooftops',
        ),
        dark_section(
            'Cell Tower Leases',
            [
                'Cell tower ground leases commit a parcel of land to a tower for decades, commonly 25 years or more once renewal options are counted. Rent, escalators, and revenue sharing on subtenant colocations drive the value; termination rights, expansion rights, and access easements drive the risk.',
                'Tower companies negotiate these leases every day. Most landowners negotiate one in a lifetime. We close that gap, and we also advise owners fielding lease buyout and easement purchase offers on existing towers.',
            ],
            label='Towers',
            extra=grid_wrap(
                svc_list('Wireless Services', [
                    'Rooftop antenna leases with carriers and tower companies',
                    'Cell tower ground lease negotiation and renewals',
                    'Perpetual easement and lease buyout offer review',
                    'Rent escalators, colocation revenue share, and expansion rights',
                    'Ownership, maintenance, insurance, and removal obligations',
                    'Assignment, termination, and relocation provisions',
                ], light=False),
                feature_box(ICO_TREND, 'Know What the Site Is Worth',
                    'Carriers and tower companies price sites on network value: coverage gaps, zoning scarcity, and colocation potential. We evaluate offers against those drivers rather than against the first number on the page.', light=False),
            ),
        ),
        light_section(
            'Perpetual Easements &amp; Buyouts',
            [
                'Owners of existing tower sites are regularly approached with offers to buy the lease or convert it into a perpetual easement for a lump sum. These offers trade a stream of future rent for cash today, and they permanently encumber the property, surviving sale and passing to future owners.',
                'Whether a buyout makes sense depends on the offer price against the discounted value of remaining rent, your plans for the property, and the fine print of what rights the purchaser acquires. We review the economics and the instrument itself before you sign away a permanent interest.',
            ],
            label='Easements',
        ),
        faq_section('Wireless Infrastructure Questions', [
            ('What should I look for in a rooftop antenna lease?',
             'Beyond rent and escalators: lease duration and renewal options, defined equipment and access areas, structural and engineering review rights, roof warranty protection, insurance and indemnification, relocation rights during roof work, and equipment removal obligations at the end of the term. Each of these becomes expensive if it is missing when you need it.'),
            ('How long do cell tower leases run?',
             'A typical tower ground lease has an initial term of five years with multiple automatic renewal options, frequently totaling 25 years or more. Because the commitment is so long, escalator structure and revenue sharing on future colocations often matter more to total value than the starting rent.'),
            ('Should I accept a lease buyout or perpetual easement offer?',
             'Sometimes. A buyout converts uncertain future rent into certain present cash, which can make sense for estate planning or a pending sale. But offers are typically priced below the value of the remaining rent stream, and a perpetual easement permanently encumbers the parcel. Have the economics and the easement instrument reviewed before deciding.'),
            ('Can I negotiate with a major carrier, or are terms take-it-or-leave-it?',
             'Carriers and tower companies open with form documents, but sites they want are negotiable: rent, escalators, equipment limits, insurance, and termination rights all move when the site matters to the network. Knowing which sites have leverage is a large part of what industry experience adds.'),
        ]),
    ]),
)

# ---------- REAL ESTATE SUBPAGES ----------
PAGES['purchase-sale.html'] = dict(
    title='Purchase &amp; Sale Transactions | Real Estate | Premier Law',
    desc='Tampa real estate attorney for purchase and sale transactions: contract negotiation, due diligence, and closings, with title and closing support through Title Insights.',
    parent=('real-estate.html', 'Real Estate'),
    crumb='Purchase &amp; Sale Transactions',
    h1='Purchase &amp; Sale Transactions',
    subtitle='Contract to closing for buyers, sellers, developers, and investors, residential and commercial.',
    cta_h='Under Contract or About to Be?',
    cta_p='The best time to involve counsel is before you sign. The second-best time is now.',
    body_fn=lambda: '\n\n'.join([
        dark_section(
            'From Letter of Intent to Recorded Deed',
            [
                'Premier Law represents buyers, sellers, developers, and investors in residential and commercial purchase and sale transactions across Florida. We draft and negotiate the contract, manage due diligence, resolve title issues, and coordinate the closing so the deal you signed is the deal that records.',
                'Florida does not require an attorney at the closing table, and most problems we are hired to fix trace back to that fact. Contract contingencies, inspection and financing deadlines, title exceptions, and closing adjustments all carry real money. We watch them so you do not learn about them after closing.',
            ],
            extra=grid_wrap(
                svc_list('Purchase &amp; Sale Services', [
                    'Purchase and sale agreement drafting and negotiation',
                    'Letters of intent and offer strategy for competitive deals',
                    'Due diligence management: title, survey, inspections, estoppels',
                    'Title defect resolution and curative work',
                    'Closing coordination, document review, and funds management',
                    'Post-closing matters: recording, escrow releases, disputes',
                ], light=False),
                feature_box(ICO_TREND, '$1B+ Closed', 'A decade of closed residential and commercial transactions across Florida and beyond.', light=False)
                + feature_box(ICO_DOC, 'Deal-First Drafting', 'Contracts written to close, with contingencies and remedies that protect you if the deal does not.', light=False),
            ),
        ),
        light_section(
            'Title &amp; Closing Support Through Title Insights',
            [
                'For closings and title work, Premier Law works alongside Title Insights, a trusted Florida title partner with experience in both residential and commercial transactions. Title Insights handles title searches, title insurance, escrow services, and full closing coordination.',
                'This relationship gives clients who want it a complete, end-to-end experience from contract negotiation through final recording, with legal counsel and the title team working from the same playbook. Our legal services stand independently of the closing process, so you can engage us with or without the title work.',
            ],
            label='Trusted Title Partner',
        ),
        faq_section('Purchase &amp; Sale Questions', [
            ('Do I need an attorney to buy or sell property in Florida?',
             'Florida law does not require it, but title companies do not represent you, and real estate agents cannot give legal advice. An attorney is the only party at the table whose job is protecting your interests in the contract, the title, and the closing documents. On commercial deals and any transaction with unusual terms, counsel is essential.'),
            ('How long does a closing take?',
             'Residential closings typically run 30 to 45 days from contract execution. Commercial transactions may take 60 to 120 days depending on due diligence, financing, and other contingencies. Premier Law works to keep transactions on schedule and resolve issues quickly.'),
            ('What happens if a title problem turns up?',
             'Common issues include open permits, unreleased mortgages, judgment liens, and boundary or survey conflicts. Most are curable, but curing them takes time and legal work: payoff negotiations, corrective instruments, or quiet title actions in harder cases. Finding them early in the contingency period is what preserves your leverage to fix, renegotiate, or walk.'),
        ]),
    ]),
)

PAGES['leases.html'] = dict(
    title='Commercial &amp; Residential Leases | Real Estate | Premier Law',
    desc='Tampa lease attorney: commercial office, retail, and industrial leases plus residential leases compliant with Chapter 83, Florida Statutes.',
    parent=('real-estate.html', 'Real Estate'),
    crumb='Commercial &amp; Residential Leases',
    h1='Commercial &amp; Residential Leases',
    subtitle='Leases drafted and negotiated to hold up for the full term, on either side of the table.',
    cta_h='Need a Lease Drafted or Reviewed?',
    cta_p='A lease is cheaper to fix before signature than in court. Send it over first.',
    body_fn=lambda: '\n\n'.join([
        dark_section(
            'The Document That Runs the Relationship',
            [
                'A lease governs a relationship measured in years, and it is read most carefully when that relationship is at its worst. Premier Law drafts and negotiates commercial and residential leases for landlords, tenants, and investors throughout Florida, with terms built for the day something goes wrong.',
            ],
        ),
        light_section(
            'Commercial Leases',
            [
                'Office, retail, industrial, and mixed-use leases each carry their own economics: base rent and escalations, CAM and operating expense pass-throughs, build-out allowances, exclusivity and co-tenancy clauses, assignment and subletting rights, options to renew or expand, and personal guaranties.',
                'These are negotiated documents, and the form the other side sends is written for the other side. We negotiate the terms that decide what the space really costs and what happens if either party needs out.',
            ],
            label='Commercial',
            extra=grid_wrap(
                svc_list('Commercial Lease Services', [
                    'Office, retail, industrial, and ground lease drafting',
                    'CAM, operating expense, and escalation negotiation',
                    'Build-out, tenant improvement, and delivery terms',
                    'Assignment, subletting, and exit strategies',
                    'Guaranties, defaults, and remedies',
                ], light=True),
                feature_box(ICO_DOC, 'Landlord or Tenant', 'We represent both sides (never in the same deal), which means we know the other side’s playbook when we negotiate yours.', light=True),
            ),
        ),
        dark_section(
            'Residential Leases',
            [
                'Residential leases in Florida are governed by Part II of Chapter 83, Florida Statutes, the Residential Landlord and Tenant Act. The statute controls security deposit handling, notice requirements, and remedies, and a lease that conflicts with it will not protect the landlord who signed it.',
                'We draft residential leases that comply with the statute and actually fit the property, and we review portfolio leases for investors who inherited someone else’s forms.',
            ],
            label='Residential',
        ),
        faq_section('Lease Questions', [
            ('What is the difference between commercial and residential lease law in Florida?',
             'Residential tenancies are closely regulated by the Residential Landlord and Tenant Act, which dictates deposit handling, notices, and remedies regardless of what the lease says. Commercial leases are governed primarily by the contract itself, which makes the drafting and negotiation of the document far more consequential.'),
            ('What should a landlord never leave out of a residential lease?',
             'Statutorily compliant deposit and notice provisions, clear rent and late fee terms, maintenance responsibilities, rules on alterations and occupancy, and properly drafted default and remedies clauses. Just as important is leaving out unenforceable terms that can expose the landlord to liability.'),
            ('Can I use a form lease I found online?',
             'Form leases are where many eviction problems start. Generic forms routinely conflict with Florida statutory requirements or omit protections specific to your property type. A lease drafted once, correctly, is reused across every unit and tenancy you own.'),
        ]),
    ]),
)

PAGES['landlord-evictions.html'] = dict(
    title='Landlord Representation &amp; Evictions | Real Estate | Premier Law',
    desc='Tampa landlord attorney: residential and commercial evictions, statutory notices, and ongoing landlord representation across Florida.',
    parent=('real-estate.html', 'Real Estate'),
    crumb='Landlord Representation &amp; Evictions',
    h1='Landlord Representation &amp; Evictions',
    subtitle='Statutory compliance, enforceable notices, and evictions handled start to finish.',
    cta_h='Dealing With a Non-Paying Tenant?',
    cta_p='The clock starts when the notice is served correctly. Get it right the first time.',
    body_fn=lambda: '\n\n'.join([
        dark_section(
            'Counsel for Landlords, Before and During the Dispute',
            [
                'Premier Law represents residential and commercial landlords across Florida: individual owners, investors, and property management companies. The best eviction is the one your lease and your process prevented, so our representation starts with compliant leases and notice practices and extends through the courtroom when a tenancy fails.',
                'Florida eviction procedure is unforgiving about the details. A defective notice, a miscounted deadline, or accepting rent at the wrong moment can restart the entire process. We handle the sequence correctly the first time.',
            ],
            extra=grid_wrap(
                svc_list('Landlord Services', [
                    'Residential and commercial eviction actions',
                    'Statutory notices: 3-day nonpayment, 7-day cure and termination',
                    'Lease enforcement, defaults, and negotiated resolutions',
                    'Security deposit claims and disputes',
                    'Unauthorized occupant and holdover proceedings',
                    'Ongoing counsel for portfolios and property managers',
                ], light=False),
                feature_box(ICO_DOC, 'Process Discipline', 'Evictions are won on procedure. Notices, service, filing, and timelines handled by counsel who does this routinely.', light=False),
            ),
        ),
        light_section(
            'How a Florida Eviction Proceeds',
            [
                'A residential eviction begins with the statutorily required notice: a 3-day notice for nonpayment of rent, or a 7-day notice for other lease violations. If the tenant does not cure or vacate, suit is filed in county court, and the tenant must respond within a short statutory window and generally must deposit disputed rent into the court registry to contest the case.',
                'Handled correctly, an uncontested residential eviction moves quickly. Handled incorrectly, each defect resets the clock. Commercial evictions follow their own track with more room for lease-driven remedies, including termination, damages, and recovery of the premises.',
            ],
            label='The Process',
        ),
        faq_section('Eviction Questions', [
            ('How long does an eviction take in Florida?',
             'An uncontested residential eviction often completes within three to six weeks from notice to writ of possession, depending on the county. Contested cases, procedural defects, or improper notices extend that considerably. The single biggest factor landlords control is starting with a correct notice.'),
            ('Can I remove a tenant myself by changing the locks or shutting off utilities?',
             'No. Self-help evictions are unlawful in Florida and expose the landlord to statutory damages, including up to three months’ rent per violation, plus attorney fees. The writ of possession executed by the sheriff is the only lawful way to recover possession from an unwilling tenant.'),
            ('Do commercial evictions work the same way as residential?',
             'The framework differs. Commercial tenancies fall outside the Residential Landlord and Tenant Act, so the lease terms control much more, and remedies like landlord liens and accelerated rent may be available. Notice and procedure still matter, but the lease you signed largely defines your options.'),
        ]),
    ]),
)

PAGES['land-trusts.html'] = dict(
    title='Land Trusts | Real Estate | Premier Law',
    desc='Florida land trust attorney: privacy-focused ownership structures under the Florida Land Trust Act for investors and property owners.',
    parent=('real-estate.html', 'Real Estate'),
    crumb='Land Trusts',
    h1='Land Trusts',
    subtitle='Private, flexible property ownership under the Florida Land Trust Act.',
    cta_h='Considering a Land Trust?',
    cta_p='Tell us what you own and what you want kept private. We will tell you if a land trust fits.',
    body_fn=lambda: '\n\n'.join([
        dark_section(
            'Ownership Without the Public Record',
            [
                'A Florida land trust is an ownership structure authorized by the Florida Land Trust Act (Section 689.071, Florida Statutes) in which a trustee holds title to real property for the benefit of the trust’s beneficiaries. Only the trustee appears in the public record. Who actually owns and controls the property stays private.',
                'Premier Law forms land trusts for investors, landlords, and private individuals, serves as counsel on trustee arrangements, and structures the beneficial interests behind the trust. We also move existing properties into trust and coordinate financing and insurance so the structure works in practice, not just on paper.',
            ],
        ),
        light_section(
            'Why Property Owners Use Land Trusts',
            [
                'Privacy is the headline benefit: your name stays off the deed, which matters to landlords, public figures, and anyone who prefers not to advertise their holdings. But the structure carries practical advantages beyond privacy.',
                'Beneficial interests in a land trust are personal property, so they can be assigned without recording a new deed, divided among multiple owners cleanly, and integrated with your broader estate and asset planning. Each property can sit in its own trust, isolating it from the others for liability and management purposes.',
            ],
            label='Benefits',
            extra=grid_wrap(
                svc_list('Land Trust Services', [
                    'Land trust formation under Section 689.071, Florida Statutes',
                    'Trustee arrangements and successor trustee planning',
                    'Beneficial interest assignments and transfers',
                    'Moving existing properties into trust',
                    'Coordination with lenders, insurers, and estate plans',
                ], light=True),
                feature_box(ICO_KEY, 'Privacy by Design', 'Only the trustee appears in public records. Ownership, control, and succession live in the unrecorded trust agreement.', light=True),
            ),
        ),
        faq_section('Land Trust Questions', [
            ('What is a Florida land trust?',
             'A legal arrangement under the Florida Land Trust Act in which real property is held by a trustee for the benefit of named beneficiaries. The key advantage is privacy: only the trustee’s name appears in public records. Land trusts also simplify transfers, provide a degree of asset protection, and make it easier to divide or assign property interests.'),
            ('Does a land trust protect me from lawsuits?',
             'A land trust provides privacy and some separation, but it is not by itself a complete asset protection device. Serious protection usually comes from combining the trust with the right beneficiary structure, such as an LLC holding the beneficial interest. We design the combination to match your actual risk.'),
            ('Can I still get financing and insurance on property in a land trust?',
             'Yes, though it takes coordination. Many lenders finance land trust properties routinely, and insurance simply needs to name the right parties. We handle the lender and insurer mechanics as part of setting up the trust so nothing surprises you at closing or claim time.'),
        ]),
    ]),
)

PAGES['surplus-funds.html'] = dict(
    title='Surplus Funds Recovery | Real Estate | Premier Law',
    desc='Florida surplus funds attorney: recovering mortgage foreclosure surplus, tax deed surplus, and state unclaimed funds for former owners and heirs.',
    parent=('real-estate.html', 'Real Estate'),
    crumb='Surplus Funds Recovery',
    h1='Surplus Funds Recovery',
    subtitle='When a foreclosure or tax deed sale brings more than the debt, the difference may be yours. We recover it.',
    cta_h='Think You May Be Owed Surplus Funds?',
    cta_p='Deadlines apply, and third-party recovery firms are already looking at the same court file. Talk to a lawyer first.',
    body_fn=lambda: '\n\n'.join([
        dark_section(
            'Money the Sale Left Behind',
            [
                'When a foreclosed or tax-delinquent property sells at auction for more than what was owed, the extra money, the surplus, does not belong to the bank or the county. It generally belongs to the former owner, or to heirs and lienholders with a valid claim. Recovering it means filing the right claim, in the right proceeding, before the deadline.',
                'Premier Law represents former owners and heirs in surplus recovery across Florida. We locate the funds, establish your entitlement, respond to competing claims, and move the court or agency to release the money. Fees are discussed up front, and unlike the "asset recovery" companies that cold-call after every auction, you are represented by a law firm the whole way.',
            ],
        ),
        light_section(
            'Mortgage Foreclosure Surplus',
            [
                'After a mortgage foreclosure sale, proceeds beyond the judgment amount are deposited with the clerk of court. Florida’s foreclosure statutes set out who may claim the surplus and in what order: subordinate lienholders first, then the former owner, with strict claim windows measured in days, not months.',
                'Heirs claiming a deceased owner’s surplus face an extra layer of proof, and competing claims are common. We prepare the claim, the supporting record, and the hearing presentation.',
            ],
            label='Foreclosure',
        ),
        dark_section(
            'Tax Deed Surplus',
            [
                'When property is sold at a tax deed auction for more than the delinquent taxes and costs, the surplus is held for governmental lienholders and then the former owner of record. Chapter 197, Florida Statutes governs the process, with its own notice procedure and claim deadlines administered by the clerk.',
                'Tax deed surpluses are frequently substantial, and frequently unclaimed, because notice reaches owners at addresses they left years earlier. If you lost property to a tax deed sale, it is worth checking whether money is waiting.',
            ],
            label='Tax Deed',
        ),
        light_section(
            'State Unclaimed Funds',
            [
                'Surplus money that goes unclaimed long enough is transferred to the Florida Department of Financial Services as unclaimed property under Chapter 717, Florida Statutes. It does not disappear, but recovering it moves to a different process with its own documentation requirements, particularly for heirs and estates.',
                'We handle unclaimed property claims tied to real estate proceeds: proving entitlement, assembling the documentation the Department requires, and pushing stalled claims through.',
            ],
            label='Unclaimed Property',
        ),
        faq_section('Surplus Funds Questions', [
            ('How do I know if I am owed surplus funds?',
             'If a property you owned (or inherited an interest in) was sold at a foreclosure or tax deed auction, the court or clerk file will show whether the sale produced a surplus. We check the file, the payoff amounts, and the clerk’s registry, and we also search state unclaimed property records for funds that have already been transferred.'),
            ('How long do I have to claim a foreclosure surplus?',
             'The claim windows are short and strictly enforced, generally a matter of days from the date of the sale for the initial claim period, with the analysis differing for owners, lienholders, and heirs. Because the deadlines are unforgiving, the right move is to have the file reviewed immediately, not after the recovery letters start arriving.'),
            ('A company contacted me offering to recover my surplus for a percentage. Should I sign?',
             'Read nothing, sign nothing, until you know what you are owed. Florida law caps what third-party recovery agreements can charge in some circumstances, and many solicitations ask you to sign away a large share of money you could recover with counsel at a lower cost. A short consultation will tell you what the funds are, what the recovery actually requires, and what it should cost.'),
            ('Can heirs claim a deceased owner’s surplus?',
             'Yes. Heirs regularly recover surplus funds, but the claim requires proving the chain of entitlement, which may involve probate documents, affidavits of heirship, or a probate proceeding. We evaluate what the specific court or agency will require before you spend money on the wrong path.'),
        ]),
    ]),
)

# ---------- RESOURCES ----------
RESOURCE_CARDS = [
    ('article-bulk-agreements.html', 'Telecommunications', 'Bulk Broadband Agreements: What Every Board Should Know',
     'How bulk deals work, what they are worth, and the terms that decide whether your community wins or loses over a ten-year term.'),
    ('article-surplus-funds.html', 'Real Estate', 'Surplus Funds After a Florida Foreclosure: How Recovery Works',
     'The auction brought more than the debt. Here is who the difference belongs to, the deadlines that apply, and how to claim it safely.'),
    (None, 'Telecommunications', 'Exclusive vs. Non-Exclusive Marketing Agreements',
     'What providers are really buying, what the FCC allows, and how to price marketing rights on your property.'),
    (None, 'Telecommunications', 'Rooftop Antenna Leases: The Terms That Matter',
     'Rent is the headline, but structure, access, and removal terms decide what the lease costs your building.'),
    (None, 'Real Estate', 'Florida Land Trusts: Privacy for Property Owners',
     'How the Florida Land Trust Act keeps your name off the deed, and when a land trust fits your holdings.'),
    (None, 'Real Estate', 'The Anatomy of a Clean Closing',
     'What happens between contract and recording, and where deals go sideways without counsel watching.'),
]

def resources_body():
    cards = []
    for href, cat, title, blurb in RESOURCE_CARDS:
        inner = f'''        <p class="resource-card-cat">{cat}</p>
        <h3>{title}</h3>
        <p class="resource-card-blurb">{blurb}</p>'''
        if href:
            cards.append(f'''      <a href="{href}" class="resource-card reveal">
{inner}
        <span class="practice-card-link">Read the article <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
      </a>''')
        else:
            cards.append(f'''      <div class="resource-card resource-card--soon reveal">
{inner}
        <span class="resource-soon">Coming soon</span>
      </div>''')
    grid = '\n'.join(cards)
    return f'''<section class="content-section content-section--light">
  <div class="container">
    <div class="content-text content-text--light reveal" style="max-width: 760px;">
      <p class="section-label" style="color: var(--crimson);">Plain-English Guides</p>
      <h2>Legal Guides for Property Owners and Communities</h2>
      <p>Short, practical articles on the questions our telecom and real estate clients ask most. No legalese, no fluff, and no substitute for advice about your specific situation.</p>
    </div>
    <div class="resource-grid reveal reveal-delay-1">
{grid}
    </div>
  </div>
</section>'''

PAGES['resources.html'] = dict(
    title='Resources | Telecom &amp; Real Estate Guides | Premier Law',
    desc='Plain-English legal guides on telecommunications agreements and Florida real estate from Premier Law.',
    parent=None,
    crumb='Resources',
    h1='Resources',
    subtitle='Plain-English guides to the telecom and real estate questions we hear most.',
    cta_h='Have a Question the Guides Did Not Answer?',
    cta_p='Ask us directly. The first conversation costs nothing.',
    body_fn=resources_body,
)

# ---------- ARTICLES ----------
def article_body(sections):
    parts = []
    for h2, paras in sections:
        ps = '\n'.join(f'      <p>{p}</p>' for p in paras)
        h = f'      <h2>{h2}</h2>\n' if h2 else ''
        parts.append(f'''<section class="content-section content-section--light article-section">
  <div class="container">
    <div class="content-text content-text--light reveal" style="max-width: 800px; margin: 0 auto;">
{h}{ps}
    </div>
  </div>
</section>''')
    return '\n\n'.join(parts)

PAGES['article-bulk-agreements.html'] = dict(
    title='Bulk Broadband Agreements: What Every Board Should Know | Premier Law',
    desc='A plain-English guide to bulk broadband agreements for HOA and condo boards: how they work, what they are worth, and the terms that matter.',
    parent=('resources.html', 'Resources'),
    crumb='Bulk Broadband Agreements',
    h1='Bulk Broadband Agreements: What Every Board Should Know',
    subtitle='Telecommunications &middot; A Premier Law guide for community associations',
    cta_h='Negotiating a Bulk Deal?',
    cta_p='Have the draft reviewed before the board votes. It is the cheapest leverage you will ever buy.',
    body_fn=lambda: article_body([
        (None, [
            'If your community association has been approached about a bulk broadband agreement, or your existing one is coming up for renewal, the decision in front of the board is bigger than it looks. A bulk deal sets what every resident pays for internet, what service they get, and what the association earns, for as long as a decade.',
        ]),
        ('How a bulk agreement works', [
            'In a bulk agreement, the association purchases broadband service for every unit at a wholesale rate, typically a steep discount to retail, and recovers the cost through assessments. Residents get service automatically, usually at half or less of what they would pay on their own. The provider gets one hundred percent penetration and predictable revenue. The association gets an amenity that helps sales and rentals, and often compensation on top.',
            'Contrast that with retail arrangements, where the provider sells to residents one by one and the association is compensated only for marketing rights or property access. Retail preserves individual choice; bulk delivers price and amenity value. Neither is automatically right, and the same community can reasonably land in different places at different points in its life.',
        ]),
        ('What the deal is worth', [
            'Boards tend to negotiate the monthly rate and stop there. The provider’s negotiators know the value lives elsewhere: in the escalator that compounds over ten years, in door fees and construction contributions paid up front, in revenue sharing, and in service-level commitments that determine whether residents actually get what the contract promises.',
            'A one-dollar difference in the per-unit rate on a 300-unit community is roughly $36,000 over a ten-year term. The escalator cap is worth more. Boards that bid the contract competitively, rather than renewing with the incumbent by default, routinely improve both.',
        ]),
        ('The terms that bite later', [
            'Watch the renewal mechanics: automatic renewals with short notice windows quietly hand back the leverage you had at signing. Watch technology refresh obligations: ten years is a long time in broadband, and a contract without upgrade commitments can leave the community paying 2026 prices for 2026 technology in 2036. Watch assignment provisions if the property may sell, and termination rights if the provider underperforms.',
            'Finally, remember the association side of the deal. A bulk assessment has to fit your governing documents, your budgeting process, and Florida’s association statutes, and board approval should be documented cleanly. A great provider deal implemented badly is still a problem.',
        ]),
        ('The bottom line', [
            'A bulk broadband agreement is one of the few contracts an association signs that touches every unit, every month, for years. Treat it like the major transaction it is: run a competitive process, negotiate past the rate card, and have counsel who has seen the provider’s form before reading yours.',
        ]),
    ]),
)

PAGES['article-surplus-funds.html'] = dict(
    title='Surplus Funds After a Florida Foreclosure: How Recovery Works | Premier Law',
    desc='A plain-English guide to Florida foreclosure and tax deed surplus funds: who the money belongs to, the deadlines, and how to claim it safely.',
    parent=('resources.html', 'Resources'),
    crumb='Surplus Funds After Foreclosure',
    h1='Surplus Funds After a Florida Foreclosure: How Recovery Works',
    subtitle='Real Estate &middot; A Premier Law guide for former owners and heirs',
    cta_h='Checking on a Surplus?',
    cta_p='We will review the court file and tell you what is there before you sign anything with anyone.',
    body_fn=lambda: article_body([
        (None, [
            'Losing a property at a foreclosure or tax deed auction feels final. But when the auction brings more than what was owed, the extra money, called the surplus, does not go to the bank, and it does not go to the county. In most cases it belongs to the person who lost the property, or to their heirs. Every year, millions of dollars of it goes unclaimed in Florida.',
        ]),
        ('Where the money comes from', [
            'At a foreclosure sale, the winning bid first pays the judgment: the loan balance, interest, fees, and costs. Anything above that is deposited with the clerk of court. At a tax deed sale, the bid first covers the delinquent taxes and sale costs, and the remainder is held for lienholders and the former owner under Chapter 197 of the Florida Statutes.',
            'Bidding competition is what creates surpluses, and in a market where properties carry equity, surpluses of tens of thousands of dollars are common. The court file will show the exact number.',
        ]),
        ('Who gets paid, and in what order', [
            'The surplus is not a free-for-all. Subordinate lienholders, such as second mortgages, HOA liens, and judgment creditors, may claim first, in priority order. What remains belongs to the former owner of record. If the owner has died, heirs may claim, but they must prove their entitlement, which can require probate documents or affidavits establishing the family tree.',
            'Deadlines are the trap. The claim windows under Florida’s foreclosure statutes are measured in days from the sale, and tax deed claims run on their own clock. Miss the window and the analysis gets harder; wait long enough and the funds transfer to the state as unclaimed property under Chapter 717, where a different process with different documentation requirements takes over. The money survives, but every stage adds friction.'
        ]),
        ('About those letters and phone calls', [
            'Surplus files are public record, and within days of an auction, former owners start hearing from "asset recovery" companies offering to collect the money for a percentage, sometimes a very large one. Some are legitimate; many charge far more than the work justifies; a few are outright scams that collect signatures, not surpluses.',
            'Before signing anything, understand three things: exactly how much is on deposit, what competing claims exist, and what the recovery actually requires. Those are questions a real estate attorney can answer quickly. In many cases the claim is straightforward, and the percentage you were about to sign away vastly exceeds what counsel would cost.',
        ]),
        ('The bottom line', [
            'If you lost a Florida property at auction, or inherited from someone who did, check for a surplus now, before deadlines run and before a recovery company’s contract locks in their share. The review takes little time, the deadlines are real, and the money is yours.',
        ]),
    ]),
)


# ============================================================
# BUILD
# ============================================================

def crumb_mid(parent):
    if not parent:
        return ''
    href, label = parent
    return f'<a href="{href}">{label}</a>\n      <span class="sep">/</span>\n      '

def active_key(fname):
    return fname

def build_new_pages():
    for fname, spec in PAGES.items():
        header = HEADER_TMPL.replace('{NAV}', nav_html(active_key(fname) if fname in dict(TELECOM_SUBS) or fname in dict(RE_SUBS) else ('resources' if fname.startswith(('resources', 'article-')) else fname)))
        html = PAGE_TMPL.format(cache=CACHE, 
            title=spec['title'], desc=spec['desc'],
            header=header, mobile=MOBILE_MENU,
            crumb_mid=crumb_mid(spec['parent']), crumb=spec['crumb'],
            h1=spec['h1'], subtitle=spec['subtitle'],
            body=spec['body_fn'](),
            cta=CTA_BAND.format(cta_h=spec['cta_h'], cta_p=spec['cta_p']),
            footer=FOOTER,
        )
        with open(fname, 'w') as f:
            f.write(html)
        print('wrote', fname)

NAV_ACTIVE_BY_PAGE = {
    'index.html': 'index',
    'telecommunications.html': 'telecom',
    'real-estate.html': 'realestate',
    'about.html': 'about',
    'contact.html': 'contact',
    'privacy-policy.html': 'privacy',
}

def patch_existing_pages():
    nav_re = re.compile(r'<nav class="nav-links"[^>]*>.*?</nav>', re.S)
    menu_re = re.compile(r'<div class="mobile-menu"[^>]*>.*?</div>', re.S)
    footer_re = re.compile(r'<footer class="footer">.*?</footer>', re.S)
    for fname, key in NAV_ACTIVE_BY_PAGE.items():
        s = open(fname).read()
        s = nav_re.sub(lambda m: nav_html(key), s, count=1)
        s = menu_re.sub(lambda m: MOBILE_MENU, s, count=1)
        s = footer_re.sub(lambda m: FOOTER, s, count=1)
        if 'assets/favicon.ico' not in s:
            s = s.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                          '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + FAVICON_LINKS, 1)
        s = re.sub(r'styles\.css\?v=[\w]+', 'styles.css?v=' + CACHE, s)
        open(fname, 'w').write(s)
        print('patched', fname)

def remove_moved_sections():
    # About: Title Insights section now lives on purchase-sale.html
    s = open('about.html').read()
    s2 = re.sub(r'<!-- =+\n     TITLE INSIGHTS\n     =+ -->\n<section class="content-section content-section--light">.*?</section>\n\n', '', s, count=1, flags=re.S)
    if s2 != s:
        open('about.html', 'w').write(s2)
        print('about.html: moved Title Insights section to purchase-sale.html')
    # Real estate overview: Title & Closing Support section now on purchase-sale.html
    s = open('real-estate.html').read()
    s2 = re.sub(r'<!-- =+\n     TITLE & CLOSING SERVICES \(supporting role\)\n     =+ -->\n<section class="content-section content-section--dark">.*?</section>\n\n', '', s, count=1, flags=re.S)
    if s2 != s:
        open('real-estate.html', 'w').write(s2)
        print('real-estate.html: moved Title & Closing section to purchase-sale.html')

EXTRA_CSS_MARK = '/* NAV DROPDOWNS, RESOURCE GRID, ARTICLE PAGES */'
EXTRA_CSS = EXTRA_CSS_MARK + '''
/* Nav dropdowns */
.nav-item { position: relative; display: flex; align-items: center; }
.nav-item > a { display: inline-flex; align-items: center; gap: 5px; }
.nav-caret { width: 12px; height: 12px; opacity: 0.55; transition: transform 0.25s; flex-shrink: 0; }
.nav-item:hover .nav-caret, .nav-item:focus-within .nav-caret { transform: rotate(180deg); }
.nav-dropdown {
  position: absolute; top: calc(100% + 14px); left: -18px; min-width: 300px;
  background: #fff; border-radius: 12px; padding: 10px;
  box-shadow: 0 18px 50px rgba(15, 17, 21, 0.14), 0 2px 8px rgba(15, 17, 21, 0.08);
  opacity: 0; visibility: hidden; transform: translateY(10px);
  transition: opacity 0.22s ease, transform 0.22s ease, visibility 0.22s;
  z-index: 1200;
}
.nav-dropdown::before {
  content: ''; position: absolute; top: -14px; left: 0; right: 0; height: 14px;
}
.nav-dropdown a {
  display: block; padding: 11px 14px; border-radius: 8px;
  font-size: 0.84rem; font-weight: 500; color: rgba(30, 32, 37, 0.85);
  white-space: nowrap;
}
.nav-dropdown a::after { display: none; }
.nav-dropdown a:hover { background: rgba(139, 21, 40, 0.06); color: var(--crimson); }
.nav-dropdown a.active { color: var(--crimson); }
.nav-item:hover .nav-dropdown, .nav-item:focus-within .nav-dropdown {
  opacity: 1; visibility: visible; transform: translateY(0);
}

/* Mobile submenu indent */
.mobile-menu .mobile-sub { padding-left: 22px; font-size: 0.95em; opacity: 0.8; }

/* Resources grid */
.resource-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 48px;
}
.resource-card {
  background: #fff; border: 1px solid rgba(30, 32, 37, 0.09); border-radius: 14px;
  padding: 30px 28px; display: flex; flex-direction: column; gap: 12px;
  transition: transform 0.3s, box-shadow 0.3s; color: inherit;
}
a.resource-card:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(15, 17, 21, 0.10); }
.resource-card h3 { font-family: 'Playfair Display', serif; font-size: 1.25rem; line-height: 1.3; margin: 0; color: var(--text-dark, #1e2025); }
.resource-card-cat { font-size: 0.72rem; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; color: var(--crimson); margin: 0; }
.resource-card-blurb { font-size: 0.92rem; line-height: 1.7; color: rgba(30, 32, 37, 0.7); margin: 0; text-align: justify; flex: 1; }
.resource-card--soon { opacity: 0.72; }
.resource-soon { font-size: 0.72rem; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; color: rgba(30, 32, 37, 0.45); }
@media (max-width: 900px) { .resource-grid { grid-template-columns: 1fr; } }

/* Article pages */
.article-section .content-text h2 { margin-top: 8px; }

'''

def patch_css():
    s = open('styles.css').read()
    if EXTRA_CSS_MARK in s:
        s = s[:s.index(EXTRA_CSS_MARK)].rstrip() + '\n\n' + EXTRA_CSS
    else:
        s = s.rstrip() + '\n\n' + EXTRA_CSS
    open('styles.css', 'w').write(s)
    print('patched styles.css')

def write_cname():
    open('CNAME', 'w').write('premier.law\n')
    print('wrote CNAME (premier.law)')

if __name__ == '__main__':
    build_new_pages()
    patch_existing_pages()
    remove_moved_sections()
    patch_css()
    write_cname()
    print('build complete (cache-buster v=%s)' % CACHE)
