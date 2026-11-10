# Tiny SVG renderer for BJJ diagrams (top-down and side views).
#
# Readability rules baked in here:
#  - Every limb/body part gets a white halo, so where one limb crosses another
#    there is a visible gap and you can tell which is on top.
#  - Limbs are drawn as one polyline per chain (no seams at the joints).
#  - *_FAR colours are a darker shade for limbs that are underneath / far side.
#  - Widths are scaled by K so limbs are thinner than the bodies they sit on.
YOU=dict(fill='#2f6fd6',dark='#163f86',light='#9cc0f5')
YOU_FAR=dict(fill='#1f4fa3',dark='#0f2f66',light='#7aa6e8')
THEM=dict(fill='#b9bfc8',dark='#5d6672',light='#e3e6ea')
THEM_FAR=dict(fill='#8d95a1',dark='#4a525d',light='#c9ced5')
ORANGE='#e8590c'; INK='#1d2433'; HALO='#f6f7f9'
K=0.8          # limb width scale
FONT='DejaVu Sans,sans-serif'

class Scene:
    def __init__(s,w=420,h=300): s.w,s.h=w,h; s.items=[]; s.marks={}
    def add(s,z,svg): s.items.append((z,len(s.items),svg))
    def chain(s,c,pts,w=13,z=0,halo=True):
        w=w*K; d=' '.join(f'{x},{y}' for x,y in pts)
        pl=lambda col,sw:f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="{sw:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
        s.add(z,(pl(HALO,w+8) if halo else '')+pl(c['dark'],w+3)+pl(c['fill'],w))
    def limb(s,c,a,b,w=13,z=0): s.chain(c,[a,b],w,z)
    def torso(s,c,pts,z=0):
        d=' '.join(f'{x},{y}' for x,y in pts)
        s.add(z,f'<polygon points="{d}" fill="{HALO}" stroke="{HALO}" stroke-width="9" stroke-linejoin="round"/>'
                f'<polygon points="{d}" fill="{c["fill"]}" stroke="{c["dark"]}" stroke-width="3" stroke-linejoin="round"/>')
    def blob(s,c,cx,cy,rx,ry,rot=0,z=0):
        e=lambda f,st,sw:f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" fill="{f}" stroke="{st}" stroke-width="{sw}"/>'
        s.add(z,e(HALO,HALO,9)+e(c['fill'],c['dark'],3))
    def head(s,c,p,r=15,z=0):
        s.add(z,f'<circle cx="{p[0]}" cy="{p[1]}" r="{r+4}" fill="{HALO}"/><circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{c["light"]}" stroke="{c["dark"]}" stroke-width="3"/>')
    def mat(s,y,x0=14,x1=None):
        x1=x1 or s.w-14
        s.add(-50,f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#9aa1ab" stroke-width="3" stroke-linecap="round"/>')
    def arrow(s,a,b,col='#6b7280',z=90,curve=0):
        (ax,ay),(bx,by)=a,b; mx,my=(ax+bx)/2,(ay+by)/2
        nx,ny=-(by-ay),(bx-ax); L=max((nx*nx+ny*ny)**.5,1); cx,cy=mx+nx/L*curve,my+ny/L*curve
        import math; ang=math.atan2(by-cy,bx-cx); h=9
        p1=(bx-h*math.cos(ang-0.45),by-h*math.sin(ang-0.45)); p2=(bx-h*math.cos(ang+0.45),by-h*math.sin(ang+0.45))
        s.add(z,f'<path d="M{ax},{ay} Q{cx:.1f},{cy:.1f} {bx},{by}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 4"/>'
                f'<polygon points="{bx},{by} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{col}"/>')
    def mark(s,n,p,z=99):
        s.marks[n]=p; r,f=(15,18) if getattr(s,'ms',False) else (10,12)
        s.add(z,f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{ORANGE}" stroke="#fff" stroke-width="2"/><text x="{p[0]}" y="{p[1]+f*0.37:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{f}" font-weight="700" fill="#fff">{n}</text>')
    def tag(s,text,p,z=98,col=INK,size=12,anchor='middle'):
        s.add(z,f'<text x="{p[0]}" y="{p[1]}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" font-weight="700" fill="{col}" stroke="{HALO}" stroke-width="3" paint-order="stroke">{text}</text>')
    def you(s,p): s.tag('YOU',p,col=YOU['dark'])
    def them(s,p): s.tag('THEM',p,col=THEM['dark'])
    def note(s,text,p): s.tag(text,p,col='#6b7280',size=11)
    def svg(s,eye=None):
        body=''.join(x for _,_,x in sorted(s.items))
        if eye in s.marks:   # eye-test ring around the one marker that matters most
            x,y=s.marks[eye]; r=24 if getattr(s,'ms',False) else 17; body+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="5 3"/>'
        return f'<svg viewBox="0 0 {s.w} {s.h}" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="{s.w}" height="{s.h}" rx="10" fill="{HALO}"/>{body}</svg>'

def supine(S,c,head=(70,150),z=0,arms='sides',legs='straight',far=None):
    """Person on their back, top-down, head left. `far` colours the limbs (they're under someone)."""
    hx,hy=head; lc=far or c
    sl=(hx+32,hy-30); sr=(hx+32,hy+30); hl=(hx+132,hy-20); hr=(hx+132,hy+20)
    if arms=='sides':
        S.chain(lc,[sl,(hx+75,hy-52),(hx+120,hy-55)],12,z-1); S.chain(lc,[sr,(hx+75,hy+52),(hx+120,hy+55)],12,z-1)
    if legs=='straight':
        lc=c   # legs are rarely under anyone; only the arms take the far shade
        S.chain(lc,[hl,(hx+200,hy-25),(hx+262,hy-28)],15,z-1); S.chain(lc,[hr,(hx+200,hy+25),(hx+262,hy+28)],15,z-1)
    S.torso(c,[sl,(hx+20,hy),sr,hr,hl],z)
    S.head(c,head,16,z+1)
    return dict(sl=sl,sr=sr,hl=hl,hr=hr)

def figure_html(obj,eye=None):
    """HTML for a scene result: one Scene, or a list of (caption, Scene|decision) panels."""
    import html
    if isinstance(obj,Scene): return obj.svg(eye)
    cells=[]
    for cap,x in obj:
        if isinstance(x,Scene): inner=x.svg(eye)
        else:
            title,rows=x
            inner='<div class="dec"><b>'+html.escape(title)+'</b>'+''.join(f'<div class="row"><span>{html.escape(a)}</span><span class="to">&rarr; {html.escape(b)}</span></div>' for a,b in rows)+'</div>'
        cells.append(f'<div class="cell"><div class="cap">{html.escape(cap)}</div>{inner}</div>')
    return f'<div class="panels n{len(obj)}">'+''.join(cells)+'</div>'

PANEL_CSS=""".panels{display:grid;grid-template-columns:1fr 1fr;gap:2mm}
.panels .cell svg{width:100%;height:auto;display:block}
.cap{font:600 8.2pt Fredoka,DejaVu Sans,sans-serif;color:#1d2433;margin:0 0 .6mm}
.dec{background:#f6f7f9;border-radius:1.5mm;padding:2mm;font-size:7.6pt;line-height:1.25}
.dec .row{display:flex;justify-content:space-between;gap:2mm;border-top:1px solid #dde1e7;padding:1mm 0}
.dec .to{font-weight:700;color:#163f86;white-space:nowrap}"""
