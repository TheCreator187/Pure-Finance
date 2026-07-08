#!/usr/bin/env python3
"""SEO meta tag helpers for Pure Capital static site."""

from __future__ import annotations

import json
from datetime import date

SITE_URL = "https://purecapital.us"
SITE_NAME = "Pure Capital"
ORG_NAME = "Pure Capital US LLC"
OG_IMAGE = f"{SITE_URL}/assets/banner.jpg"
LOGO_URL = f"{SITE_URL}/assets/IMG_20260531_000449-removebg-preview.png"
PHONE = "+1-347-201-2166"

PAGES = {
    "index.html": {
        "title": "Business Funding & Loans | Pure Capital US LLC",
        "description": "Pure Capital US LLC offers business lines of credit, SBA loans, and real estate financing. Apply online in minutes for fast business funding. Call (347) 201-2166.",
        "path": "/",
        "og_type": "website",
        "robots": "index, follow",
        "json_ld": "home",
    },
    "prequalify.html": {
        "title": "Business Funding Prequalification | Pure Capital US LLC",
        "description": "Complete the Pure Capital US LLC prequalification form. 4-step wizard for company info, owner details, MCA/real estate, and document upload.",
        "path": "/prequalify.html",
        "robots": "index, follow",
        "json_ld": "page",
    },
    "apply.html": {
        "title": "Apply for Business Funding | Pure Capital US LLC",
        "description": "Submit your business funding application to Pure Capital US LLC. Lines of credit, SBA loans, and real estate financing. Secure online form.",
        "path": "/apply.html",
        "robots": "index, follow",
        "json_ld": "page",
    },
    "business-line-of-credit.html": {
        "title": "Business Lines of Credit | Pure Capital US LLC",
        "description": "Get a flexible business line of credit from Pure Capital US LLC. Draw funds when you need them and pay interest only on what you use. Apply today.",
        "path": "/business-line-of-credit.html",
        "robots": "index, follow",
        "json_ld": "service",
        "service_name": "Business Line of Credit",
    },
    "real-estate-financing.html": {
        "title": "Real Estate Financing | Pure Capital US LLC",
        "description": "Commercial and investment real estate financing from Pure Capital US LLC. Purchase, refinance, or grow your property portfolio. Apply online.",
        "path": "/real-estate-financing.html",
        "robots": "index, follow",
        "json_ld": "service",
        "service_name": "Real Estate Financing",
    },
    "sba-loans.html": {
        "title": "SBA Loans for Small Business | Pure Capital US LLC",
        "description": "Explore SBA loan options with Pure Capital US LLC. Government-backed small business financing with competitive rates and flexible terms. Apply now.",
        "path": "/sba-loans.html",
        "robots": "index, follow",
        "json_ld": "service",
        "service_name": "SBA Loans",
    },
    "terms.html": {
        "title": "Terms of Use | Pure Capital US LLC",
        "description": "Read the Terms of Use for Pure Capital US LLC and purecapital.us. Business funding services, applications, and legal agreements.",
        "path": "/terms.html",
        "robots": "index, follow",
        "json_ld": "page",
    },
    "privacy.html": {
        "title": "Privacy Policy | Pure Capital US LLC",
        "description": "Pure Capital US LLC privacy policy. Learn how we collect, use, and protect your personal and business information at purecapital.us.",
        "path": "/privacy.html",
        "robots": "index, follow",
        "json_ld": "page",
    },
    "thank-you.html": {
        "title": "Application Received | Pure Capital",
        "description": "Your business funding application has been received by Pure Capital US LLC.",
        "path": "/thank-you.html",
        "robots": "noindex, nofollow",
    },
    "small-business-loans.html": {
        "title": "Small Business Loans | Pure Capital",
        "description": "Small business loans from Pure Capital.",
        "path": "/small-business-loans.html",
        "robots": "noindex, follow",
    },
    "equipment-finance-loans.html": {
        "title": "Equipment Finance | Pure Capital",
        "description": "Equipment financing from Pure Capital.",
        "path": "/equipment-finance-loans.html",
        "robots": "noindex, follow",
    },
    "short-term-business-loans.html": {
        "title": "Short-Term Business Loans | Pure Capital",
        "description": "Short-term business loans from Pure Capital.",
        "path": "/short-term-business-loans.html",
        "robots": "noindex, follow",
    },
}


