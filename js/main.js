/* ============ CONFIGURATION — à compléter avec la boutique ============ */
const CONFIG = {
  phone: "",          // ex. "03 27 00 00 00"  → active « Appeler »
  whatsapp: "",       // ex. "33612345678" (sans +) → active WhatsApp
  email: "",          // ex. "contact@popstudio.fr"
  formEndpoint: "",   // ex. "https://formspree.io/f/xxxxxx" → reçoit les demandes par e-mail
  reassortDay: null,  // ex. 3 = mercredi (0 = dimanche) → compte à rebours dans le bandeau
  lat: 50.1753339, lng: 3.2335155
};
/* Horaires : minutes depuis minuit [ouverture, fermeture] — 0 = dimanche */
const HOURS = {0:[],1:[],2:[],3:[[600,780],[840,1110]],4:[[840,1080]],5:[[660,780],[840,1110]],6:[[600,780],[840,1140]]};
/* Sorties à surveiller : date, modèle, coloris (à mettre à jour chaque mois) */
const DROPS = [
  {d:"2026-11-21", n:"Air Jordan 3 « Not Nice »",     c:"Noir / rouge / or"},
  {d:"2026-11-27", n:"Air Jordan 4 OG « Bred »",      c:"Noir / rouge / gris ciment"},
  {d:"2026-12-05", n:"Air Jordan 10 « Sacramento »",  c:"Noir / argent / violet"},
  {d:"2026-12-12", n:"Air Jordan 11 « Space Jam »",   c:"Noir / bleu royal / blanc"},
  {d:"2026-12-19", n:"Air Jordan 4 « Pink Thunder »", c:"Noir / blanc / rose"}
];
const IG = "https://www.instagram.com/pop_studio_cambrai/";
/* ====================================================================== */

const $ = (s, el=document) => el.querySelector(s);
const $$ = (s, el=document) => [...el.querySelectorAll(s)];
const DAYS = ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'];
const fmt = m => { const h = Math.floor(m/60), mn = m%60; return h + 'h' + (mn ? String(mn).padStart(2,'0') : ''); };
function parisNow(){ try { return new Date(new Date().toLocaleString('en-US', {timeZone:'Europe/Paris'})); } catch(e){ return new Date(); } }

$$('.year').forEach(e => e.textContent = new Date().getFullYear());

/* Rails horizontaux */
$$('[data-scroll]').forEach(b => b.addEventListener('click', () => {
  const r = document.getElementById(b.dataset.scroll);
  r.scrollBy({left: b.dataset.dir * r.clientWidth * .8, behavior: 'smooth'});
}));

/* Statut ouvert / fermé (toutes les pages qui ont .js-status) */
function openStatus(){
  const now = parisNow(), d = now.getDay(), m = now.getHours()*60 + now.getMinutes();
  const open = HOURS[d].some(([a,b]) => m>=a && m<b);
  if (open) { const end = HOURS[d].find(([a,b]) => m>=a && m<b)[1]; return {open, text:'Ouvert jusqu’à ' + fmt(end)}; }
  for (let k=0;k<8;k++){ const dd=(d+k)%7; const slot=HOURS[dd].find(([a]) => k>0 || a>m);
    if (slot) return {open, text:'Fermé · ouvre ' + (k===0?"aujourd'hui":k===1?'demain':DAYS[dd].toLowerCase()) + ' à ' + fmt(slot[0])}; }
  return {open, text:'Fermé'};
}
(function(){
  const s = openStatus();
  $$('.js-status').forEach(el => { el.textContent = '● ' + s.text; el.classList.add('status', s.open ? 'open' : 'closed'); });
})();

/* Tableau des horaires */
(function(){
  const tb = $('#hours tbody'); if (!tb) return;
  const d = parisNow().getDay();
  tb.innerHTML = [1,2,3,4,5,6,0].map(i => {
    const s = HOURS[i]; const txt = s.length ? s.map(([a,b]) => fmt(a)+' – '+fmt(b)).join(' · ') : 'Fermé';
    return `<tr class="${s.length?'':'off'} ${i===d?'today':''}"><th scope="row">${DAYS[i]}${i===d?' <span class="sr">(aujourd’hui)</span>':''}</th><td>${txt}</td></tr>`;
  }).join('');
})();

/* Bandeau réassort */
(function(){
  const el = $('#announce'); if (!el || CONFIG.reassortDay == null) return;
  const days=['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'];
  const diff = (CONFIG.reassortDay - parisNow().getDay() + 7) % 7;
  el.textContent = diff===0 ? "C'est jour de réassort : les nouvelles paires arrivent aujourd'hui !" : `Prochain réassort ${days[CONFIG.reassortDay]} (dans ${diff} jour${diff>1?'s':''}) : jusqu'à 100 nouvelles paires.`;
})();

