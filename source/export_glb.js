// Export the scene (given mode) to GLB using three's GLTFExporter, plus camera presets as JSON
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [,,dir,mode,out]=process.argv;
const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:400,height:300}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+dir+'/test.html#entree1');await p.waitForFunction(()=>window.__qg&&window.__qgFonts===true&&window.__qgTex===true,null,{timeout:120000});
await p.addScriptTag({url:'https://cdn.jsdelivr.net/npm/three@0.147.0/examples/js/exporters/GLTFExporter.js'});
const b64=await p.evaluate(async(mode)=>{const q=window.__qg;q.go('entree1',false);q.setMode(mode);q.renderer.setAnimationLoop(null);
  // strip label objects
  const rm=[];q.scene.traverse(o=>{if(o.isCSS2DObject)rm.push(o);});rm.forEach(o=>o.parent.remove(o));
  q.scene.background=null;q.scene.environment=null;
  const ex=new THREE.GLTFExporter();
  const buf=await new Promise((res,rej)=>ex.parse(q.scene,res,rej,{binary:true,onlyVisible:true,maxTextureSize:2048}));
  let s='';const u=new Uint8Array(buf);for(let i=0;i<u.length;i+=0x8000)s+=String.fromCharCode.apply(null,u.subarray(i,i+0x8000));return btoa(s);},mode);
fs.writeFileSync(out,Buffer.from(b64,'base64'));console.log('glb bytes',fs.statSync(out).size,errs.join('|'));await b.close();})();
