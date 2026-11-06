import re
d=open('data_block.js').read()
new_f='''const FACADES=[
 {a:[6.627,10.14],b:[9.694,10.10],n:[0,-1],door:[7.127,7.95]},
 {a:[11.441,10.425],b:[14.942,10.416],n:[0,-1]},
 {a:[14.942,10.416],b:[16.167,8.769],n:[-0.802,-0.597]},
 {a:[16.658,4.733],b:[16.453,7.923],n:[-0.998,-0.064]},
 {a:[14.548,4.549],b:[16.658,4.733],n:[-0.087,0.996]}
];
'''
d2=re.sub(r'// thin façades.*?\n\];\n', new_f, d, flags=re.S)
assert 'n:[0,-1],door' in d2
t=open('qg-3d/template.html').read().replace('__LEOPARD__',open('leopard.b64').read().strip())
open('qg-3d/index.html','w').write(t.replace('/*__DATA__*/',d2))
open('qg-3d/test.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>[hidden]{display:none!important}</style></head><body>'+t.replace('/*__DATA__*/',d2)+'</body></html>')
print('built')
