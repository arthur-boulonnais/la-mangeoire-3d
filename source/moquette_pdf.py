# Plan moquette — La Mangeoire. Contour mesuré sur le plan Kieffer 1/50 (A3).
import json, math, os, sys
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

D = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1]
SOLID = json.load(open(os.path.join(D, 'solid.json'))); BAR = json.load(open(os.path.join(D, 'bargeo.json')))
F = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('S', F + 'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('SB', F + 'DejaVuSans-Bold.ttf'))
W, H = landscape(A4)
INK = HexColor('#1f1a17'); GREY = HexColor('#8a837c'); LGREY = HexColor('#d8d3cd'); BLUE = HexColor('#1d4e89'); RED = HexColor('#a3202b')
CARPET = HexColor('#e8cfa6'); SERV = HexColor('#f3e6c9'); EXCL = HexColor('#ffffff'); WCF = HexColor('#e9e2e2')
fr = lambda v, d=2: f"{v:.{d}f}".replace('.', ',')
c = canvas.Canvas(out, pagesize=(W, H)); c.setTitle('La Mangeoire — plan moquette'); page = [0]

def T(x, y, s, size=8, font='S', col=INK, align='l'):
    c.setFont(font, size); c.setFillColor(col); {'l': c.drawString, 'c': c.drawCentredString, 'r': c.drawRightString}[align](x, y, s)
def header(title, sub):
    page[0] += 1
    T(12*mm, H-13*mm, 'La Mangeoire — ' + title, 14, 'SB'); T(12*mm, H-18.5*mm, sub, 8, 'S', GREY)
    T(W-12*mm, H-13*mm, f'Plan moquette · page {page[0]}/2', 8, 'S', GREY, 'r')
    c.setStrokeColor(LGREY); c.setLineWidth(0.5); c.line(12*mm, H-21*mm, W-12*mm, H-21*mm)
    T(12*mm, 7*mm, "Contour mesuré sur le plan Kieffer Menuiserie (éch. 1/50, A3, indice A du 11/09/2026). Cotes à vérifier par relevé sur place avant découpe.", 6.5, 'S', RED)
def area(poly):
    a = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % len(poly)]; a += x1*y2 - x2*y1
    return abs(a)/2

# inner outline of the dining room (room side of every wall), threshold lines across the doors
P = [(4.578,10.158),(6.627,10.135),(9.694,10.10),(11.123,10.08),(11.485,9.741),(11.807,10.08),(11.441,10.425),(14.942,10.416),(16.167,8.769),(16.216,8.805),(16.48,7.925),(16.453,7.923),(16.658,4.733),(14.548,4.549),(14.514,4.942),(14.065,4.932),(14.099,4.553),(12.45,4.604),(11.72,5.309),(7.391,5.37),(6.667,5.381),(6.335,5.385),(6.346,5.643),(5.582,5.654),(5.565,5.395),(5.393,5.397),(4.578,5.40)]
L = lambda i: math.dist(P[i], P[(i+1) % len(P)])
POTEAU = [(13.871,7.049),(14.334,7.084),(14.277,7.772),(13.82,8.198),(13.492,7.857),(13.824,7.546)]
BARP = [tuple(p) for p in BAR['inner'] + BAR['outer']]
BACK = [(4.578,6.99),(5.21,6.99),(5.21,10.13),(4.578,10.13)]
inner = [tuple(p) for p in BAR['inner']]
SERVICE = [(5.21,6.99),(5.21,10.13)] + inner + [(6.196,6.99)]
A_room = area(P); A_pot = area(POTEAU); A_bar = area(BARP); A_back = area(BACK); A_serv = area(SERVICE)
A_full = A_room - A_pot; A_noFurn = A_full - A_bar - A_back; A_salle = A_noFurn - A_serv

# ---------------- page 1 : plan ----------------
header('Plan moquette (échelle 1/50)', "Vue de dessus · zone à moquetter en couleur · longueurs des murs côté salle, en mètres")
SC = 20*mm; X0, Y0 = 4.15, 4.05; OX, OY = 16*mm, H-26*mm
Q = lambda x, y: (OX + (x-X0)*SC, OY - (y-Y0)*SC)
def poly(pts, fill=None, stroke=INK, lw=0.5, dash=None):
    p = c.beginPath(); p.moveTo(*Q(*pts[0]))
    for q in pts[1:]: p.lineTo(*Q(*q))
    p.close(); c.setLineWidth(lw)
    if stroke: c.setStrokeColor(stroke)
    if dash: c.setDash(*dash)
    if fill is not None: c.setFillColor(fill)
    c.drawPath(p, stroke=1 if stroke else 0, fill=1 if fill is not None else 0); c.setDash()
