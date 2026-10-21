# Накладывает подписи (сейчас русские) и колесо мастерской Уилла на чистую карту presets/maps/clean/. Для английских подписей — поправить список txt(...) ниже. Запуск из корня репо: python3 tools/maplabels.py
from PIL import Image, ImageDraw, ImageFont
import math
im=Image.open('presets/maps/clean/south-saltham-clean-full.jpg').convert('RGBA')
S=2.4
FD='/usr/share/fonts/truetype/freefont/'
def font(sz,b=False): return ImageFont.truetype(FD+('FreeSerifBoldItalic.ttf' if b else 'FreeSerifItalic.ttf'),int(sz*S))
INK=(46,31,20,255);HALO=(244,232,196,255);SEA=(240,232,205,255);SEAH=(30,36,44,255)
def txt(x,y,s,sz=26,b=False,ink=INK,halo=HALO,rot=0,anchor='mm',w=None):
    f=font(sz,b);sw=w if w is not None else max(3,int(sz*S*0.14))
    tmp=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(tmp)
    d.text((x*S,y*S),s,font=f,fill=ink,anchor=anchor,stroke_width=sw,stroke_fill=halo)
    if rot:
        tmp=tmp.rotate(rot,center=(x*S,y*S),resample=Image.BICUBIC)
    im.alpha_composite(tmp)
# water wheel at Will's workshop (west stream, next to red-roofed building by the bridge)
d=ImageDraw.Draw(im)
cx,cy,r=(553*S,628*S,19*S)
for k in range(12):
    a=k*math.pi/6
    d.line([(cx,cy),(cx+r*math.cos(a),cy+r*math.sin(a))],fill=(70,44,26,255),width=int(2.2*S))
    px,py=cx+r*math.cos(a),cy+r*math.sin(a)
    d.line([(px-5*S*math.sin(a),py+5*S*math.cos(a)),(px+5*S*math.sin(a),py-5*S*math.cos(a))],fill=(95,62,38,255),width=int(3.2*S))
d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(40,26,16,255),width=int(2.6*S))
d.ellipse([cx-r*0.82,cy-r*0.82,cx+r*0.82,cy+r*0.82],outline=(110,72,44,255),width=int(2*S))
d.ellipse([cx-4*S,cy-4*S,cx+4*S,cy+4*S],fill=(30,20,12,255))
# labels
txt(1040,548,'Солтхэм',46,True)
txt(905,707,'часовня',20);txt(822,688,'кладбище',18)
txt(1045,724,'рынок',20)
txt(1135,892,'«Якорь»',22)
txt(1560,722,'виноградники',22);txt(1670,425,'виноградники',22)
txt(1385,908,'масличная роща',22)
txt(1812,492,'мельница',22)
txt(920,414,'Длинные полосы',24)
txt(330,478,'опушка Глухолесья',24)
txt(402,350,'пасека',22)
txt(570,375,'Тихий ручей',22,rot=-82)
txt(1708,330,'р. Брин',26,rot=-84)
txt(545,977,'Рыбацкая бухта',26,True)
txt(255,1262,'Чёрные скалы',28,True,ink=SEA,halo=SEAH)
txt(1195,1122,'пристань',24,ink=SEA,halo=SEAH)
txt(1850,1207,'Воронья крепость',30,True,ink=SEA,halo=SEAH)
txt(1850,1243,'дом барона',22,ink=SEA,halo=SEAH)
txt(1020,1300,'Серое море',70,True,ink=(226,222,205,200),halo=(26,30,38,160),w=8)
txt(310,1380,'Солтхэм и окрестности',34,True,ink=(60,36,22,255),halo=(240,228,190,0),w=0)
txt(150,818,'← к Лисьей бухте',22)
txt(960,252,'↑ на юг, через лес — в Эшфорд',22)
txt(1855,850,'к крепости барона →',20)
txt(1740,1408,'десять минут пешком',20,ink=SEA,halo=SEAH)
im=im.convert('RGB')
im.save('/tmp/labeled.png')
im.resize((2400,int(2400*im.size[1]/im.size[0])),Image.LANCZOS).save('/tmp/labeled_2400.jpg',quality=90)
im.resize((1600,int(1600*im.size[1]/im.size[0])),Image.LANCZOS).save('/tmp/view.png')
