#!/usr/bin/env python3
"""
fix_blog.py - Mass fix all blog HTML files for cowmonitor.live
Fixes: titles, meta descriptions, inLanguage, canonical URLs, og:url,
       mainEntityOfPage, og:image, FEBRUARY dates, and blog listing pages.
"""
import os
import re
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
BASE_URL = "https://cowmonitor.live"

# ─── Title translations: filename (without .html) -> {lang: title} ───
TITLES = {
    "come-accorgersi-subito-dei-ritardi-su-lely-astronaut": {
        "it": "Come accorgersi subito dei ritardi su Lely Astronaut",
        "en": "How to Immediately Spot Delays on Lely Astronaut",
        "es": "Como detectar de inmediato los retrasos en Lely Astronaut",
        "fr": "Comment detecter immediatement les retards sur Lely Astronaut",
        "de": "Wie man Verspatungen am Lely Astronaut sofort erkennt",
    },
    "come-accorgersi-subito-se-qualcosa-non-va-sul-robot-lely": {
        "it": "Come accorgersi subito se qualcosa non va sul robot Lely",
        "en": "How to Quickly Notice if Something Is Wrong with the Lely Robot",
        "es": "Como notar de inmediato si algo va mal con el robot Lely",
        "fr": "Comment remarquer immediatement si quelque chose ne va pas sur le robot Lely",
        "de": "Wie man sofort bemerkt wenn etwas mit dem Lely Roboter nicht stimmt",
    },
    "come-avere-finalmente-il-controllo-totale-su-lely-astronaut": {
        "it": "Come avere finalmente il controllo totale su Lely Astronaut",
        "en": "How to Finally Get Total Control Over Lely Astronaut",
        "es": "Como tener finalmente el control total de Lely Astronaut",
        "fr": "Comment avoir enfin le controle total sur Lely Astronaut",
        "de": "Wie man endlich die volle Kontrolle uber den Lely Astronaut bekommt",
    },
    "come-avere-il-pieno-controllo-del-tuo-lely-astronaut": {
        "it": "Come avere il pieno controllo del tuo Lely Astronaut",
        "en": "How to Have Full Control of Your Lely Astronaut",
        "es": "Como tener el control total de tu Lely Astronaut",
        "fr": "Comment avoir le plein controle de votre Lely Astronaut",
        "de": "Wie man die volle Kontrolle uber seinen Lely Astronaut hat",
    },
    "come-avere-il-pieno-controllo-della-mungitura-con-lely-astronaut": {
        "it": "Come avere il pieno controllo della mungitura con Lely Astronaut",
        "en": "How to Have Full Control of Milking with Lely Astronaut",
        "es": "Como tener el control total del ordeno con Lely Astronaut",
        "fr": "Comment avoir le plein controle de la traite avec Lely Astronaut",
        "de": "Wie man das Melken mit Lely Astronaut voll im Griff hat",
    },
    "come-avere-la-fetch-list-sempre-visibile-con-lely-astronaut": {
        "it": "Come avere la fetch list sempre visibile con Lely Astronaut",
        "en": "How to Always Have the Fetch List Visible with Lely Astronaut",
        "es": "Como tener la fetch list siempre visible con Lely Astronaut",
        "fr": "Comment avoir la fetch list toujours visible avec Lely Astronaut",
        "de": "Wie man die Fetch List mit Lely Astronaut immer sichtbar hat",
    },
    "come-avere-le-informazioni-del-robot-lely-sempre-visibili": {
        "it": "Come avere le informazioni del robot Lely sempre visibili",
        "en": "How to Always Have Lely Robot Information Visible",
        "es": "Como tener la informacion del robot Lely siempre visible",
        "fr": "Comment avoir les informations du robot Lely toujours visibles",
        "de": "Wie man die Lely Roboter Informationen immer sichtbar hat",
    },
    "come-avere-lely-astronaut-sempre-sotto-controllo-in-stalla": {
        "it": "Come avere Lely Astronaut sempre sotto controllo in stalla",
        "en": "How to Always Keep Lely Astronaut Under Control in the Barn",
        "es": "Como tener Lely Astronaut siempre bajo control en el establo",
        "fr": "Comment garder Lely Astronaut toujours sous controle dans l'etable",
        "de": "Wie man den Lely Astronaut im Stall immer unter Kontrolle hat",
    },
    "come-avere-sempre-sotto-controllo-il-robot-lely-astronaut": {
        "it": "Come avere sempre sotto controllo il robot Lely Astronaut",
        "en": "How to Always Keep the Lely Astronaut Robot Under Control",
        "es": "Como tener siempre bajo control el robot Lely Astronaut",
        "fr": "Comment toujours garder le robot Lely Astronaut sous controle",
        "de": "Wie man den Lely Astronaut Roboter immer unter Kontrolle hat",
    },
    "come-avere-sicurezza-con-il-robot-lely-astronaut": {
        "it": "Come avere sicurezza con il robot Lely Astronaut",
        "en": "How to Have Peace of Mind with the Lely Astronaut Robot",
        "es": "Como tener seguridad con el robot Lely Astronaut",
        "fr": "Comment avoir confiance avec le robot Lely Astronaut",
        "de": "Wie man Sicherheit mit dem Lely Astronaut Roboter hat",
    },
    "come-avere-tutto-sotto-controllo-senza-aprire-horizon": {
        "it": "Come avere tutto sotto controllo senza aprire Horizon",
        "en": "How to Keep Everything Under Control Without Opening Horizon",
        "es": "Como tener todo bajo control sin abrir Horizon",
        "fr": "Comment tout garder sous controle sans ouvrir Horizon",
        "de": "Wie man alles unter Kontrolle hat ohne Horizon zu offnen",
    },
    "come-controllare-astronaut-mentre-sei-in-stalla": {
        "it": "Come controllare Astronaut mentre sei in stalla",
        "en": "How to Monitor Astronaut While You Are in the Barn",
        "es": "Como controlar Astronaut mientras estas en el establo",
        "fr": "Comment surveiller Astronaut pendant que vous etes dans l'etable",
        "de": "Wie man den Astronaut uberwacht wahrend man im Stall ist",
    },
    "come-controllare-fetch-cows-mentre-lavori-in-stalla": {
        "it": "Come controllare fetch cows mentre lavori in stalla",
        "en": "How to Monitor Fetch Cows While Working in the Barn",
        "es": "Como controlar las fetch cows mientras trabajas en el establo",
        "fr": "Comment surveiller les fetch cows en travaillant dans l'etable",
        "de": "Wie man Fetch Cows uberwacht wahrend man im Stall arbeitet",
    },
    "come-controllare-horizon-senza-andare-in-ufficio": {
        "it": "Come controllare Horizon senza andare in ufficio",
        "en": "How to Check Horizon Without Going to the Office",
        "es": "Como controlar Horizon sin ir a la oficina",
        "fr": "Comment verifier Horizon sans aller au bureau",
        "de": "Wie man Horizon pruft ohne ins Buro zu gehen",
    },
    "come-controllare-i-ritardi-senza-aprire-lely-horizon": {
        "it": "Come controllare i ritardi senza aprire Lely Horizon",
        "en": "How to Check Delays Without Opening Lely Horizon",
        "es": "Como controlar los retrasos sin abrir Lely Horizon",
        "fr": "Comment verifier les retards sans ouvrir Lely Horizon",
        "de": "Wie man Verspatungen pruft ohne Lely Horizon zu offnen",
    },
    "come-controllare-il-robot-lely-senza-aprire-horizon": {
        "it": "Come controllare il robot Lely senza aprire Horizon",
        "en": "How to Monitor the Lely Robot Without Opening Horizon",
        "es": "Como controlar el robot Lely sin abrir Horizon",
        "fr": "Comment surveiller le robot Lely sans ouvrir Horizon",
        "de": "Wie man den Lely Roboter uberwacht ohne Horizon zu offnen",
    },
    "come-controllare-la-fetch-list-su-lely-astronaut": {
        "it": "Come controllare la fetch list su Lely Astronaut",
        "en": "How to Check the Fetch List on Lely Astronaut",
        "es": "Como controlar la fetch list en Lely Astronaut",
        "fr": "Comment verifier la fetch list sur Lely Astronaut",
        "de": "Wie man die Fetch List am Lely Astronaut pruft",
    },
    "come-controllare-la-mungitura-mentre-lavori-con-lely-astronaut": {
        "it": "Come controllare la mungitura mentre lavori con Lely Astronaut",
        "en": "How to Monitor Milking While Working with Lely Astronaut",
        "es": "Como controlar el ordeno mientras trabajas con Lely Astronaut",
        "fr": "Comment surveiller la traite en travaillant avec Lely Astronaut",
        "de": "Wie man das Melken uberwacht wahrend man mit Lely Astronaut arbeitet",
    },
    "come-controllare-lely-horizon-senza-aprire-il-pc-principale": {
        "it": "Come controllare Lely Horizon senza aprire il PC principale",
        "en": "How to Check Lely Horizon Without Opening the Main PC",
        "es": "Como controlar Lely Horizon sin abrir el PC principal",
        "fr": "Comment verifier Lely Horizon sans ouvrir le PC principal",
        "de": "Wie man Lely Horizon pruft ohne den Haupt-PC zu offnen",
    },
    "come-controllare-ritardi-su-lely-astronaut-a5": {
        "it": "Come controllare ritardi su Lely Astronaut A5",
        "en": "How to Check Delays on Lely Astronaut A5",
        "es": "Como controlar los retrasos en Lely Astronaut A5",
        "fr": "Comment verifier les retards sur Lely Astronaut A5",
        "de": "Wie man Verspatungen am Lely Astronaut A5 pruft",
    },
    "come-evitare-che-una-vacca-resti-troppo-tempo-senza-mungitura-con-astronaut": {
        "it": "Come evitare che una vacca resti troppo tempo senza mungitura con Astronaut",
        "en": "How to Prevent a Cow from Going Too Long Without Milking with Astronaut",
        "es": "Como evitar que una vaca pase demasiado tiempo sin ordeno con Astronaut",
        "fr": "Comment eviter qu'une vache reste trop longtemps sans traite avec Astronaut",
        "de": "Wie man verhindert dass eine Kuh zu lange ohne Melken bleibt mit Astronaut",
    },
    "come-evitare-di-aprire-continuamente-lely-horizon": {
        "it": "Come evitare di aprire continuamente Lely Horizon",
        "en": "How to Avoid Constantly Opening Lely Horizon",
        "es": "Como evitar abrir continuamente Lely Horizon",
        "fr": "Comment eviter d'ouvrir constamment Lely Horizon",
        "de": "Wie man vermeidet standig Lely Horizon zu offnen",
    },
    "come-evitare-di-controllare-continuamente-astronaut": {
        "it": "Come evitare di controllare continuamente Astronaut",
        "en": "How to Avoid Constantly Checking Astronaut",
        "es": "Como evitar controlar continuamente Astronaut",
        "fr": "Comment eviter de verifier constamment Astronaut",
        "de": "Wie man vermeidet den Astronaut standig zu kontrollieren",
    },
    "come-evitare-ritardi-non-visti-su-lely-horizon": {
        "it": "Come evitare ritardi non visti su Lely Horizon",
        "en": "How to Avoid Unseen Delays on Lely Horizon",
        "es": "Como evitar retrasos no vistos en Lely Horizon",
        "fr": "Comment eviter les retards non vus sur Lely Horizon",
        "de": "Wie man ungesehene Verspatungen auf Lely Horizon vermeidet",
    },
    "come-fidarsi-davvero-del-robot-lely-astronaut": {
        "it": "Come fidarsi davvero del robot Lely Astronaut",
        "en": "How to Truly Trust the Lely Astronaut Robot",
        "es": "Como confiar realmente en el robot Lely Astronaut",
        "fr": "Comment vraiment faire confiance au robot Lely Astronaut",
        "de": "Wie man dem Lely Astronaut Roboter wirklich vertraut",
    },
    "come-lavorare-con-pi-tranquillit-con-lely-astronaut": {
        "it": "Come lavorare con piu tranquillita con Lely Astronaut",
        "en": "How to Work with More Peace of Mind with Lely Astronaut",
        "es": "Como trabajar con mas tranquilidad con Lely Astronaut",
        "fr": "Comment travailler plus sereinement avec Lely Astronaut",
        "de": "Wie man mit mehr Ruhe mit dem Lely Astronaut arbeitet",
    },
    "come-lavorare-senza-preoccupazioni-con-lely-astronaut": {
        "it": "Come lavorare senza preoccupazioni con Lely Astronaut",
        "en": "How to Work Without Worries with Lely Astronaut",
        "es": "Como trabajar sin preocupaciones con Lely Astronaut",
        "fr": "Comment travailler sans souci avec Lely Astronaut",
        "de": "Wie man sorgenfrei mit dem Lely Astronaut arbeitet",
    },
    "come-monitorare-facilmente-lely-astronaut-a5": {
        "it": "Come monitorare facilmente Lely Astronaut A5",
        "en": "How to Easily Monitor Lely Astronaut A5",
        "es": "Como monitorear facilmente Lely Astronaut A5",
        "fr": "Comment surveiller facilement Lely Astronaut A5",
        "de": "Wie man den Lely Astronaut A5 einfach uberwacht",
    },
    "come-non-dimenticare-mai-una-vacca-in-ritardo-con-astronaut-a5": {
        "it": "Come non dimenticare mai una vacca in ritardo con Astronaut A5",
        "en": "How to Never Forget a Delayed Cow with Astronaut A5",
        "es": "Como no olvidar nunca una vaca retrasada con Astronaut A5",
        "fr": "Comment ne jamais oublier une vache en retard avec Astronaut A5",
        "de": "Wie man nie eine verspatete Kuh mit Astronaut A5 vergisst",
    },
    "come-non-dimenticare-vacche-in-fetch-list-su-astronaut": {
        "it": "Come non dimenticare vacche in fetch list su Astronaut",
        "en": "How to Never Forget Cows on the Fetch List on Astronaut",
        "es": "Como no olvidar vacas en la fetch list de Astronaut",
        "fr": "Comment ne jamais oublier les vaches sur la fetch list d'Astronaut",
        "de": "Wie man Kuhe auf der Fetch List am Astronaut nie vergisst",
    },
    "come-non-perdere-fetch-cows-su-lely-astronaut": {
        "it": "Come non perdere fetch cows su Lely Astronaut",
        "en": "How to Never Miss Fetch Cows on Lely Astronaut",
        "es": "Como no perder fetch cows en Lely Astronaut",
        "fr": "Comment ne jamais manquer les fetch cows sur Lely Astronaut",
        "de": "Wie man keine Fetch Cows am Lely Astronaut verpasst",
    },
    "come-non-perdere-il-controllo-del-robot-lely-astronaut": {
        "it": "Come non perdere il controllo del robot Lely Astronaut",
        "en": "How to Never Lose Control of the Lely Astronaut Robot",
        "es": "Como no perder el control del robot Lely Astronaut",
        "fr": "Comment ne jamais perdre le controle du robot Lely Astronaut",
        "de": "Wie man nie die Kontrolle uber den Lely Astronaut Roboter verliert",
    },
    "come-non-perdere-le-vacche-in-fetch-list-su-lely-horizon": {
        "it": "Come non perdere le vacche in fetch list su Lely Horizon",
        "en": "How to Never Lose Track of Cows on the Fetch List in Lely Horizon",
        "es": "Como no perder las vacas de la fetch list en Lely Horizon",
        "fr": "Comment ne jamais perdre les vaches de la fetch list sur Lely Horizon",
        "de": "Wie man die Kuhe auf der Fetch List in Lely Horizon nie verliert",
    },
    "come-ridurre-la-fetch-list-con-lely-astronaut": {
        "it": "Come ridurre la fetch list con Lely Astronaut",
        "en": "How to Reduce the Fetch List with Lely Astronaut",
        "es": "Como reducir la fetch list con Lely Astronaut",
        "fr": "Comment reduire la fetch list avec Lely Astronaut",
        "de": "Wie man die Fetch List mit Lely Astronaut reduziert",
    },
    "come-sapere-che-tutto-funziona-correttamente-su-lely-horizon": {
        "it": "Come sapere che tutto funziona correttamente su Lely Horizon",
        "en": "How to Know Everything Is Working Correctly on Lely Horizon",
        "es": "Como saber que todo funciona correctamente en Lely Horizon",
        "fr": "Comment savoir que tout fonctionne correctement sur Lely Horizon",
        "de": "Wie man weiss dass alles auf Lely Horizon korrekt funktioniert",
    },
    "come-sapere-quali-vacche-devono-ancora-andare-al-robot-lely": {
        "it": "Come sapere quali vacche devono ancora andare al robot Lely",
        "en": "How to Know Which Cows Still Need to Go to the Lely Robot",
        "es": "Como saber que vacas aun necesitan ir al robot Lely",
        "fr": "Comment savoir quelles vaches doivent encore aller au robot Lely",
        "de": "Wie man weiss welche Kuhe noch zum Lely Roboter mussen",
    },
    "come-sapere-quali-vacche-sono-nella-fetch-list-su-horizon": {
        "it": "Come sapere quali vacche sono nella fetch list su Horizon",
        "en": "How to Know Which Cows Are on the Fetch List in Horizon",
        "es": "Como saber que vacas estan en la fetch list de Horizon",
        "fr": "Comment savoir quelles vaches sont sur la fetch list dans Horizon",
        "de": "Wie man weiss welche Kuhe auf der Fetch List in Horizon sind",
    },
    "come-sapere-subito-quali-vacche-recuperare-con-astronaut": {
        "it": "Come sapere subito quali vacche recuperare con Astronaut",
        "en": "How to Instantly Know Which Cows to Fetch with Astronaut",
        "es": "Como saber de inmediato que vacas recuperar con Astronaut",
        "fr": "Comment savoir immediatement quelles vaches recuperer avec Astronaut",
        "de": "Wie man sofort weiss welche Kuhe man mit dem Astronaut holen muss",
    },
    "come-sapere-subito-quali-vacche-sono-in-ritardo-con-lely-astronaut": {
        "it": "Come sapere subito quali vacche sono in ritardo con Lely Astronaut",
        "en": "How to Instantly Know Which Cows Are Delayed with Lely Astronaut",
        "es": "Como saber de inmediato que vacas estan retrasadas con Lely Astronaut",
        "fr": "Comment savoir immediatement quelles vaches sont en retard avec Lely Astronaut",
        "de": "Wie man sofort weiss welche Kuhe mit dem Lely Astronaut verspatet sind",
    },
    "come-sapere-subito-se-una-vacca-non-stata-munta-dal-robot-lely": {
        "it": "Come sapere subito se una vacca non e stata munta dal robot Lely",
        "en": "How to Instantly Know if a Cow Hasn't Been Milked by the Lely Robot",
        "es": "Como saber de inmediato si una vaca no ha sido ordenada por el robot Lely",
        "fr": "Comment savoir immediatement si une vache n'a pas ete traite par le robot Lely",
        "de": "Wie man sofort weiss ob eine Kuh nicht vom Lely Roboter gemolken wurde",
    },
    "come-vedere-fetch-cows-senza-aprire-lely-horizon": {
        "it": "Come vedere fetch cows senza aprire Lely Horizon",
        "en": "How to See Fetch Cows Without Opening Lely Horizon",
        "es": "Como ver las fetch cows sin abrir Lely Horizon",
        "fr": "Comment voir les fetch cows sans ouvrir Lely Horizon",
        "de": "Wie man Fetch Cows sieht ohne Lely Horizon zu offnen",
    },
    "come-vedere-fetch-list-su-lely-astronaut-a4": {
        "it": "Come vedere fetch list su Lely Astronaut A4",
        "en": "How to See the Fetch List on Lely Astronaut A4",
        "es": "Como ver la fetch list en Lely Astronaut A4",
        "fr": "Comment voir la fetch list sur Lely Astronaut A4",
        "de": "Wie man die Fetch List am Lely Astronaut A4 sieht",
    },
    "come-vedere-i-ritardi-senza-andare-al-computer-lely": {
        "it": "Come vedere i ritardi senza andare al computer Lely",
        "en": "How to See Delays Without Going to the Lely Computer",
        "es": "Como ver los retrasos sin ir al ordenador Lely",
        "fr": "Comment voir les retards sans aller a l'ordinateur Lely",
        "de": "Wie man Verspatungen sieht ohne zum Lely Computer zu gehen",
    },
    "come-vedere-la-situazione-del-robot-astronaut-in-tempo-reale": {
        "it": "Come vedere la situazione del robot Astronaut in tempo reale",
        "en": "How to See the Astronaut Robot Status in Real Time",
        "es": "Como ver la situacion del robot Astronaut en tiempo real",
        "fr": "Comment voir la situation du robot Astronaut en temps reel",
        "de": "Wie man den Status des Astronaut Roboters in Echtzeit sieht",
    },
    "come-vedere-lely-horizon-direttamente-in-stalla": {
        "it": "Come vedere Lely Horizon direttamente in stalla",
        "en": "How to See Lely Horizon Directly in the Barn",
        "es": "Como ver Lely Horizon directamente en el establo",
        "fr": "Comment voir Lely Horizon directement dans l'etable",
        "de": "Wie man Lely Horizon direkt im Stall sieht",
    },
    "come-vedere-subito-cosa-sta-succedendo-sul-robot-lely-astronaut": {
        "it": "Come vedere subito cosa sta succedendo sul robot Lely Astronaut",
        "en": "How to Instantly See What Is Happening on the Lely Astronaut Robot",
        "es": "Como ver de inmediato lo que esta pasando en el robot Lely Astronaut",
        "fr": "Comment voir immediatement ce qui se passe sur le robot Lely Astronaut",
        "de": "Wie man sofort sieht was auf dem Lely Astronaut Roboter passiert",
    },
    "come-vedere-subito-le-vacche-che-non-sono-andate-al-robot-lely-astronaut": {
        "it": "Come vedere subito le vacche che non sono andate al robot Lely Astronaut",
        "en": "How to Instantly See Which Cows Haven't Gone to the Lely Astronaut Robot",
        "es": "Como ver de inmediato las vacas que no han ido al robot Lely Astronaut",
        "fr": "Comment voir immediatement les vaches qui ne sont pas allees au robot Lely Astronaut",
        "de": "Wie man sofort sieht welche Kuhe nicht zum Lely Astronaut Roboter gegangen sind",
    },
    "non-ho-tempo-di-controllare-lely-horizon-tutto-il-giorno-cosa-fare": {
        "it": "Non ho tempo di controllare Lely Horizon tutto il giorno: cosa fare",
        "en": "I Don't Have Time to Check Lely Horizon All Day: What to Do",
        "es": "No tengo tiempo de controlar Lely Horizon todo el dia: que hacer",
        "fr": "Je n'ai pas le temps de verifier Lely Horizon toute la journee: que faire",
        "de": "Ich habe keine Zeit Lely Horizon den ganzen Tag zu prufen: Was tun",
    },
    "perch-alcune-vacche-sono-sempre-in-ritardo-con-lely-astronaut": {
        "it": "Perche alcune vacche sono sempre in ritardo con Lely Astronaut",
        "en": "Why Some Cows Are Always Delayed with Lely Astronaut",
        "es": "Por que algunas vacas siempre estan retrasadas con Lely Astronaut",
        "fr": "Pourquoi certaines vaches sont toujours en retard avec Lely Astronaut",
        "de": "Warum manche Kuhe mit dem Lely Astronaut immer verspatet sind",
    },
    "perch-scopro-tardi-che-una-vacca-non-andata-al-robot-lely": {
        "it": "Perche scopro tardi che una vacca non e andata al robot Lely",
        "en": "Why I Find Out Too Late That a Cow Didn't Go to the Lely Robot",
        "es": "Por que descubro tarde que una vaca no fue al robot Lely",
        "fr": "Pourquoi je decouvre trop tard qu'une vache n'est pas allee au robot Lely",
        "de": "Warum ich zu spat erfahre dass eine Kuh nicht zum Lely Roboter gegangen ist",
    },
}

