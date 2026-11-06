# Dimensioned drawing of the La Mangeoire bar (plan 1:30, section 1:10, back-bar elevation 1:30)
import json, math, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas

D = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(D, 'bargeo.json')))
SOLID = json.load(open(os.path.join(D, 'solid.json')))
out = sys.argv[1]
W, H = A4
INK = HexColor('#222222'); GREY = HexColor('#8a8580'); WALL = HexColor('#cfcac3'); BAR = HexColor('#e6d3bd')
BACK = HexColor('#efe4d6'); RED = HexColor('#8c1c24'); DIM = HexColor('#1d4e89'); LIGHT = HexColor('#b9b4ad')
fr = lambda v: f"{v:.2f}".replace('.', ',')

c = canvas.Canvas(out, pagesize=A4)
c.setTitle('La Mangeoire - Bar - plan coté'); c.setAuthor('Maquette La Mangeoire')

def header(title, sub, page):
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 15); c.drawString(15*mm, H-17*mm, 'La Mangeoire — ' + title)
    c.setFont('Helvetica', 8.5); c.setFillColor(GREY); c.drawString(15*mm, H-22.5*mm, sub)
    c.drawRightString(W-15*mm, H-17*mm, f'Page {page}/2')
    c.setStrokeColor(LIGHT); c.setLineWidth(0.4); c.line(15*mm, H-25*mm, W-15*mm, H-25*mm)
    c.setFont('Helvetica', 7); c.setFillColor(GREY)
    c.drawString(15*mm, 9*mm, "Cotes issues de la maquette 3D (plan Kieffer au 1/50 + plan de disposition). À vérifier par relevé sur place avant fabrication.")

def arrow_dim(x1, y1, x2, y2, text, size=7.5, col=DIM, tick=1.6*mm, tpos=0.5, toff=1.6*mm):
    c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(0.5)
    c.line(x1, y1, x2, y2)
    a = math.atan2(y2-y1, x2-x1)
    for (x, y) in ((x1, y1), (x2, y2)):  # architectural ticks
        c.line(x - tick*math.cos(a+math.pi/4), y - tick*math.sin(a+math.pi/4), x + tick*math.cos(a+math.pi/4), y + tick*math.sin(a+math.pi/4))
    mx, my = x1+(x2-x1)*tpos, y1+(y2-y1)*tpos
    deg = math.degrees(a)
    if deg > 90 or deg < -90: deg += 180
    c.saveState(); c.translate(mx, my); c.rotate(deg); c.setFont('Helvetica-Bold', size)
    tw = c.stringWidth(text, 'Helvetica-Bold', size)
    c.setFillColor(white); c.rect(-tw/2-0.8*mm, toff-0.6*mm, tw+1.6*mm, size*0.95+0.6*mm, stroke=0, fill=1)
    c.setFillColor(col); c.drawCentredString(0, toff, text); c.restoreState()

def ext(x1, y1, x2, y2, col=DIM):
    c.setStrokeColor(col); c.setLineWidth(0.25); c.setDash(1.2, 1.2); c.line(x1, y1, x2, y2); c.setDash()

def note(x, y, text, size=7, col=INK, bold=False, align='l'):
    c.setFillColor(col); c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    (c.drawString if align == 'l' else c.drawCentredString if align == 'c' else c.drawRightString)(x, y, text)

# ------------------------------------------------------------------ page 1: plan 1:30
header('Bar · plan coté', 'Vue de dessus, échelle 1/30 sur A4 · même orientation que le plan Kieffer (cuisine à gauche, entrée 2 en bas)', 1)
S = 1000/30*mm/1000  # points per mm at 1:30 -> per metre below
SC = 1000/30*mm      # points per metre
X0, X1, Y0, Y1 = 4.1, 8.95, 5.2, 10.95
LEFT, TOP = 22*mm, H-32*mm
P = lambda x, y: (LEFT + (x-X0)*SC, TOP - (y-Y0)*SC)
def poly(pts, fill=None, stroke=INK, lw=0.6, dash=None):
    p = c.beginPath(); x, y = P(*pts[0]); p.moveTo(x, y)
    for q in pts[1:]: p.lineTo(*P(*q))
    p.close(); c.setLineWidth(lw); c.setStrokeColor(stroke)
    if dash: c.setDash(*dash)
    if fill is not None: c.setFillColor(fill)
    c.drawPath(p, stroke=1 if stroke else 0, fill=1 if fill is not None else 0); c.setDash()

