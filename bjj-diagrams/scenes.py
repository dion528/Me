"""One function per position.

A function returns either
  (Scene, [checklist])                      -> a single diagram, or
  ([(caption, Scene|str), ...], [checklist]) -> panels (a sequence, or two views).
A str panel is a short text cell (e.g. the "their reaction picks the finish" box).
Marker numbers run across all panels and match the checklist order.
"""
from fig import *

def upright(S,c,cx,cy,face='left',z=5,hr=15):
    # shoulders seen from above, head slightly forward
    vert = face in ('left','right')
    S.blob(c,cx,cy,20 if vert else 40,40 if vert else 20,0,z)
    dx={'left':-6,'right':6,'up':0,'down':0}[face]; dy={'up':-6,'down':6,'left':0,'right':0}[face]
    S.head(c,(cx+dx,cy+dy),hr,z+2)

def side_person(S,c,j,z=0,far=None,torso_w=34):
    """Side view. j: head, sh, hip, arm/leg (near, list of pts), farm/farl (far side, drawn dark & behind)."""
    f=far or (YOU_FAR if c is YOU else THEM_FAR)
    if 'farl' in j: S.chain(f,j['farl'],15,z-2)
    if 'farm' in j: S.chain(f,j['farm'],12,z-2)
    S.chain(c,[j['sh'],j['hip']],torso_w,z)
    S.head(c,j['head'],15,z+1)
    if 'leg' in j: S.chain(c,j['leg'],15,z+2)
    if 'arm' in j: S.chain(c,j['arm'],12,z+3)

# Panels are drawn in the same 420x300 space but shown half size, so bump marks and tags.
def P(): S=Scene(); S.ms=True; return S

# ---------------------------------------------------------------- pins (top-down)
def mount():
    S=Scene(); supine(S,THEM,far=THEM_FAR)
    S.chain(YOU,[(178,130),(128,96),(182,90)],15,5); S.chain(YOU,[(178,170),(128,204),(182,210)],15,5)
    upright(S,YOU,170,150)
    S.chain(YOU,[(165,122),(132,130),(114,142)],11,7); S.chain(YOU,[(165,178),(132,170),(114,158)],11,7)
    for n,p in [(1,(128,96)),(2,(185,150)),(3,(182,210)),(4,(114,142))]: S.mark(n,p)
    S.you((215,108)); S.them((330,100))
    return S,["Knees pinched up toward their armpits","Hips low and heavy on their belly","Feet tucked under their thighs (or crossed under their hips)","Hand deep in the collar: your default first action"]

def high_mount():
    S=Scene(); supine(S,THEM,far=THEM_FAR)
    S.chain(YOU,[(150,130),(98,104),(140,84)],15,5); S.chain(YOU,[(150,170),(98,196),(140,216)],15,5)
    upright(S,YOU,142,150)
    S.chain(YOU,[(137,122),(100,128),(86,140)],11,7); S.chain(YOU,[(137,178),(100,172),(86,160)],11,7)
    S.arrow((190,236),(120,214),curve=-10); S.note('walk the knees up',(230,256))
    for n,p in [(1,(98,104)),(2,(150,150)),(3,(205,150))]: S.mark(n,p)
    S.you((180,96)); S.them((330,100))
    return S,["Knees walked up into their armpits","Weight on their chest: their elbows can't stay on the ribs","Their hips are free to bridge, so post if they buck"]

def _s_mount_top():
    S=P(); supine(S,THEM,arms='none',far=THEM_FAR)
    S.chain(THEM_FAR,[(102,180),(150,205),(190,210)],12,-1)        # their far arm at their side
    S.chain(YOU,[(150,140),(84,112),(118,82)],15,5)                  # knee by their head (folded)
    S.chain(YOU,[(160,162),(184,200),(214,186)],15,4)                # other foot planted by their hip
    upright(S,YOU,150,150)
    S.chain(THEM,[(102,120),(126,92),(140,62)],12,6)                 # trapped arm, raised, hugged
    S.chain(YOU,[(140,126),(122,100),(136,80)],11,8); S.chain(YOU,[(160,126),(160,98),(144,84)],11,8)
    for n,p in [(1,(84,112)),(2,(216,186)),(3,(140,70)),(4,(150,150))]: S.mark(n,p)
    S.tag('YOU',(214,124),col=YOU['dark'],size=20); S.tag('THEM',(330,96),col=THEM['dark'],size=20)
    return S