# Month localization for the "FEBRUARY" issue
MONTH_MAP = {
    "it": "FEBBRAIO",
    "en": "FEBRUARY",
    "es": "FEBRERO",
    "fr": "FEVRIER",
    "de": "FEBRUAR",
}

# inLanguage codes
LANG_CODES = {
    "it": "it-IT",
    "en": "en",
    "es": "es",
    "fr": "fr",
    "de": "de",
}

CORRECT_OG_IMAGE = f"{BASE_URL}/lelydisplaydelay.png"
WRONG_OG_IMAGE = f"{BASE_URL}/assets/images/nordic-01.jpg"


def get_slug(filename):
    """Get slug from filename (without .html)."""
    return filename.replace(".html", "")


def extract_first_paragraph(content):
    """Extract text from first <p> in .content div."""
    # Find the content div then first <p> inside it
    content_match = re.search(r'<div class="content">\s*<p>(.*?)</p>', content, re.DOTALL)
    if content_match:
        text = content_match.group(1)
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        text = html.unescape(text)
        # Truncate to ~155 chars at word boundary
        if len(text) > 155:
            text = text[:152].rsplit(' ', 1)[0] + '...'
        return text
    return None


def fix_article(filepath, lang, filename):
    """Fix a single article HTML file."""
    slug = get_slug(filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # ── Fix canonical URL (all languages including IT) ──
    # Change blog/filename.html to blog/it/filename.html (IT is canonical)
    wrong_canonical = f'{BASE_URL}/blog/{filename}'
    correct_canonical = f'{BASE_URL}/blog/it/{filename}'
    content = content.replace(
        f'<link rel="canonical" href="{wrong_canonical}">',
        f'<link rel="canonical" href="{correct_canonical}">'
    )

    # ── Fix og:url (language-specific) ──
    correct_og_url = f'{BASE_URL}/blog/{lang}/{filename}'
    # Replace og:url pointing to blog/filename.html (without lang)
    content = re.sub(
        r'<meta property="og:url" content="' + re.escape(BASE_URL) + r'/blog/' + re.escape(filename) + r'">',
        f'<meta property="og:url" content="{correct_og_url}">',
        content
    )

    # ── Fix mainEntityOfPage @id ──
    content = content.replace(
        f'"@id": "{BASE_URL}/blog/{filename}"',
        f'"@id": "{correct_og_url}"'
    )

    # ── Fix og:image and twitter:image ──
    content = content.replace(
        f'content="{WRONG_OG_IMAGE}"',
        f'content="{CORRECT_OG_IMAGE}"'
    )

    # ── Fix FEBRUARY date ──
    correct_month = MONTH_MAP.get(lang, "FEBRUARY")
    content = re.sub(r'\bFEBRUARY\b', correct_month, content)

    # ── Fix inLanguage ──
    correct_lang_code = LANG_CODES[lang]
    content = content.replace('"inLanguage": "it-IT"', f'"inLanguage": "{correct_lang_code}"')

    # ── For non-IT languages: fix titles and descriptions ──
    if lang != "it" and slug in TITLES:
        title = TITLES[slug][lang]

        # Extract meta description from body content (already translated)
        desc = extract_first_paragraph(content)
        if not desc:
            desc = title  # fallback

        # Fix <title> tag
        content = re.sub(
            r'<title>[^<]+</title>',
            f'<title>{title} - Cow Delays Monitor</title>',
            content
        )

        # Fix <h1>
        content = re.sub(
            r'<h1>[^<]+</h1>',
            f'<h1>{title}</h1>',
            content
        )

        # Fix og:title
        content = re.sub(
            r'<meta property="og:title" content="[^"]+">',
            f'<meta property="og:title" content="{html.escape(title)}">',
            content
        )

        # Fix twitter:title
        content = re.sub(
            r'<meta name="twitter:title" content="[^"]+">',
            f'<meta name="twitter:title" content="{html.escape(title)}">',
            content
        )

        # Fix JSON-LD headline
        content = re.sub(
            r'"headline": "[^"]+"',
            f'"headline": "{title}"',
            content
        )

        # Fix meta description
        escaped_desc = html.escape(desc, quote=True)
        content = re.sub(
            r'<meta name="description" content="[^"]+">',
            f'<meta name="description" content="{escaped_desc}">',
            content
        )

        # Fix og:description
        content = re.sub(
            r'<meta property="og:description" content="[^"]+">',
            f'<meta property="og:description" content="{escaped_desc}">',
            content
        )

        # Fix twitter:description
        content = re.sub(
            r'<meta name="twitter:description" content="[^"]+">',
            f'<meta name="twitter:description" content="{escaped_desc}">',
            content
        )

        # Fix JSON-LD description
        content = re.sub(
            r'"description": "[^"]+"',
            f'"description": "{desc}"',
            content
        )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_blog_listing(filepath, lang):
    """Fix blog listing page (blog/{lang}/blog.html) titles."""
    if lang == "it":
        return False  # IT titles are already correct

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace each article link title in the listing
    for slug, titles in TITLES.items():
        if lang in titles:
            new_title = titles[lang]
            # Match the <a> tag pattern in blog listing: ">OLD TITLE</a>
            # The href contains the slug
            pattern = re.compile(
                r'(href="\./?' + re.escape(slug) + r'\.html">)([^<]+)(</a>)'
            )
            content = pattern.sub(r'\g<1>' + new_title + r'\3', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def convert_orphan_to_redirect(filepath, filename):
    """Convert an orphan blog/*.html file to a redirect to blog/it/."""
    redirect_html = f'''<!DOCTYPE html>
<html><head>
<meta http-equiv="refresh" content="0; url=./it/{filename}">
<link rel="canonical" href="{BASE_URL}/blog/it/{filename}">
</head><body></body></html>
'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(redirect_html)


def main():
    stats = {"articles_fixed": 0, "listings_fixed": 0, "orphans_converted": 0}

    # ── Step 1: Fix articles in all language dirs ──
    for lang in ["it", "en", "es", "fr", "de"]:
        lang_dir = os.path.join(BLOG_DIR, lang)
        if not os.path.isdir(lang_dir):
            print(f"WARNING: {lang_dir} not found, skipping")
            continue

        for filename in sorted(os.listdir(lang_dir)):
            if not filename.endswith('.html') or filename == 'blog.html':
                continue

            filepath = os.path.join(lang_dir, filename)
            if fix_article(filepath, lang, filename):
                stats["articles_fixed"] += 1
                print(f"  FIXED: {lang}/{filename}")

    # ── Step 2: Fix blog listing pages ──
    for lang in ["en", "es", "fr", "de"]:
        listing_path = os.path.join(BLOG_DIR, lang, "blog.html")
        if os.path.exists(listing_path):
            if fix_blog_listing(listing_path, lang):
                stats["listings_fixed"] += 1
                print(f"  FIXED LISTING: {lang}/blog.html")

    # ── Step 3: Convert orphan files to redirects ──
    for filename in sorted(os.listdir(BLOG_DIR)):
        filepath = os.path.join(BLOG_DIR, filename)
        if not filename.endswith('.html') or not os.path.isfile(filepath):
            continue
        # blog.html is also an orphan (redirect to blog/it/blog.html)
        convert_orphan_to_redirect(filepath, filename)
        stats["orphans_converted"] += 1
        print(f"  REDIRECT: blog/{filename} -> blog/it/{filename}")

    print(f"\nDone! Articles fixed: {stats['articles_fixed']}, "
          f"Listings fixed: {stats['listings_fixed']}, "
          f"Orphans converted: {stats['orphans_converted']}")


if __name__ == "__main__":
    main()