c.saveState(); cl = c.beginPath(); x0, y0 = Q(4.15, 11.0); x1, y1 = Q(17.0, 4.15); cl.rect(x0, y0, x1-x0, y1-y0); c.clipPath(cl, stroke=0, fill=0)
poly(P, fill=CARPET, stroke=None)
poly(SERVICE, fill=SERV, stroke=GREY, lw=0.4, dash=(2, 1.5))
for s in SOLID: poly(s, fill=HexColor('#cfc9c2'), stroke=GREY, lw=0.3)
poly(BACK, fill=EXCL, stroke=INK, lw=0.6); poly(BARP, fill=EXCL, stroke=INK, lw=0.6); poly(POTEAU, fill=EXCL, stroke=INK, lw=0.6)
poly(P, fill=None, stroke=INK, lw=1.1)
c.restoreState()
# thresholds (doors) in red
for (a, b, lab) in [((7.391,5.37),(6.667,5.381),'seuil WC 0,72'), ((5.393,5.397),(4.578,5.40),'seuil cuisine 0,82'), ((7.127,10.12),(7.95,10.11),'seuil entrée 2 0,82'), ((16.216,8.805),(16.48,7.925),'seuil entrée 1 0,92')]:
    c.setStrokeColor(RED); c.setLineWidth(2.2); c.line(*Q(*a), *Q(*b))
CEN = (10.5, 7.5)
def face_label(a, b, text, off=0.22, size=6.3, col=BLUE):
    m = ((a[0]+b[0])/2, (a[1]+b[1])/2); dx, dy = b[0]-a[0], b[1]-a[1]; l = math.hypot(dx, dy); n = (-dy/l, dx/l)
    if (CEN[0]-m[0])*n[0] + (CEN[1]-m[1])*n[1] < 0: n = (-n[0], -n[1])
    p = Q(m[0]+n[0]*off, m[1]+n[1]*off); ang = math.degrees(math.atan2(-dy, dx))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    c.saveState(); c.translate(*p); c.rotate(ang); c.setFont('SB', size); tw = c.stringWidth(text, 'SB', size)
    c.setFillColor(white); c.rect(-tw/2-0.6*mm, -0.8*mm, tw+1.2*mm, size*0.95+0.6*mm, stroke=0, fill=1); c.setFillColor(col); c.drawCentredString(0, 0, text); c.restoreState()
for i in range(len(P)):
    if L(i) >= 0.33: face_label(P[i], P[(i+1) % len(P)], fr(L(i)))
# overall dimensions
def dimline(a, b, text, col=INK):
    c.setStrokeColor(col); c.setLineWidth(0.5); c.line(*Q(*a), *Q(*b))
    ang = math.atan2(b[1]-a[1], b[0]-a[0])
    for p in (a, b):
        x, y = Q(*p); c.line(x-1.4*mm*math.cos(ang+math.pi/4)*0+(-1.2*mm), y, x+1.2*mm, y) if abs(math.cos(ang)) < 0.5 else c.line(x, y-1.2*mm, x, y+1.2*mm)
    m = Q((a[0]+b[0])/2, (a[1]+b[1])/2); c.saveState(); c.translate(*m)
    if abs(math.cos(ang)) < 0.5: c.rotate(90)
    c.setFont('SB', 7.5); tw = c.stringWidth(text, 'SB', 7.5); c.setFillColor(white); c.rect(-tw/2-1*mm, -1*mm, tw+2*mm, 3.6*mm, stroke=0, fill=1); c.setFillColor(col); c.drawCentredString(0, 0, text); c.restoreState()
dimline((4.578, 10.85), (16.658, 10.85), 'longueur hors tout 12,08 m (mur cuisine → vitrine droite)')
dimline((17.0, 4.549), (17.0, 10.425), 'largeur hors tout 5,88 m')
dimline((10.0, 5.33), (10.0, 10.09), '4,76 m')
dimline((12.9, 4.59), (12.9, 10.42), '5,83 m')
T(*Q(13.25, 8.55), 'poteau', 6, 'SB', INK, 'c'); T(*Q(6.0, 8.6), 'bar', 6.5, 'SB', INK, 'c'); T(*Q(4.9, 8.6), 'arrière-', 6, 'S', INK, 'c'); T(*Q(4.9, 8.8), 'bar', 6, 'S', INK, 'c')
T(*Q(5.55, 7.6), 'zone', 6, 'S', GREY, 'c'); T(*Q(5.55, 7.8), 'service', 6, 'S', GREY, 'c')
T(*Q(7.03, 4.95), 'WC', 7, 'SB', GREY, 'c'); T(*Q(4.4, 4.7), 'CUISINE', 7, 'SB', GREY)
T(*Q(8.3, 7.9), 'MOQUETTE', 11, 'SB', HexColor('#a8875b'), 'c')
# legend + scale
lx, ly = 16*mm, 26*mm
for k, (col, txt, dash) in enumerate([(CARPET, 'Moquette léopard', None), (SERV, 'Zone service derrière le bar : à décider', (2, 1.5)), (EXCL, 'Pas de moquette (bar, arrière-bar, poteau)', None), (RED, 'Seuil / barre de seuil', None)]):
    x = lx + k*66*mm; c.setFillColor(col); c.setStrokeColor(GREY if col != RED else RED); c.setLineWidth(0.5)
    if dash: c.setDash(*dash)
    c.rect(x, ly, 8*mm, 3*mm, fill=1, stroke=1); c.setDash(); T(x+10*mm, ly+0.6*mm, txt, 7.2)
