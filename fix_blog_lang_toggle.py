#!/usr/bin/env python3
"""
fix_blog_lang_toggle.py - Add #lang-select styling to all blog files
to match the home.html toggle appearance.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")

STYLE_RULE = "#lang-select { background: #111; color: #2ecc71; border: 1px solid #333; padding: 5px 10px; border-radius: 5px; font-weight: 700; cursor: pointer; text-transform: uppercase; }\n"

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
        if "#lang-select" in content:
            continue
        if "</style>" in content:
            content = content.replace("</style>", STYLE_RULE + "</style>")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1

print(f"Done! {count} files updated.")