def _s_mount_side():
    # Seen from the side of your planted foot: they're flat (head left), you sit high on their chest.
    S=P(); S.mat(266)
    S.chain(THEM,[(150,248),(300,252)],34,0)                         # their body, flat
    S.chain(THEM,[(290,252),(400,256)],15,-1)
    S.head(THEM,(108,242),17,1)
    side_person(S,YOU,dict(head=(172,92),sh=(176,126),hip=(176,214),
        leg=[(176,214),(250,160),(262,250)],                         # near leg: foot planted by their hip, knee up
        farl=[(176,214),(104,192),(130,236)]),z=5,torso_w=44)        # far leg: knee up by their head
    S.chain(THEM,[(140,238),(150,170),(160,112)],12,7)               # their arm, straight up between your arms
    S.chain(YOU,[(184,138),(150,148),(146,176)],11,9)                # your arm hugging it to your chest
    S.mark(4,(176,206)); S.mark(1,(104,192)); S.mark(2,(262,246)); S.mark(3,(160,116))
    S.tag('YOU',(240,100),col=YOU['dark'],size=20); S.tag('THEM',(340,226),col=THEM['dark'],size=20)
    return S

def s_mount():
    return [('From above: the S shape',_s_mount_top()),('From the side: sit up, weight on the chest',_s_mount_side())], \
        ["One knee up by their head","Other foot planted by their hip","Their arm hugged tight to your chest, thumb up","Weight stays on their chest until you swing the leg over"]

def side_control():
    S=Scene(); supine(S,THEM,far=THEM_FAR)
    S.torso(YOU,[(96,126),(156,126),(160,214),(98,214)],5)
    S.chain(YOU,[(102,208),(74,246),(112,282)],15,4)
    S.chain(YOU,[(156,208),(186,186),(232,240)],15,4)
    S.chain(YOU,[(98,132),(66,128),(46,150)],11,6)
    S.chain(YOU,[(154,132),(196,112),(210,128)],11,6)
    S.head(YOU,(126,106),15,7)
    for n,p in [(1,(52,148)),(2,(128,170)),(3,(186,186)),(4,(210,128)),(5,(102,208))]: S.mark(n,p)
    S.you((150,268)); S.them((330,100))
    return S,["Crossface: shoulder turns their chin away","Chest to chest, hips low","Knee tight to their near hip","Hand blocks the far hip (or far underhook)","Other knee by their head: blocks the turn in"]

def knee_on_belly():
    S=Scene(); supine(S,THEM,far=THEM_FAR)
    S.chain(YOU,[(196,214),(250,250),(300,262)],15,4)                # far leg posted wide
    upright(S,YOU,184,214,face='up')
    S.chain(YOU,[(178,206),(174,152),(208,184)],15,8)                # knee on belly, shin across
    S.chain(YOU,[(166,208),(132,176),(112,150)],11,7)                # collar grip
    S.chain(YOU,[(204,208),(226,184),(222,172)],11,7)                # hand on hip/belt
    for n,p in [(1,(174,152)),(2,(300,262)),(3,(112,150)),(4,(222,170))]: S.mark(n,p)
    S.you((150,262)); S.them((330,100))
    return S,["Knee on their belly, shin across it","Other leg posted wide for base","Collar grip pulls them into the knee","Hand on hip or belt: follow when they move"]

def closed_guard():
    S=Scene(); supine(S,YOU,arms='none',legs='none')
    S.chain(THEM,[(250,130),(205,108),(290,96)],15,2); S.chain(THEM,[(250,170),(205,192),(290,204)],15,2)
    upright(S,THEM,246,150,z=3)
    S.chain(THEM,[(242,122),(222,128),(206,134)],11,4); S.chain(THEM,[(242,178),(222,172),(206,166)],11,4)
    S.chain(YOU,[(202,130),(236,104),(268,140)],15,6); S.chain(YOU,[(202,170),(236,196),(270,158)],15,6)
    S.chain(YOU,[(102,120),(160,110),(232,126)],11,7); S.chain(YOU_FAR,[(102,180),(150,198),(190,176)],11,1)
    for n,p in [(1,(270,150)),(2,(232,126)),(3,(206,166)),(4,(150,150))]: S.mark(n,p)
    S.you((110,215)); S.them((330,80))
    return S,["Ankles locked behind their back","Collar grip: pull to break their posture","Their counter: hands on your hips, head up","Your hips off the mat to angle for sweeps and attacks"]