sx, sy = W-14*mm-5*SC, 15*mm
for i in range(5):
    c.setFillColor(INK if i % 2 == 0 else white); c.setStrokeColor(INK); c.setLineWidth(0.4); c.rect(sx+i*SC, sy, SC, 1.8*mm, fill=1)
T(sx, sy-3.5*mm, '0', 6.5); T(sx+5*SC, sy-3.5*mm, '5 m', 6.5, 'S', INK, 'c'); T(sx, sy+4*mm, 'Échelle 1/50 si imprimé en A4 paysage à 100 %', 7, 'SB')
c.showPage()

# ---------------- page 2 : surfaces ----------------
header('Surfaces et points à régler', "Surfaces nettes calculées sur le plan (sans chutes) · la quantité à commander dépend de la largeur du rouleau et du raccord du motif")
y = H-34*mm
T(14*mm, y, 'Surface', 8, 'SB', GREY); T(W-14*mm, y, 'm²', 8, 'SB', GREY, 'r'); y -= 2*mm; c.setStrokeColor(LGREY); c.line(12*mm, y, W-12*mm, y)
rows = [('Salle entière (contour des murs)', A_room, False), ('− poteau', -A_pot, False), ('− bar', -A_bar, False), ('− arrière-bar', -A_back, False)]
for name, v, b in rows:
    y -= 6.5*mm; T(14*mm, y, name, 8.5); T(W-14*mm, y, fr(v), 9, 'S', INK, 'r')
y -= 3*mm; c.line(12*mm, y, W-12*mm, y)
y -= 7*mm; T(14*mm, y, 'Option A — moquette partout, zone service derrière le bar comprise', 9.5, 'SB'); T(W-14*mm, y, fr(A_noFurn), 11, 'SB', BLUE, 'r')
y -= 8*mm; T(14*mm, y, 'Option B — sans la zone service (' + fr(A_serv) + ' m², sol dur conseillé : eau, passages)', 9.5, 'SB'); T(W-14*mm, y, fr(A_salle), 11, 'SB', BLUE, 'r')
y -= 9*mm; T(14*mm, y, 'Avec 10 % de chutes : option A ≈ ' + fr(A_noFurn*1.1, 1) + ' m² · option B ≈ ' + fr(A_salle*1.1, 1) + ' m² (indicatif ; le poseur calcule selon son calepinage).', 8.5, 'S', INK)
y -= 14*mm
T(14*mm, y, 'Dimensions utiles', 9.5, 'SB'); y -= 6*mm
for s in ["Longueur hors tout : 12,08 m (mur côté cuisine → vitrine de droite).",
          "Largeur : 4,76 m au niveau du bar (mur A1 → mur côté entrée 2), 5,83 m au coin piano (mur du piano → vitrine C1), 5,88 m hors tout.",
          "Périmètre de la salle : " + fr(sum(L(i) for i in range(len(P)))) + " m (ouvertures comprises) · poteau : 3,21 m de périmètre · bar : 4,62 m côté clients.",
          "Toutes les longueurs de murs sont notées sur le plan, page 1."]:
    T(18*mm, y, '• ' + s, 8); y -= 5*mm
y -= 6*mm
T(14*mm, y, 'À régler avec le poseur', 9.5, 'SB', RED); y -= 6*mm
for s in ["Zone service derrière le bar : moquette ou sol dur ? (option A ou B ci-dessus).",
          "Bar et arrière-bar : posés sur la moquette ou sur la chape ? Ici, la moquette s'arrête au pied des meubles.",
          "Seuils (en rouge) : entrée 1 (0,92 m), entrée 2 (0,82 m), porte cuisine (0,82 m), porte WC (0,72 m, côté WC sol en marbre).",
          "Motif léopard : raccord du motif à prévoir entre les lés ; sens de pose conseillé dans la longueur de la salle.",
          "Les WC (damier marbre) et la cuisine (carrelage) ne sont pas comptés."]:
    T(18*mm, y, '• ' + s, 8); y -= 5*mm
c.showPage(); c.save()
print('ok', round(A_room, 2), round(A_pot, 2), round(A_bar, 2), round(A_back, 2), round(A_serv, 2), round(A_noFurn, 2), round(A_salle, 2))
