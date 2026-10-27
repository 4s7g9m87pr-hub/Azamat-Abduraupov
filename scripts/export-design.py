"""Convert browser-measured page geometry into editable, outlined SVG layers.

Usage: python scripts/export-design.py /absolute/path/to/layout-json-directory
The JSON records are measured from the four live frames in design/frames.html.
"""
import copy
import json
import re
import math
import sys
from pathlib import Path
from io import BytesIO
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
fonts = {}

def node(tag, parent, **attrs):
    return ET.SubElement(parent, f'{{{SVG}}}{tag}', {k.replace('_','-'):str(v) for k,v in attrs.items()})

def color(value):
    numbers=re.findall(r'[\d.]+',value)
    if value.startswith('rgb') and len(numbers)>=3:
        rgb='#'+''.join(f'{round(float(n)):02x}' for n in numbers[:3])
        return rgb,float(numbers[3]) if len(numbers)>3 else 1.0
    return value,1

def rounded_shape(parent,x,y,w,h,r,corner='',**attrs):
    r=max(0,min(r,w/2,h/2))
    if r and ('squircle' in corner or 'superellipse(2)' in corner):
        # CSS superellipse(2): Lamé exponent 4. Samples preserve the live contour.
        points=[]
        for cx,cy,start in [(x+w-r,y+r,-math.pi/2),(x+w-r,y+h-r,0),(x+r,y+h-r,math.pi/2),(x+r,y+r,math.pi)]:
            for i in range(25):
                a=start+i*math.pi/48
                c,s=math.cos(a),math.sin(a)
                points.append((cx+r*math.copysign(abs(c)**.5,c),cy+r*math.copysign(abs(s)**.5,s)))
        d='M '+' L '.join(f'{px:.3f} {py:.3f}' for px,py in points)+' Z'
        return node('path',parent,d=d,**attrs)
    return node('rect',parent,x=x,y=y,width=w,height=h,rx=r,**attrs)

def font_for(item, char):
    serif='Georgia' in item['font'] or 'serif' == item['font']
    bold=int(item.get('weight','400'))>=600
    italic=item.get('italic')=='italic'
    stem='NimbusRoman' if serif else 'NimbusSans'
    style='BoldItalic' if bold and italic else 'Bold' if bold else 'Italic' if italic else 'Regular'
    path=Path(f'/usr/share/fonts/opentype/urw-base35/{stem}-{style}.otf')
    if path not in fonts:
        f=TTFont(path);fonts[path]=(f,f.getGlyphSet(),f.getBestCmap())
    f,glyphs,cmap=fonts[path]
    if ord(char) not in cmap:
        path=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
        if path not in fonts:
            f=TTFont(path);fonts[path]=(f,f.getGlyphSet(),f.getBestCmap())
        f,glyphs,cmap=fonts[path]
    return f,glyphs,cmap

def draw_text(item,parent):
    x=item['x']; baseline=None
    for char in item['value']:
        f,glyphs,cmap=font_for(item,char);scale=item['size']/f['head'].unitsPerEm
        glyph_name=cmap.get(ord(char),'.notdef');advance=f['hmtx'].metrics[glyph_name][0]
        if baseline is None:
            h=f['hhea'];baseline=item['y']+item['h']*(h.ascent/(h.ascent-h.descent))
        pen=SVGPathPen(glyphs);glyphs[glyph_name].draw(pen)
        horizontal=scale
        if item['type']=='glyph' and advance:
            horizontal=item['w']/advance
        fill,alpha=color(item['color'])
        if pen.getCommands():
            node('path',parent,d=pen.getCommands(),fill=fill,opacity=alpha,transform=f'translate({x:.3f} {baseline:.3f}) scale({horizontal:.7f} {-scale:.7f})')
        x+=advance*scale

def draw_box(item,parent):
    fill,alpha=color(item['bg'])
    x,y,w,h=(item[k] for k in ['x','y','w','h']);radius=min(item['radius'],w/2,h/2)
    if alpha>0:rounded_shape(parent,x,y,w,h,radius,item.get('corner',''),fill=fill,opacity=alpha)
    sides=item['sides']
    if all(s['width']==sides[0]['width'] and s['color']==sides[0]['color'] and s['style']==sides[0]['style'] for s in sides) and sides[0]['width']>0:
        side=sides[0];stroke,alpha=color(side['color']);b=side['width']
        rounded_shape(parent,x+b/2,y+b/2,max(0,w-b),max(0,h-b),max(0,radius-b/2),item.get('corner',''),fill='none',stroke=stroke,stroke_width=b,opacity=alpha)
    else:
        positions=[(x,y,x+w,y),(x+w,y,x+w,y+h),(x,y+h,x+w,y+h),(x,y,x,y+h)]
        for side,pos in zip(sides,positions):
            if side['width']>0 and side['style']!='none':
                stroke,alpha=color(side['color']);node('line',parent,x1=pos[0],y1=pos[1],x2=pos[2],y2=pos[3],stroke=stroke,stroke_width=side['width'],opacity=alpha)

def draw_image(item,parent,defs,idx):
    original=ET.parse(ROOT/item['src']).getroot();cid=f'image-clip-{idx}'
    clip=node('clipPath',defs,id=cid);rounded_shape(clip,item['x'],item['y'],item['w'],item['h'],item['radius'],item.get('corner',''))
    group=node('g',parent,clip_path=f'url(#{cid})')
    nested=node('svg',group,x=item['x'],y=item['y'],width=item['w'],height=item['h'],viewBox=original.get('viewBox'),preserveAspectRatio='xMidYMid slice' if item.get('fit')=='cover' else 'xMidYMid meet')
    for child in original:nested.append(copy.deepcopy(child))

source=Path(sys.argv[1])
for name in ['desktop-light','desktop-dark','mobile-light','mobile-dark']:
    data=json.loads((source/f'{name}.json').read_text())
    root=ET.Element(f'{{{SVG}}}svg',{'width':str(data['width']),'height':str(data['height']),'viewBox':f"0 0 {data['width']} {data['height']}",'role':'img','aria-label':f"Azamat portfolio {name}"})
    title=node('title',root);title.text=f"Azamat / {name} / {data['width']}"
    defs=node('defs',root)
    fill,alpha=color(data['background']);node('rect',root,width=data['width'],height=data['height'],fill=fill)
    for i,item in enumerate(data['items']):
        group=node('g',root,id=f"layer-{i:04}-{item['type']}")
        if item['type']=='box':draw_box(item,group)
        elif item['type']=='image':draw_image(item,group,defs,i)
        else:draw_text(item,group)
    output=ROOT/'design'/f'{name}.svg';ET.ElementTree(root).write(output,encoding='utf-8',xml_declaration=True)
    png=cairosvg.svg2png(url=str(output))
    im=Image.open(BytesIO(png)).convert('RGB');im.save(ROOT/'design'/f'{name}.webp','WEBP',quality=90,method=6)
    if name=='desktop-light':
        im.crop((0,0,data['width'],1100)).resize((1000,764)).save(source/'desktop-preview.png')
    if name=='mobile-light':
        im.crop((0,0,data['width'],1400)).save(source/'mobile-preview.png')
    print(f'{name}: {data["width"]} × {data["height"]}, {len(data["items"])} vector layers')