def half_guard_top():
    S=Scene(); supine(S,THEM,legs='none',far=THEM_FAR)
    S.chain(YOU,[(180,196),(232,160),(300,150)],15,1)                # your trapped leg, between theirs
    S.chain(THEM,[(202,130),(250,120),(272,158)],15,3); S.chain(THEM_FAR,[(202,170),(250,178),(272,152)],15,0)
    S.torso(YOU,[(98,120),(160,112),(190,200),(132,214)],5)
    S.chain(YOU,[(140,210),(182,250),(240,262)],15,4)                # free leg posted
    S.chain(YOU,[(100,126),(66,128),(48,150)],11,6)                  # crossface
    S.chain(YOU,[(156,120),(120,92),(98,88)],11,6)                   # underhook far arm
    S.head(YOU,(124,100),15,7)
    for n,p in [(1,(52,148)),(2,(104,88)),(3,(300,150)),(4,(240,262))]: S.mark(n,p)
    S.you((160,286)); S.them((330,100))
    return S,["Crossface first","Far-side underhook, flatten their shoulders","Your trapped leg: walk it free once they're flat","Free leg posted for base"]

def back_control():
    S=Scene()
    S.chain(THEM,[(192,170),(178,105),(186,40)],15,2); S.chain(THEM,[(228,170),(242,105),(234,40)],15,2)
    upright(S,THEM,210,172,face='up',z=3)
    upright(S,YOU,210,236,face='up',z=1)
    # your legs come round the outside of their hips, over the thigh, heel INSIDE the thigh
    S.chain(YOU,[(186,232),(160,172),(166,124),(198,110)],15,5)
    S.chain(YOU,[(234,232),(260,172),(254,124),(222,110)],15,5)
    S.head(YOU,(186,206),14,6)                                       # head beside theirs, choking side
    S.chain(YOU,[(192,222),(180,196),(232,186)],11,7)                # choking arm over the shoulder
    S.chain(YOU,[(232,228),(244,206),(232,188)],11,7)                # under arm, hands meet
    for n,p in [(1,(232,187)),(2,(196,110)),(3,(170,214)),(4,(224,110))]: S.mark(n,p)
    S.them((290,60)); S.you((290,270))
    return S,["Seatbelt: one arm over the shoulder, one under","Hooks inside their thighs","Your head tight beside theirs on the choking side","Feet never crossed in front of them"]

def turtle_top():
    S=Scene()
    S.torso(THEM,[(120,128),(220,132),(220,168),(120,172)],1)
    S.chain(THEM_FAR,[(122,132),(92,118),(80,124)],12,0); S.chain(THEM_FAR,[(122,168),(92,182),(80,176)],12,0)
    S.chain(THEM_FAR,[(216,136),(200,118),(262,112)],14,0); S.chain(THEM_FAR,[(216,164),(200,182),(262,188)],14,0)
    S.head(THEM,(104,150),15,2)
    S.torso(YOU,[(140,112),(200,108),(206,196),(146,200)],4)
    S.chain(YOU,[(146,116),(118,128),(118,158)],11,5); S.chain(YOU,[(150,196),(128,182),(118,160)],11,5)
    S.chain(YOU,[(200,192),(232,236),(270,226)],15,3); S.chain(YOU,[(196,112),(238,76),(276,86)],15,3)
    S.head(YOU,(172,92),14,6)
    for n,p in [(1,(118,158)),(2,(175,150)),(3,(270,226))]: S.mark(n,p)
    S.them((330,150)); S.you((172,62))
    return S,["Seatbelt first: one arm over the shoulder, one under","Chest heavy on their back","Then insert hooks one at a time, or roll them over"]

