import random, math
W,H=1357,1920
random.seed(31)
o=[]
a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#1D1429"/><stop offset="0.28" stop-color="#171022"/><stop offset="0.75" stop-color="#140F1E"/><stop offset="1" stop-color="#110C19"/></linearGradient>
<radialGradient id="moonglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#E9DDF7" stop-opacity="0.22"/><stop offset="0.45" stop-color="#BD9AF7" stop-opacity="0.08"/><stop offset="1" stop-color="#BD9AF7" stop-opacity="0"/></radialGradient>
<radialGradient id="moon" cx="0.42" cy="0.4" r="0.6"><stop offset="0" stop-color="#F4EBDD"/><stop offset="0.7" stop-color="#E2D3E8"/><stop offset="1" stop-color="#C9B8E0"/></radialGradient>
<radialGradient id="spineglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#BD9AF7" stop-opacity="0.07"/><stop offset="1" stop-color="#BD9AF7" stop-opacity="0"/></radialGradient>
<radialGradient id="mintglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#B4F2C4" stop-opacity="0.07"/><stop offset="1" stop-color="#B4F2C4" stop-opacity="0"/></radialGradient>
<radialGradient id="bloodglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FF858E" stop-opacity="0.06"/><stop offset="1" stop-color="#FF858E" stop-opacity="0"/></radialGradient>
<filter id="blur30"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 0.75  0 0 0 0 0.65  0 0 0 0 0.9  0 0 0 0.05 0"/></filter>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
# moon top right
a('<circle cx="1228" cy="150" r="200" fill="url(#moonglow)"/>')
a('<circle cx="1228" cy="150" r="78" fill="url(#moon)" opacity="0.92"/>')
for (x,y,r) in [(1206,132,10),(1250,170,7),(1236,122,5),(1200,172,6)]:
    a(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#C9B8E0" opacity="0.45"/>')
# stars
for i in range(110):
    x=random.uniform(30,W-30); y=random.uniform(30,420)
    if (x-1228)**2+(y-150)**2<140**2: continue
    r=random.choice([0.6,0.8,1,1.2,1.6]); op=random.uniform(0.25,0.7)
    a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#F4EBDD" opacity="{op:.2f}"/>')
# bats
def bat(x,y,s,op):
    return f'<path transform="translate({x},{y}) scale({s})" opacity="{op}" fill="#0E0A14" d="M0,0 C-4,-6 -10,-8 -18,-6 C-14,-3 -13,1 -15,4 C-11,2 -8,3 -6,6 C-5,3 -3,2 0,3 C3,2 5,3 6,6 C8,3 11,2 15,4 C13,1 14,-3 18,-6 C10,-8 4,-6 0,0 Z"/>'
a(bat(1150,120,1.5,0.9)); a(bat(1262,236,1.0,0.85)); a(bat(1090,214,0.8,0.7))
# gothic double frame with pointed arch at top
m=20
a(f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="none" stroke="#3E2F52" stroke-width="1.6"/>')
m2=28
a(f'<rect x="{m2}" y="{m2}" width="{W-2*m2}" height="{H-2*m2}" fill="none" stroke="#2C2139" stroke-width="1"/>')
# corner quatrefoils
def quat(cx,cy,r,col):
    s=''.join(f'<circle cx="{cx+dx*r}" cy="{cy+dy*r}" r="{r}" fill="none" stroke="{col}" stroke-width="1.2"/>' for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])
    return s+f'<rect x="{cx-3}" y="{cy-3}" width="6" height="6" transform="rotate(45 {cx} {cy})" fill="{col}"/>'
for cx,cy in [(m+4,m+4),(W-m-4,m+4),(m+4,H-m-4),(W-m-4,H-m-4)]:
    a(quat(cx,cy,7,"#5A4775"))
# section dividers
def divider(y,col="#4A3860"):
    cx=W/2
    return (f'<line x1="56" y1="{y}" x2="{cx-28}" y2="{y}" stroke="{col}" stroke-width="1"/>'
            f'<line x1="{cx+28}" y1="{y}" x2="{W-56}" y2="{y}" stroke="{col}" stroke-width="1"/>'
            f'<path d="M{cx-18},{y} L{cx},{y-8} L{cx+18},{y} L{cx},{y+8} Z" fill="none" stroke="{col}" stroke-width="1.2"/>'
            f'<circle cx="{cx}" cy="{y}" r="2.5" fill="{col}"/>')
for y in [414,1250,1554,1806]:
    a(divider(y))
# soft section glows
a('<ellipse cx="678" cy="840" rx="560" ry="380" fill="url(#spineglow)"/>')
a('<ellipse cx="260" cy="1390" rx="330" ry="170" fill="url(#mintglow)"/>')
a('<ellipse cx="300" cy="1690" rx="330" ry="150" fill="url(#bloodglow)"/>')
# spider web bottom-right corner of section IV
cx,cy=W-30,1560
web=[]
for k in range(7):
    ang=math.radians(90+ k*15)
    web.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+170*math.cos(ang):.1f}" y2="{cy+170*math.sin(ang):.1f}"/>')
for rr in [40,75,110,150]:
    pts=[(cx+rr*math.cos(math.radians(90+k*15)),cy+rr*math.sin(math.radians(90+k*15))) for k in range(7)]
    d='M'+' Q'.join(f'{(pts[i][0]+pts[i+1][0])/2+ (cx-(pts[i][0]+pts[i+1][0])/2)*0.08:.1f},{(pts[i][1]+pts[i+1][1])/2+(cy-(pts[i][1]+pts[i+1][1])/2)*0.08:.1f} {pts[i+1][0]:.1f},{pts[i+1][1]:.1f}' for i in range(6))
    d=f'M{pts[0][0]:.1f},{pts[0][1]:.1f} '+'Q'+d[1:]
    web.append(f'<path d="{d}" fill="none"/>')
a('<g stroke="#3A2D4B" stroke-width="1" opacity="0.9">'+''.join(web)+'</g>')
# fog at bottom
for i in range(9):
    x=random.uniform(0,W); y=random.uniform(1830,1930)
    a(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(200,380):.0f}" ry="{random.uniform(30,60):.0f}" fill="#BD9AF7" opacity="0.05" filter="url(#blur30)"/>')
# gothic skyline at the bottom
sky=[]
x=0; base=H
random.seed(5)
pts=[f"0,{H}"]
while x<W:
    w=random.choice([40,60,80,30]); h=random.choice([10,16,22,14,26])
    kind=random.random()
    if kind<0.25:  # spire
        pts+= [f"{x},{H-h}",f"{x+w/2},{H-h-30}",f"{x+w},{H-h}"]
    elif kind<0.45: # pointed arch roof
        pts+= [f"{x},{H-h}",f"{x+w/2},{H-h-14}",f"{x+w},{H-h}"]
    else:
        pts+= [f"{x},{H-h}",f"{x+w},{H-h}"]
    x+=w
pts.append(f"{W},{H}")
a(f'<polygon points="{" ".join(pts)}" fill="#0D0913" opacity="0.95"/>')
a(f'<rect width="{W}" height="{H}" filter="url(#noise)" opacity="0.6"/>')
a('</svg>')
open('background.svg','w').write('\n'.join(o))
print(len('\n'.join(o)))
