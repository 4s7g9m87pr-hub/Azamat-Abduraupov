"""Create original SVG interface illustrations and export outlined SVG + WebP."""
from pathlib import Path
from io import BytesIO
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'images'
OUT.mkdir(exist_ok=True)
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
FONT = TTFont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT['head'].unitsPerEm

def rect(x,y,w,h,fill,rx=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'
def text(x,y,value,size=16,fill='#242421',weight=400):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{size}" fill="{fill}" font-weight="{weight}">{value}</text>'
def svg(content,w=960,h=680):
    return f'<svg xmlns="{SVG}" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{content}</svg>'
def window(x,y,w,h,bg):
    return rect(x+5,y+15,w,h,'#000000',14,'opacity=".08"')+rect(x,y,w,h,bg,14)+rect(x,y,w,34,'#ffffff',14)+rect(x,y+19,w,15,'#ffffff')+''.join(f'<circle cx="{x+18+i*14}" cy="{y+17}" r="3.5" fill="{c}"/>' for i,c in enumerate(['#e4b1a6','#e6ce94','#acc4a5']))+rect(x+w*.35,y+9,w*.35,16,'#f1f1ec',5)

def export(name,content,w=960,h=680):
    root=ET.fromstring(svg(content,w,h))
    # Export all lettering as vector paths: no font dependency in Figma.
    for parent in root.iter():
        for element in list(parent):
            if element.tag != f'{{{SVG}}}text': continue
            size=float(element.get('font-size','16')); scale=size/UPM
            x=float(element.get('x','0')); y=float(element.get('y','0'))
            group=ET.Element(f'{{{SVG}}}g',{'fill':element.get('fill','#242421'),'aria-label':element.text or ''})
            for char in element.text or '':
                glyph_name=CMAP.get(ord(char),'.notdef'); pen=SVGPathPen(GLYPHS); GLYPHS[glyph_name].draw(pen)
                if pen.getCommands():
                    ET.SubElement(group,f'{{{SVG}}}path',{'d':pen.getCommands(),'transform':f'translate({x:.3f} {y:.3f}) scale({scale:.6f} {-scale:.6f})'})
                x += FONT['hmtx'].metrics[glyph_name][0]*scale
            parent.remove(element); parent.append(group)
    path=OUT/f'{name}.svg'; ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
    png=cairosvg.svg2png(url=str(path),output_width=w,output_height=h)
    Image.open(BytesIO(png)).convert('RGB').save(OUT/f'{name}.webp','WEBP',quality=93,method=6)
    print(f'{name}: outlined SVG + WebP')

portrait='''<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#e8e4d7"/><stop offset="1" stop-color="#c3c4af"/></linearGradient><linearGradient id="face" x1="0" x2="1"><stop stop-color="#dab18a"/><stop offset=".6" stop-color="#e7c4a2"/><stop offset="1" stop-color="#bd9575"/></linearGradient><linearGradient id="shirt" x2="1" y2="1"><stop stop-color="#374938"/><stop offset="1" stop-color="#1d2e24"/></linearGradient></defs><rect width="640" height="760" fill="url(#bg)"/><circle cx="345" cy="283" r="218" fill="#ede9dc" opacity=".5"/><path d="M50 760 Q60 523 227 486 L413 486 Q574 522 595 760Z" fill="url(#shirt)"/><path d="M261 422 L262 507 Q320 550 379 504 L379 416Z" fill="#caa17e"/><path d="M245 468 Q314 509 393 463 L409 493 Q327 580 228 493Z" fill="#2f4030"/><ellipse cx="215" cy="336" rx="22" ry="39" fill="#cda482"/><ellipse cx="427" cy="336" rx="21" ry="39" fill="#cda482"/><path d="M220 254 Q220 172 321 170 Q424 171 426 272 L418 375 Q403 448 322 472 Q250 452 228 382Z" fill="url(#face)"/><path d="M213 295 Q192 223 235 183 Q248 129 335 143 Q405 132 431 203 Q457 236 425 305 L411 256 Q359 271 287 220 Q258 256 231 258 L228 305Z" fill="#252923"/><path d="M242 171 Q294 122 365 152 Q396 145 422 195 Q354 157 290 187Z" fill="#343a2e"/><path d="M254 302 Q274 294 291 301 M350 301 Q374 292 394 304" fill="none" stroke="#4b4032" stroke-width="7" stroke-linecap="round"/><path d="M259 325 Q275 316 292 325 M351 325 Q369 316 388 325" fill="none" stroke="#5d4c39" stroke-width="3" stroke-linecap="round"/><ellipse cx="278" cy="325" rx="5" ry="6" fill="#2c3028"/><ellipse cx="369" cy="325" rx="5" ry="6" fill="#2c3028"/><path d="M326 321 L315 367 Q324 376 339 367" stroke="#b98f6d" fill="none" stroke-width="3" stroke-linecap="round"/><path d="M288 398 Q323 414 357 396" fill="none" stroke="#8d654e" stroke-width="4" stroke-linecap="round"/><path d="M274 431 Q321 452 369 428" fill="none" stroke="#a78668" stroke-width="2" opacity=".35"/><path d="M160 591 L140 760 M475 591 L502 760" stroke="#53614b" stroke-width="2" opacity=".5"/><path d="M261 507 Q319 547 379 505" fill="none" stroke="#68745b" stroke-width="3"/><circle cx="85" cy="125" r="4" fill="#506348"/><path d="M505 442 l20 -15 M516 455 l25 -5" stroke="#8c9475" stroke-width="2"/>'''
export('portrait',portrait,640,760)

noma=rect(0,0,960,680,'#dce2cf')+window(72,76,816,528,'#f7f5ec')
noma+=text(111,158,'noma',30)+text(535,152,'Shop',11)+text(608,152,'Our story',11)+text(709,152,'Journal',11)+text(818,152,'Bag (0)',11)
noma+=text(111,221,'OBJECTS FOR A SLOWER EVERYDAY',10,'#53623f')+text(110,285,'Less,',63)+text(110,352,'but better.',63)
noma+=text(114,393,'Thoughtful things. A little room to breathe.',12,'#636457')+rect(112,420,151,39,'#3d4c33',22)+text(131,445,'Explore collection',11,'#ffffff')
noma+=rect(502,188,337,300,'#e4e4d3',5)+'''<ellipse cx="675" cy="465" rx="114" ry="11" fill="#65754c" opacity=".17"/><path d="M627 334 L625 438 Q631 470 679 467 Q724 466 730 436 L726 333Z" fill="#c09c70"/><ellipse cx="676" cy="335" rx="50" ry="12" fill="#b38e60"/><path d="M673 340 Q664 256 701 214 M673 315 Q625 270 612 246 M677 287 Q717 273 743 237" fill="none" stroke="#56633f" stroke-width="5"/><path d="M699 231 Q660 213 690 190 Q724 190 707 226 M655 292 Q614 300 601 255 Q641 240 655 292 M694 278 Q712 228 752 232 Q755 275 694 278" fill="#64764b"/><path d="M640 434 Q671 442 715 434" fill="none" stroke="#e2c49a" stroke-width="3"/>'''
noma+=text(112,536,'Made to keep. Designed to matter.',14)+text(112,565,'Explore everyday essentials with a calmer point of view.',10,'#636457')+text(695,559,'Discover the collection  →',10,'#485437')
export('noma',noma)

moneta=rect(0,0,960,680,'#ded5ef')+'''<circle cx="781" cy="111" r="138" fill="#c4b4e5" opacity=".5"/><circle cx="162" cy="555" r="174" fill="#cec0e8" opacity=".6"/>'''
moneta+=text(80,112,'moneta',30,'#3e3157')+text(81,146,'A LITTLE MORE CLARITY.',10,'#615275')
for x,y in [(245,156),(523,76)]:
    moneta+=rect(x+6,y+12,246,498,'#513d73',34,'opacity=".12"')+rect(x,y,246,498,'#25222e',34)+rect(x+7,y+7,232,484,'#fbf9ff',28)+rect(x+84,y+15,80,17,'#25222e',12)
moneta+=text(269,208,'Good morning, Alex',11,'#514961')+text(268,239,'Your overview',22,'#272130')+rect(266,258,204,122,'#bfa7e4',19)+text(283,286,'TOTAL BALANCE',9,'#483761')+text(282,328,'₸ 184,500',27,'#2c223a')+text(283,356,'A clear view of your everyday.',9,'#483761')
for i,(label,color) in enumerate([('Send','#ebe4f6'),('Add','#ecebe3'),('Save','#ebe4f6')]):
    moneta+=rect(267+i*70,397,62,53,color,12)+text(279+i*70,429,label,11,'#463753')
moneta+=text(268,485,'Recent activity',13,'#2c223a')
for i,(name,price,color) in enumerate([('Groceries','− ₸ 8,200','#e5ead7'),('Coffee','− ₸ 1,800','#ecddd0'),('Transport','− ₸ 950','#e4ddee')]):
    cy=514+i*35;moneta+=rect(269,cy-12,22,22,color,7)+text(300,cy+2,name,10,'#514961')+text(402,cy+2,price,9,'#514961')
moneta+=text(547,135,'Make space',22,'#272130')+text(547,164,'for your goals.',22,'#272130')+text(549,197,'One small step at a time.',11,'#6d627a')
moneta+='''<circle cx="646" cy="305" r="72" fill="none" stroke="#ece6f4" stroke-width="14"/><circle cx="646" cy="305" r="72" fill="none" stroke="#9271c3" stroke-width="14" stroke-dasharray="320 452" transform="rotate(-90 646 305)" stroke-linecap="round"/>'''+text(608,312,'70%',29,'#3d2b56')+text(597,338,'OF YOUR GOAL',9,'#6d627a')
moneta+=rect(547,409,197,76,'#eee8f7',14)+text(561,433,'Weekend away',13,'#423252')+text(561,457,'₸ 70,000 of ₸ 100,000',10,'#6d627a')+rect(548,505,194,37,'#3e2e52',20)+text(596,529,'Add to savings',11,'#ffffff')
export('moneta',moneta)

forma=rect(0,0,960,680,'#cad7d9')+window(72,76,816,528,'#f5f3ec')+text(107,157,'FORMA',22)+text(623,152,'Projects',10)+text(706,152,'Studio',10)+text(784,152,'Contact',10)
forma+=text(110,211,'ARCHITECTURE / INTERIORS / PERSPECTIVES',9,'#596361')+text(108,275,'Spaces that',54)+text(109,333,'shape the everyday.',54)
forma+=rect(111,363,736,176,'#9dafa9')+'''<path d="M111 486 L847 462 V539 H111Z" fill="#c2c2ae"/><path d="M184 537 V401 L388 376 L556 426 V539Z" fill="#d4ccba"/><path d="M388 376 L388 536 L556 539 V426Z" fill="#a4a290"/><path d="M225 537 V440 L331 432 V537Z" fill="#5d6960"/><path d="M406 444 L527 468 V513 L406 496Z" fill="#647b78"/><path d="M588 535 V399 L730 377 L803 412 V536Z" fill="#e7dfcc"/><path d="M730 377 V536 L803 536 V412Z" fill="#b3ae9d"/><path d="M616 440 L707 425 V488 L616 498Z" fill="#66796e"/><path d="M111 527 Q227 511 378 529 T847 519 V539 H111Z" fill="#7b8d73"/>'''
forma+=text(112,569,'01 / Courtyard residence',11)+text(642,569,'A quieter way to live.  ↗',11,'#596361')
export('forma',forma)

dala=rect(0,0,960,680,'#e5d3bb')+window(72,76,816,528,'#fffaf2')+text(112,157,'dala',30,'#3e4b3b')+text(574,150,'Discover',11,'#3e4b3b')+text(672,150,'Journeys',11,'#3e4b3b')+rect(760,126,88,34,'#3e4b3b',19)+text(778,148,'Let’s go ↗',10,'#ffffff')
dala+=rect(106,185,748,273,'#dce6d7',10)+'''<circle cx="698" cy="254" r="38" fill="#eac58d"/><path d="M443 458 L594 259 L678 366 L754 280 L854 396 V458Z" fill="#8b9e86"/><path d="M594 259 L556 309 L602 293 L626 300Z" fill="#eef0e2"/><path d="M754 280 L716 323 L759 310 L781 319Z" fill="#eef0e2"/><path d="M106 398 Q249 366 430 417 Q651 348 854 429 V458 H106Z" fill="#acb39a"/><path d="M106 427 Q289 385 460 442 Q701 402 854 438 V458 H106Z" fill="#73866c"/>'''
dala+=text(133,226,'A LITTLE CLOSER TO NATURE',9,'#44563d')+text(131,283,'Go somewhere',43,'#303e2c')+text(132,335,'that feels like you.',43,'#303e2c')
dala+=rect(133,365,287,54,'#fffaf2',28)+text(152,398,'Where would you like to go?',11,'#5d6857')+rect(367,371,46,42,'#3f5138',22)+text(381,398,'→',19,'#ffffff')
dala+=text(109,501,'Find your kind of escape',20,'#3e4b3b')
for i,(name,color) in enumerate([('Open landscapes','#d5dfc7'),('Quiet weekends','#e5cba3'),('New perspectives','#c2d3cc')]):
    x=108+i*252;dala+=rect(x,521,242,54,color,8)+text(x+15,553,name,13,'#3e4b3b')+text(x+211,554,'↗',17,'#3e4b3b')
export('dala',dala)
export('mark',rect(0,0,64,64,'#252621',16)+text(10,47,'a.',43,'#d8ccf1'),64,64)
