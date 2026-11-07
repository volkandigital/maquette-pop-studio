"""Génère les pages statiques du site POP Studio (en-tête, onglets et pied de page communs)."""
import re, pathlib

SRC = open('/home/claude/pop2/index.html', encoding='utf-8').read()

def block(start):
    """Extrait un élément <div ...> complet à partir d'une chaîne de départ (div équilibrés)."""
    i = SRC.index(start)
    depth = 0
    for m in re.finditer(r'<div\b|</div>', SRC[i:]):
        depth += 1 if m.group() == '<div' else -1
        if depth == 0:
            return SRC[i:i + m.end()]
    raise ValueError(start)

def between(a, b):
    i = SRC.index(a); j = SRC.index(b, i)
    return SRC[i:j + len(b)]

BENTO   = block('<div class="bento">').replace(' Et on vérifie aussi les tiennes, gratuitement.', ' Et on peut aussi vérifier les tiennes.')
RAIL    = block('<div class="rail-wrap">')
IGBAR   = block('<div class="ig-bar rv">')
POINTS  = between('<ul class="points">', '</ul>')
REVIEWS = block('<div class="reviews" id="reviews"')
SCORES  = block('<div class="scores">')
FORM    = block('<div class="form rv" id="cherche">')
HOURSBOX= block('<div class="box rv">')
MAPBOX  = block('<div class="box rv">\n        <h3>Adresse</h3>')
SHOP2   = block('<div class="shop2 rv">')
DIALOGS = between('<dialog id="legal"', '</dialog>') + '\n\n' + between('<dialog id="privacy"', '</dialog>')
MARQUEE = block('<div class="marquee"')
RAILCTRL = '''<div class="rail-ctrl">
        <button class="round" data-scroll="rail" data-dir="-1" aria-label="Défiler vers la gauche">←</button>
        <button class="round" data-scroll="rail" data-dir="1" aria-label="Défiler vers la droite">→</button>
      </div>'''
REVCTRL = '''<div class="rail-ctrl">
        <button class="round" data-scroll="reviews" data-dir="-1" aria-label="Avis précédents">←</button>
        <button class="round" data-scroll="reviews" data-dir="1" aria-label="Avis suivants">→</button>
      </div>'''

# Le tableau d'horaires utilise désormais la classe .js-status partagée
HOURSBOX = HOURSBOX.replace('<span class="status" id="status" aria-live="polite"></span>', '<span class="js-status" aria-live="polite"></span>')

PAGES = [
    # fichier, libellé onglet, libellé court mobile, icône
    ('index.html',           'Accueil',          'Accueil',   '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>'),
    ('boutique.html',        'La boutique',      'Boutique',  '<path d="M4 9h16l-1.2 10.2a2 2 0 0 1-2 1.8H7.2a2 2 0 0 1-2-1.8z"/><path d="M8.5 9V7a3.5 3.5 0 0 1 7 0v2"/>'),
    ('nouveautes.html',      'Nouveautés',       'Nouveautés','<path d="M12 2l2.6 6.3L21 9l-5 4.4 1.5 6.6L12 16.6 6.5 20l1.5-6.6L3 9l6.4-.7z"/>'),
    ('authentification.html','Authentification', 'Legit',     '<path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>'),
    ('contact.html',         'Horaires & contact','Contact',  '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'),
]

def head(title, desc, extra=''):
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- MAQUETTE : retirer la ligne suivante à la mise en ligne officielle -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b0b0b">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="POP Studio Cambrai">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="img/mur-dunk.webp">
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preload" href="fonts/anton-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
{extra}</head>'''

def header(active):
    CUR = ' aria-current="page"'; BTN = ' class="btn btn-neon"'
    desk = '\n'.join(
        f'      <a href="{f}"{CUR if f == active else ""}{BTN if f == "contact.html" else ""}>{lbl}</a>'
        for f, lbl, _, _ in PAGES)
    return f'''<body>
<a class="skip" href="#main">Aller au contenu</a>

<div class="announce" role="region" aria-label="Annonce">
  <div class="wrap"><span class="dot" aria-hidden="true"></span><span id="announce">Réassort chaque semaine : jusqu'à 100 nouvelles paires d'un coup.</span><a href="nouveautes.html">Voir les nouveautés</a></div>
