#!/usr/bin/env python3
"""Inject SEO tags into HTML pages and write robots.txt / sitemap.xml."""

import re
from pathlib import Path

from seo import PAGES, render_robots, render_seo_tags, render_sitemap

ROOT = Path(__file__).parent


def inject_file(filename: str) -> None:
    path = ROOT / filename
    if not path.exists() or filename not in PAGES:
        return

    content = path.read_text(encoding="utf-8")
    page = PAGES[filename]
    seo_block = render_seo_tags(page)

    match = re.search(r"<head>(.*?)</head>", content, re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError(f"<head> not found in {filename}")

    head_inner = match.group(1)
    asset_lines = []
    for line in head_inner.splitlines():
        stripped = line.strip()
        if stripped.startswith("<link rel=\"preconnect") or stripped.startswith(
            "<link href=\"https://fonts"
        ) or stripped.startswith("<link rel=\"stylesheet"):
            asset_lines.append("  " + stripped + "\n")

    new_head = (
        "  <meta charset=\"UTF-8\" />\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
        f"{seo_block}\n"
        + "".join(asset_lines)
    )

    content = content[: match.start(1)] + "\n" + new_head + content[match.end(1) :]
    path.write_text(content, encoding="utf-8")
    print(f"Updated {filename}")


def main() -> None:
    for filename in PAGES:
        inject_file(filename)

    (ROOT / "robots.txt").write_text(render_robots(), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8")
    print("Wrote robots.txt and sitemap.xml")


if __name__ == "__main__":
    main()
