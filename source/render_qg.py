# Cycles render of the exported QG scene.
# usage: python render_qg.py <glb> <view> <soir|jour> <out.png> <width> <height> <samples>
import bpy, sys, math
from mathutils import Vector

glb, view, mode, out, W, H, SPP = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
night = mode == 'soir'
CX, CZ = 10.2, 7.4
VIEWS = {
    'entree1': ([13.35, 1.62, 7.9], [7.6, 1.05, 7.75], 56),
    'fond': ([16.2, 1.65, 5.35], [9.0, 0.9, 8.3], 52),
    'bar': ([9.7, 1.7, 8.3], [5.2, 1.3, 8.4], 52),
    'entree2': ([7.6, 1.6, 9.75], [13.5, 1.1, 6.3], 54),
    'banquettes': ([12.6, 1.55, 7.75], [7.0, 1.0, 7.6], 52),
    'piano': ([12.25, 1.45, 7.55], [13.05, 1.35, 4.75], 50),
    'facade': ([21.8, 1.65, 15.6], [14.4, 2.0, 9.0], 46),
}
def B(p):  # plan coords [x, height, z] -> Blender
    return Vector((p[0] - CX, -(p[2] - CZ), p[1]))

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
sc = bpy.context.scene

for o in [o for o in bpy.data.objects if o.type == 'LIGHT']:
    bpy.data.objects.remove(o, do_unlink=True)

def bsdf(m):
    if not m.use_nodes: return None
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED': return n
    return None
def setin(n, name, v):
    if n and name in n.inputs: n.inputs[name].default_value = v

for m in bpy.data.materials:
    n = bsdf(m); name = m.name
    if name in ('velvet', 'curtain'):
        setin(n, 'Roughness', 0.85); setin(n, 'Sheen Weight', 0.9); setin(n, 'Sheen Roughness', 0.35); setin(n, 'Sheen Tint', (1, 0.55, 0.55, 1))
    elif name == 'boucle':
        setin(n, 'Roughness', 0.9); setin(n, 'Sheen Weight', 0.25); setin(n, 'Sheen Roughness', 0.5); setin(n, 'Sheen Tint', (0.75, 0.32, 0.15, 1)); setin(n, 'Specular IOR Level', 0.2)
    elif name == 'dipoWood':
        setin(n, 'Roughness', 0.35); setin(n, 'Coat Weight', 0.3)
    elif name == 'leather':
        setin(n, 'Roughness', 0.42); setin(n, 'Coat Weight', 0.25); setin(n, 'Coat Roughness', 0.3)
    elif name == 'chairWood' or name == 'wood' or name == 'wall':
        setin(n, 'Roughness', 0.4); setin(n, 'Coat Weight', 0.3); setin(n, 'Coat Roughness', 0.2)
    elif name == 'blackTop' or name == 'piano':
        setin(n, 'Roughness', 0.08); setin(n, 'Coat Weight', 1.0); setin(n, 'Coat Roughness', 0.03)
    elif name == 'marbleBlack':
        setin(n, 'Roughness', 0.1); setin(n, 'Coat Weight', 0.6)
    elif name == 'brass':
        setin(n, 'Metallic', 1.0); setin(n, 'Roughness', 0.22)
    elif name == 'mirror':
        setin(n, 'Metallic', 1.0); setin(n, 'Roughness', 0.02); setin(n, 'Base Color', (0.75, 0.68, 0.56, 1))
    elif name == 'glass':
        setin(n, 'Alpha', 1.0); setin(n, 'Transmission Weight', 1.0); setin(n, 'Roughness', 0.0); setin(n, 'IOR', 1.45); setin(n, 'Base Color', (0.92, 0.96, 0.96, 1))
    elif name == 'carpet':
        setin(n, 'Roughness', 0.95); setin(n, 'Sheen Weight', 0.0); setin(n, 'Specular IOR Level', 0.2)
    elif name == 'porcelain':
        setin(n, 'Roughness', 0.15); setin(n, 'Coat Weight', 0.6)
    elif name == 'cloth':
        setin(n, 'Roughness', 0.9); setin(n, 'Sheen Weight', 0.4); setin(n, 'Subsurface Weight', 0.05)
    elif name == 'ceiling':
        setin(n, 'Emission Strength', 0.0); setin(n, 'Roughness', 0.9)
    elif name == 'burl':
        setin(n, 'Roughness', 0.3); setin(n, 'Coat Weight', 0.7); setin(n, 'Coat Roughness', 0.05)
    elif name == 'rosso':
        setin(n, 'Roughness', 0.08); setin(n, 'Coat Weight', 1.0); setin(n, 'Coat Roughness', 0.02)
    elif name == 'backlit':
        setin(n, 'Emission Strength', 5.0 if night else 3.0)
    elif name == 'globe':
        setin(n, 'Emission Strength', 9.0 if night else 3.0)
    elif name in ('crystal', 'glassware'):
        setin(n, 'Alpha', 1.0); setin(n, 'Transmission Weight', 1.0); setin(n, 'Roughness', 0.02); setin(n, 'Emission Strength', 0.4 if name == 'crystal' and night else 0.0)
    elif name == 'awningText':
        setin(n, 'Emission Strength', 5.0 if night else 0.2)
    elif name == 'winGlass':
        setin(n, 'Roughness', 0.03); setin(n, 'Metallic', 0.3)
    elif name in ('facadePaint', 'whitePaint'):
        setin(n, 'Roughness', 0.4); setin(n, 'Coat Weight', 0.25)
    elif name in ('foliage', 'foliageLight'):
        setin(n, 'Roughness', 0.7); setin(n, 'Subsurface Weight', 0.15)
    elif name == 'opal':
        setin(n, 'Emission Strength', 7.0 if night else 3.0); setin(n, 'Emission Color', (1.0, 0.78, 0.5, 1))
    elif name == 'cove':
        setin(n, 'Emission Strength', 30.0 if night else 4.0); setin(n, 'Emission Color', (1.0, 0.66, 0.35, 1))
    elif name == 'flame':
        # unlit material: replace with a strong emission
        nt = m.node_tree; nt.nodes.clear()
        e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (1.0, 0.62, 0.25, 1); e.inputs['Strength'].default_value = 40.0
        o_ = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o_.inputs[0])
    if name.startswith('bottle'):
        setin(n, 'Transmission Weight', 0.85); setin(n, 'Alpha', 1.0); setin(n, 'Roughness', 0.05)
    # importer uses blended alpha for transparent glTF materials; Cycles reads Alpha directly
    try: m.surface_render_method = 'DITHERED'
    except Exception: pass

