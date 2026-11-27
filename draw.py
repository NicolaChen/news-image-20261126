"""Authoring tool: Pillow + macOS Supplemental fonts. Not used by the judge."""
from functools import lru_cache
from math import cos, sin, tau
from pathlib import Path
from random import Random
from sys import argv

from PIL import Image, ImageDraw, ImageFont

S = 2
PAPER, INK, RUST = "#f5efde", "#192823", "#a43828"
FONTS = Path("/System/Library/Fonts/Supplemental")
im = Image.new("RGB", (1024*S, 1024*S), PAPER)
d = ImageDraw.Draw(im)


def xy(points):
    return [(round(x*S), round(y*S)) for x, y in points]


def box(x, y, w, h, fill):
    d.rectangle((x*S, y*S, (x+w)*S-1, (y+h)*S-1), fill=fill)


def poly(points, fill):
    d.polygon(xy(points), fill=fill)


def line(points, fill, width=2):
    d.line(xy(points), fill=fill, width=round(width*S), joint="curve")


def oval(x, y, w, h, fill):
    d.ellipse((x*S, y*S, (x+w)*S, (y+h)*S), fill=fill)


@lru_cache
def font(face, size):
    return ImageFont.truetype(str(FONTS / (face + ".ttf")), size*S)


def text(x, y, words, size, color=INK, face="Arial Bold"):
    d.text((x*S, y*S), words, font=font(face, size), fill=color, anchor="lt")


def texture(x, y, w, h, n, color, seed):
    rng = Random(seed)
    for _ in range(n):
        a, b = rng.randrange(x, x+w), rng.randrange(y, y+h)
        box(a, b, rng.choice((1, 1, 2)), 1, color)


def gaza(x, y):
    box(x, y, 480, 300, "#deb582")
    for yy in range(0,210):
        t=yy/210
        box(x,y+yy,480,1,(int(226-20*t),int(184-30*t),int(133-18*t)))
    oval(x+288, y+24, 131, 131, "#f2c989")
    texture(x, y, 479, 211, 3400, "#dcb17d", 1)
    for i, h in enumerate((42, 65, 58, 79, 48, 110, 76, 55, 85, 39, 55, 71)):
        box(x+i*40, y+220-h, 42, h, "#ad7a5f")
    poly([(x,y+217),(x+45,y+204),(x+110,y+228),(x+220,y+215),
          (x+285,y+232),(x+364,y+208),(x+480,y+221),(x+480,y+299),(x,y+299)], "#694f40")
    poly([(x+48,y+224),(x+48,y+88),(x+135,y+81),(x+153,y+102),
          (x+171,y+84),(x+200,y+99),(x+203,y+151),(x+178,y+163),
          (x+221,y+180),(x+227,y+225)], "#463933")
    for i in range(3):
        box(x+64+i*39,y+119,22,26,"#d2a379")
        box(x+64+i*39,y+164,22,29,"#d2a379")
    for u,v in [(74,119),(114,119),(153,164)]:
        poly([(x+u,y+v),(x+u+12,y+v),(x+u,y+v+19)],"#775847")
    for j in (108,153,200):
        line([(x+50,y+j),(x+128,y+j-4),(x+175,y+j+4)],"#ab7d61",4)
    poly([(x+176,y+226),(x+223,y+194),(x+247,y+205),(x+269,y+191),
          (x+306,y+228),(x+346,y+218),(x+399,y+249),(x+480,y+253),
          (x+480,y+299),(x+100,y+299)], "#574137")
    for a,b,w,h in [(220,226,67,29),(141,245,48,18),(390,252,51,24),(40,253,80,29)]:
        poly([(x+a,y+b),(x+a+w*.7,y+b-h),(x+a+w,y+b-6),(x+a+w*.8,y+b+10)],"#927057")
    rng = Random(26)
    for _ in range(66):
        a,b = x+rng.randrange(3,470),y+rng.randrange(230,296)
        line([(a,b),(a+rng.randrange(3,10),b-rng.randrange(0,4))],"#8d654d",2)
    # Two small people show scale, not identifiable individuals.
    for a,b in [(x+331,y+243),(x+357,y+256)]:
        oval(a-5,b-23,10,10,INK)
        line([(a,b-11),(a,b+7),(a-7,b+19)],INK,6)
        line([(a,b+6),(a+6,b+19)],INK,5)


