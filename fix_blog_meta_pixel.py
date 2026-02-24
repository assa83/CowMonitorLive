#!/usr/bin/env python3
"""
fix_blog_meta_pixel.py - Insert Meta Pixel code before </head> in all blog files.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")

META_PIXEL = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '3237109576678867');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=3237109576678867&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->"""

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
        if "Meta Pixel Code" in content:
            continue
        if "</head>" in content:
            content = content.replace("</head>", META_PIXEL + "\n</head>")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            print(f"  UPDATED: {lang}/{filename}")

print(f"\nDone! {count} files updated.")
