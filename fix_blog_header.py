#!/usr/bin/env python3
"""
fix_blog_header.py - Unify blog header (above the fold) to match home.html style.
Changes CSS (backdrop-filter, letter-spacing, nav-links style) and
HTML structure (nav-right wrapper with plain text links).
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")

# Translated nav labels per language
NAV = {
    "it": {"home": "Home", "blog": "Blog"},
    "en": {"home": "Home", "blog": "Blog"},
    "es": {"home": "Inicio", "blog": "Blog"},
    "fr": {"home": "Accueil", "blog": "Blog"},
    "de": {"home": "Startseite", "blog": "Blog"},
}


def fix_css(content):
    """Add backdrop-filter, letter-spacing; replace .nav-link with .nav-links styles."""

    # ── Article CSS (spaced format) ──
    content = content.replace(
        "header { padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); background: rgba(0,0,0,0.95); position: sticky; top: 0; z-index: 1000; }",
        "header { padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); background: rgba(0,0,0,0.95); position: sticky; top: 0; z-index: 1000; backdrop-filter: blur(10px); }"
    )
    content = content.replace(
        ".logo { font-weight: 900; font-size: 1.4rem; text-transform: uppercase; text-decoration: none; color: #fff; }",
        ".logo { font-weight: 900; font-size: 1.4rem; letter-spacing: -1px; text-transform: uppercase; text-decoration: none; color: #fff; }"
    )
    content = content.replace(
        ".nav-link { font-weight: 700; color: #fff; text-decoration: none; font-size: 0.9rem; padding: 10px 20px; border: 1px solid #333; border-radius: 50px; transition: 0.3s; }\n.nav-link:hover { background: #fff; color: #000; }",
        ".nav-right { display: flex; align-items: center; }\n.nav-links { display: flex; gap: 20px; align-items: center; }\n.nav-links a { color: #fff; text-decoration: none; font-weight: 700; font-size: 0.9rem; transition: 0.3s; }\n.nav-links a:hover { color: var(--primary); }"
    )

    # ── Blog listing CSS (minified format) ──
    content = content.replace(
        "header{padding:15px 5%;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border-color);background:rgba(0,0,0,0.95);position:sticky;top:0;z-index:1000}",
        "header{padding:15px 5%;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border-color);background:rgba(0,0,0,0.95);position:sticky;top:0;z-index:1000;backdrop-filter:blur(10px)}"
    )
    content = content.replace(
        ".logo{font-weight:900;font-size:1.4rem;text-transform:uppercase;text-decoration:none;color:#fff}",
        ".logo{font-weight:900;font-size:1.4rem;letter-spacing:-1px;text-transform:uppercase;text-decoration:none;color:#fff}"
    )
    content = content.replace(
        ".nav-link{font-weight:700;color:#fff;text-decoration:none;font-size:.9rem;padding:10px 20px;border:1px solid #333;border-radius:50px;transition:.3s}\n.nav-link:hover{background:#fff;color:#000}",
        ".nav-right{display:flex;align-items:center}\n.nav-links{display:flex;gap:20px;align-items:center}\n.nav-links a{color:#fff;text-decoration:none;font-weight:700;font-size:.9rem;transition:.3s}\n.nav-links a:hover{color:var(--primary)}"
    )

    return content


def fix_article_html(content, lang):
    """Replace article header HTML with nav-right structure."""
    nav = NAV[lang]
    new_header = (
        '<header>\n'
        '<a href="../../home.html" class="logo">COW DELAYS<span> MONITOR</span></a>\n'
        '<div class="nav-right">\n'
        '    <nav class="nav-links">\n'
        f'        <a href="../../home.html">{nav["home"]}</a>\n'
        f'        <a href="./blog.html" style="color:#ff9f1c">{nav["blog"]}</a>\n'
        '    </nav>\n'
        '    <div style="margin-left: 20px;">\n'
        '        <select id="lang-select">'
    )
    # Match: <header> ... <a class="nav-link">...</a> ... <select id="lang-select">
    pattern = re.compile(
        r'<header>\s*\n'
        r'<a href="../../home\.html" class="logo">COW DELAYS<span> MONITOR</span></a>\s*\n'
        r'<a href="\./blog\.html" class="nav-link">[^<]+</a>\s*\n'
        r'<div style="margin-left: 20px;">\s*\n'
        r'\s*<select id="lang-select">',
        re.MULTILINE
    )
    content = pattern.sub(new_header, content)

    # Fix closing: </select>\n</div>\n</header> → add </div> for nav-right
    content = content.replace(
        '  </select>\n</div>\n</header>',
        '        </select>\n'
        '    </div>\n'
        '</div>\n'
        '</header>'
    )

    return content


def fix_listing_html(content, lang):
    """Replace blog listing header HTML with nav-right structure."""
    nav = NAV[lang]
    new_header = (
        '  <header>\n'
        '    <a href="../../home.html" class="logo">COW DELAYS<span> MONITOR</span></a>\n'
        '    <div class="nav-right">\n'
        '        <nav class="nav-links">\n'
        f'            <a href="../../home.html">{nav["home"]}</a>\n'
        '        </nav>\n'
        '        <div style="margin-left: 20px;">\n'
        '  <select id="lang-select">'
    )
    # Match listing header pattern
    pattern = re.compile(
        r'  <header>\s*\n'
        r'    <a href="../../home\.html" class="logo">COW DELAYS<span> MONITOR</span></a>\s*\n'
        r'    <a href="../../home\.html" class="nav-link">[^<]+</a>\s*\n'
        r'    <div style="margin-left: 20px;">\s*\n'
        r'  <select id="lang-select">',
        re.MULTILINE
    )
    content = pattern.sub(new_header, content)

    # Fix closing for listing
    content = content.replace(
        '  </select>\n</div>\n  </header>',
        '  </select>\n'
        '        </div>\n'
        '    </div>\n'
        '  </header>'
    )

    return content


def main():
    count = 0
    for lang in ["it", "en", "es", "fr", "de"]:
        lang_dir = os.path.join(BLOG_DIR, lang)
        if not os.path.isdir(lang_dir):
            continue
        for filename in sorted(os.listdir(lang_dir)):
            if not filename.endswith(".html"):
                continue
            filepath = os.path.join(lang_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            original = content

            content = fix_css(content)

            if filename == "blog.html":
                content = fix_listing_html(content, lang)
            else:
                content = fix_article_html(content, lang)

            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
                print(f"  UPDATED: {lang}/{filename}")

    print(f"\nDone! {count} files updated.")


if __name__ == "__main__":
    main()