def _json_ld_block(kind: str, page: dict, canonical: str) -> str:
    graph = []

    org = {
        "@type": "Organization",
        "@id": f"{SITE_URL}/#organization",
        "name": ORG_NAME,
        "url": SITE_URL,
        "logo": LOGO_URL,
        "image": LOGO_URL,
        "telephone": PHONE,
        "email": "info@purecapital.us",
        "sameAs": [
            "https://x.com/purecapitalus",
            "https://instagram.com/purecapitalus",
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "customer service",
            "areaServed": "US",
            "availableLanguage": "English",
        },
    }
    graph.append(org)

    if kind in ("service", "page"):
        graph.append({
            "@type": "WebSite",
            "@id": f"{SITE_URL}/#website",
            "url": SITE_URL,
            "name": SITE_NAME,
            "publisher": {"@id": f"{SITE_URL}/#organization"},
            "inLanguage": "en-US",
        })

    if kind == "home":
        graph.extend([
            {
                "@type": "WebSite",
                "@id": f"{SITE_URL}/#website",
                "url": SITE_URL,
                "name": SITE_NAME,
                "publisher": {"@id": f"{SITE_URL}/#organization"},
                "inLanguage": "en-US",
            },
            {
                "@type": "FinancialService",
                "@id": f"{SITE_URL}/#financialservice",
                "name": SITE_NAME,
                "url": SITE_URL,
                "telephone": PHONE,
                "email": "info@purecapital.us",
                "areaServed": {"@type": "Country", "name": "United States"},
                "description": page["description"],
                "provider": {"@id": f"{SITE_URL}/#organization"},
            },
        ])
    elif kind == "service":
        service_name = page.get("service_name", "Business Funding")
        graph.append({
            "@type": "Service",
            "name": service_name,
            "url": canonical,
            "provider": {"@id": f"{SITE_URL}/#organization"},
            "areaServed": {"@type": "Country", "name": "United States"},
            "description": page["description"],
        })
        graph.append({
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumb",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": SITE_URL + "/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": service_name,
                    "item": canonical,
                },
            ],
        })
    elif kind == "page":
        graph.append({
            "@type": "WebPage",
            "@id": f"{canonical}#webpage",
            "name": page["title"],
            "url": canonical,
            "description": page["description"],
            "isPartOf": {"@id": f"{SITE_URL}/#website"},
            "about": {"@id": f"{SITE_URL}/#organization"},
            "inLanguage": "en-US",
        })

    payload = {"@context": "https://schema.org", "@graph": graph}
    return (
        '<script type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False)
        + "</script>"
    )


def render_seo_tags(page: dict) -> str:
    canonical = SITE_URL + page["path"]
    title = page["title"]
    description = page["description"]
    robots = page.get("robots", "index, follow")
    og_type = page.get("og_type", "website")

    lines = [
        f'  <title>{title}</title>',
        f'  <meta name="description" content="{description}" />',
        f'  <meta name="robots" content="{robots}" />',
        f'  <link rel="canonical" href="{canonical}" />',
        '  <meta name="author" content="Pure Capital US LLC" />',
        '  <meta name="theme-color" content="#0c1a2e" />',
        f'  <link rel="icon" href="{LOGO_URL}" type="image/png" />',
        f'  <link rel="apple-touch-icon" href="{LOGO_URL}" />',
        f'  <meta property="og:type" content="{og_type}" />',
        f'  <meta property="og:site_name" content="{SITE_NAME}" />',
        f'  <meta property="og:title" content="{title}" />',
        f'  <meta property="og:description" content="{description}" />',
        f'  <meta property="og:url" content="{canonical}" />',
        f'  <meta property="og:image" content="{OG_IMAGE}" />',
        '  <meta property="og:image:alt" content="Pure Capital business funding" />',
        '  <meta property="og:locale" content="en_US" />',
        '  <meta name="twitter:card" content="summary_large_image" />',
        f'  <meta name="twitter:title" content="{title}" />',
        f'  <meta name="twitter:description" content="{description}" />',
        f'  <meta name="twitter:image" content="{OG_IMAGE}" />',
    ]

    if page.get("json_ld"):
        for script_line in _json_ld_block(page["json_ld"], page, canonical).split("\n"):
            lines.append("  " + script_line)

    return "\n".join(lines)


def _sitemap_priority(path: str) -> str:
    if path == "/":
        return "1.0"
    if path in ("/terms.html", "/privacy.html"):
        return "0.4"
    return "0.9"


def render_sitemap() -> str:
    lastmod = date.today().isoformat()
    urls = []
    for _name, cfg in PAGES.items():
        if cfg.get("robots", "").startswith("noindex"):
            continue
        path = cfg["path"]
        urls.append((SITE_URL + path, lastmod, _sitemap_priority(path)))

    items = []
    for loc, lastmod, priority in urls:
        items.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(items)
        + "\n</urlset>\n"
    )


def render_robots() -> str:
    return f"""User-agent: *
Allow: /

Disallow: /submissions/

Sitemap: {SITE_URL}/sitemap.xml
"""