/* Sorties à surveiller */
(function(){
  const box = $('#drops'); if (!box) return;
  const months=['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.'];
  const today = parisNow(); today.setHours(0,0,0,0);
  const list = DROPS.filter(x => new Date(x.d+'T12:00:00') >= today).slice(0,5);
  box.innerHTML = list.length ? list.map(x => { const dt=new Date(x.d+'T12:00:00');
    return `<li class="drop"><div class="date"><b>${dt.getDate()}</b><small>${months[dt.getMonth()]}</small></div><div><h3>${x.n}</h3><p>${x.c}</p></div><button type="button" data-model="${x.n.replace(/[«»]/g,'').replace(/\s+/g,' ').trim()}">Je la veux</button></li>`; }).join('')
    : '<li class="drop"><div></div><div><h3>Nouvelles sorties bientôt annoncées</h3><p>Suis @pop_studio_cambrai pour ne rien rater.</p></div></li>';
  $$('button', box).forEach(b => b.addEventListener('click', () => {
    $('#f-model').value = b.dataset.model;
    $('#cherche').scrollIntoView({behavior:'smooth', block:'center'});
    setTimeout(() => $('#f-size').focus({preventScroll:true}), 650);
  }));
})();

/* Formulaire « Je cherche une paire » */
(function(){
  const form = $('#pair-form'); if (!form) return;
  const sel = $('#f-size');
  for (let s=28; s<=48; s+=0.5) { if (s<36 && s%1) continue; const o=document.createElement('option'); o.value=o.textContent=String(s).replace('.',','); sel.appendChild(o); }
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const req = $$('[required]', form); req.forEach(i => i.classList.remove('err'));
    const bad = req.filter(i => i.type==='checkbox' ? !i.checked : !i.value.trim());
    if (bad.length) { bad.forEach(i => i.classList.add('err')); bad[0].focus(); return; }
    if (form._gotcha.value) return;
    if (CONFIG.formEndpoint) { try { await fetch(CONFIG.formEndpoint, {method:'POST', headers:{Accept:'application/json'}, body:new FormData(form)}); } catch(err){} }
    $('#cherche').classList.add('sent');
  });
})();

/* Carte : chargée seulement au clic (RGPD) */
(function(){
  const btn = $('#map-btn'); if (!btn) return;
  btn.addEventListener('click', () => {
    let framed = false; try { framed = window.self !== window.top; } catch(e){ framed = true; }
    if (framed) { window.open(`https://www.google.com/maps/search/?api=1&query=${CONFIG.lat},${CONFIG.lng}`, '_blank', 'noopener'); return; }
    const f = document.createElement('iframe');
    f.src = `https://www.google.com/maps?q=${CONFIG.lat},${CONFIG.lng}&z=17&output=embed`;
    f.title = 'Plan d’accès POP Studio Cambrai'; f.loading = 'lazy'; f.referrerPolicy = 'no-referrer-when-downgrade';
    $('#map').replaceChildren(f);
  });
})();

/* Canaux de contact (page Contact) */
(function(){
  const box = $('#channels'); if (!box) return;
  const c = [];
  c.push(CONFIG.phone ? `<a class="ch" href="tel:${CONFIG.phone.replace(/\s/g,'')}"><span class="ic">📞</span><b>Appeler</b><span>${CONFIG.phone}</span></a>`
                      : `<div class="ch off"><span class="ic">📞</span><b>Téléphone</b><span>Bientôt disponible</span></div>`);
  c.push(CONFIG.whatsapp ? `<a class="ch" href="https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent('Bonjour POP Studio, vous avez la paire… en taille… ?')}" target="_blank" rel="noopener"><span class="ic">💬</span><b>WhatsApp</b><span>Réponse rapide</span></a>`
                         : `<div class="ch off"><span class="ic">💬</span><b>WhatsApp</b><span>Bientôt disponible</span></div>`);
  c.push(`<a class="ch" href="${IG}" target="_blank" rel="noopener"><span class="ic">📸</span><b>Instagram</b><span>Écris-nous en message privé</span></a>`);
  c.push(`<a class="ch" href="https://www.facebook.com/p/Pop-Studio-Cambrai-61562744890953/" target="_blank" rel="noopener"><span class="ic">👍</span><b>Facebook</b><span>Pop Studio Cambrai</span></a>`);
  box.innerHTML = c.join('');
})();

/* Fenêtres mentions légales / confidentialité */
$$('[data-dialog]').forEach(b => b.addEventListener('click', () => document.getElementById(b.dataset.dialog).showModal()));
$$('dialog').forEach(d => d.addEventListener('click', e => { if (e.target === d || e.target.hasAttribute('data-close')) d.close(); }));

/* Apparition au scroll */
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), {threshold:.08, rootMargin:'0px 0px -30px 0px'});
  $$('.rv').forEach(el => io.observe(el));
} else { $$('.rv').forEach(el => el.classList.add('in')); }
