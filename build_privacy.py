#!/usr/bin/env python3
"""Build privacy.html from privacy-source.txt for Pure Capital US LLC."""

import html
import re
from pathlib import Path

from seo import PAGES, render_seo_tags

ROOT = Path(__file__).parent
source = (ROOT / "privacy-source.txt").read_text(encoding="utf-8")

replacements = [
    ("OnDeck\\_Privacy@enova.com", "privacy@purecapital.us"),
    ("OnDeck_Privacy@enova.com", "privacy@purecapital.us"),
    ("Pure Capital US LLC\\_Privacy@enova.com", "privacy@purecapital.us"),
    (
        "On Deck Capital, Inc., ODK Capital, LLC, and its parents, subsidiaries, and affiliates "
        "doing business under the OnDeck brand (collectively, “OnDeck,” “we,” “our,” or “us”)",
        "Pure Capital US LLC and its parents, subsidiaries, and affiliates "
        "(collectively, “Pure Capital,” “we,” “our,” or “us”)",
    ),
    ("At OnDeck, we’re committed", "At Pure Capital, we’re committed"),
    ("ads for OnDeck that", "ads for Pure Capital that"),
    ("not owned by OnDeck", "not owned by Pure Capital US LLC"),
    ("OnDeck employees cannot", "Pure Capital US LLC employees cannot"),
    ("As a subsidiary of Enova International, Inc. (“Enova”), with Enova or its subsidiaries",
     "With our parent companies, affiliates, and partners"),
    ("Headway Capital", "affiliated partners"),
    ("legal@ondeck.com", "legal@purecapital.us"),
    ("customerservice@ondeck.com", "info@purecapital.us"),
    ("optout@ondeck.com", "optout@purecapital.us"),
    ("1-888-994-1389", "(347) 201-2166"),
    ("(888) 269-4246", "(347) 201-2166"),
    ("(888) 556-3483", "(347) 201-2166"),
    ("1 (888) 556-3483", "(347) 201-2166"),
    ("ondeck.com", "purecapital.us"),
    ("www.ondeck.com", "purecapital.us"),
    (
        "OnDeck\n OnDeck Client Service Center\n 4700 W. Daybreak Pkwy., Suite 200\n South Jordan, UT 84009",
        "Pure Capital US LLC\nEmail: info@purecapital.us\nPhone: (347) 201-2166",
    ),
    ("view our Security Policy", "contact us regarding security practices"),
    ('"Do Not Sell or Share My Personal Information"', '"Do Not Sell or Share My Personal Information" (when available on our Site)'),
]

for old, new in replacements:
    source = source.replace(old, new)

source = re.sub(r"\bOnDeck\b", "Pure Capital US LLC", source)
source = re.sub(r"\bOn Deck\b", "Pure Capital US LLC", source)
source = source.replace("Pure Capital US LLC US LLC", "Pure Capital US LLC")
source = source.replace("Pure Capital US LLC’s Pure Capital", "Pure Capital’s")


