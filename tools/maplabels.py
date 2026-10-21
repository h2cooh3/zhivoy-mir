# Накладывает подписи (сейчас русские) и колесо мастерской Уилла на чистую карту presets/maps/clean/.
# Запуск из корня репо: python3 tools/maplabels.py   → /tmp/labeled_2400.jpg (положить в presets/maps/south-saltham.jpg)
# Для английских подписей — поправить список txt(...) внизу. Шрифты (Google Fonts, OFL): Ruslan Display — заголовки, Cormorant SC Bold — мелкие подписи.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
SRC='presets/maps/clean/south-saltham-clean-full.jpg'
im=Image.open(SRC).convert('RGBA'); S=im.size[0]/2000
F={'title':'tools/fonts/RuslanDisplay.ttf','small':'tools/fonts/CormorantSC-Bold.ttf'}
FALL='/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf'  # знаки препинания и стрелки, которых нет в шрифтах
def runs(s,fk,sz):
    main=ImageFont.truetype(F[fk],int(sz*S));fb=ImageFont.truetype(FALL,int(sz*S));cm=main.getmask
    out=[]
    for ch in s:
        ok=ch==' ' or (ord(ch)>=0x400 and ord(ch)<=0x4FF) or ch.isdigit()
        out.append((ch,main if ok else fb))
    return out
def width(r): return sum(f.getlength(c) for c,f in r)
CREAM=(244,232,196);INK=(40,26,16);SEAINK=(238,230,205);SEADK=(18,24,32)
def txt(x,y,s,sz=30,fk='small',kind='land',rot=0,track=0):
    r=runs(s,fk,sz);w=width(r)+track*S*(len(s)-1);h=int(sz*S*1.5)
    pad=int(sz*S*0.9);W=int(w+2*pad);H=h+2*pad
    mask=Image.new('L',(W,H),0);d=ImageDraw.Draw(mask);cx=pad
    for c,f in r:
        d.text((cx,H//2),c,font=f,fill=255,anchor='lm');cx+=f.getlength(c)+track*S
    k=int(sz*S*0.22)|1
    glow=mask.filter(ImageFilter.MaxFilter(k*2+1 if k*2+1<=61 else 61)).filter(ImageFilter.GaussianBlur(sz*S*0.18))
    ink,gl,ga=((INK,CREAM,230) if kind=='land' else (SEAINK,SEADK,215))
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    layer.paste(Image.new('RGBA',(W,H),gl+(255,)),(0,0),glow.point(lambda v:int(v*ga/255)))
    edge=mask.filter(ImageFilter.MaxFilter(5)).point(lambda v:v)
    layer.paste(Image.new('RGBA',(W,H),gl+(255,)),(0,0),edge)
    layer.paste(Image.new('RGBA',(W,H),ink+(255,)),(0,0),mask)
    if rot: layer=layer.rotate(rot,expand=True,resample=Image.BICUBIC)
    im.alpha_composite(layer,(int(x*S-layer.size[0]/2),int(y*S-layer.size[1]/2)))
# колесо мастерской Уилла на западном ручье
d=ImageDraw.Draw(im);cx,cy,r=(553*S,628*S,19*S)
for k in range(12):
    a=k*math.pi/6;px,py=cx+r*math.cos(a),cy+r*math.sin(a)
    d.line([(cx,cy),(px,py)],fill=(70,44,26,255),width=int(2.2*S))
    d.line([(px-5*S*math.sin(a),py+5*S*math.cos(a)),(px+5*S*math.sin(a),py-5*S*math.cos(a))],fill=(95,62,38,255),width=int(3.2*S))
d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(40,26,16,255),width=int(2.6*S))
d.ellipse([cx-r*.82,cy-r*.82,cx+r*.82,cy+r*.82],outline=(110,72,44,255),width=int(2*S))
d.ellipse([cx-4*S,cy-4*S,cx+4*S,cy+4*S],fill=(30,20,12,255))
# ---- подписи ----
txt(1040,545,'Солтхэм',58,'title',track=2)
txt(910,712,'часовня',30);txt(815,690,'кладбище',28)
txt(1045,728,'рынок',30)
txt(1135,897,'Якорь',32)
txt(1560,728,'виноградники',32);txt(1670,430,'виноградники',32)
txt(1385,915,'масличная роща',32)
txt(1812,500,'мельница',32)
txt(920,414,'Длинные полосы',34)
txt(300,472,'опушка Глухолесья',34)
txt(402,352,'пасека',32)
txt(600,330,'Тихий ручей',30,rot=-82)
txt(1705,300,'река Брин',32,rot=-84)
txt(545,985,'Рыбацкая бухта',36,'title')
txt(255,1275,'Чёрные скалы',42,'title',kind='sea')
txt(1195,1125,'пристань',34,kind='sea')
txt(1745,1215,'Воронья крепость',36,'title',kind='sea')
txt(1745,1255,'дом барона',32,kind='sea')
txt(1020,1310,'Серое море',92,'title',kind='sea',track=6)
txt(310,1380,'Солтхэм и окрестности',36,'title',kind='land')
txt(165,822,'← к Лисьей бухте',32)
txt(960,252,'↑ на юг, через лес, в Эшфорд',32)
txt(1845,858,'к крепости барона →',30)
txt(1740,1415,'десять минут пешком',30,kind='sea')
im=im.convert('RGB')
im.resize((2400,int(2400*im.size[1]/im.size[0])),Image.LANCZOS).save('/tmp/labeled_2400.jpg',quality=90)
im.resize((1600,int(1600*im.size[1]/im.size[0])),Image.LANCZOS).save('/tmp/view.png')
