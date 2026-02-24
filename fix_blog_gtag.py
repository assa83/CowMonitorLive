#!/usr/bin/env python3
"""
fix_blog_gtag.py - Replace basic gtag with enhanced gtag + scroll depth
in all blog HTML files (articles + listing pages, all languages).
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")

OLD_GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KMBRBVCGBH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-KMBRBVCGBH');
</script>"""

NEW_GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KMBRBVCGBH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-KMBRBVCGBH', { 'send_page_view': true });

  // SCROLL DEPTH
  const scrollMilestones = [25, 50, 75, 90];
  const scrollFired = {};
  window.addEventListener('scroll', () => {
    const pct = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
    scrollMilestones.forEach(m => {
      if (pct >= m && !scrollFired[m]) {
        scrollFired[m] = true;
        gtag('event', 'scroll_depth', { depth_percentage: m });
      }
    });
  }, { passive: true });
</script>"""

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
        if OLD_GTAG in content:
            content = content.replace(OLD_GTAG, NEW_GTAG)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            print(f"  UPDATED: {lang}/{filename}")

print(f"\nDone! {count} files updated.")
