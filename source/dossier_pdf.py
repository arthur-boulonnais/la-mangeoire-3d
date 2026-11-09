# Dossier déco La Mangeoire : rendus + toutes les références mobilier/matériaux, A4 paysage
import sys, os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refs')
out = sys.argv[1]
F = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('Sans', F + 'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('SansB', F + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Serif', F + 'DejaVuSerif.ttf')); pdfmetrics.registerFont(TTFont('SerifB', F + 'DejaVuSerif-Bold.ttf'))
W, H = landscape(A4)
INK = HexColor('#241a15'); MUTED = HexColor('#7a6a5f'); RED = HexColor('#7a1420'); BRASS = HexColor('#9a7426'); CREAM = HexColor('#f6f1ea'); LINE = HexColor('#d9cfc4')
c = canvas.Canvas(out, pagesize=(W, H)); c.setTitle('La Mangeoire — dossier déco'); c.setAuthor('La Mangeoire')
page = [0]

def img(name, x, y, w, h, fit=True, frame=False):
    p = os.path.join(R, name + '.jpg'); ir = ImageReader(p); iw, ih = ir.getSize()
    s = min(w/iw, h/ih) if fit else max(w/iw, h/ih); dw, dh = iw*s, ih*s
    dx, dy = x + (w-dw)/2, y + (h-dh)/2
    if not fit:
        c.saveState(); pth = c.beginPath(); pth.rect(x, y, w, h); c.clipPath(pth, stroke=0, fill=0)
    c.drawImage(ir, dx, dy, dw, dh)
    if not fit: c.restoreState()
    if frame: c.setStrokeColor(LINE); c.setLineWidth(0.5); c.rect(x, y, w, h)

def text(x, y, s, size=10, font='Sans', col=INK, align='l'):
    c.setFont(font, size); c.setFillColor(col)
    {'l': c.drawString, 'c': c.drawCentredString, 'r': c.drawRightString}[align](x, y, s)

def para(x, y, s, size=9, font='Sans', col=INK, width=100*mm, lead=1.35):
    c.setFont(font, size); c.setFillColor(col); words = s.split(); line = ''
    for wd in words:
        t = (line + ' ' + wd).strip()
        if c.stringWidth(t, font, size) > width: c.drawString(x, y, line); y -= size*lead; line = wd
        else: line = t
    if line: c.drawString(x, y, line); y -= size*lead
    return y

def frame_page(title, sub=None):
    page[0] += 1
    c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
    text(15*mm, H-16*mm, title, 17, 'SerifB')
    if sub: text(15*mm, H-22*mm, sub, 9, 'Sans', MUTED)
    text(W-15*mm, H-16*mm, 'La Mangeoire', 10, 'Serif', RED, 'r')
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(15*mm, H-25.5*mm, W-15*mm, H-25.5*mm)
    text(15*mm, 8*mm, 'Dossier déco · maquette 3D : la-mangeoire-3d.vercel.app', 7.5, 'Sans', MUTED)
    text(W-15*mm, 8*mm, str(page[0]), 7.5, 'Sans', MUTED, 'r')

# ---------------- cover
page[0] += 1
img('r-soir-entree1', 0, 0, W, H, fit=False)
c.setFillColor(HexColor('#140c0a')); c.setFillAlpha(0.72); c.rect(0, 0, 135*mm, H, fill=1, stroke=0); c.setFillAlpha(1)
text(18*mm, H-70*mm, 'La Mangeoire', 40, 'SerifB', white)
text(18*mm, H-84*mm, 'Dossier déco intérieur', 16, 'Serif', HexColor('#e8cf96'))
y = para(18*mm, H-102*mm, "Rendus 3D de la salle et de la façade, puis toutes les références retenues : moquette, papier peint, banquettes, chaises, tables, chaises de bar, luminaires, bar et piano, avec les quantités.", 10.5, 'Sans', HexColor('#efe6dc'), 100*mm)
text(18*mm, 30*mm, 'Maquette 3D interactive', 9, 'SansB', HexColor('#e8cf96'))
text(18*mm, 24*mm, 'la-mangeoire-3d.vercel.app', 11, 'Sans', white)
text(18*mm, 15*mm, 'Version du 9 novembre 2026 · quantités issues de la maquette, à confirmer sur place', 7.5, 'Sans', HexColor('#bfb2a5'))
c.showPage()

# ---------------- renders
RENDERS = [('r-soir-entree1', 'Soir · la salle depuis l\'entrée 1'), ('r-soir-bar', 'Soir · le bar'), ('r-soir-fond', 'Soir · le coin piano'),
           ('r-soir-piano', 'Soir · le piano et le papier peint'), ('r-jour-entree1', 'Jour · la salle, rideaux ouverts'), ('r-jour-facade', 'Jour · la façade'), ('r-soir-facade', 'Soir · la façade')]