</div>

<header class="nav" id="nav">
  <div class="wrap">
    <a href="index.html" class="brand" aria-label="POP Studio, accueil"><img src="img/logo-ps.png" alt="" width="42" height="42"><span>POP <em>STUDIO</em></span></a>
    <nav class="menu" aria-label="Navigation principale">
{desk}
    </nav>
    <a class="btn btn-neon nav-cta" href="https://www.google.com/maps/dir/?api=1&amp;destination=50.1753339,3.2335155" target="_blank" rel="noopener">Itinéraire</a>
  </div>
</header>
'''

def tabbar(active):
    CUR = ' aria-current="page"'
    items = '\n'.join(
        f'  <a href="{f}"{CUR if f == active else ""}><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ic}</svg>{short}</a>'
        for f, _, short, ic in PAGES)
    return f'<nav class="tabbar" aria-label="Navigation mobile">\n{items}\n</nav>\n'

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <img class="logo" src="img/logo-pop-studio.png" alt="POP Studio" width="508" height="505" loading="lazy">
        <p>Sneakers &amp; streetwear · homme, femme, enfant.<br>Authenticité, originalité &amp; passion.</p>
      </div>
      <div>
        <h4>Le site</h4>
        <ul>
          {''.join(f'<li><a href="{f}">{lbl}</a></li>' for f, lbl, _, _ in PAGES)}
        </ul>
      </div>
      <div>
        <h4>Boutiques & réseaux</h4>
        <ul>
          <li>40 Place Aristide Briand, 59400 Cambrai</li>
          <li>22 Rue de Lyon, 02100 Saint-Quentin</li>
          <li><a href="https://www.instagram.com/pop_studio_cambrai/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.facebook.com/p/Pop-Studio-Cambrai-61562744890953/" target="_blank" rel="noopener">Facebook</a></li>
          <li><button type="button" data-dialog="legal">Mentions légales</button> · <button type="button" data-dialog="privacy">Confidentialité</button></li>
        </ul>
      </div>
    </div>
    <div class="legal-line">
      <span>© <span class="year">2026</span> POP Studio Cambrai</span>
      <span>Site réalisé par <a href="#" rel="author">NK Digital</a></span>
    </div>
  </div>
</footer>

{DIALOGS}
'''

def page(fname, title, desc, body, extra_head=''):
    html = head(title, desc, extra_head) + '\n' + header(fname) + '\n<main id="main">\n' + body + '\n</main>\n\n' + FOOTER + tabbar(fname) + \
        '<div class="demo">Maquette <b>NK Digital</b> · contenus issus de vos réseaux</div>\n<script src="js/main.js" defer></script>\n</body>\n</html>\n'
    # liens internes de l'ancienne page unique → nouvelles pages
    for a, b in [('href="#infos"', 'href="contact.html"'), ('href="#cherche"', 'href="nouveautes.html#cherche"'),
                 ('href="#legit"', 'href="authentification.html"'), ('href="#reassort"', 'href="nouveautes.html"')]:
        html = html.replace(a, b)
    pathlib.Path(fname).write_text(html, encoding='utf-8')

def page_hero(crumb, h1, lead, img, kicker):
    return f'''<section class="page-hero" aria-labelledby="h1">
  <img class="ph-bg" src="img/{img}" alt="" width="650" height="868" fetchpriority="high">
  <div class="wrap">
    <ol class="crumbs"><li><a href="index.html">Accueil</a></li><li aria-current="page">{crumb}</li></ol>
    <span class="kicker">{kicker}</span>
    <h1 id="h1">{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
'''

SCHEMA = '<script type="application/ld+json">' + between('{\n  "@context"', '\n}\n') + '</script>\n'

