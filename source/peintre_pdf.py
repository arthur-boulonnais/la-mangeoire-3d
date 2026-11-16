# Plans et métrés pour le peintre — La Mangeoire. Longueurs mesurées sur le plan Kieffer 1/50 (A3), hauteurs = choix de la maquette.
import json, math, os, sys
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

D = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1]
SOLID = json.load(open(os.path.join(D, 'solid.json'))); BAR = json.load(open(os.path.join(D, 'bargeo.json')))
F = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('S', F + 'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('SB', F + 'DejaVuSans-Bold.ttf'))
W, H = landscape(A4)
INK = HexColor('#1f1a17'); GREY = HexColor('#8a837c'); LGREY = HexColor('#d8d3cd'); BLUE = HexColor('#1d4e89'); RED = HexColor('#a3202b')
C_DECO = HexColor('#b5414c'); C_WP = HexColor('#d98fa0'); C_PAINT = HexColor('#8a5a3c'); C_GLASS = HexColor('#5aa0c8'); C_JOIN = HexColor('#c9b49a')
HC = 3.00  # hypothèse

fr = lambda v, d=2: f"{v:.{d}f}".replace('.', ',')
c = canvas.Canvas(out, pagesize=(W, H)); c.setTitle('La Mangeoire — plans et métrés peintre'); page = [0]

def T(x, y, s, size=8, font='S', col=INK, align='l'):
    c.setFont(font, size); c.setFillColor(col); {'l': c.drawString, 'c': c.drawCentredString, 'r': c.drawRightString}[align](x, y, s)

def header(title, sub):
    page[0] += 1
    T(12*mm, H-13*mm, 'La Mangeoire — ' + title, 14, 'SB'); T(12*mm, H-18.5*mm, sub, 8, 'S', GREY)
    T(W-12*mm, H-13*mm, f'Plans peintre · page {page[0]}/4', 8, 'S', GREY, 'r')
    c.setStrokeColor(LGREY); c.setLineWidth(0.5); c.line(12*mm, H-21*mm, W-12*mm, H-21*mm)
    T(12*mm, 7*mm, "Longueurs mesurées sur le plan Kieffer Menuiserie (éch. 1/50, A3, indice A du 11/09/2026). Hauteur sous plafond NON relevée : 3,00 m pris par hypothèse. Tout est à vérifier sur place avant commande.", 6.5, 'S', RED)

# ---- wall faces (room side), from the 1/50 plan ----
P = [(4.578,10.158),(6.627,10.135),(9.694,10.10),(11.123,10.08),(11.485,9.741),(11.807,10.08),(11.441,10.425),(14.942,10.416),(16.167,8.769),(16.216,8.805),(16.48,7.925),(16.453,7.923),(16.658,4.733),(14.548,4.549),(14.514,4.942),(14.065,4.932),(14.099,4.553),(12.45,4.604),(11.72,5.309),(7.391,5.37),(6.667,5.381),(6.335,5.385),(6.346,5.643),(5.582,5.654),(5.565,5.395),(5.393,5.397),(4.578,5.40)]
L = lambda i: math.dist(P[i], P[(i+1) % len(P)])
# id, edges, kind, label
WALLS = [
 ('M1', [26], 'mix', 'Mur côté cuisine'), ('M2', [0], 'mix2', 'Mur côté entrée 2 (derrière le bar)'), ('F1', [1], 'glass', 'Façade entrée 2'),
 ('M3', [2], 'deco', 'Trumeau entre les façades'), ('P1', [3, 4, 5], 'paint', "Pilier d'angle (3 faces)"), ('F2', [6], 'glass', 'Façade banquette C1'),
 ('F3', [7], 'glass', 'Façade en biais (C2)'), ('F4', [9], 'glass', 'Entrée 1 (porte vitrée)'), ('F5', [11], 'glass', 'Façade banquette B2'),
 ('F6', [12], 'glass', 'Façade banquette B1'), ('M4', [13, 14, 15], 'paint', 'Retours du pilier, coin piano (3 faces)'), ('M5', [16], 'wp', 'Mur du piano'),
 ('M6', [17], 'wp', 'Mur en biais du coin piano'), ('M7', [18], 'deco', 'Grand mur banquette A1'), ('O1', [19], 'open', 'Porte des WC (ouverture)'),
 ('M8', [20], 'paint', 'Retour vers WC / couloir'), ('M9', [21, 22, 23, 24], 'paint', 'Massif entre WC et cuisine (4 faces)'), ('O2', [25], 'open', 'Passage cuisine (porte coulissante)'),
]
KCOL = {'deco': C_DECO, 'wp': C_WP, 'paint': C_PAINT, 'glass': C_GLASS, 'open': LGREY, 'mix': C_PAINT, 'mix2': C_PAINT}
for w in WALLS: w_len = sum(L(i) for i in w[1])
POTEAU = [[13.871,7.049],[14.334,7.084],[14.277,7.772],[13.82,8.198],[13.492,7.857],[13.824,7.546]]

# ================= page 1 : plan 1/50 =================
header('Plan coté (échelle 1/50)', "Vue de dessus · chaque mur est numéroté (M = mur, F = façade vitrée, P = pilier, O = ouverture) · cotes en mètres, côté salle")
SC = 20*mm  # 1 m = 20 mm -> 1/50
X0, Y0 = 4.15, 4.05
OX, OY = 16*mm, H-24*mm
Q = lambda x, y: (OX + (x-X0)*SC, OY - (y-Y0)*SC)
def poly(pts, fill=None, stroke=INK, lw=0.5, dash=None):
    p = c.beginPath(); p.moveTo(*Q(*pts[0]))
    for q in pts[1:]: p.lineTo(*Q(*q))
    p.close(); c.setLineWidth(lw)
    if stroke: c.setStrokeColor(stroke)
    if dash: c.setDash(*dash)
    if fill is not None: c.setFillColor(fill)
    c.drawPath(p, stroke=1 if stroke else 0, fill=1 if fill is not None else 0); c.setDash()
# clip to drawing area
c.saveState(); cl = c.beginPath(); x0, y0 = Q(4.15, 11.05); x1, y1 = Q(17.0, 4.05); cl.rect(x0, y0, x1-x0, y1-y0); c.clipPath(cl, stroke=0, fill=0)
poly(P, fill=HexColor('#faf8f5'), stroke=None)
for s in SOLID: poly(s, fill=HexColor('#cfc9c2'), stroke=GREY, lw=0.3)
# coloured finish strips along each face
for wid, edges, kind, lab in WALLS:
    for i in edges:
        a, b = P[i], P[(i+1) % len(P)]
        c.setStrokeColor(KCOL[kind]); c.setLineWidth(3.2 if kind != 'open' else 1);
        if kind == 'open': c.setDash(2, 1.5)
        c.line(*Q(*a), *Q(*b)); c.setDash()
# back bar / bar / column
poly([(4.578,6.99),(5.21,6.99),(5.21,10.13),(4.578,10.13)], fill=None, stroke=GREY, lw=0.5, dash=(2,1.5))
poly(BAR['inner']+BAR['outer'], fill=None, stroke=GREY, lw=0.5, dash=(2,1.5))
poly(POTEAU, fill=C_PAINT, stroke=INK, lw=0.5)
c.restoreState()
T(*Q(4.65, 8.6), 'arrière-bar', 6, 'S', GREY); T(*Q(6.2, 8.3), 'bar', 6, 'S', GREY)
T(*Q(13.25, 8.55), 'POTEAU', 6, 'SB', INK, 'c'); T(*Q(13.25, 8.8), 'périmètre ' + fr(3.207) + ' m', 6, 'S', INK, 'c')
T(*Q(4.25, 4.95), 'CUISINE', 7, 'SB', GREY); T(*Q(6.85, 4.85), 'WC', 7, 'SB', GREY)
T(*Q(9.2, 7.9), 'SALLE', 10, 'SB', LGREY, 'c'); T(*Q(9.2, 8.25), 'plafond ' + fr(59.04, 1) + ' m²', 7, 'S', GREY, 'c')

# dimension labels along faces, inside the room
CEN = (10.5, 7.5)
def face_label(a, b, text, off=0.22, size=6.3, col=BLUE):
    m = ((a[0]+b[0])/2, (a[1]+b[1])/2); dx, dy = b[0]-a[0], b[1]-a[1]; l = math.hypot(dx, dy); n = (-dy/l, dx/l)
    if (CEN[0]-m[0])*n[0] + (CEN[1]-m[1])*n[1] < 0: n = (-n[0], -n[1])
    p = Q(m[0]+n[0]*off, m[1]+n[1]*off); ang = math.degrees(math.atan2(-(dy), dx))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    c.saveState(); c.translate(*p); c.rotate(ang); c.setFont('SB', size); tw = c.stringWidth(text, 'SB', size)
    c.setFillColor(white); c.rect(-tw/2-0.6*mm, -0.8*mm, tw+1.2*mm, size*0.95+0.6*mm, stroke=0, fill=1); c.setFillColor(col); c.drawCentredString(0, 0, text); c.restoreState()
def inward(a, b, off):
    m = ((a[0]+b[0])/2, (a[1]+b[1])/2); dx, dy = b[0]-a[0], b[1]-a[1]; l = math.hypot(dx, dy); n = (-dy/l, dx/l)
    if (CEN[0]-m[0])*n[0] + (CEN[1]-m[1])*n[1] < 0: n = (-n[0], -n[1])
    return (m[0]+n[0]*off, m[1]+n[1]*off)
OVR = {'P1': (11.47, 9.55), 'M4': (14.3, 5.45), 'M8': (6.5, 5.95), 'M9': (5.95, 6.25), 'O1': (7.03, 5.95), 'O2': (5.0, 5.95), 'M1': (4.95, 6.55), 'F4': (15.75, 8.3)}
for wid, edges, kind, lab in WALLS:
    for i in edges:
        if L(i) >= 0.33: face_label(P[i], P[(i+1) % len(P)], fr(L(i)))
    if wid in OVR: pos = OVR[wid]
    else:
        i = max(edges, key=L); a, b = P[i], P[(i+1) % len(P)]; pos = inward(a, b, 0.62)
    x, y = Q(*pos); c.setFillColor(KCOL[kind] if kind != 'open' else GREY); c.circle(x, y, 2.6*mm, stroke=0, fill=1)
    T(x, y-1.1*mm, wid, 6.2, 'SB', white, 'c')
# legend + scale
lx, ly = 16*mm, 30*mm
for k, (col, txt) in enumerate([(C_DECO, 'Mur habillé : boiserie + velours / miroirs'), (C_WP, 'Mur habillé : boiserie + papier peint'), (C_PAINT, 'Peinture toute hauteur'),
                               (C_GLASS, 'Façade vitrée : allège bois + vitrage + imposte'), (LGREY, 'Ouverture')]):
    x = lx + (k % 3)*88*mm; y = ly - (k // 3)*6*mm
    c.setFillColor(col); c.rect(x, y, 8*mm, 2.4*mm, stroke=0, fill=1); T(x+10*mm, y+0.3*mm, txt, 7.5)
sx, sy = W-14*mm-5*SC, 16*mm
for i in range(5):
    c.setFillColor(INK if i % 2 == 0 else white); c.setStrokeColor(INK); c.setLineWidth(0.4); c.rect(sx+i*SC, sy, SC, 1.8*mm, fill=1)
T(sx, sy-3.5*mm, '0', 6.5); T(sx+5*SC, sy-3.5*mm, '5 m', 6.5, 'S', INK, 'c'); T(sx, sy+4*mm, 'Échelle 1/50 si imprimé en A4 paysage à 100 %', 7, 'SB')
c.showPage()

# ================= page 2 : tableau =================
header('Tableau des murs et finitions', "Longueurs côté salle, ouvertures et finition prévue par la maquette · surfaces calculées avec H = 3,00 m (hypothèse)")
FIN = {'deco': 'Boiserie 0–0,95 · velours / miroirs 0,95–2,67 · corniche bois 2,67–2,86 · peinture au-dessus',
       'wp': 'Boiserie 0–0,95 · PAPIER PEINT 0,95–2,67 · corniche bois 2,67–2,86 · peinture au-dessus',
       'paint': 'Peinture toute hauteur, teinte « brun boiserie »', 'glass': 'Allège bois 0–0,90 · vitrage 0,90–2,60 · imposte peinte 2,60–plafond',
       'open': '—', 'mix': 'Peinture sur 1,59 m visibles ; reste caché par l\'arrière-bar', 'mix2': 'Peinture sur 0,78 m visibles (entre arrière-bar et bar)'}
NOTE = {'M1': "ancienne porte de service (0,82 m) à reboucher, derrière l'arrière-bar", 'M2': 'arrière-bar 0,63 m · zone service 0,78 m · bar 0,65 m',
        'F1': 'porte 0,82 m + vitrines 0,50 m et 1,74 m', 'M7': '4 panneaux ≈ 1,06 m (velours, miroir, velours, miroir) · 2 appliques', 'M5': '1 applique',
        'M6': '1 applique', 'M3': '1 panneau velours', 'F4': 'imposte 2,25–plafond', 'O1': 'tableaux 0,20 m de chaque côté', 'O2': 'dont 0,08 m de mur plein'}
cols = [12*mm, 24*mm, 92*mm, 112*mm, 222*mm]
y = H-30*mm
for x, t in zip(cols, ['N°', 'Emplacement', 'Longueur', 'Finition prévue', 'Remarque']): T(x, y, t, 7.5, 'SB', GREY)
y -= 2*mm; c.setStrokeColor(LGREY); c.line(12*mm, y, W-12*mm, y)
tot = 0
for wid, edges, kind, lab in WALLS:
    l = sum(L(i) for i in edges); tot += l; y -= 8.0*mm
    c.setFillColor(KCOL[kind] if kind != 'open' else LGREY); c.circle(cols[0]+3*mm, y+1.2*mm, 2.6*mm, stroke=0, fill=1); T(cols[0]+3*mm, y, wid, 6.2, 'SB', white, 'c')
    T(cols[1], y, lab, 7.5, 'SB'); T(cols[2], y, fr(l) + ' m', 8, 'SB', BLUE)
    if len(edges) > 1: T(cols[2], y-3.2*mm, ' + '.join(fr(L(i)) for i in edges), 5.8, 'S', GREY)
    # wrap finish text
    words = FIN[kind].split(); line = ''; yy = y
    for wd in words:
        t = (line + ' ' + wd).strip()
        if c.stringWidth(t, 'S', 6.8) > 106*mm: T(cols[3], yy, line, 6.8); yy -= 3.1*mm; line = wd
        else: line = t
    T(cols[3], yy, line, 6.8)
    nw = NOTE.get(wid, '').split(); line = ''; yy = y
    for wd in nw:
        tt = (line + ' ' + wd).strip()
        if c.stringWidth(tt, 'S', 6.2) > (W-14*mm-cols[4]): T(cols[4], yy, line, 6.2, 'S', GREY); yy -= 2.9*mm; line = wd
        else: line = tt
    if line: T(cols[4], yy, line, 6.2, 'S', GREY)
    c.setStrokeColor(HexColor('#eeeae5')); c.line(12*mm, y-4.4*mm, W-12*mm, y-4.4*mm)
y -= 7*mm
T(cols[1], y, 'Périmètre total (ouvertures comprises)', 7.5, 'SB'); T(cols[2]+18*mm, y, fr(tot) + ' m', 8, 'SB', BLUE)
T(cols[1], y-5*mm, 'Poteau (ex-desserte) : 6 faces ' + ' · '.join(fr(math.dist(POTEAU[i], POTEAU[(i+1) % 6])) for i in range(6)) + ' = ' + fr(3.207) + ' m de périmètre, peinture toute hauteur (socle et corniche bois)', 7)
c.showPage()

# ================= page 3 : coupes de hauteur + coloris =================
header('Hauteurs des finitions et coloris', "Coupes types (sans échelle, cotes en mètres) · hauteurs choisies dans la maquette, à valider · hauteur sous plafond à mesurer")
K = 42*mm  # 1 m = 42 mm (sans échelle, cotes écrites)
def band(x, y0, y1, w, col, label, txtcol=INK):
    c.setFillColor(col); c.setStrokeColor(INK); c.setLineWidth(0.4); c.rect(x, BY + y0*K, w, (y1-y0)*K, fill=1, stroke=1)
    if label: T(x + w/2, BY + (y0+y1)/2*K - 1.2*mm, label, 6.2, 'SB', txtcol, 'c')
def dim(x, ys):
    c.setStrokeColor(BLUE); c.setLineWidth(0.4)
    for a, b in zip(ys[:-1], ys[1:]):
        c.line(x, BY + a*K, x, BY + b*K)
        for v in (a, b): c.line(x-1.2*mm, BY + v*K, x+1.2*mm, BY + v*K)
        T(x - 1.8*mm, BY + (a+b)/2*K - 1*mm, fr(b-a), 6, 'SB', BLUE, 'r')
    for v in ys: T(x + 2*mm, BY + v*K - 1*mm, fr(v), 5.8, 'S', GREY)
BY = 30*mm; bw = 26*mm
TYPES = [
 ('Mur habillé velours / miroirs', 'M3, M7 (et M2 caché)', [(0, .95, C_JOIN, 'boiserie'), (.95, 2.67, C_DECO, 'velours / miroirs'), (2.67, 2.86, C_JOIN, 'corniche'), (2.86, 3.0, C_PAINT, '')], [0, .95, 2.67, 2.86, 3.0]),
 ('Mur habillé papier peint', 'M5, M6 (coin piano)', [(0, .95, C_JOIN, 'boiserie'), (.95, 2.67, C_WP, 'papier peint'), (2.67, 2.86, C_JOIN, 'corniche'), (2.86, 3.0, C_PAINT, '')], [0, .95, 2.67, 2.86, 3.0]),
 ('Façade vitrée (côté salle)', 'F1, F2, F3, F5, F6', [(0, .90, C_JOIN, 'allège bois'), (.90, 2.60, HexColor('#cfe3ee'), 'vitrage'), (2.60, 3.0, C_PAINT, 'imposte')], [0, .90, 2.60, 3.0]),
 ('Peinture toute hauteur', 'M1, M2 visibles, M4, M8, M9, P1, poteau', [(0, 3.0, C_PAINT, 'peinture')], [0, 3.0]),
]
for k, (tt, which, bands, ys) in enumerate(TYPES):
    x = 26*mm + k*50*mm
    for (a, b, col, lab) in bands: band(x, a, b, bw, col, lab, white if col in (C_DECO, C_PAINT) else INK)
    dim(x - 3*mm, ys); T(x + bw/2, BY + 3.0*K + 6*mm, tt, 7.5, 'SB', INK, 'c'); T(x + bw/2, BY + 3.0*K + 2.2*mm, which, 6.3, 'S', GREY, 'c')
    c.setStrokeColor(INK); c.setLineWidth(0.8); c.line(x-6*mm, BY, x+bw+4*mm, BY)
T(26*mm, BY - 6*mm, "Filet laiton à 0,95 m sur les murs habillés · corniche bois avec ruban LED (éclairage indirect) de 2,67 à 2,86 m · le haut de mur au-dessus de la corniche prend la teinte du plafond.", 6.8)
# colours
cy = 20*mm
COLS = [('#3a2216', 'Plafond et haut de mur', 'brun très foncé, mat (proche RAL 8017)'), ('#4a2c1f', 'Peinture murs / poteau / impostes', 'brun « boiserie » (proche RAL 8017), velours ou satin'),
        ('#6a1820', 'Devanture extérieure', 'bordeaux (proche RAL 3005), satin')]
T(222*mm, BY + 3.0*K + 6*mm, 'Coloris de la maquette', 7.5, 'SB')
for k, (hx, name, desc) in enumerate(COLS):
    yy = BY + 3.0*K - 6*mm - k*14*mm
    c.setFillColor(HexColor(hx)); c.rect(222*mm, yy-5*mm, 10*mm, 9*mm, stroke=0, fill=1)
    T(234*mm, yy+0.5*mm, name, 7, 'SB'); T(234*mm, yy-3.2*mm, desc, 5.8, 'S', GREY); T(234*mm, yy-6.5*mm, hx, 5.8, 'S', GREY)
T(222*mm, BY + 3.0*K - 48*mm, 'Teintes indicatives d\'après l\'écran :', 6.5, 'S', RED); T(222*mm, BY + 3.0*K - 51.5*mm, 'à choisir sur nuancier réel avant achat.', 6.5, 'S', RED)
c.showPage()

# ================= page 4 : surfaces =================
header('Récapitulatif des surfaces', "Calculé avec une hauteur sous plafond de 3,00 m (HYPOTHÈSE) · surfaces nettes, sans majoration pour pertes")
WP_L = L(16) + L(17)
paint_full = {'M1 (partie visible)': 1.59, 'M2 (zone service visible)': 0.78, 'M4': sum(L(i) for i in (13, 14, 15)), 'M8': L(20), 'M9': sum(L(i) for i in (21, 22, 23, 24)), 'P1': sum(L(i) for i in (3, 4, 5)), 'Poteau': 3.207}
deco_top = L(2) + L(18) + WP_L
glass = [L(1), L(6), L(7), L(11), L(12)]
rows = []
for k, v in paint_full.items(): rows.append(('Peinture murs toute hauteur — ' + k, f'{fr(v)} m × {fr(HC)} m', v*HC))
rows.append(('Haut de mur au-dessus des corniches (M3, M5, M6, M7)', f'{fr(deco_top)} m × {fr(HC-2.86)} m', deco_top*(HC-2.86)))
rows.append(('Impostes au-dessus des vitrines (F1, F2, F3, F5, F6)', f'{fr(sum(glass))} m × {fr(HC-2.60)} m', sum(glass)*(HC-2.60)))
rows.append(('Imposte au-dessus de l\'entrée 1 (F4)', f'{fr(L(9))} m × {fr(HC-2.25)} m', L(9)*(HC-2.25)))
paint_tot = sum(r[2] for r in rows)
rows2 = [('Plafond salle (poteau déduit)', f'{fr(59.57)} − {fr(0.53)} m²', 59.04), ('Papier peint coin piano (M5 + M6)', f'{fr(WP_L)} m × {fr(1.70)} m', WP_L*1.70)]
y = H-32*mm
T(14*mm, y, 'Poste', 7.5, 'SB', GREY); T(160*mm, y, 'Calcul', 7.5, 'SB', GREY); T(W-14*mm, y, 'Surface', 7.5, 'SB', GREY, 'r'); y -= 2*mm; c.setStrokeColor(LGREY); c.line(12*mm, y, W-12*mm, y)
for name, calc, s in rows:
    y -= 6.6*mm; T(14*mm, y, name, 7.5); T(160*mm, y, calc, 7.5, 'S', GREY); T(W-14*mm, y, fr(s) + ' m²', 8, 'SB', BLUE, 'r')
y -= 7*mm; c.line(12*mm, y+4.5*mm, W-12*mm, y+4.5*mm); T(14*mm, y, 'Total peinture murs', 8.5, 'SB'); T(W-14*mm, y, fr(paint_tot) + ' m²', 9, 'SB', BLUE, 'r')
y -= 4*mm
for name, calc, s in rows2:
    y -= 7*mm; T(14*mm, y, name, 8.5, 'SB'); T(160*mm, y, calc, 7.5, 'S', GREY); T(W-14*mm, y, fr(s) + ' m²', 9, 'SB', BLUE, 'r')
y -= 10*mm
T(14*mm, y, 'À vérifier ou à mesurer sur place avant le devis du peintre :', 8.5, 'SB', RED)
for k, s in enumerate(["Hauteur sous plafond réelle (toutes les surfaces ci-dessus changent avec elle : ± 10 cm = ± " + fr((sum(paint_full.values()))*0.10) + " m² sur les murs peints toute hauteur).",
                       "Hauteurs des boiseries (0,95 m), du vitrage (2,60 m), de la corniche (2,67–2,86 m) et des portes : ce sont des choix de la maquette, pas des relevés.",
                       "Qui fait quoi : boiseries, corniches et allèges (menuisier), velours (tapissier), miroirs (miroitier), papier peint (peintre ou poseur).",
                       "Ancienne porte de service sur M1 à reboucher avant peinture (cachée ensuite par l'arrière-bar).",
                       "Les faces du pilier P1 et du massif M9 sont mesurées au plan : relever leurs faces réelles (habillage éventuel).",
                       "Plafond : surface de la salle seule (cuisine et WC non compris)."]):
    T(18*mm, y - (k+1)*5.2*mm, '• ' + s, 7.3)
c.showPage(); c.save(); print('ok', out, 'peinture murs', round(paint_tot, 2), 'pp', round(WP_L*1.7, 2), 'perim', round(sum(L(i) for i in range(len(P))), 3))
