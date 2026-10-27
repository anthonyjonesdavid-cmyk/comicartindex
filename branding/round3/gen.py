import subprocess
H='''<html><head><style>body{margin:0;width:900px;height:600px;overflow:hidden;font-family:Anton}
.dots{background-image:radial-gradient(%s 28%%,transparent 30%%);background-size:14px 14px}</style></head><body>%s</body></html>'''
D={}
# A extruded 3D block
ext=",".join(f"{i}px {i}px 0 #e23b2e" for i in range(1,14))+",14px 14px 0 #111,18px 20px 0 #111"
D['A-extruded-3d']=H%('rgba(17,17,17,.18)',f'''<div class="dots" style="background-color:#ffd23f;width:900px;height:600px;display:flex;align-items:center;justify-content:center">
<div style="transform:perspective(600px) rotateX(18deg) skewX(-8deg);text-align:center;line-height:.9">
<div style="font-size:150px;color:#f7f1e3;-webkit-text-stroke:4px #111;text-shadow:{ext};letter-spacing:4px">COMIC ART</div>
<div style="font-size:190px;color:#f7f1e3;-webkit-text-stroke:5px #111;text-shadow:{ext};letter-spacing:22px">INDEX</div></div></div>''')
# B chrome jagged
D['B-chrome-90s']=H%('rgba(255,210,63,.15)','''<svg width="900" height="600" xmlns="http://www.w3.org/2000/svg"><defs>
<linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".45" stop-color="#9aa3ad"/><stop offset=".5" stop-color="#2b2a26"/><stop offset=".62" stop-color="#cfd6dd"/><stop offset="1" stop-color="#ffd23f"/></linearGradient></defs>
<rect width="900" height="600" fill="#2b2a26"/>
<polygon points="40,120 200,60 330,110 470,40 600,100 760,50 870,130 830,250 880,380 720,470 560,430 420,560 300,470 120,520 60,380 20,260" fill="#e23b2e" stroke="#111" stroke-width="8"/>
<g font-family="Anton" text-anchor="middle" stroke="#111" stroke-width="6" paint-order="stroke" transform="skewX(-12) translate(60,0)">
<text x="450" y="270" font-size="150" fill="url(#c)" letter-spacing="6">COMIC ART</text>
<text x="450" y="440" font-size="190" fill="url(#c)" letter-spacing="24">INDEX</text></g>
<polygon points="700,450 860,520 690,500" fill="#ffd23f" stroke="#111" stroke-width="4"/></svg>''')
# C corner box
D['C-corner-box']=H%('rgba(17,17,17,.2)','''<div class="dots" style="background-color:#f7f1e3;width:900px;height:600px;display:flex;align-items:center;justify-content:center">
<div style="display:flex;border:6px solid #111;background:#fff;box-shadow:12px 12px 0 #111">
<div style="width:230px;border-right:6px solid #111;text-align:center;font-family:Anton">
<div style="background:#e23b2e;color:#fff;font-size:30px;padding:8px">PRIME ERA</div>
<div style="font-size:30px;padding-top:10px">No.</div><div style="font-size:120px;line-height:1">01</div>
<div style="background:#111;color:#ffd23f;font-size:30px;padding:6px">OCT</div>
<div style="font-size:40px;padding:10px">$1.25 US</div>
<div style="font-size:18px;border-top:4px solid #111;padding:6px">$1.75 CAN</div></div>
<div style="background:#ffd23f;padding:30px 40px;font-family:Anton;line-height:.9">
<div style="font-size:120px;color:#111;text-shadow:6px 6px 0 #e23b2e">COMIC</div>
<div style="font-size:120px;color:#111;text-shadow:6px 6px 0 #e23b2e">ART</div>
<div style="font-size:120px;color:#e23b2e;text-shadow:6px 6px 0 #111">INDEX</div>
<div style="font-size:22px;letter-spacing:3px;margin-top:12px">COMICARTINDEX.COM</div></div></div></div>''')
# D code seal
D['D-code-seal']=H%('rgba(17,17,17,.15)','''<svg width="900" height="600" xmlns="http://www.w3.org/2000/svg"><rect width="900" height="600" fill="#f7f1e3"/>
<g transform="translate(250,300)"><path d="M-150,-180 H150 V40 Q150,140 0,190 Q-150,140 -150,40 Z" fill="#fff" stroke="#111" stroke-width="10"/>
<rect x="-150" y="-180" width="300" height="70" fill="#111"/>
<text y="-130" text-anchor="middle" font-family="Anton" font-size="40" fill="#ffd23f">APPROVED</text>
<text y="-50" text-anchor="middle" font-family="Anton" font-size="34" fill="#111">BY THE</text>
<text y="20" text-anchor="middle" font-family="Anton" font-size="62" fill="#e23b2e">COMIC ART</text>
<text y="80" text-anchor="middle" font-family="Anton" font-size="62" fill="#e23b2e">INDEX</text>
<text y="135" text-anchor="middle" font-family="Anton" font-size="18" fill="#111">AUTHORITY</text></g>
<g font-family="Anton" fill="#111"><text x="480" y="230" font-size="64">1985–1995</text><text x="480" y="320" font-size="64" fill="#e23b2e">ORIGINAL</text><text x="480" y="410" font-size="64">ART</text>
<text x="480" y="460" font-size="22" letter-spacing="2">COMICARTINDEX.COM</text></g></svg>''')
# E banner ribbon
D['E-banner-ribbon']=H%('rgba(255,210,63,.18)','''<svg width="900" height="600" xmlns="http://www.w3.org/2000/svg"><rect width="900" height="600" fill="#2b2a26"/>
<polygon points="20,330 110,330 80,380 110,430 20,430" fill="#8c1f17" stroke="#111" stroke-width="5"/>
<polygon points="880,330 790,330 820,380 790,430 880,430" fill="#8c1f17" stroke="#111" stroke-width="5"/>
<path d="M90,290 Q450,250 810,290 L810,410 Q450,370 90,410 Z" fill="#e23b2e" stroke="#111" stroke-width="7"/>
<text x="450" y="375" text-anchor="middle" font-family="Anton" font-size="86" fill="#ffd23f" stroke="#111" stroke-width="4" paint-order="stroke" letter-spacing="8">COMIC ART INDEX</text>
<text x="450" y="200" text-anchor="middle" font-family="Bangers" font-size="54" fill="#f7f1e3" letter-spacing="4">THE PRIME ERA PRICE GUIDE</text>
<text x="450" y="480" text-anchor="middle" font-family="Anton" font-size="28" fill="#ffd23f" letter-spacing="6">★ LAST WEEK'S TOP AUCTIONS ★</text></svg>''')
# F Ben-Day pop burst
D['F-benday-burst']=H%('#e23b2e','''<div class="dots" style="background-color:#ffd23f;width:900px;height:600px;position:relative">
<svg width="900" height="600" style="position:absolute" xmlns="http://www.w3.org/2000/svg">
<polygon points="450,30 520,150 660,70 640,210 820,190 700,300 850,410 680,420 720,560 570,470 450,580 360,470 190,560 230,420 50,410 200,300 80,190 260,210 240,70 380,150" fill="#f7f1e3" stroke="#111" stroke-width="8"/>
<g font-family="Bangers" text-anchor="middle" fill="#111" transform="rotate(-6 450 300)">
<text x="450" y="290" font-size="120" fill="#e23b2e" stroke="#111" stroke-width="5" paint-order="stroke">COMIC ART</text>
<text x="450" y="410" font-size="140" stroke="#ffd23f" stroke-width="0">INDEX!</text></g></svg></div>''')
for k,v in D.items():
    open(k+'.html','w').write(v)
    subprocess.run(['google-chrome','--headless','--no-sandbox','--hide-scrollbars','--window-size=900,600',f'--screenshot={k}.png',k+'.html'],capture_output=True)
from PIL import Image,ImageDraw,ImageFont
ks=list(D);S=Image.new('RGB',(1860,1950),'#111');f=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Anton/Anton-Regular.ttf',44)
for i,k in enumerate(ks):
    x=20+(i%2)*920;y=20+(i//2)*650
    S.paste(Image.open(k+'.png').convert('RGB'),(x,y+50));ImageDraw.Draw(S).text((x,y-4),k.replace('-',' ',1).upper(),fill='#ffd23f',font=f)
S.save('sheet.png')