for i in range(0, len(RENDERS), 2):
    frame_page('Rendus', 'Images calculées dans Blender à partir de la maquette 3D (lumière, ombres et matières réalistes)')
    pair = RENDERS[i:i+2]; bw = (W - 30*mm - 8*mm)/2; bh = bw*900/1440
    for j, (f, cap) in enumerate(pair):
        x = 15*mm + j*(bw + 8*mm); y = H - 32*mm - bh
        img(f, x, y, bw, bh, fit=False)
        text(x, y - 6*mm, cap, 10, 'SansB')
    c.showPage()

# ---------------- references
REFS = [
 ('moquette', 'Moquette léopard', 'Sol de toute la salle', [('Surface', 'salle ≈ 66 m² (dont bar et arrière-bar ≈ 4,6 m²)'), ('À commander', 'prévoir ≈ 73 m² avec 10 % de chutes'), ('Motif', 'taches d\'environ 7 cm')], 'Photo fournie. Pose bord à bord dans toute la salle ; à valider sous le bar et l\'arrière-bar.'),
 ('papier-peint', 'Papier peint tulipes', 'Coin piano : mur du fond et mur en biais', [('Surface', '≈ 4,5 m² (2,67 m de long × 1,70 m de haut)'), ('Pose', 'de la boiserie (0,95 m) à la corniche'), ('Raccord', 'motif ≈ 17,5 × 18 cm, raccord sauté')], 'Échantillon 50 × 50 cm fourni. Prévoir les chutes de raccord en plus de la surface.'),
 ('banquette', 'Banquettes', 'Le long des murs et des vitrines', [('Longueurs', 'D1 2500 · A1 3200 · C1 3100 · angle 700 · C2 1200 · B1 2100 · B2 2700 mm'), ('Total', '≈ 15,5 m linéaires, 15 places'), ('Finition', 'cuir anthracite patiné, côtes verticales, clous laiton, socle bois foncé')], 'LED cachées en haut du dossier, éclairage vers le haut (ambiance soir).'),
 ('chaise', 'Chaises de salle', 'Fauteuil bistrot en bois courbé', [('Quantité', '25'), ('Finition', 'bois noyer, assise cuir noir cloutée laiton'), ('Placement', 'face aux banquettes et autour des tables')], 'Modèle à accoudoirs en fer à cheval, dossier haut clouté.'),
 ('table', 'Tables', 'Plateau noir uni cerclé laiton, pied fonte', [('Carrées 60 × 60', '18'), ('Rondes Ø 90', '2 (même style)'), ('Hauteur', '≈ 75 cm')], 'Le soir : nappe blanche, bougeoir laiton au centre, assiettes, couverts et verres.'),
 ('dipo', 'Chaises de bar Dipo', 'Hauteur d\'assise 80 cm', [('Quantité', '6'), ('Finition', 'velours bouclé rouille, piétement bois foncé, repose-pieds métal'), ('Pourquoi 80 cm', 'bar à 1,08 m : assise 28 cm sous le plateau')], 'Réparties le long de la face galbée du bar, au moins 68 cm entre deux chaises.'),
 ('suspension', 'Suspensions tambour', 'Laiton et verre opalin, au-dessus des tables', [('Quantité', '6 dans la salle'), ('Hauteur', 'bas du tambour à ≈ 2,20 m')], 'Référence fournie.'),
 ('applique', 'Appliques murales', 'Laiton et verre opalin', [('Quantité', '6'), ('Hauteur', 'centre à ≈ 1,80 m'), ('Coin piano', '2 appliques encadrant le piano')], 'Posées sur les panneaux de velours et sur le papier peint.'),
 ('bar-ref', 'Bar, arrière-bar et lustres', 'Référence de style', [('Bar', 'ronce encadrée laiton, plateau marbre rouge, liseré lumineux, repose-pieds laiton'), ('Arrière-bar', 'niches rétroéclairées, miroir rond laiton Ø 0,89 m'), ('Lustres', '2 lustres en cristal au-dessus du bar')], 'Cotes du bar : voir le PDF « bar-cotes ».'),
 ('piano', 'Piano droit', 'Existant, coin piano', [('Finition', 'palissandre, bougeoirs laiton'), ('Dessus', 'lampe champignon laiton et bouquet blanc')], 'Photo fournie.'),
]
for i in range(0, len(REFS), 2):
    frame_page('Mobilier et matériaux', 'Références fournies et utilisées dans la maquette')
    for j, (f, name, where, rows, note) in enumerate(REFS[i:i+2]):
        x0 = 15*mm + j*((W-30*mm)/2 + 4*mm); cw = (W-30*mm)/2 - 4*mm; top = H - 32*mm
        ih = 88*mm; c.setFillColor(white); c.rect(x0, top-ih, cw, ih, fill=1, stroke=0); img(f, x0+3*mm, top-ih+3*mm, cw-6*mm, ih-6*mm)
        y = top - ih - 9*mm
        text(x0, y, name, 14, 'SerifB'); y -= 5.5*mm
        text(x0, y, where, 9, 'Sans', MUTED); y -= 7*mm
        for k, v in rows:
            text(x0, y, k, 8.5, 'SansB', RED); y = para(x0 + 34*mm, y, v, 8.5, 'Sans', INK, cw - 34*mm); y -= 1.2*mm
        y -= 1*mm; para(x0, y, note, 8, 'Sans', MUTED, cw)
    c.showPage()

