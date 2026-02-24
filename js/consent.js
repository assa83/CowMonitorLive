/* Cow Delays Monitor - Cookie Consent Manager (GDPR / Garante IT) */
(function () {
  'use strict';

  /* ── 1. Translations ─────────────────────────────────────── */
  var T = {
    it: {
      banner: 'Questo sito utilizza cookie analitici e di marketing. Puoi accettare, rifiutare o personalizzare le tue preferenze.',
      accept: 'Accetta tutto',
      reject: 'Rifiuta tutto',
      customize: 'Personalizza',
      save: 'Salva preferenze',
      necessary: 'Necessari',
      necessaryDesc: 'Cookie tecnici indispensabili per il funzionamento del sito.',
      analytics: 'Analitici',
      analyticsDesc: 'Ci aiutano a capire come viene usato il sito (Google Analytics).',
      marketing: 'Marketing',
      marketingDesc: 'Utilizzati per mostrare contenuti e pubblicita\u0300 pertinenti (Meta Pixel).',
      privacyLink: 'Privacy Policy',
      cookieLink: 'Cookie Policy'
    },
    en: {
      banner: 'This site uses analytics and marketing cookies. You can accept, reject or customize your preferences.',
      accept: 'Accept all',
      reject: 'Reject all',
      customize: 'Customize',
      save: 'Save preferences',
      necessary: 'Necessary',
      necessaryDesc: 'Essential cookies required for the site to function.',
      analytics: 'Analytics',
      analyticsDesc: 'Help us understand how the site is used (Google Analytics).',
      marketing: 'Marketing',
      marketingDesc: 'Used to show relevant content and ads (Meta Pixel).',
      privacyLink: 'Privacy Policy',
      cookieLink: 'Cookie Policy'
    },
    es: {
      banner: 'Este sitio utiliza cookies anal\u00edticas y de marketing. Puedes aceptar, rechazar o personalizar tus preferencias.',
      accept: 'Aceptar todo',
      reject: 'Rechazar todo',
      customize: 'Personalizar',
      save: 'Guardar preferencias',
      necessary: 'Necesarias',
      necessaryDesc: 'Cookies t\u00e9cnicas esenciales para el funcionamiento del sitio.',
      analytics: 'Anal\u00edticas',
      analyticsDesc: 'Nos ayudan a entender c\u00f3mo se usa el sitio (Google Analytics).',
      marketing: 'Marketing',
      marketingDesc: 'Se usan para mostrar contenido y publicidad relevante (Meta Pixel).',
      privacyLink: 'Pol\u00edtica de Privacidad',
      cookieLink: 'Pol\u00edtica de Cookies'
    },
    fr: {
      banner: 'Ce site utilise des cookies analytiques et marketing. Vous pouvez accepter, refuser ou personnaliser vos pr\u00e9f\u00e9rences.',
      accept: 'Tout accepter',
      reject: 'Tout refuser',
      customize: 'Personnaliser',
      save: 'Enregistrer',
      necessary: 'N\u00e9cessaires',
      necessaryDesc: 'Cookies techniques essentiels au fonctionnement du site.',
      analytics: 'Analytiques',
      analyticsDesc: 'Nous aident \u00e0 comprendre l\u2019utilisation du site (Google Analytics).',
      marketing: 'Marketing',
      marketingDesc: 'Utilis\u00e9s pour afficher du contenu et des publicit\u00e9s pertinents (Meta Pixel).',
      privacyLink: 'Politique de confidentialit\u00e9',
      cookieLink: 'Politique des cookies'
    },
    de: {
      banner: 'Diese Website verwendet Analyse- und Marketing-Cookies. Sie k\u00f6nnen akzeptieren, ablehnen oder Ihre Einstellungen anpassen.',
      accept: 'Alle akzeptieren',
      reject: 'Alle ablehnen',
      customize: 'Anpassen',
      save: 'Einstellungen speichern',
      necessary: 'Notwendige',
      necessaryDesc: 'Technisch notwendige Cookies f\u00fcr den Betrieb der Website.',
      analytics: 'Analytische',
      analyticsDesc: 'Helfen uns zu verstehen, wie die Website genutzt wird (Google Analytics).',
      marketing: 'Marketing',
      marketingDesc: 'Werden verwendet, um relevante Inhalte und Werbung anzuzeigen (Meta Pixel).',
      privacyLink: 'Datenschutzerkl\u00e4rung',
      cookieLink: 'Cookie-Richtlinie'
    }
  };

  /* ── 2. Cookie helpers ───────────────────────────────────── */
  var COOKIE_NAME = 'cm_consent';

  function getConsent() {
    var m = document.cookie.match(new RegExp('(?:^|; )' + COOKIE_NAME + '=([^;]*)'));
    if (!m) return null;
    try { return JSON.parse(decodeURIComponent(m[1])); } catch (e) { return null; }
  }

  function setConsent(prefs) {
    var val = JSON.stringify({ analytics: !!prefs.analytics, marketing: !!prefs.marketing, timestamp: new Date().toISOString() });
    var d = new Date(); d.setFullYear(d.getFullYear() + 1);
    document.cookie = COOKIE_NAME + '=' + encodeURIComponent(val) + ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
  }

  /* ── 3. Language detection ───────────────────────────────── */
  function detectLang() {
    var ls = null;
    try { ls = localStorage.getItem('lang'); } catch (e) { /* private browsing */ }
    if (ls && T[ls]) return ls;
    var html = document.documentElement.lang;
    if (html && T[html]) return html;
    var path = window.location.pathname;
    var langs = ['it', 'en', 'es', 'fr', 'de'];
    for (var i = 0; i < langs.length; i++) {
      if (path.indexOf('/blog/' + langs[i] + '/') !== -1) return langs[i];
    }
    return 'it';
  }

  /* ── 4. Load Analytics (GA4 + scroll depth) ──────────────── */
  var analyticsLoaded = false;
  function loadAnalytics() {
    if (analyticsLoaded) return;
    analyticsLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-KMBRBVCGBH';
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', 'G-KMBRBVCGBH', { send_page_view: true });
    // Scroll depth tracking
    var milestones = [25, 50, 75, 90], fired = {};
    window.addEventListener('scroll', function () {
      var h = document.body.scrollHeight - window.innerHeight;
      if (h <= 0) return;
      var pct = Math.round((window.scrollY / h) * 100);
      milestones.forEach(function (m) {
        if (pct >= m && !fired[m]) {
          fired[m] = true;
          window.gtag('event', 'scroll_depth', { depth_percentage: m });
          if (m === 75 && typeof window.fbq === 'function') window.fbq('trackCustom', 'DeepScroll', { depth: 75 });
        }
      });
    }, { passive: true });
  }

  /* ── 5. Load Marketing (Meta Pixel) ──────────────────────── */
  var marketingLoaded = false;
  function loadMarketing() {
    if (marketingLoaded) return;
    marketingLoaded = true;
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
      n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', '3237109576678867');
    window.fbq('track', 'PageView');
  }

  /* ── 6. Render banner ────────────────────────────────────── */
  function renderBanner() {
    var lang = detectLang();
    var t = T[lang] || T.it;

    // Resolve policy paths (relative: works from root and blog subfolders)
    var base = '';
    if (window.location.pathname.indexOf('/blog/') !== -1) base = '../../';
    var privacyHref = base + 'privacy.html';
    var cookieHref = base + 'cookie-policy.html';

    var overlay = document.createElement('div');
    overlay.id = 'cm-consent-overlay';
    overlay.innerHTML =
      '<div id="cm-consent-banner">' +
        '<div class="cm-text">' +
          '<p>' + t.banner + '</p>' +
          '<p class="cm-links"><a href="' + privacyHref + '">' + t.privacyLink + '</a> | <a href="' + cookieHref + '">' + t.cookieLink + '</a></p>' +
        '</div>' +
        '<div class="cm-buttons">' +
          '<button id="cm-accept">' + t.accept + '</button>' +
          '<button id="cm-reject">' + t.reject + '</button>' +
          '<button id="cm-customize">' + t.customize + '</button>' +
        '</div>' +
        '<div id="cm-prefs" style="display:none">' +
          '<label class="cm-toggle">' +
            '<span><strong>' + t.necessary + '</strong><br><small>' + t.necessaryDesc + '</small></span>' +
            '<input type="checkbox" checked disabled><span class="cm-slider"></span>' +
          '</label>' +
          '<label class="cm-toggle">' +
            '<span><strong>' + t.analytics + '</strong><br><small>' + t.analyticsDesc + '</small></span>' +
            '<input type="checkbox" id="cm-tog-analytics"><span class="cm-slider"></span>' +
          '</label>' +
          '<label class="cm-toggle">' +
            '<span><strong>' + t.marketing + '</strong><br><small>' + t.marketingDesc + '</small></span>' +
            '<input type="checkbox" id="cm-tog-marketing"><span class="cm-slider"></span>' +
          '</label>' +
          '<button id="cm-save">' + t.save + '</button>' +
        '</div>' +
      '</div>';

    // Inject styles
    var style = document.createElement('style');
    style.textContent =
      '#cm-consent-overlay{position:fixed;bottom:0;left:0;right:0;z-index:9999;padding:16px;pointer-events:none}' +
      '#cm-consent-banner{pointer-events:auto;background:#111;border:1px solid #333;border-radius:14px;padding:24px;max-width:720px;margin:0 auto;font-family:Inter,sans-serif;color:#fff;font-size:14px;box-shadow:0 -4px 24px rgba(0,0,0,.6)}' +
      '#cm-consent-banner .cm-text p{margin:0 0 12px;line-height:1.5}' +
      '#cm-consent-banner .cm-links a{color:#2ecc71;text-decoration:underline;font-size:13px}' +
      '#cm-consent-banner .cm-buttons{display:flex;gap:10px;flex-wrap:wrap}' +
      '#cm-consent-banner button{border:none;border-radius:8px;padding:12px 22px;font-weight:700;font-size:14px;cursor:pointer;flex:1;min-width:120px;text-align:center}' +
      '#cm-accept{background:#2ecc71;color:#000}' +
      '#cm-reject{background:#333;color:#fff}' +
      '#cm-customize{background:transparent;color:#2ecc71;border:1px solid #2ecc71!important}' +
      '#cm-save{background:#2ecc71;color:#000;margin-top:12px;width:100%}' +
      '#cm-prefs{margin-top:16px;border-top:1px solid #333;padding-top:16px}' +
      '.cm-toggle{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:14px}' +
      '.cm-toggle span:first-child{flex:1}' +
      '.cm-toggle small{color:#888}' +
      '.cm-toggle input{width:44px;height:24px;appearance:none;-webkit-appearance:none;background:#444;border-radius:12px;position:relative;cursor:pointer;outline:none;flex-shrink:0}' +
      '.cm-toggle input::before{content:"";position:absolute;width:18px;height:18px;border-radius:50%;background:#fff;top:3px;left:3px;transition:transform .2s}' +
      '.cm-toggle input:checked{background:#2ecc71}' +
      '.cm-toggle input:checked::before{transform:translateX(20px)}' +
      '.cm-toggle input:disabled{opacity:.6;cursor:default}' +
      '@media(max-width:600px){#cm-consent-banner .cm-buttons{flex-direction:column}#cm-consent-banner button{min-width:auto}}';
    document.head.appendChild(style);
    document.body.appendChild(overlay);

    // Wire events
    document.getElementById('cm-accept').addEventListener('click', function () {
      applyConsent({ analytics: true, marketing: true });
      closeBanner();
    });
    document.getElementById('cm-reject').addEventListener('click', function () {
      applyConsent({ analytics: false, marketing: false });
      closeBanner();
    });
    document.getElementById('cm-customize').addEventListener('click', function () {
      var p = document.getElementById('cm-prefs');
      p.style.display = p.style.display === 'none' ? 'block' : 'none';
    });
    document.getElementById('cm-save').addEventListener('click', function () {
      applyConsent({
        analytics: document.getElementById('cm-tog-analytics').checked,
        marketing: document.getElementById('cm-tog-marketing').checked
      });
      closeBanner();
    });
  }

  function closeBanner() {
    var el = document.getElementById('cm-consent-overlay');
    if (el) el.parentNode.removeChild(el);
  }

  /* ── 7. Apply consent ────────────────────────────────────── */
  function applyConsent(prefs) {
    setConsent(prefs);
    if (prefs.analytics) loadAnalytics();
    if (prefs.marketing) loadMarketing();
  }

  /* ── 8. Global API ───────────────────────────────────────── */
  window.CmConsent = {
    show: function () {
      closeBanner();
      renderBanner();
      // Pre-fill toggles from existing consent
      var c = getConsent();
      if (c) {
        var ta = document.getElementById('cm-tog-analytics');
        var tm = document.getElementById('cm-tog-marketing');
        if (ta) ta.checked = !!c.analytics;
        if (tm) tm.checked = !!c.marketing;
      }
    }
  };

  /* ── 9. Init ─────────────────────────────────────────────── */
  var consent = getConsent();
  if (consent) {
    applyConsent(consent);
  } else {
    // Show banner once DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', renderBanner);
    } else {
      renderBanner();
    }
  }
})();