c.saveState()
bx0, by0 = P(X0, Y1); bx1, by1 = P(X1, Y0)
clip = c.beginPath(); clip.rect(bx0, by0, bx1-bx0, by1-by0); c.clipPath(clip, stroke=0, fill=0)
for s in SOLID: poly(s, fill=WALL, stroke=GREY, lw=0.4)
# thin facade (entrée 2) and its sliding door
for (a, b) in [((6.627, 10.14), (9.694, 10.10)), ((6.627, 10.19), (9.694, 10.155))]:
    c.setStrokeColor(GREY); c.setLineWidth(0.5); c.line(*P(*a), *P(*b))
# kitchen sliding door + WC door
c.setStrokeColor(GREY); c.setLineWidth(1.2); c.line(*P(4.66, 5.35), *P(5.39, 5.35)); c.line(*P(6.67, 5.28), *P(7.39, 5.28))
# neighbouring furniture (grey)
for (tx, tz) in [(8.24, 6.28), (8.30, 9.22)]:
    poly([(tx-.3, tz-.3), (tx+.3, tz-.3), (tx+.3, tz+.3), (tx-.3, tz+.3)], fill=white, stroke=LIGHT, lw=0.5)
c.setStrokeColor(LIGHT); c.circle(*P(8.30, 8.74), 0.25*SC, stroke=1, fill=0)
poly([(8.52, 5.355), (9.2, 5.35), (9.2, 5.965), (8.52, 5.965)], fill=white, stroke=LIGHT, lw=0.5)
poly([(8.62, 9.49), (9.2, 9.49), (9.2, 10.10), (8.62, 10.10)], fill=white, stroke=LIGHT, lw=0.5)
# back bar
poly([(4.578, 6.99), (5.21, 6.99), (5.21, 10.13), (4.578, 10.13)], fill=BACK, stroke=INK, lw=0.6)
# bar: top overhang (dashed), body, stools
inner, outer = R['inner'], R['outer']
def offset_outer(d):
    res = []
    for p in outer:
        q = min(inner, key=lambda r: math.dist(p, r)); n = math.dist(p, q)
        res.append((p[0]+(p[0]-q[0])/n*d, p[1]+(p[1]-q[1])/n*d))
    return res
poly(inner+offset_outer(0.05), fill=None, stroke=INK, lw=0.4, dash=(2, 1.5))
poly(inner+outer, fill=BAR, stroke=INK, lw=0.9)
for i, (sx, sz) in enumerate(R['stools']):
    c.setStrokeColor(GREY); c.setLineWidth(0.4); c.setDash(1.5, 1); c.circle(*P(sx, sz), 0.19*SC, stroke=1, fill=0); c.setDash()
    note(P(sx, sz)[0], P(sx, sz)[1]-2.5, str(i+1), 7, GREY, True, 'c')
c.restoreState()
# frame and room labels
c.setStrokeColor(LIGHT); c.setLineWidth(0.4); c.rect(bx0, by0, bx1-bx0, by1-by0)
note(*P(4.25, 5.75), 'CUISINE', 7, GREY, True); note(*P(6.75, 5.12), 'WC', 7, GREY, True)
note(*P(7.3, 10.8), 'ENTRÉE 2 (façade)', 7, GREY, True); note(*P(4.62, 8.6), 'ARRIÈRE-', 6.5, INK, True); note(*P(4.62, 8.75), 'BAR', 6.5, INK, True)
note(*P(6.32, 8.25), 'BAR', 9, RED, True, 'c'); note(*P(5.55, 8.0), 'service', 6.5, GREY, False, 'c'); note(*P(7.2, 9.95), 'côté clients', 6.5, GREY, False, 'c')
note(*P(8.3, 6.28), 'table', 6, GREY, False, 'c'); note(*P(8.3, 9.22), 'table', 6, GREY, False, 'c')