# ============================== ACCUEIL ==============================
home_reviews = re.findall(r'<article class="review">.*?</article>', REVIEWS, re.S)[:3]
ACCUEIL = f'''
<section class="hero" aria-labelledby="h1">
  <div class="wrap">
    <div>
      <img class="hero-logo" src="img/logo-pop-studio.png" alt="Logo POP Studio" width="508" height="505" fetchpriority="high">
      <h1 id="h1">Sneakers <span class="neon">&amp;</span> streetwear<small>au cœur de Cambrai</small></h1>
      <p class="lead">Des paires hype, des modèles qu'on ne voit nulle part ailleurs et des classiques à petit prix. Tout est authentique, et le mur se remplit de nouveautés chaque semaine.</p>
      <div class="cta">
        <a class="btn btn-neon" href="contact.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>Venir en boutique</a>
        <a class="btn btn-line" href="nouveautes.html">Voir les nouveautés</a>
      </div>
      <div class="chips">
        <span class="chip"><span class="ico g">G</span><span><b>5,0</b> <span class="stars" aria-hidden="true">★★★★★</span> · 27 avis</span></span>
        <span class="chip"><span class="ico f">f</span><span><b>100 %</b> recommandé · 25 avis</span></span>
        <span class="chip"><span class="ico s">✓</span><span><b>Homme · Femme · Enfant</b></span></span>
      </div>
    </div>
    <div class="collage rv">
      <figure><img src="img/mur-dunk.webp" alt="Mur de Nike Dunk dans la boutique POP Studio" width="649" height="868" fetchpriority="high"></figure>
      <figure><img src="img/devanture.webp" alt="Devanture de POP Studio, Place Aristide Briand à Cambrai" width="664" height="868" style="object-position:center 30%"></figure>
      <figure><img src="img/neon.webp" alt="Mur végétal et néon POP Studio" width="649" height="868" style="object-position:60% 40%"></figure>
      <span class="badge">100 % authentique</span>
    </div>
  </div>
</section>

{MARQUEE}

<section aria-label="Infos pratiques" style="padding:2.5rem 0 0">
  <div class="wrap quick">
    <div class="q rv"><span class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><div><b>Aujourd'hui</b><span class="js-status"></span><br><a href="contact.html">Tous les horaires →</a></div></div>
    <div class="q rv"><span class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></span><div><b>40 Place Aristide Briand</b><span>59400 Cambrai, centre-ville</span><br><a href="https://www.google.com/maps/dir/?api=1&amp;destination=50.1753339,3.2335155" target="_blank" rel="noopener">Itinéraire →</a></div></div>
    <div class="q rv"><span class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/></svg></span><div><b>Un doute sur une paire ?</b><span>On l'authentifie en boutique</span><br><a href="authentification.html">Legit check →</a></div></div>
  </div>
</section>

<section aria-labelledby="t-explore">
  <div class="wrap">
    <div class="head rv"><div><span class="kicker">Bienvenue chez POP</span><h2 id="t-explore">Explore<br>la boutique</h2></div>
      <p class="lead">L'une des plus belles boutiques sneakers du Nord, en plein centre de Cambrai.</p></div>
    <div class="explore">
      <a class="ex rv" href="boutique.html"><img src="img/mur-2.webp" alt="" width="650" height="868" loading="lazy"><div><small>La boutique</small><h3>Le paradis des sneakers</h3><p>Des murs de paires, un coin salon et une équipe de passionnés.</p><span class="go">Découvrir →</span></div></a>
      <a class="ex rv" href="nouveautes.html"><img src="img/jordan4.webp" alt="" width="468" height="840" loading="lazy" style="object-position:center 35%"><div><small>Nouveautés</small><h3>Réassort & sorties</h3><p>Les arrivages de la semaine et les grosses sorties à venir.</p><span class="go">Voir les nouveautés →</span></div></a>
      <a class="ex rv" href="authentification.html"><img src="img/jordan1.webp" alt="" width="468" height="840" loading="lazy" style="object-position:center 55%"><div><small>Legit check</small><h3>Authentification</h3><p>Achetée ailleurs ? On vérifie si ta paire est authentique.</p><span class="go">Comment ça marche →</span></div></a>
    </div>
  </div>
</section>

<section aria-labelledby="t-avis" style="padding-top:0">
  <div class="wrap">
    <div class="head rv"><div><span class="kicker">Ils sont passés en boutique</span><h2 id="t-avis">Ce qu'ils en disent</h2></div>
    {SCORES}</div>
    <div class="review-row">
      {''.join(r.replace('<article class="review">', '<article class="review rv">') for r in home_reviews)}
    </div>
    <div class="reviews-foot rv"><a href="boutique.html#avis">Tous les avis →</a></div>
  </div>
</section>

<section style="padding-top:0" aria-label="Instagram">
  <div class="wrap">
    {IGBAR}
  </div>
</section>
'''
page('index.html', 'POP Studio Cambrai · Boutique sneakers & streetwear',
     'POP Studio, boutique de sneakers et streetwear au centre de Cambrai (40 Place Aristide Briand). Nike, Jordan, Adidas : paires hype, originales et 100 % authentiques.',
     ACCUEIL, SCHEMA + '<link rel="preload" href="img/mur-dunk.webp" as="image">\n')