def headlock():
    S=Scene(); supine(S,THEM,arms='none',far=THEM_FAR)
    S.chain(THEM_FAR,[(102,180),(150,205),(190,210)],12,-1)
    S.chain(YOU,[(172,92),(170,40),(118,30)],15,4)                   # one leg forward
    S.chain(YOU,[(176,112),(250,70),(318,64)],15,4)                  # other leg back: legs wide
    S.torso(YOU,[(84,104),(118,134),(176,118),(168,86)],5)
    S.chain(THEM,[(102,120),(122,90),(150,66)],12,6)                 # their near arm, clamped
    S.chain(YOU,[(112,104),(132,76),(150,62)],11,7)                  # your hand holds it under your armpit
    S.chain(YOU,[(92,118),(36,140),(52,192),(96,186)],11,7)          # arm wraps round their head
    S.head(YOU,(84,92),14,8)
    for n,p in [(1,(40,160)),(2,(150,66)),(3,(178,108)),(4,(318,64))]: S.mark(n,p)
    S.you((250,40)); S.them((330,160))
    return S,["Their head wrapped under your arm","Their near arm trapped under your armpit","Your hip tight against their ribs","Legs spread wide for base"]

def headlock_bottom():
    # Same hold, you underneath. Their control points are what each escape removes.
    S=Scene(); supine(S,YOU,arms='none',far=YOU_FAR)
    S.chain(THEM,[(172,92),(170,40),(118,30)],15,4)
    S.chain(THEM,[(176,112),(250,70),(318,64)],15,4)
    S.torso(THEM,[(84,104),(118,134),(176,118),(168,86)],5)
    S.chain(YOU,[(102,120),(122,90),(150,66)],12,6)                  # your near arm, clamped under their armpit
    S.chain(THEM,[(112,104),(132,76),(150,62)],11,7)
    S.chain(THEM,[(92,118),(36,140),(52,192),(96,186)],11,7)         # their arm round your head
    S.head(THEM,(84,92),14,8)
    S.chain(YOU,[(102,180),(132,150),(98,112)],12,9)                 # your far forearm framed across their neck/jaw
    S.arrow((210,200),(250,262),col=YOU['dark'],curve=-12); S.note('hip escape away',(300,250))
    for n,p in [(1,(40,160)),(2,(104,114)),(3,(176,118))]: S.mark(n,p)
    S.you((360,220)); S.them((250,40))
    return S,["Their arm wraps your head: protect the neck before you move","Free arm: forearm frame across their neck or jaw","Their hip on your ribs: frame, then hip escape away to make the gap"]

# ---------------------------------------------------------------- sequences
def _cg_base(S,legs_closed=True):
    supine(S,YOU,arms='none',legs='none',far=YOU_FAR)
    S.chain(THEM,[(250,130),(205,108),(290,96)],15,2); S.chain(THEM,[(250,170),(205,192),(290,204)],15,2)
    upright(S,THEM,246,150,z=3)

def k_guard():
    # 1. closed guard, they posture up
    A=P(); _cg_base(A)
    A.chain(YOU,[(202,130),(236,104),(268,140)],15,6); A.chain(YOU,[(202,170),(236,196),(270,158)],15,6)
    A.arrow((270,60),(350,60),col=THEM['dark']); A.tag('they stand up',(310,40),col=THEM['dark'],size=20)
    A.tag('YOU',(110,230),col=YOU['dark'],size=20)
    # 2. K guard shape: on your side, under their near leg
    B=P()
    B.chain(THEM,[(262,132),(222,118),(292,104)],15,1)
    B.chain(THEM,[(262,168),(222,188),(296,198)],15,1)               # near leg (the one you attack)
    upright(B,THEM,262,150,z=4)
    B.chain(YOU_FAR,[(118,232),(178,212)],11,1)                      # far arm, underneath
    B.torso(YOU,[(100,244),(116,268),(196,236),(184,214)],2)          # on your side: narrow from above
    B.head(YOU,(78,262),15,3)
    B.chain(YOU,[(190,218),(236,232),(248,150)],15,6)                # inside shin across their near hip, knee out
    B.chain(YOU,[(196,236),(336,250),(300,138)],15,5)                # outside leg round and over their back
    B.chain(YOU,[(112,264),(176,270),(224,196)],11,7)                # gable round their near leg
    for n,p in [(1,(150,244)),(2,(246,170)),(3,(300,138)),(4,(222,196))]: B.mark(n,p)
    B.tag('YOU',(110,296),col=YOU['dark'],size=20); B.tag('THEM',(330,70),col=THEM['dark'],size=20)
    decide=("Their reaction picks the finish",[("Lean in, one arm inside your legs","Triangle"),
            ("Post a hand or push with a straight arm","Armbar"),
            ("Stand tall, back away, turn their hips","Crab ride, then back"),
            ("Square up and close the angle","Back to closed guard")])
    return [('1. They posture up or start to stand',A),('2. Side, shin, hook, grip',B),('3. Then',decide)], \
        ["On your side, angled under them. Never flat","Inside shin across their near hip, knee pointing out","Outside leg hooked over their back or lat","Grip their near leg: pant grip or gable"]