# dimensions
x_d = 8.72
ext(*P(6.158, 6.598), *P(x_d+0.05, 6.598)); ext(*P(6.64, 10.14), *P(x_d+0.05, 10.14))
arrow_dim(*P(x_d, 6.598), *P(x_d, 10.14), 'Longueur hors tout ' + fr(10.14-6.598) + ' m')
y_d = 10.78
ext(*P(R['xmin'], 9.44), *P(R['xmin'], y_d+0.04)); ext(*P(R['xmax'], 7.75), *P(R['xmax'], y_d+0.04))
arrow_dim(*P(R['xmin'], y_d), *P(R['xmax'], y_d), 'Largeur hors tout ' + fr(R['xmax']-R['xmin']) + ' m')
y_w = 10.42
ext(*P(4.578, 10.16), *P(4.578, y_w+0.04))
arrow_dim(*P(4.578, y_w), *P(5.99, y_w), fr(5.99-4.578) + ' m depuis le mur cuisine', size=6.5)
arrow_dim(*P(5.99, y_w), *P(6.64, y_w), fr(0.65), size=6.5)
arrow_dim(*P(5.21, R['aisle_at'][1]), *P(R['aisle_at'][0], R['aisle_at'][1]), fr(R['aisle_min']), size=6.5, col=RED)
note(*P(5.25, R['aisle_at'][1]+0.17), 'passage service mini', 6, RED)
arrow_dim(*P(6.158, 5.654), *P(6.158, 6.598), fr(6.598-5.654), size=6.5, col=RED, tpos=0.5)
note(*P(6.22, 6.2), 'passage', 6, RED); note(*P(6.22, 6.32), 'vers cuisine/WC', 6, RED)
x_b = 4.24
ext(*P(4.377, 6.99), *P(x_b-0.04, 6.99)); ext(*P(4.377, 10.13), *P(x_b-0.04, 10.13))
arrow_dim(*P(x_b, 6.99), *P(x_b, 10.13), 'Arrière-bar ' + fr(10.13-6.99) + ' m', size=6.5)
arrow_dim(*P(4.578, 6.88), *P(5.21, 6.88), fr(0.63), size=6, tpos=0.5)
# counter depths at four sections
for (a, b, t) in [((7.436, 7.751), (6.736, 7.76), fr(0.70)), (tuple(R['depth_min_at']), None, fr(R['depth_min'])),
                  ((6.158, 6.598), (6.196, 7.344), fr(0.75))]:
    if b is None:
        q = min(inner, key=lambda r: math.dist(a, r)); b = tuple(q)
    arrow_dim(*P(*a), *P(*b), t, size=6, col=INK, toff=1.2*mm)
ra = R['rad_min_at']; c.setStrokeColor(INK); c.setLineWidth(0.3); c.line(*P(*ra), *P(ra[0]+0.45, ra[1]-0.32))
note(*P(ra[0]+0.47, ra[1]-0.34), 'R mini ≈ ' + fr(R['rad_min']) + ' m', 6.5, INK, True)

# scale bar
sx, sy = LEFT, by0 - 9*mm
for i in range(5):
    c.setFillColor(INK if i % 2 == 0 else white); c.setStrokeColor(INK); c.setLineWidth(0.4); c.rect(sx + i*0.5*SC, sy, 0.5*SC, 1.6*mm, fill=1)
note(sx, sy - 3.5*mm, '0', 6.5); note(sx + 2.5*SC, sy - 3.5*mm, '2,5 m', 6.5, INK, False, 'c'); note(sx + 2.6*SC + 4*mm, sy + 0.3*mm, 'Échelle 1/30', 7, INK, True)
# legend / notes block
ny = sy - 12*mm
note(15*mm, ny, 'À retenir', 8.5, INK, True)
lines = [
    f"Développé côté clients (face galbée) : {fr(R['len_outer'])} m  ·  côté service : {fr(R['len_inner'])} m  ·  profondeur du comptoir {fr(R['depth_min'])} à {fr(R['depth_max'])} m (env. 0,70 m).",
    "Le bar part du mur de façade (entrée 2) sur 0,65 m et se termine en crochet côté cuisine ; plateau débordant de 5 cm côté clients (pointillés).",
    f"6 tabourets (cercles numérotés, Ø 38 cm) espacés d'environ 0,95 m ; tabouret 6 très proche du 5 (0,46 m), à repositionner ou supprimer.",
    "Points serrés : tabouret 2 à ~18 cm de la table près des WC ; tabouret 4 à ~23 cm de la chaise de la table près de l'entrée 2.",
]
for i, l in enumerate(lines): note(15*mm, ny - (i+1)*4.2*mm, '• ' + l, 6.8)
c.showPage()