def linkify(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(
        r"(https?://[^\s\)\]]+)",
        r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>',
        escaped,
    )
    escaped = escaped.replace('href="terms.html"', 'href="terms.html"')  # already escaped wrong - fix
    escaped = re.sub(
        r'&lt;a href="terms\.html"&gt;Terms of Use&lt;/a&gt;',
        '<a href="terms.html">Terms of Use</a>',
        escaped,
    )
    escaped = re.sub(
        r"terms\.html",
        lambda m: '<a href="terms.html">Terms of Use</a>' if "href" not in escaped[max(0, escaped.find(m.group()) - 20):m.start()] else m.group(),
        escaped,
    )
    # Fix double linkification - simpler approach after escape:
    return escaped


def linkify_simple(text: str) -> str:
    t = html.escape(text)
    t = re.sub(
        r"(https?://[^\s\)&]+)",
        r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>',
        t,
    )
    if "Terms of Use" in t and "terms.html" not in t:
        t = t.replace("Terms of Use", '<a href="terms.html">Terms of Use</a>', 1)
    return t


def is_section_heading(s: str) -> bool:
    m = re.match(r"^(\d{1,2})\.\s+(.+)", s)
    if not m:
        return False
    num, rest = int(m.group(1)), m.group(2)
    if rest.startswith("The right to") or rest.startswith("If we "):
        return False
    return num <= 13 and len(rest) < 80


def is_subheading(s: str) -> bool:
    if is_section_heading(s) or len(s) > 100 or s.endswith("."):
        return False
    keywords = (
        "Information You", "Information as", "Information We", "Third Party",
        "How We", "How You", "Platform Controls", "Advertising Industry",
        "Our Process", "Right to Opt", "Shine the Light", "Notice at",
        "Sale, Sharing", "Retention", "Your Rights", "Review and",
        "Marketing Communications", "Blog/", "Testimonials", "Google Analytics",
        "FullStory", "LiveRamp", "Other Types",
    )
    return any(s.startswith(k) for k in keywords) or s in {
        "Introduction", "Information You Provide", "Apply for Financing.",
    }


def parse_inline(text: str) -> str:
    """Bold italic markers from source."""
    t = html.escape(text)
    t = re.sub(r"_(.+?)_", r"<em>\1</em>", t)
    return t


def to_html(text: str) -> str:
    lines = text.split("\n")
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "Privacy Policy":
            i += 1
            continue

        if stripped.startswith("Effective as of") or stripped.startswith("Last updated"):
            out.append(f'<p class="legal-effective">{linkify_simple(stripped)}</p>')
            i += 1
            continue

        if stripped.startswith("We take privacy seriously"):
            out.append(f'<p class="legal-lead">{linkify_simple(stripped)}</p>')
            i += 1
            continue

        if is_section_heading(stripped):
            out.append(f"<h2>{linkify_simple(stripped)}</h2>")
            i += 1
            continue

        if stripped == "Introduction" or is_subheading(stripped):
            out.append(f"<h3>{linkify_simple(stripped)}</h3>")
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if row and not all(re.match(r"^-+$", c) for c in row):
                    rows.append(row)
                i += 1
            if rows:
                out.append('<table class="legal-table"><thead><tr>')
                for cell in rows[0]:
                    out.append(f"<th>{linkify_simple(cell)}</th>")
                out.append("</tr></thead><tbody>")
                for row in rows[1:]:
                    out.append("<tr>")
                    for cell in row:
                        out.append(f"<td>{linkify_simple(cell)}</td>")
                    out.append("</tr>")
                out.append("</tbody></table>")
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            items = []
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith("- ") or s.startswith("* "):
                    items.append(parse_inline(s[2:].strip()))
                    i += 1
                elif s.startswith("    - "):
                    items.append(parse_inline(s.strip().lstrip("- ").strip()))
                    i += 1
                else:
                    break
            out.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s", stripped) and len(stripped) < 120:
            items = []
            while i < len(lines):
                s = lines[i].strip()
                if re.match(r"^\d+\.\s", s):
                    items.append(linkify_simple(re.sub(r"^\d+\.\s*", "", s)))
                    i += 1
                else:
                    break
            out.append("<ol>" + "".join(f"<li>{it}</li>" for it in items) + "</ol>")
            continue

        para = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                break
            if is_section_heading(nxt) or nxt == "Introduction" or is_subheading(nxt):
                break
            if nxt.startswith("- ") or nxt.startswith("|"):
                break
            if re.match(r"^\d+\.\s", nxt) and len(nxt) < 120:
                break
            para.append(nxt)
            i += 1
        out.append(f"<p>{linkify_simple(' '.join(para))}</p>")

    return "\n".join(out)


_privacy_seo = render_seo_tags(PAGES["privacy.html"])

HEADER = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{_privacy_seo}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="site-header">
    <div class="header-container">
      <a href="index.html" class="logo">
        <img src="assets/IMG_20260531_000449-removebg-preview.png" alt="Pure Capital US LLC — business funding" width="180" height="52" />
      </a>
      <nav class="main-nav" aria-label="Main navigation">
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="apply.html">Apply</a></li>
          <li><a href="terms.html">Terms of Use</a></li>
        </ul>
      </nav>
      <div class="header-actions">
        <a href="apply.html" class="btn btn-primary">Apply Now</a>
      </div>
      <button class="menu-toggle" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
  <nav class="mobile-nav" aria-label="Mobile navigation">
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="apply.html">Apply</a></li>
      <li><a href="terms.html">Terms of Use</a></li>
    </ul>
  </nav>
  <main class="legal-page">
    <div class="legal-container">
      <p class="legal-lead">We take privacy seriously. At Pure Capital, we’re committed to keeping our customers’ information safe, and being transparent about how we collect and use the data from your account.</p>
      <h1>Privacy Policy</h1>
      <p class="legal-effective">Effective as of May 16, 2026 · Last updated May 16, 2026</p>
      <nav class="legal-toc" aria-label="Privacy Policy sections">
        <p><strong>This Privacy Policy covers the following topics:</strong></p>
        <ol>
          <li><a href="#section-1">Information We Collect</a></li>
          <li><a href="#section-2">How We Use Your Information</a></li>
          <li><a href="#section-3">How We Share Your Information</a></li>
          <li><a href="#section-4">Cookies and Other Tracking Technologies</a></li>
          <li><a href="#section-5">Opt-Out Preference Signals</a></li>
          <li><a href="#section-6">Choices About Your Information</a></li>
          <li><a href="#section-7">Security</a></li>
          <li><a href="#section-8">Third Party Links</a></li>
          <li><a href="#section-9">Children’s Privacy</a></li>
          <li><a href="#section-10">Notice to Nevada Residents</a></li>
          <li><a href="#section-11">Notice to California Residents</a></li>
          <li><a href="#section-12">Accessibility</a></li>
          <li><a href="#section-13">How to Contact Us</a></li>
        </ol>
      </nav>
"""

FOOTER = """
    </div>
  </main>
  <footer class="site-footer">
    <div class="footer-bottom">
      <div class="footer-container">
        <p>&copy; 2026 Pure Capital US LLC. <a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms of Use</a></p>
      </div>
    </div>
  </footer>
  <script src="main.js"></script>
</body>
</html>
"""

body = to_html(source)

def add_ids(html_body: str) -> str:
    return re.sub(
        r"<h2>(\d+)\.\s([^<]+)</h2>",
        lambda m: f'<h2 id="section-{m.group(1)}">{m.group(1)}. {m.group(2)}</h2>',
        html_body,
    )

body = add_ids(body)

(ROOT / "privacy.html").write_text(HEADER + body + FOOTER, encoding="utf-8")
print(f"Wrote privacy.html ({len(body)} chars)")