# viewer-only light wash planes are replaced by real light from the LED strips
for o in [o for o in bpy.data.objects if o.name.startswith('washFX')]:
    bpy.data.objects.remove(o, do_unlink=True)
for m in bpy.data.materials:
    if m.name == 'ledUp':
        n = bsdf(m); setin(n, 'Emission Strength', 40.0 if night else 0.0); setin(n, 'Emission Color', (1.0, 0.62, 0.32, 1))
# glass does not block light or sun
for o in bpy.data.objects:
    if o.type == 'MESH' and o.active_material and o.active_material.name == 'glass':
        o.visible_shadow = False

# candle flames: small warm point lights
def add_point(loc, power, color, radius=0.05, name='pt'):
    ld = bpy.data.lights.new(name, 'POINT'); ld.energy = power; ld.color = color; ld.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, ld); ob.location = loc; sc.collection.objects.link(ob); return ob
for o in bpy.data.objects:
    if o.type == 'MESH' and o.active_material and o.active_material.name == 'flame':
        add_point(o.matrix_world.translation + Vector((0, 0, 0.02)), 1.6, (1.0, 0.6, 0.3), 0.01, 'candle')

# drum pendants: a light inside each, under the opal disc
for o in list(bpy.data.objects):
    if o.type != 'EMPTY': continue
    base = o.name.split('.')[0]
    loc = o.matrix_world.translation
    if base == 'drum': add_point(loc + Vector((0, 0, 0.1)), 70 if night else 35, (1.0, 0.8, 0.58), 0.18, 'drumL')
    elif base == 'chandelier': add_point(loc + Vector((0, 0, 0.2)), 90 if night else 30, (1.0, 0.82, 0.6), 0.2, 'chandL')
    elif base == 'lantern' and night: add_point(loc, 10, (1.0, 0.72, 0.4), 0.06, 'lanternL')
add_point(B([12.75, 1.49, 4.92]), 12 if night else 0, (1.0, 0.75, 0.45), 0.05, 'pianolamp')

world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']
if night:
    bg.inputs['Color'].default_value = (0.03, 0.045, 0.09, 1); bg.inputs['Strength'].default_value = 1.2 if view == 'facade' else 0.3
    if view == 'facade':
        for sx, sz in [(19.6, 12.6), (13.0, 13.4), (19.2, 4.2)]:
            sl = add_point(B([sx, 4.2, sz]), 450, (1.0, 0.78, 0.5), 0.25, 'streetlamp'); sl.visible_camera = False; sl.visible_glossy = False
else:
    bg.inputs['Color'].default_value = (0.42, 0.6, 0.92, 1) if view == 'facade' else (0.8, 0.86, 0.96, 1); bg.inputs['Strength'].default_value = 1.3 if view == 'facade' else 4.0
    sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 7.0; sd.angle = math.radians(1.5); sd.color = (1.0, 0.95, 0.88)
    so = bpy.data.objects.new('sun', sd); sc.collection.objects.link(so)
    so.rotation_euler = (Vector((0, 0, 0)) - Vector((9, -9, 12))).to_track_quat('-Z', 'Y').to_euler()

pos, tgt, fov = VIEWS[view]
cd = bpy.data.cameras.new('cam'); cd.sensor_fit = 'VERTICAL'; cd.angle = math.radians(fov - 6)
cd.clip_start = 0.05
cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = B(pos); cam.rotation_euler = (B(tgt) - B(pos)).to_track_quat('-Z', 'Y').to_euler()

sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = SPP; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.03
sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3; sc.cycles.transmission_bounces = 6
sc.cycles.sample_clamp_indirect = 8.0; sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.render.resolution_x = W; sc.render.resolution_y = H; sc.render.resolution_percentage = 100
sc.render.threads_mode = 'AUTO'
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    try: sc.view_settings.look = 'Medium High Contrast'
    except Exception: pass
sc.view_settings.exposure = (1.0 if night else -0.4) if view == 'facade' else (0.9 if night else 1.1)
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print('RENDERED', out)
