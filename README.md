# POP Studio Cambrai — site vitrine

Maquette réalisée par **NK Digital**. Site statique (HTML/CSS/JS, aucune dépendance) prêt pour GitHub Pages ou Cloudflare Pages.

## Structure
- `index.html` : accueil
- `boutique.html` : la boutique, l'équipe et les avis
- `nouveautes.html` : réassort, sorties à surveiller, formulaire « Je cherche une paire »
- `authentification.html` : legit check
- `contact.html` : horaires, accès, contact, boutique de Saint-Quentin
- `css/style.css` et `js/main.js` : styles et scripts communs à toutes les pages
- `build.py` : régénère les 5 pages (en-tête, onglets, pied de page communs) — optionnel
- `img/` : photos optimisées (WebP), logos, favicon
- `fonts/` : polices auto-hébergées (Anton, Space Grotesk, Permanent Marker), sans appel à Google Fonts

## À compléter avant la mise en ligne
Dans `js/main.js`, bloc `CONFIG` en haut du fichier (horaires `HOURS` et sorties `DROPS` juste en dessous) :
| Clé | Rôle |
|---|---|
| `phone` | active le bouton « Appeler » |
| `whatsapp` | numéro au format international sans `+` (ex. `33612345678`) |
| `formEndpoint` | URL Formspree (gratuit) pour recevoir les demandes « Je cherche une paire » par e-mail |
| `reassortDay` | jour du réassort (0 = dimanche … 6 = samedi) pour le compte à rebours |

Autres points :
1. Mentions légales : remplacer les champs `[à compléter]` (SIRET, gérant, contact, hébergeur).
2. Supprimer la ligne `<meta name="robots" content="noindex, nofollow">` et le badge `.demo` sur chaque page (ou dans `build.py`).
3. Fil Instagram automatique : coller le widget Behold ou LightWidget à l'emplacement indiqué en commentaire.
4. Mettre à jour la liste `DROPS` (sorties à surveiller) une fois par mois.

## Déploiement GitHub Pages
Settings → Pages → Branch `main` / dossier `/ (root)`.