def _standing_them(S,hip=(240,160),lean=1.0,z=1):
    hx,hy=hip
    side_person(S,THEM,dict(head=(hx-70*lean,hy-56),sh=(hx-48*lean,hy-44),hip=hip,
        leg=[hip,(hx-6,hy+56),(hx+2,268)],farl=[hip,(hx+14,hy+54),(hx+26,268)],
        arm=[(hx-48*lean,hy-44),(hx-60*lean,hy+2),(hx-58*lean,hy+36)]),z=z)

def crab_ride():
    # 1. from K guard they stand tall and back away
    A=P(); A.mat(270); _standing_them(A,(250,150),0.6)
    side_person(A,YOU,dict(head=(70,256),sh=(96,254),hip=(160,250),
        leg=[(160,250),(212,214),(236,172)],farl=[(160,250),(226,238),(262,120)]),z=4,torso_w=30)
    A.arrow((290,110),(370,110),col=THEM['dark']); A.tag('they back away',(330,92),col=THEM['dark'],size=20)
    A.tag('YOU',(80,226),col=YOU['dark'],size=20)
    # 2. the crab ride: inverted, shoulders on the mat, chest glued to their hips
    B=P(); B.mat(270)
    H=(232,168)                                                      # their hips
    B.chain(THEM_FAR,[H,(222,214),(232,268)],15,0)                    # their far leg
    B.chain(THEM,[H,(168,122)],34,2); B.head(THEM,(148,116),15,3)
    B.chain(THEM,[(168,124),(152,170),(152,212)],12,4)
    B.chain(YOU,[(262,256),(262,152)],30,5)                          # you: shoulders on the mat, hips straight up
    B.head(YOU,(290,258),14,6)
    B.chain(YOU,[(262,152),(226,178),(220,220)],15,6)                # your leg between theirs, instep behind the knee
    B.chain(THEM,[H,(206,214),(214,268)],15,7)                       # their near leg, in front of your leg
    B.chain(YOU,[(262,236),(244,206),(240,176)],11,8)                # hand on the belt
    for n,p in [(1,(262,256)),(2,(222,226)),(3,(240,176))]: B.mark(n,p)
    B.tag('YOU',(352,230),col=YOU['dark'],size=20); B.tag('THEM',(150,80),col=THEM['dark'],size=20)
    # 3. sit them down: hooks inside the thighs, seatbelt
    C=P(); C.mat(270)
    side_person(C,THEM,dict(head=(164,140),sh=(180,170),hip=(204,252),
        leg=[(204,252),(140,206),(104,262)],farl=[(204,252),(152,214),(124,264)]),z=2)
    side_person(C,YOU,dict(head=(214,134),sh=(234,168),hip=(266,254),
        leg=[(266,254),(200,230),(152,220)],farl=[(266,254),(206,240),(170,232)],
        farm=[(236,180),(212,212),(182,200)],arm=[(234,168),(194,150),(176,192)]),z=4)
    C.mark(4,(152,220)); C.tag('THEM',(110,110),col=THEM['dark'],size=20); C.tag('YOU',(330,200),col=YOU['dark'],size=20)
    return [('1. From K guard they stand tall or back away',A),('2. Invert: the crab ride',B),('3. Sit them down, swap the hooks',C)], \
        ["Invert onto your shoulders, never your head","Insteps hooked behind their knees","Belt or hip grip: pull their hips onto your chest, no gap","Sit them down, swap to hooks inside the thighs, then seatbelt"]

SC=[('Mount',mount),('High mount',high_mount),('S-mount',s_mount),('Side control (cross body)',side_control),('Knee on belly',knee_on_belly),('Closed guard',closed_guard),('Half guard (you on top)',half_guard_top),('Back control',back_control),('Turtle (you on top)',turtle_top),('Cross body headlock (scarf hold)',headlock),('Cross body headlock: you underneath',headlock_bottom),('K guard',k_guard),('Crab ride',crab_ride)]