# ------------------------------------------------------------------ page 2: section and back-bar elevation
header('Bar · coupe et arrière-bar', 'Coupe type du comptoir au 1/15 · élévation de l\'arrière-bar au 1/30 · hauteurs en mètres', 2)
# section A-A, 1:10
K = 1000/15*mm  # points per metre at 1:15
ox, oy = 45*mm, H-118*mm
Q = lambda x, y: (ox + x*K, oy + y*K)
dep = 0.70
note(15*mm, H-33*mm, 'Coupe type A-A (au 1/15)', 9, INK, True)
c.setStrokeColor(INK); c.setLineWidth(0.8); c.line(*Q(-0.25, 0), *Q(1.25, 0))
for i in range(20): c.setLineWidth(0.3); c.line(*Q(-0.25+i*0.075, 0), *Q(-0.29+i*0.075, -0.03))
def rect(x, y, w, h, fill, stroke=INK, lw=0.6):
    c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(lw); c.rect(*Q(x, y), w*K, h*K, fill=1, stroke=1 if stroke else 0)
rect(0, 0, dep, 0.10, HexColor('#3b3532'))
rect(0, 0.10, dep, 0.92, HexColor('#6b4a33'))
rect(dep, 0.22, 0.012, 0.64, HexColor('#7a2a18'))
rect(0, 1.02, dep+0.05, 0.014, HexColor('#c9a24e'))
rect(0, 1.034, dep+0.05, 0.05, HexColor('#6e2a20'))
c.setFillColor(HexColor('#ffcf7a')); c.circle(*Q(dep+0.03, 1.012), 0.006*K, fill=1, stroke=0)
c.setFillColor(HexColor('#c9a24e')); c.setStrokeColor(INK); c.circle(*Q(dep+0.14, 0.24), 0.022*K, fill=1, stroke=1)
rect(dep+0.133, 0, 0.014, 0.218, HexColor('#c9a24e'), lw=0.3)
c.setDash(2, 1.5); c.setStrokeColor(GREY); c.setLineWidth(0.5)
c.rect(*Q(dep+0.45-0.19, 0.72), 0.38*K, 0.08*K); c.line(*Q(dep+0.45, 0), *Q(dep+0.45, 0.72)); c.setDash()
note(*Q(dep+0.45, 0.83), 'tabouret (assise 0,76)', 6.5, GREY, False, 'c')
note(*Q(dep/2, 0.55), 'caisson bois', 7, white, True, 'c'); note(*Q(dep+0.08, 0.6), 'panneau', 6.5, INK); note(*Q(dep+0.08, 0.565), 'ronce', 6.5, INK)
note(*Q(0.0, 1.17), 'SERVICE', 7, GREY, True); note(*Q(dep+0.62, 0.5), 'CLIENTS', 7, GREY, True)
note(*Q(dep+0.1, 1.12), 'plateau marbre rouge 5 cm + jonc laiton', 6.5, INK)
note(*Q(dep+0.1, 0.98), 'liseré LED sous débord', 6.5, INK)
note(*Q(dep+0.2, 0.27), 'repose-pieds laiton Ø 44', 6.5, INK)
# vertical dims (left side)
xl = -0.12
for (y0, y1, t) in [(0, 0.10, '0,10'), (0.10, 1.02, '0,92'), (1.02, 1.084, '0,064')]:
    arrow_dim(*Q(xl, y0), *Q(xl, y1), t, size=6.5)
for y in (0, 0.10, 1.02, 1.084): ext(*Q(-0.01, y), *Q(xl-0.02, y))
arrow_dim(*Q(-0.22, 0), *Q(-0.22, 1.084), 'Hauteur totale 1,084', size=7)
ext(*Q(-0.01, 1.084), *Q(-0.24, 1.084))
# customer side dims
xr = dep + 0.30
arrow_dim(*Q(dep+0.03, 0.22), *Q(dep+0.03, 0.86), '0,64', size=6, col=INK, toff=-3.2*mm)
arrow_dim(*Q(xr, 0), *Q(xr, 0.24), '0,24', size=6.5)
ext(*Q(dep+0.16, 0.24), *Q(xr+0.02, 0.24))
arrow_dim(*Q(0, -0.08), *Q(dep, -0.08), 'profondeur 0,70 (0,57 à 0,78)', size=6.5)
arrow_dim(*Q(dep, 1.16), *Q(dep+0.05, 1.16), '0,05', size=6, toff=1.2*mm)
arrow_dim(*Q(dep, 0.16), *Q(dep+0.14, 0.16), '0,14', size=6, toff=1.0*mm)