def emblem(kind,x,y,fg,bg):
    box(x,y,126,126,bg)
    def p(points, c): poly([(x+a,y+b) for a,b in points],c)
    def l(points, c, w): line([(x+a,y+b) for a,b in points],c,w)
    def b(a,e,w,h,c): box(x+a,y+e,w,h,c)
    if kind == "storm":
        for a,h,w in ((4,37,19),(25,57,20),(52,83,24),(82,47,15),(100,67,22)):
            b(a,126-h,w,h,fg)
            for dy in range(8,h-5,13): b(a+5,126-h+dy,4,5,bg)
        for a in (32,52,72,92): l([(a,17),(a-17,40)],fg,3)
        b(0,104,126,22,"#507784")
        for dy in (104,116):
            l([(0,dy),(23,dy-4),(47,dy),(71,dy-4),(97,dy),(125,dy-4)],fg,2)
    if kind == "vote":
        p([(23,59),(100,59),(112,74),(13,74)],fg)
        b(14,78,98,36,fg)
        b(39,66,48,5,bg)
        p([(38,21),(77,12),(88,56),(48,65)],fg)
        l([(50,38),(59,44),(74,26)],bg,4)
        b(50,91,26,9,bg)
    if kind == "court":
        p([(12,45),(63,14),(114,45)],fg)
        for a in (25,51,77,98): b(a,51,7,43,fg)
        b(19,96,88,6,fg)
        b(12,107,102,6,fg)
        l([(53,45),(69,57),(61,70),(72,84),(67,97)],bg,4)
    if kind == "euro":
        text(x+29,y+27,"€",75,fg)
        for i in range(12):
            a = i*tau/12
            u,v=round(x+63+51*cos(a)),round(y+63+51*sin(a))
            oval(u-2,v-2,4,4,fg)


def card(x,y,region,head,kind,palette):
    line([(x,y),(x+464,y)],INK,2)
    emblem(kind,x,y+19,*palette)
    text(x+144,y+19,region,23,RUST)
    size = 31 if len(head) == 4 else 34
    for i, row in enumerate(head):
        assert font("Arial Bold",size).getlength(row)/S <= 310, row
        text(x+144,y+53+i*(size+2),row,size)


text(40,33,"THE WORLD IN FIVE",29,RUST)
text(819,35,"DAILY BRIEF",25,INK)
text(40,75,"26 November 2026",86,INK,"Georgia Bold")
line([(40,183),(984,183)],INK,4)
box(40,204,944,300,INK)
gaza(504,204)
text(66,227,"01   /   GAZA",26,"#f5bb83")
for yy, words in [(272,"Israeli fire"),(328,"kills 10"),(384,"Palestinians")]:
    text(66,yy,words,53,PAPER,"Georgia Bold")
text(67,458,"Gaza hospitals, via AP",26,"#f5bb83")

card(40,532,"02   /   UNITED STATES",("Thanksgiving", "storms flood", "the East Coast"),
     "storm", ("#eef0e2","#365968"))
card(520,532,"03   /   GUINEA-BISSAU",("Junta delays", "elections to", "November 2028"),
     "vote", ("#ecdc9b","#384e39"))
card(40,725,"04   /   MYANMAR",("Rejects parts of", "ICJ ruling on", "the Rohingya", "genocide"),
     "court", ("#f4d9ad","#8c473b"))
card(520,725,"05   /   EUROPE",("EU nominates", "Pablo Hernández", "de Cos for ECB", "president"),
     "euro", ("#f5dda7","#52476c"))
line([(40,934),(984,934)],INK,4)
text(40,956,"THURSDAY   /   WORLD NEWS",24,RUST)
text(685,956,"ILLUSTRATED EDITION",24,INK)
im.resize((1024,1024),Image.Resampling.LANCZOS).save(argv[1], optimize=True)
