import html, io, base64, urllib.parse, qrcode
import scenes as SC
from fig import figure_html, PANEL_CSS
e=html.escape
def qr(u):
    q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=4,border=2); q.add_data(u); q.make(fit=True)
    b=io.BytesIO(); q.make_image().convert('1').save(b,'PNG'); return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
yt=lambda s:'https://www.youtube.com/results?search_query='+urllib.parse.quote_plus(s)
# Eye test: (marker number, the one detail to check first). Ringed on the diagram.
EYE={
 "Mount":(1,"Knees pinched high toward their armpits. Sitting tall on your knees = easy to bump."),
 "High mount":(1,"Knees in their armpits. That's what lifts their elbows off the ribs."),
 "S-mount":(4,"Weight on their chest. Swing the leg from low mount and you get stacked."),
 "Side control (cross body)":(1,"Crossface: their chin turned away. A head turned away can't bridge into you."),
 "Knee on belly":(1,"Weight through the knee on their belly, not sitting back on your heel."),
 "Closed guard":(2,"Break their posture first. A postured opponent can't be attacked."),
 "Half guard (you on top)":(1,"Crossface and underhook before you try to free your leg."),
 "Back control":(1,"Seatbelt first, hooks second."),
 "Turtle (you on top)":(1,"Seatbelt first, then the hooks one at a time."),
 "Cross body headlock (scarf hold)":(1,"The head wrap. Lose it and they're out."),
 "Cross body headlock: you underneath":(2,"Frame first, then move. Moving without a frame lets them close the gap."),
 "K guard":(1,"On your side. Flat on your back, they just pass."),
 "Crab ride":(4,"Crab hooks aren't back control. Swap to hooks inside the thighs plus a seatbelt."),
}
# Arrival script (book p. 8): settle 3 s, where are their elbows?, then the default.
LAND={
 "Mount":"Feed one hand deep in the collar",
 "Side control (cross body)":"Crossface, then work to mount",
 "Back control":"Lock the seatbelt, attack with the choking hand",
 "Half guard (you on top)":"Crossface and underhook, flatten them, free the knee",
}
# name -> (scene fn, view, refs, search, one-line idea)
P=[
 ("Mount",SC.mount,"Top-down",["Book p. 8: the arrival script","Book p. 9: Mount system (holding, table, finishes)","Book p. 21: Getting to mount","Book p. 42–43: curriculum 23–27"],"BJJ mount position basics gi","The best pin. Hold it first, then let their defence choose your attack."),
 ("High mount",SC.high_mount,"Top-down",["Book p. 9–10: Mount system, armbar","Book p. 28: Chapter 4, getting there"],"BJJ high mount position","Walk your knees up and their elbows come off the ribs."),
 ("S-mount",SC.s_mount,"Top-down and side view",["Book p. 10: Armbar","Book p. 28–29: Chapter 4","Book p. 44: card 31"],"BJJ S mount armbar setup","The step between high mount and the armbar. Weight stays on their chest."),
 ("Side control (cross body)",SC.side_control,"Top-down",["Book p. 11: Side control system","Book p. 20–21: Getting to side control and mount","Book p. 50: curriculum 50–56"],"BJJ side control crossface basics","The pin before mount. Kill the head and the near arm."),
 ("Knee on belly",SC.knee_on_belly,"Top-down",["Book p. 7: The map (rung 3)"],"BJJ knee on belly position basics","A mobile pin. It's not on your curriculum sheet, but it's a common bridge between side control and mount."),
 ("Closed guard",SC.closed_guard,"Top-down",["Book p. 13: Getting on top (guard)","Book p. 22: Cross collar from guard","Book p. 46–47: curriculum 33–41"],"BJJ closed guard basics breaking posture","Legs locked around them. From the bottom: break posture, sweep, then finish on top."),
 ("Half guard (you on top)",SC.half_guard_top,"Top-down",["Book p. 8: Top half guard default","Book p. 13: Top half guard"],"BJJ top half guard crossface underhook pass","Where most of your passes stall. Crossface and underhook, flatten, free the knee."),
 ("Back control",SC.back_control,"Top-down",["Book p. 12: Back system","Book p. 32: Chapter 6, rear naked choke","Book p. 54: curriculum 58–62"],"BJJ back control seatbelt hooks","Your best finishing position. Seatbelt first, hooks second."),
 ("Turtle (you on top)",SC.turtle_top,"Top-down",["Book p. 12: Back system table (turtle row)","Book p. 20: paths table"],"BJJ attacking the turtle seatbelt back take","They're on hands and knees. Get the seatbelt, then the hooks."),
 ("Cross body headlock (scarf hold)",SC.headlock,"Top-down",["Book p. 54–55: curriculum 68, 74, 80, 81 (the escapes)"],"BJJ scarf hold kesa gatame escape","Drawn with you on top so you know what they're holding. The next card is the one you'll live in."),
 ("Cross body headlock: you underneath",SC.headlock_bottom,"Top-down",["Book p. 54: 68 (head low), 74 (make a frame)","Book p. 55: 80 (go to back), 81 (go to knees)"],"BJJ escape scarf hold kesa gatame frame","Neck, frame, hips. Then two exits: turn away and slide out the back to take it (80), or turn in, post and come up to your knees (81). Which one when: ask your coach and write it here."),
 ("K guard",SC.k_guard,"Sequence, top-down schematic",["K Guard Study Page (separate)"],"K guard BJJ from closed guard","A hub, not a home. Their reaction picks triangle, armbar or crab ride."),
 ("Crab ride",SC.crab_ride,"Sequence, side-view schematic",["K Guard Study Page (separate)"],"crab ride BJJ back take gi","A transition to the back, not a place to stay. Inverting loads your neck: roll over the shoulder, never onto your head, and learn it with your coach first."),
]
css='''@font-face{font-family:Fredoka;font-weight:700;src:url(fonts/package/files/fredoka-latin-700-normal.woff2)}
@font-face{font-family:Fredoka;font-weight:600;src:url(fonts/package/files/fredoka-latin-600-normal.woff2)}
@page{size:A4;margin:12mm 13mm 13mm}
body{margin:0;font-family:"DejaVu Sans",sans-serif;font-size:9.4pt;color:#1d2433;-webkit-print-color-adjust:exact;print-color-adjust:exact}
h1,h2,h3,.ff{font-family:Fredoka,sans-serif;font-weight:700}
.pos{break-inside:avoid;border:1.4px solid #d5d9e0;border-radius:4mm;padding:3.5mm 4mm;margin:0 0 5mm}
.pos h2{font-size:15pt;margin:0 0 1mm} .view{font-family:Fredoka;font-weight:600;font-size:9pt;color:#6b7280;margin-left:2mm}
.grid{display:flex;gap:4mm} .grid .d{flex:0 0 108mm} .grid .t{flex:1}
.d svg{width:108mm;height:auto;display:block}
.idea{font-size:9.6pt;margin:0 0 2mm;font-style:italic}
ol{margin:0 0 2mm;padding-left:5mm} li{margin:0 0 1mm}
.refs{background:#eef0f3;border-radius:2mm;padding:2mm 2.5mm;font-size:8.6pt;margin-bottom:2mm}
.refs b{font-family:Fredoka;font-weight:600}
.qr{display:flex;gap:2mm;align-items:center;font-size:8pt;color:#4a5568} .qr img{width:20mm;height:20mm}
.key{display:inline-block;width:4mm;height:4mm;border-radius:1mm;vertical-align:middle;margin-right:1.5mm;border:1.5px solid}
.pb{page-break-before:always}
.rq{display:flex;gap:2mm;align-items:flex-start} .rq .refs{flex:1;margin:0} .rq .qr{flex-direction:column;gap:.5mm;text-align:center;font-size:7pt} .rq .qr img{width:17mm;height:17mm}
.seq .rq{flex-direction:column}
.eye{border-left:3mm solid #e8590c;background:#fff4ec;border-radius:1.5mm;padding:1.6mm 2.5mm;margin:0 0 2mm;font-size:9.4pt}
.eye b{font-family:Fredoka;font-weight:700;color:#e8590c;margin-right:1.5mm}
.land{background:#e9f0fc;border-radius:1.5mm;padding:1.6mm 2.5mm;margin:0 0 2mm;font-size:8.6pt}
.land b{font-family:Fredoka;font-weight:600;color:#163f86}
.seq .d{margin:1mm 0 2.5mm} .seq .panels.n2,.seq .panels.n3,.seq .panels.n4{grid-template-columns:repeat(var(--n),1fr)}
.seq .bot{display:flex;gap:5mm} .seq .bot .t{flex:1} .seq .bot .side{flex:0 0 58mm}
'''+PANEL_CSS
out=[f'''<div><div style="background:#1d2433;color:#fff;border-radius:4mm;padding:7mm 8mm;margin-bottom:5mm"><div class="ff" style="font-size:11pt;opacity:.8">Companion to Dion's Jiu-Jitsu Book</div><h1 style="font-size:30pt;margin:1mm 0 0;color:#fff">Position Atlas</h1><div style="font-size:11pt;margin-top:2mm;opacity:.9">A picture for every position the books talk about, with the page to read for each one.</div></div>
<h3 style="font-size:13pt;margin:0 0 2mm">How to read the diagrams</h3>
<ul style="margin:0 0 3mm;padding-left:5mm"><li><span class="key" style="background:#2f6fd6;border-color:#163f86"></span><b>Blue is you.</b> <span class="key" style="background:#b9bfc8;border-color:#5d6672;margin-left:3mm"></span><b>Grey is your partner.</b></li>
<li><b>Most views are from directly above,</b> as if you were looking down from the ceiling. An upright person looks like a head on a shoulder oval, with their legs folded out from underneath. Two are side views, and they're labelled.</li>
<li><b>Orange numbers</b> match the numbered checklist beside each diagram: the control points to check when you\'re in that position.</li><li><b>The ringed number is the eye test:</b> the one detail to check first. If that one is wrong, nothing else matters.</li><li><b>Darker shade = underneath.</b> A limb drawn darker is on the far side or under someone. A white gap shows which limb is on top where two cross.</li><li><b>Sequences</b> (K guard, crab ride) are movements, so they get numbered panels instead of one picture.</li>
<li><b>"Book p."</b> means the page in the complete Dion's Jiu-Jitsu Book (98 pages). Read the diagram and that page together.</li>
<li><b>The QR code</b> opens a YouTube search for the position, so you can see it moving. Search results, not hand-picked videos.</li></ul>
<div style="background:#fff8d6;border-radius:3mm;padding:3mm 4mm;font-size:9pt"><b>Be honest with yourself about these.</b> They're simplified drawings, made to show where the control points are, not exact body shapes. K guard and crab ride are movements more than pins, so they're marked "schematic": use the QR video and your coach's demonstration for those. Where a diagram and your coach disagree, your coach is right.</div></div>''']
for i,(name,fn,view,refs,q,idea) in enumerate(P):
    fig,keys=fn()
    en,et=EYE[name]
    kl=''.join(f'<li>{e(k)}</li>' for k in keys)
    rl='<br>'.join(e(r) for r in refs)
    pb=''
    eye=f'<div class="eye"><b>EYE TEST ({en})</b>{e(et)}</div>'
    land=f'<div class="land"><b>Land here:</b> settle 3 seconds → where are their elbows? → default: {e(LAND[name])}</div>' if name in LAND else ''
    refbox=f'<div class="rq"><div class="refs"><b>Read in your book</b><br>{rl}</div><div class="qr"><img src="{qr(yt(q))}"><span>Scan:<br>YouTube</span></div></div>'
    head=f'<h2>{e(name)}<span class="view">{e(view)}</span></h2>'
    if isinstance(fig,list):   # sequence / two views: full-width panels, text underneath
        out.append(f'''<div class="pos seq{pb}">{head}<div class="d" style="--n:{len(fig)}">{figure_html(fig,en)}</div>
<div class="bot"><div class="t"><p class="idea">{e(idea)}</p>{eye}{land}<ol>{kl}</ol></div><div class="side">{refbox}</div></div></div>''')
    else:
        out.append(f'''<div class="pos{pb}">{head}
<div class="grid"><div class="d">{figure_html(fig,en)}</div><div class="t"><p class="idea">{e(idea)}</p>{eye}{land}<ol>{kl}</ol>
{refbox}</div></div></div>''')
open('atlas.html','w',encoding='utf-8').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(out)}</body></html>')
print('ok')