# back-bar elevation 1:30
L = 3.14; col, cen = 0.13, 1.04; nic = (L - cen - 4*col)/2
ex, ey = 30*mm, 38*mm
E = lambda x, y: (ex + x*SC, ey + y*SC)
note(15*mm, ey + 3.25*SC, "Arrière-bar · élévation vue du service (au 1/30)", 9, INK, True)
def erect(x, y, w, h, fill, lw=0.5):
    c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(lw); c.rect(*E(x, y), w*SC, h*SC, fill=1, stroke=1)
c.setStrokeColor(INK); c.setLineWidth(0.8); c.line(*E(-0.2, 0), *E(L+0.2, 0))
erect(0, 0.94, L, 1.9, HexColor('#6b4a33'))
xs = [0]
for w in (col, nic, col, cen, col, nic, col): xs.append(xs[-1] + w)
for i, w in enumerate((col, nic, col, cen, col, nic, col)):
    x = xs[i]
    if w == nic:
        erect(x, 0.94, w, 1.9, HexColor('#ffd9a0'))
        for y in (1.0, 1.4, 1.8, 2.2): erect(x, y, w, 0.022, HexColor('#6b4a33'), 0.3)
    elif w == cen:
        erect(x, 0.94, w, 1.9, HexColor('#7a2a18'))
        c.setFillColor(HexColor('#d9e3e6')); c.setStrokeColor(HexColor('#c9a24e')); c.setLineWidth(1.6); c.circle(*E(x + w/2, 1.95), 0.445*SC, fill=1, stroke=1)
        erect(x + w/2 - 0.31, 0.94, 0.62, 0.40, HexColor('#b9b9b9'), 0.4)
        note(*E(x + w/2, 1.10), 'café', 5.5, INK, False, 'c')
erect(0, 2.84, L, 0.14, HexColor('#4a2c1f'))
erect(0, 0, L, 0.90, HexColor('#4a2c1f')); erect(-0.0, 0.90, L, 0.04, HexColor('#6e2a20'))
note(*E(-0.05, 0.4), 'côté façade', 6, GREY, False, 'r'); note(*E(L+0.05, 0.4), 'côté cuisine', 6, GREY)
# dims
yb = -0.22
arrow_dim(*E(0, yb), *E(L, yb), 'Longueur ' + fr(L) + ' m', size=7)
yc = 3.10
for i in range(7):
    w = xs[i+1] - xs[i]
    arrow_dim(*E(xs[i], yc), *E(xs[i+1], yc), fr(w), size=5.5)
for x in xs: ext(*E(x, 2.98), *E(x, yc + 0.04))
xr = L + 0.25
for (y0, y1, t) in [(0, 0.94, '0,94'), (0.94, 2.84, '1,90'), (2.84, 2.98, '0,14')]:
    arrow_dim(*E(xr, y0), *E(xr, y1), t, size=6)
note(*E(xs[3] + cen/2, 2.47), 'miroir Ø 0,89', 6, white, True, 'c')
note(*E(xs[1] + nic/2, 2.55), 'niche', 6, INK, False, 'c'); note(*E(xs[1] + nic/2, 2.45), 'rétroéclairée', 6, INK, False, 'c')
note(*E(xs[5] + nic/2, 2.55), 'niche', 6, INK, False, 'c'); note(*E(xs[5] + nic/2, 2.45), 'rétroéclairée', 6, INK, False, 'c')
note(*E(L + 0.55, 1.0), 'étagères à', 6, INK); note(*E(L + 0.55, 0.9), '1,00 · 1,40', 6, INK); note(*E(L + 0.55, 0.8), '1,80 · 2,20', 6, INK)
note(*E(L/2, 0.45), 'meuble bas 0,60 de profondeur, plan de travail 0,63', 6, white, True, 'c')
c.showPage(); c.save()
print('ok', out)
