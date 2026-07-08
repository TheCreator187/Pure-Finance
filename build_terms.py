#!/usr/bin/env python3
"""Build terms.html from terms-source.txt with Pure Capital US LLC replacements."""

import html
import re
from pathlib import Path

from seo import PAGES, render_seo_tags

ROOT = Path(__file__).parent
source = (ROOT / "terms-source.txt").read_text(encoding="utf-8")

replacements = [
    (
        "On Deck Capital, Inc., ODK Capital, LLC, and its parents, subsidiaries, and affiliates "
        "doing business under the OnDeck brand (collectively, “OnDeck,” “we,” “our,” or “us”)",
        "Pure Capital US LLC and its parents, subsidiaries, and affiliates "
        "(collectively, “Pure Capital,” “we,” “our,” or “us”)",
    ),
    ("ODK Capital, LLC’s (“OnDeck”)", "Pure Capital US LLC’s (“Pure Capital”)"),
    ("Ondeck’s", "Pure Capital’s"),
    ("OnDeck’s", "Pure Capital’s"),
    ("YOU AND ONDECK AGREE", "YOU AND PURE CAPITAL US LLC AGREE"),
    ("Headway Capital, LLC", "affiliated lending partners"),
    ("legal@ondeck.com", "legal@purecapital.us"),
    ("customerservice@ondeck.com", "info@purecapital.us"),
    ("(888) 269-4246", "(347) 201-2166"),
    ("(888) 556-3483", "(347) 201-2166"),
    ("1-888- 556-3483", "(347) 201-2166"),
    ("1 (888) 556-3483", "(347) 201-2166"),
    ("ondeck.com", "purecapital.us"),
    ("www.ondeck.com", "purecapital.us"),
    ("https://www.purecapital.us/privacy", "privacy.html"),
    (
        "OnDeck\nAttention: Legal Department\n175 West Jackson Blvd.\nSuite 600\nChicago, IL 60604",
        "Pure Capital US LLC\nAttention: Legal Department\nEmail: legal@purecapital.us",
    ),
    (
        "OnDeck\nOnDeck Client Service Center\n4700 W. Daybreak Pkwy., Suite 200\nSouth Jordan, UT 84009",
        "Pure Capital US LLC\nClient Service\nEmail: info@purecapital.us\nPhone: (347) 201-2166",
    ),
    (
        "4700 W. Daybreak Pkwy., Suite 200, South Jordan, UT 84009, Attn: Director of Operations",
        "info@purecapital.us, Attn: Director of Operations",
    ),
    ("text “STOP” to 35124", "text “STOP” to the number from which you received the message"),
    ("text “HELP” to 35124", "text “HELP” to the number from which you received the message"),
]

for old, new in replacements:
    source = source.replace(old, new)

source = re.sub(r"\bOnDeck\b", "Pure Capital US LLC", source)
source = source.replace("Pure Capital US LLC US LLC", "Pure Capital US LLC")
source = source.replace("Pure Capital US LLC’s Pure Capital", "Pure Capital’s")


def linkify(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(
        r"(https?://[^\s<]+|privacy\.html)",
        r'<a href="\1">\1</a>',
        escaped,
    )
    return escaped


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

        if stripped == "Terms of Use":
            out.append("<h1>Terms of Use</h1>")
            i += 1
            continue

        if stripped.startswith("Updated and effective"):
            out.append(f'<p class="legal-effective">{linkify(stripped)}</p>')
            i += 1
            continue

        if re.match(r"^\d+\.\s", stripped):
            out.append(f"<h2>{linkify(stripped)}</h2>")
            i += 1
            continue

        if (
            len(stripped) < 90
            and not stripped.endswith(".")
            and not stripped.startswith("http")
            and re.match(r"^[A-Z]", stripped)
            and ";" not in stripped
            and stripped[0].isupper()
            and not stripped.isupper()
            and (
                stripped in {
                    "Information You Provide to Us",
                    "Information We Collect Automatically",
                    "Information We Collect Through Your Use of the Website",
                    "Google Analytics",
                    "FullStory",
                    "LiveRamp Authenticated Traffic Solution",
                    "Other Types of Collecting Activities",
                    "Advertising",
                }
                or stripped.endswith("Us")
                or stripped.endswith("Activities")
                or stripped == "Advertising"
            )
        ):
            out.append(f"<h3>{linkify(stripped)}</h3>")
            i += 1
            continue

        if stripped.isupper() and len(stripped) > 12 and not stripped.startswith("HTTP"):
            out.append(f"<h3>{linkify(stripped)}</h3>")
            i += 1
            continue

        if stripped.startswith("For Ohio applicants"):
            out.append(f"<p><strong>{linkify(stripped)}</strong></p>")
            i += 1
            continue

        if line.startswith("    ") or (stripped.startswith("•") or stripped.startswith("- ")):
            items = []
            while i < len(lines):
                s = lines[i].strip()
                if not s:
                    i += 1
                    break
                if s.startswith("•") or s.startswith("- ") or lines[i].startswith("    "):
                    items.append(s.lstrip("•- ").strip())
                    i += 1
                else:
                    break
            out.append("<ul>" + "".join(f"<li>{linkify(it)}</li>" for it in items) + "</ul>")
            continue

        para = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^\d+\.\s", lines[i].strip()):
            nxt = lines[i].strip()
            if nxt.isupper() and len(nxt) > 12:
                break
            if nxt.startswith("•") or lines[i].startswith("    "):
                break
            para.append(nxt)
            i += 1
        out.append(f"<p>{linkify(' '.join(para))}</p>")

    return "\n".join(out)


_terms_seo = render_seo_tags(PAGES["terms.html"])

HEADER = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{_terms_seo}
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
          <li><a href="privacy.html">Privacy Policy</a></li>
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
      <li><a href="privacy.html">Privacy Policy</a></li>
    </ul>
  </nav>
  <main class="legal-page">
    <div class="legal-container">
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
(ROOT / "terms.html").write_text(HEADER + body + FOOTER, encoding="utf-8")
print(f"Wrote terms.html ({len(body)} chars body)")
