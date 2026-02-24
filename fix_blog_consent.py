#!/usr/bin/env python3
"""
fix_blog_consent.py
Processes all blog HTML files in blog/{it,en,es,fr,de}/:
  1. Removes inline GA4 scripts
  2. Removes inline Meta Pixel scripts
  3. Adds consent.js before </head>
  4. Updates footer with privacy/cookie links
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, 'blog')

# Localized footer texts
FOOTER_TEXTS = {
    'it': {
        'back': 'Torna alla Home',
        'privacy': 'Privacy Policy',
        'cookie': 'Cookie Policy',
        'settings': 'Impostazioni Cookie'
    },
    'en': {
        'back': 'Back to Home',
        'privacy': 'Privacy Policy',
        'cookie': 'Cookie Policy',
        'settings': 'Cookie Settings'
    },
    'es': {
        'back': 'Volver a Inicio',
        'privacy': 'Pol\u00edtica de Privacidad',
        'cookie': 'Pol\u00edtica de Cookies',
        'settings': 'Configuraci\u00f3n de Cookies'
    },
    'fr': {
        'back': "Retour \u00e0 l'accueil",
        'privacy': 'Politique de confidentialit\u00e9',
        'cookie': 'Politique des cookies',
        'settings': 'Param\u00e8tres des cookies'
    },
    'de': {
        'back': 'Zur Startseite',
        'privacy': 'Datenschutzerkl\u00e4rung',
        'cookie': 'Cookie-Richtlinie',
        'settings': 'Cookie-Einstellungen'
    }
}

# Regex patterns
# GA4: from "<!-- Google tag" through two </script> closings (async tag + config/scroll block)
GA4_PATTERN = re.compile(
    r'<!-- Google tag \(gtag\.js\) -->.*?</script>\s*<script>.*?</script>\s*',
    re.DOTALL
)

# Leftover GA4 config block (if the comment was already stripped in a previous run)
GA4_LEFTOVER_PATTERN = re.compile(
    r'<script>\s*window\.dataLayer\s*=\s*window\.dataLayer.*?</script>\s*',
    re.DOTALL
)

# Meta Pixel: from <!-- Meta Pixel Code --> to <!-- End Meta Pixel Code -->
META_PATTERN = re.compile(
    r'<!-- Meta Pixel Code -->.*?<!-- End Meta Pixel Code -->\s*',
    re.DOTALL
)

# Footer pattern - matches the entire <footer>...</footer> block
FOOTER_PATTERN = re.compile(
    r'<footer>.*?</footer>',
    re.DOTALL
)

CONSENT_SCRIPT = '<script src="/js/consent.js"></script>\n'


def get_new_footer(lang):
    """Generate the new footer HTML for a given language."""
    t = FOOTER_TEXTS.get(lang, FOOTER_TEXTS['it'])
    return f'''<footer>
        <p>&copy; 2026 Cow Delays Monitor Pro - <a href="../../home.html" style="color:#666">{t['back']}</a></p>
        <p style="margin-top:10px;font-size:0.8rem;">
            <a href="../../privacy.html" style="color:#666">{t['privacy']}</a> |
            <a href="../../cookie-policy.html" style="color:#666">{t['cookie']}</a> |
            <a href="#" onclick="window.CmConsent.show();return false;" style="color:#666">{t['settings']}</a>
        </p>
    </footer>'''


def process_file(filepath, lang):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Remove GA4 inline scripts
    content = GA4_PATTERN.sub('', content)

    # 1b. Remove leftover GA4 config block (if comment was already stripped)
    content = GA4_LEFTOVER_PATTERN.sub('', content)

    # 2. Remove Meta Pixel inline scripts
    content = META_PATTERN.sub('', content)

    # 3. Add consent.js before </head> (if not already there)
    if 'consent.js' not in content:
        content = content.replace('</head>', CONSENT_SCRIPT + '</head>')

    # 4. Update footer
    new_footer = get_new_footer(lang)
    content = FOOTER_PATTERN.sub(new_footer, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    langs = ['it', 'en', 'es', 'fr', 'de']
    total = 0
    modified = 0

    for lang in langs:
        lang_dir = os.path.join(BLOG_DIR, lang)
        if not os.path.isdir(lang_dir):
            print(f"[SKIP] Directory not found: {lang_dir}")
            continue

        files = glob.glob(os.path.join(lang_dir, '*.html'))
        for filepath in sorted(files):
            total += 1
            if process_file(filepath, lang):
                modified += 1
                print(f"[OK] {os.path.relpath(filepath, BASE_DIR)}")
            else:
                print(f"[--] {os.path.relpath(filepath, BASE_DIR)} (no changes)")

    # Also process root-level blog HTML files (if any)
    root_blog_files = glob.glob(os.path.join(BLOG_DIR, '*.html'))
    for filepath in sorted(root_blog_files):
        total += 1
        if process_file(filepath, 'it'):  # default to Italian for root files
            modified += 1
            print(f"[OK] {os.path.relpath(filepath, BASE_DIR)}")
        else:
            print(f"[--] {os.path.relpath(filepath, BASE_DIR)} (no changes)")

    print(f"\nDone: {modified}/{total} files modified.")


if __name__ == '__main__':
    main()