# ---------------- ambiance + façade refs
frame_page('Références d\'ambiance', 'Images d\'inspiration fournies : style et ambiance, sans valeur de mesure')
bw = (W - 30*mm - 8*mm)/2; bh = 92*mm
for j, (f, cap) in enumerate([('ambiance-soir', 'Soir : nappes, bougeoirs, rideaux de velours fermés'), ('ambiance-jour', 'Jour : rideaux ouverts, tables sans nappe')]):
    x = 15*mm + j*(bw + 8*mm); img(f, x, H-32*mm-bh, bw, bh, fit=False); text(x, H-32*mm-bh-6*mm, cap, 9.5, 'SansB')
y2 = H-32*mm-bh-16*mm; bh2 = y2 - 16*mm
for j, (f, cap) in enumerate([('facade-1', 'Façade : devanture bordeaux, stores, terrasse rotin'), ('facade-2', 'Façade : oliviers en jardinières, lanternes')]):
    x = 15*mm + j*(bw + 8*mm); img(f, x, 16*mm+6*mm, bw, bh2-6*mm, fit=False); text(x, 16*mm, cap, 9.5, 'SansB')
c.showPage()

# ---------------- showroom photos
frame_page('Photos showroom', 'Photos prises en magasin : première chaise envisagée et table à plateau noir cerclé laiton')
for j, f in enumerate(['showroom-1', 'showroom-2']):
    x = 15*mm + j*((W-30*mm)/2 + 4*mm); img(f, x, 16*mm, (W-30*mm)/2 - 4*mm, H - 50*mm)
c.showPage()

# ---------------- shopping list
frame_page('Récapitulatif des quantités', 'Comptées dans la maquette 3D · à confirmer par relevé sur place et avec les fournisseurs')
ROWS = [('Moquette léopard', '≈ 73 m²', 'salle ≈ 66 m² + 10 % de chutes'), ('Papier peint tulipes', '≈ 4,5 m² + raccord', 'coin piano, 2 murs, h. 1,70 m'),
        ('Banquettes cuir anthracite', '≈ 15,5 m', '7 éléments, 15 places'), ('Ruban LED banquettes', '≈ 15 m', 'en haut des dossiers, blanc chaud'),
        ('Chaises de salle bistrot', '25', 'noyer, assise cuir noir'), ('Tables 60 × 60', '18', 'plateau noir uni cerclé laiton, pied fonte'),
        ('Tables rondes Ø 90', '2', 'même style'), ('Chaises de bar Dipo 80 cm', '6', 'velours bouclé rouille'),
        ('Suspensions tambour', '6', 'laiton, verre opalin'), ('Lustres cristal', '2', 'au-dessus du bar'), ('Appliques murales', '6', 'laiton, verre opalin'),
        ('Bougeoirs laiton', '20', 'un par table, le soir'), ('Lampes champignon laiton', '2', 'bar et piano (+ terrasse si retenue)'),
        ('Rideaux velours rouge', 'toutes les vitrines', 'à mesurer sur place')]
x0, y = 15*mm, H - 36*mm
c.setFillColor(white); c.rect(x0, y - len(ROWS)*9*mm - 4*mm, W - 30*mm, len(ROWS)*9*mm + 10*mm, fill=1, stroke=0)
text(x0 + 4*mm, y, 'Article', 9, 'SansB', MUTED); text(x0 + 120*mm, y, 'Quantité', 9, 'SansB', MUTED); text(x0 + 165*mm, y, 'Détail', 9, 'SansB', MUTED)
for k, (a, q, d) in enumerate(ROWS):
    yy = y - (k+1)*9*mm
    c.setStrokeColor(LINE); c.setLineWidth(0.4); c.line(x0 + 4*mm, yy + 6*mm, W - 19*mm, yy + 6*mm)
    text(x0 + 4*mm, yy, a, 10, 'SansB'); text(x0 + 120*mm, yy, q, 10, 'Sans', RED); text(x0 + 165*mm, yy, d, 9, 'Sans', MUTED)
c.showPage(); c.save(); print('ok', out)