# ============================== BOUTIQUE ==============================
BOUTIQUE = page_hero('La boutique', 'Le paradis <span>des sneakers</span>',
    'Place Aristide Briand, POP Studio a construit l\'une des plus belles boutiques sneakers du Nord : des murs de paires à perte de vue, un coin salon et une équipe de passionnés.',
    'salon.webp', 'Authenticité, originalité & passion') + f'''
<section aria-label="La boutique en images">
  <div class="wrap">
    {BENTO}
  </div>
</section>

<section id="avis" aria-labelledby="t-avis" style="padding-top:0">
  <div class="wrap">
    <div class="head rv">
      <div><span class="kicker">L'équipe & nos clients</span><h2 id="t-avis">Ce qu'ils<br>en disent</h2></div>
      {SCORES}
    </div>
    {REVIEWS}
    <div class="reviews-foot rv">
      <a href="https://www.google.com/maps/search/?api=1&amp;query=POP+Studio+Cambrai" target="_blank" rel="noopener">Lire tous les avis Google →</a>
      {REVCTRL}
    </div>
  </div>
</section>

<section style="padding-top:0" aria-label="Nos boutiques">
  <div class="wrap">
    {SHOP2}
  </div>
</section>
'''
page('boutique.html', 'La boutique · POP Studio Cambrai',
     'Découvrez la boutique POP Studio à Cambrai : murs de sneakers Nike, Jordan, Adidas, coin salon, textile streetwear et une équipe de passionnés. Avis clients 5,0/5.', BOUTIQUE)

# ============================== NOUVEAUTÉS ==============================
NOUVEAUTES = page_hero('Nouveautés', 'Réassort <span>&amp; sorties</span>',
    'Chaque semaine, jusqu\'à 100 nouvelles paires rejoignent le mur. Voici un aperçu, les grosses sorties à surveiller, et un formulaire si tu cherches une paire précise.',
    'mur-dunk.webp', 'Fraîchement arrivé') + f'''
<section aria-labelledby="t-reassort">
  <div class="wrap">
    <div class="head rv">
      <div><span class="kicker">En boutique en ce moment</span><h2 id="t-reassort">Réassort de<br>la semaine</h2></div>
      {RAILCTRL}
    </div>
    {RAIL}
    {IGBAR}
  </div>
</section>

<section class="drops-sec" id="sorties" aria-labelledby="t-sorties">
  <div class="wrap">
    <div class="head rv">
      <div><span class="kicker">Calendrier</span><h2 id="t-sorties">Les sorties<br>à surveiller</h2></div>
      <p class="lead">Une paire te fait de l'œil ? Clique sur « Je la veux » : si on l'a ou qu'on la reçoit, on te prévient.</p>
    </div>
    <div class="drops-grid">
      <div>
        <ul class="drops" id="drops"></ul>
        <p class="fine">Dates officielles annoncées par les marques, susceptibles d'évoluer. Disponibilité en boutique non garantie.</p>
      </div>
      {FORM}
    </div>
  </div>
</section>
'''
page('nouveautes.html', 'Nouveautés & sorties sneakers · POP Studio Cambrai',
     'Réassort de la semaine chez POP Studio Cambrai, calendrier des sorties Jordan et Nike à venir, et formulaire pour demander une paire précise.', NOUVEAUTES)

