# La Mangeoire — maquette 3D

Maquette 3D interactive du restaurant La Mangeoire, construite aux cotes du plan au 1/50 :
salle, nouveau bar arrondi, arrière-bar, banquettes, tables, piano, façade et terrasse.

- `index.html` : la maquette (ouvrir dans un navigateur ; ambiances soir et jour, plusieurs points de vue).
- `rendus/` : rendus photo calculés dans Blender à partir de la maquette.

Site statique, sans étape de build : Vercel le publie tel quel.

## Sources

Le dossier `source/` garde de quoi reconstruire la maquette et les rendus :
- `template.html` + `data_block.js` + `moquette-leopard.jpg` : la maquette ; `build.py` assemble `index.html`.
- `export_glb.js` : exporte la scène en `.glb` (Playwright + three.js GLTFExporter).
- `render_qg.py` : rendus photo dans Blender (module Python `bpy`, moteur Cycles).
