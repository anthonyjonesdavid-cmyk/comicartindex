import os,hashlib,subprocess,tempfile
R='/workspace/comicartindex'
def ogimg(key,img,title,sub,tile,price,meta,root=R):
  out=f'img/og/{key}.png'
  h=f'''<html><head><link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;800&display=swap" rel="stylesheet"><style>
body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#f7f1e3;font-family:Inter;display:flex}}
.art{{width:520px;height:630px;background:#111 url(file://{root}/{img}) center/cover;border-right:10px solid #111}}
.t{{flex:1;padding:44px 48px;display:flex;flex-direction:column;border:10px solid #111;border-left:0}}
.brand{{font-family:Anton;font-style:italic;text-transform:uppercase;font-size:28px;background:#111;color:#ffd23f;align-self:flex-start;padding:6px 14px}}
h1{{font-family:Anton;font-style:italic;font-weight:400;text-transform:uppercase;font-size:80px;line-height:.95;margin:28px 0 6px}}
.sub{{font-size:28px;font-weight:800;text-transform:uppercase}}.price{{margin-top:auto;display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
.tile{{background:#e23b2e;color:#fff;border:5px solid #111;font-family:Anton;font-size:56px;padding:2px 18px}}.p{{font-family:Anton;font-size:56px}}
.m{{font-size:22px;margin-top:12px}}.url{{font-weight:800;color:#e23b2e;font-size:22px;margin-top:8px}}</style></head><body><div class=art></div><div class=t><div class=brand>Comic Art Index</div>
<h1>{title}</h1><div class=sub>{sub}</div><div class=price><span class=tile>{tile}</span><span class=p>{price}</span></div><div class=m>{meta}</div><div class=url>comicartindex.com</div></div></body></html>'''
  dig=hashlib.md5(h.encode()).hexdigest(); stamp=f'{root}/img/og/.{key}.md5'
  os.makedirs(f'{root}/img/og',exist_ok=True)
  if os.path.exists(f'{root}/{out}') and os.path.exists(stamp) and open(stamp).read()==dig: return out
  with tempfile.NamedTemporaryFile('w',suffix='.html',delete=False) as f: f.write(h)
  subprocess.run(['google-chrome','--headless=new','--no-sandbox','--hide-scrollbars','--allow-file-access-from-files','--window-size=1200,630','--virtual-time-budget=4000',f'--screenshot={root}/{out}','file://'+f.name],capture_output=True,timeout=60)
  os.unlink(f.name); open(stamp,'w').write(dig); return out
