import json,math,sys
D=sys.argv[1]
SOLID=json.load(open(D+'/solid.json'))
ROOM=[[4.4,10.5],[4.4,5.3],[5.5,5.3],[5.6,5.2],[11.65,5.12],[12.38,4.42],[14.12,4.36],[14.12,4.93],[14.55,4.93],[14.55,4.52],[16.69,4.71],[16.48,7.93],[16.19,8.79],[14.96,10.44],[11.44,10.44],[11.44,10.55],[4.4,10.55]]
def inside(p,poly):
    x,y=p;c=False
    for i in range(len(poly)):
        x1,y1=poly[i];x2,y2=poly[(i+1)%len(poly)]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
E=[]
for si,s in enumerate(SOLID):
    for i in range(len(s)):
        a=s[i];b=s[(i+1)%len(s)];L=math.dist(a,b)
        if L<0.04: continue
        u=((b[0]-a[0])/L,(b[1]-a[1])/L)
        for sg in (1,-1):
            n=(-u[1]*sg,u[0]*sg);m=((a[0]+b[0])/2+n[0]*0.06,(a[1]+b[1])/2+n[1]*0.06)
            if inside(m,ROOM) and not any(inside(m,t) for t in SOLID): E.append((si,a,b,round(L,3),n))
for e in E: print(e[0],[round(v,3) for v in e[1]],[round(v,3) for v in e[2]],e[3])