# ============================== AUTHENTIFICATION ==============================
AUTH = page_hero('Authentification', 'Un doute sur ta paire ? <span>On l\'authentifie.</span>',
    'Achetée sur une appli ou entre particuliers ? Passe en boutique avec ta paire : l\'équipe POP Studio l\'examine et te dit si elle est authentique.',
    'jordan1.webp', 'Legit check') + f'''
<section aria-labelledby="t-steps">
  <div class="wrap">
    <div class="head rv"><div><span class="kicker">Simple et rapide</span><h2 id="t-steps">Comment<br>ça marche</h2></div></div>
    <ol class="steps">
      <li class="rv"><h3>Viens avec ta paire</h3><p>Passe en boutique aux heures d'ouverture, avec la boîte et les étiquettes si tu les as.</p></li>
      <li class="rv"><h3>On l'examine</h3><p>L'équipe passe la paire en revue point par point, sous tes yeux.</p></li>
      <li class="rv"><h3>Tu repars fixé</h3><p>On t'explique notre avis et ce qui nous a permis de trancher.</p></li>
    </ol>
  </div>
</section>

<section class="legit" aria-labelledby="t-points">
  <div class="wrap">
    <div class="pic rv">
      <img src="img/neon.webp" alt="Le néon POP Studio dans la boutique" width="649" height="868" loading="lazy" style="object-position:60% 40%">
      <span class="stamp">LEGIT<br>CHECK<br>✓</span>
    </div>
    <div class="rv">
      <span class="kicker">Les points vérifiés</span>
      <h2 id="t-points">Ce qu'on <span>regarde</span></h2>
      <p class="lead">Une contrefaçon se trahit rarement sur un seul détail. On croise plusieurs indices avant de donner notre avis.</p>
      {POINTS}
    </div>
  </div>
</section>

<section aria-labelledby="t-why">
  <div class="wrap why">
    <img class="rv" src="img/mur-2.webp" alt="Mur de sneakers authentiques chez POP Studio" width="650" height="868" loading="lazy">
    <div class="rv">
      <span class="kicker">Chez POP Studio</span>
      <h2 id="t-why">Que des paires<br>authentiques</h2>
      <p class="lead" style="margin:1.2rem 0 1.8rem">Toutes les paires vendues en boutique sont authentiques. Pas de doute à avoir : tu achètes en confiance, en voyant la paire et en l'essayant avant de partir avec.</p>
      <div class="cta" style="margin-top:0"><a class="btn btn-neon" href="contact.html">Voir les horaires</a><a class="btn btn-line" href="nouveautes.html">Voir les nouveautés</a></div>
    </div>
  </div>
</section>
'''
page('authentification.html', 'Authentification de sneakers (legit check) · POP Studio Cambrai',
     'Un doute sur une paire achetée en ligne ? POP Studio à Cambrai vérifie l\'authenticité de vos sneakers en boutique : étiquette, coutures, logos, semelle, boîte.', AUTH)

# ============================== CONTACT ==============================
CONTACT = page_hero('Horaires & contact', 'Horaires <span>&amp; accès</span>',
    'POP Studio t\'accueille au 40 Place Aristide Briand, en plein centre de Cambrai. Retrouve aussi la boutique de Saint-Quentin.',
    'devanture.webp', 'On t\'attend') + f'''
<section aria-label="Horaires et adresse">
  <div class="wrap">
    <div class="infos-grid">
      {HOURSBOX}
      {MAPBOX}
    </div>
    {SHOP2}
  </div>
</section>

<section aria-labelledby="t-contact" style="padding-top:0">
  <div class="wrap">
    <div class="head rv"><div><span class="kicker">Une question ?</span><h2 id="t-contact">Nous contacter</h2></div>
      <p class="lead">Une paire, une pointure, une dispo ? Écris-nous, ou laisse une demande : on te recontacte.</p></div>
    <div class="channels rv" id="channels"></div>
    <div class="cta-band rv" style="margin-top:1rem">
      <div><h2>Tu cherches une paire ?</h2><p>Laisse ta demande en 30 secondes, on te prévient si on l'a.</p></div>
      <a class="btn btn-dark" href="nouveautes.html#cherche">Faire une demande →</a>
    </div>
  </div>
</section>
'''
page('contact.html', 'Horaires & contact · POP Studio Cambrai',
     'Horaires d\'ouverture, adresse et contact de POP Studio Cambrai, 40 Place Aristide Briand. Boutique également à Saint-Quentin, 22 Rue de Lyon.', CONTACT,
     SCHEMA)

print('ok')
