# Bar geometry exactly as built in the 3D model (centripetal Catmull-Rom, same points)
import math, json
BAR_INNER=[[5.99,10.14],[5.987,9.614],[5.988,9.356],[6.068,9.101],[6.209,8.841],[6.387,8.577],[6.56,8.309],[6.692,8.036],[6.736,7.76],[6.695,7.527],[6.599,7.386],[6.447,7.322],[6.283,7.315],[6.196,7.344]]
BAR_OUTER=[[6.158,6.598],[6.372,6.605],[6.653,6.64],[6.921,6.725],[7.134,6.84],[7.285,6.994],[7.374,7.186],[7.433,7.47],[7.436,7.751],[7.386,8.028],[7.298,8.256],[7.167,8.481],[7.009,8.677],[6.872,8.879],[6.746,9.095],[6.666,9.309],[6.628,9.519],[6.63,9.848],[6.64,10.14]]
def cr(pts,div):
    P=pts;n=len(P);out=[]
    def nu(x0,x1,x2,x3,d0,d1,d2):
        t1=((x1-x0)/d0-(x2-x0)/(d0+d1)+(x2-x1)/d1)*d1;t2=((x2-x1)/d1-(x3-x1)/(d1+d2)+(x3-x2)/d2)*d1
        return (x1,t1,-3*x1+3*x2-2*t1-t2,2*x1-2*x2+t1+t2)
    for k in range(div+1):
        t=k/div;p=(n-1)*t;i=int(math.floor(p));w=p-i
        if w==0 and i==n-1: i=n-2;w=1
        p1=P[i];p2=P[i+1]
        p0=P[i-1] if i>0 else [2*P[0][0]-P[1][0],2*P[0][1]-P[1][1]]
        p3=P[i+2] if i+2<n else [2*P[n-1][0]-P[n-2][0],2*P[n-1][1]-P[n-2][1]]
        ds=lambda a,b:max(((a[0]-b[0])**2+(a[1]-b[1])**2)**0.25,0)
        d0,d1,d2=ds(p0,p1),ds(p1,p2),ds(p2,p3)
        if d1<1e-4:d1=1
        if d0<1e-4:d0=d1
        if d2<1e-4:d2=d1
        q=[]
        for c in (0,1):
            a,b,cc,d=nu(p0[c],p1[c],p2[c],p3[c],d0,d1,d2);q.append(a+b*w+cc*w*w+d*w*w*w)
        out.append(q)
    return out
inner=cr(BAR_INNER,140);outer=cr(BAR_OUTER,180)
L=lambda pts:sum(math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1))
def dseg(p,a,b):
    ax,ay=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*ax+(p[1]-a[1])*ay)/(ax*ax+ay*ay)));return math.dist(p,(a[0]+ax*t,a[1]+ay*t))
def dpoly(p,poly): return min(dseg(p,poly[i],poly[i+1]) for i in range(len(poly)-1))
depth=[(dpoly(p,inner),p) for p in outer[8:-4]]
xs=[p[0] for p in inner+outer];ys=[p[1] for p in inner+outer]
# curvature radius along outer
def rad(a,b,c):
    A=math.dist(b,c);B=math.dist(a,c);C=math.dist(a,b);s=(A+B+C)/2;ar=max(s*(s-A)*(s-B)*(s-C),1e-12)**0.5;return A*B*C/(4*ar)
rads=[(rad(outer[i-6],outer[i],outer[i+6]),outer[i]) for i in range(6,len(outer)-6)]
aisle=min((p[0]-5.21,p) for p in inner if 6.99<=p[1]<=10.13)
tables=[(8.24,6.28),(8.30,9.22),(9.755,7.70)]
def drect(p,c,h=0.3): dx=max(abs(p[0]-c[0])-h,0);dy=max(abs(p[1]-c[1])-h,0);return math.hypot(dx,dy)
clear=min((drect(p,c),p,c) for p in outer for c in tables)
R={'inner':inner,'outer':outer,'len_outer':L(outer),'len_inner':L(inner),'xmin':min(xs),'xmax':max(xs),'ymin':min(ys),'ymax':max(ys),
 'depth_min':min(depth)[0],'depth_min_at':min(depth)[1],'depth_max':max(depth)[0],'rad_min':min(rads)[0],'rad_min_at':min(rads)[1],
 'aisle_min':aisle[0],'aisle_at':aisle[1],'clear_table':clear[0],'clear_at':clear[1],'clear_table_c':clear[2],
 'wall_end':[inner[0],outer[-1]],'hook_end':[outer[0],inner[-1]]}
json.dump(R,open(__file__.replace('bargeo.py','bargeo.json'),'w'))
for k,v in R.items():
    if k not in('inner','outer'): print(k, v if not isinstance(v,float) else round(v,3))
