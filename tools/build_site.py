import json,re,os,html,math,datetime
R='/workspace/comicartindex'
S=json.load(open(f'{R}/data/sales.json'))
e=html.escape
def money(p): return '$'+format(int(round(p)),',') if p==int(p) else '$'+format(p,',.2f')
def slug(n): return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
def fdate(d):
  return datetime.date.fromisoformat(d).strftime('%b %-d, %Y')
FEATURED=['Jim Lee','Todd McFarlane','Frank Miller','Rob Liefeld','Dan Jurgens','Arthur Adams','Sam Kieth','Mike Mignola','Bill Sienkiewicz','John Romita Jr.','George Perez','Ron Lim']
by={}
for r in S: by.setdefault(r['artist'],[]).append(r)
def page(title,desc,body,depth,cur=''):
  p='../'*depth
  nav=[('Home',''),('All sales','sales/'),('Artists','artists/'),('Top 25','sales/#top'),('About','about/'),('Newsletter','#newsletter')]
  navh=''.join(f'<a href="{p}{u}"{" aria-current=page" if cur==n else ""}>{n}</a>' for n,u in nav)
  return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#111111"><title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bangers&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/style.css"></head><body>
<header class="top"><div class="wrap"><a class="logo" href="{p}">Comic Art Index</a><nav class="main" aria-label="Main">{navh}</nav></div></header>
{body}
<section class="news dots" id="newsletter" style="background-color:var(--red)"><div class="wrap">
<h2>What sold this week, every Friday</h2>
<p>The week's biggest prime-era sales in a free weekly email.</p>
<div class="bh"><script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" data-beehiiv-form="7ed33c32-9771-46cb-b14b-cb6623312101"></script></div>
<p class="fallback">Form not loading? <a href="https://subscribe-forms.beehiiv.com/v3/forms/7ed33c32-9771-46cb-b14b-cb6623312101">Subscribe on Beehiiv →</a></p>
</div></section>
<footer><div class="wrap">© 2026 Comic Art Index · Prices are public auction results (generally including buyer's premium) as reported by the linked sources. Artwork © its creators and publishers; thumbnails credited to and linked to Heritage Auctions. Not affiliated with any auction house or publisher. <a href="{p}about/">Methodology &amp; sources</a></div></footer>
<script type="text/javascript" async src="https://subscribe-forms.beehiiv.com/attribution.js"></script>
</body></html>'''
def card(r,p):
  if r.get('image'):
    th=f'<div class="thumb"><img loading="lazy" src="{p}{r["image"]}" alt="{e(r["credit"]+" "+r["title"])} original art"></div>'
    ic=f'<br>Image: <a href="{r["image_credit"]}">Heritage Auctions</a>'
  else: th=f'<div class="thumb noimg">{e(r["page_type"])}</div>'; ic=''
  return f'''<div class="card">{th}<div class="body"><div class="price">{money(r["price"])}</div><div><b><a href="{p}artists/{slug(r["artist"])}/">{e(r["credit"])}</a></b></div><div class="meta">{e(r["title"])} · {e(r["publisher"])}, {r["year"]}</div><div class="cap">Sold {e(r["auction_house"])}, {fdate(r["sale_date"])} · <a href="{e(r["source"])}">{e(r["source_name"])}</a>{ic}</div></div></div>'''
def table(rows,p,rank=False,tid=''):
  h=f'<div class="tablewrap"><table class="board"{" id="+tid if tid else ""}><thead><tr>{"<th>#</th>" if rank else ""}<th>Artwork</th><th class="hide-s">Type</th><th class="hide-s">Sold</th><th>Price</th></tr></thead><tbody>'
  for i,r in enumerate(rows):
    h+=f'<tr>{f"<td class=rank>{i+1}</td>" if rank else ""}<td><b><a href="{p}artists/{slug(r["artist"])}/">{e(r["credit"])}</a></b><br>{e(r["title"])} <span class="meta">({e(r["publisher"])}, {r["year"]})</span><div class="meta">{e(r["auction_house"])} · <a href="{e(r["source"])}">source</a></div></td><td class="hide-s">{e(r["page_type"])}</td><td class="hide-s">{fdate(r["sale_date"])}</td><td class="num">{money(r["price"])}</td></tr>'
  return h+'</tbody></table></div>'
def chart(rows):
  W,H,pl,pb=640,280,64,34
  ds=[datetime.date.fromisoformat(r['sale_date']).toordinal() for r in rows]
  lo,hi=min(ds),max(ds)
  if lo==hi: lo-=365;hi+=365
  ps=[math.log10(r['price']) for r in rows]; pmin=math.floor(min(ps)); pmax=math.ceil(max(ps))
  if pmin==pmax: pmax+=1
  X=lambda d:pl+(d-lo)/(hi-lo)*(W-pl-20); Y=lambda v:H-pb-(v-pmin)/(pmax-pmin)*(H-pb-14)
  g=''
  for k in range(pmin,pmax+1):
    y=Y(k); lab=money(10**k).replace(',000,000','M').replace(',000','K')
    g+=f'<line x1="{pl}" x2="{W-10}" y1="{y:.1f}" y2="{y:.1f}" stroke="#ddd"/><text x="{pl-6}" y="{y+4:.1f}" font-size="12" text-anchor="end">{lab}</text>'
  y0=datetime.date.fromordinal(lo).year; y1=datetime.date.fromordinal(hi).year
  for yr in sorted(set([y0,y1]+list(range(y0,y1+1,max(1,(y1-y0)//4 or 1))))):
    d=datetime.date(yr,1,1).toordinal()
    if lo<=d<=hi: g+=f'<text x="{X(d):.1f}" y="{H-10}" font-size="12" text-anchor="middle">{yr}</text>'
  pts=''.join(f'<circle cx="{X(d):.1f}" cy="{Y(v):.1f}" r="7" fill="#e23b2e" stroke="#111" stroke-width="2"><title>{e(r["title"])}: {money(r["price"])} ({fdate(r["sale_date"])})</title></circle>' for d,v,r in zip(ds,ps,rows))
  return f'<div class="chart"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Sale prices over time (log scale)">{g}{pts}</svg><div class="cap">Each dot is one sale. Price axis is logarithmic.</div></div>'
def w(path,s):
  os.makedirs(os.path.dirname(f'{R}/{path}'),exist_ok=True); open(f'{R}/{path}','w').write(s)
total=sum(r['price'] for r in S)
recent=sorted(S,key=lambda r:(r['sale_date'],r['price']),reverse=True)[:8]
withimg=[r for r in S if r.get('image')]
herof=''.join(f'<figure><img src="{r["image"]}" alt="{e(r["credit"]+" "+r["title"])}"><figcaption><b>{e(r["credit"])}</b>, {e(r["title"])} ({e(r["publisher"])}, {r["year"]})<br><b>{money(r["price"])}</b> · {fdate(r["sale_date"])}<br>Image: <a href="{r["image_credit"]}">Heritage Auctions</a></figcaption></figure>' for r in [withimg[0],[x for x in withimg if 'Uncanny X-Men #271' in x['title']][0]])
tiles=''
for a in FEATURED:
  if a not in by: continue
  rs=by[a]; top=max(rs,key=lambda r:r['price'])
  tiles+=f'<a class="card" href="artists/{slug(a)}/"><h3>{e(a)}</h3><div class="meta">{len(rs)} sale{"s" if len(rs)>1 else ""} tracked · top {money(top["price"])}</div><div class="meta">{e(top["title"])}</div></a>'
home=f'''<div class="hero dots"><div class="wrap"><div>
<h1>What 80s &amp; 90s comic art<br><span>actually sells for</span></h1>
<p>Free, sourced sale prices for original comic pages and covers from the prime era (1985–1995). {len(S)} verified sales and counting, totaling {money(round(total))}.</p>
<form class="search" role="search" onsubmit="event.preventDefault();location.href='sales/?q='+encodeURIComponent(this.q.value)"><input name="q" id="q" placeholder="Try “Jim Lee”, “Spider-Man”, “cover”" aria-label="Search sales" autocomplete="off"><button>Search</button></form>
<div id="hits" class="cap" style="margin-top:12px"></div></div>
<div class="herothumbs">{herof}</div></div></div>
<section><div class="wrap"><h2>Recent big sales</h2><div class="grid g4">{"".join(card(r,"") for r in recent[:4])}</div></div></section>
<section class="dots" style="background-color:#fff1c9"><div class="wrap"><h2>Browse by artist</h2><div class="grid g3 tiles">{tiles}</div>
<p><a class="btn" href="artists/">All {len(by)} artists →</a></p></div></section>
<section><div class="wrap"><h2>All-time top 10</h2>{table(S[:10],"",rank=True)}
<p><a class="btn" href="sales/">See all {len(S)} sales →</a></p></div></section>
<script>
const P=location.pathname.replace(/[^/]*$/,'');let D=null;const q=document.getElementById('q'),h=document.getElementById('hits');
q.addEventListener('input',async()=>{{if(!D)D=await (await fetch('data/sales.json')).json();const t=q.value.trim().toLowerCase();if(t.length<2){{h.innerHTML='';return}}
const m=D.filter(r=>[r.artist,r.credit,r.title,r.publisher,r.page_type,String(r.year)].join(' ').toLowerCase().includes(t));
h.innerHTML='<b>'+m.length+' match'+(m.length==1?'':'es')+'</b>'+m.slice(0,5).map(r=>'<div style="padding:6px 0;border-top:1px solid #0002"><b>$'+Math.round(r.price).toLocaleString()+'</b> · '+r.credit+' · '+r.title+'</div>').join('')+(m.length>5?'<div><a href="sales/?q='+encodeURIComponent(q.value)+'">See all '+m.length+' →</a></div>':'')}});
</script>'''
w('index.html',page('Comic Art Index · What prime-era comic art sells for','Free, sourced sale prices for 1985–1995 original comic art: Jim Lee, Todd McFarlane, Frank Miller, Rob Liefeld and more.',home,0,'Home'))
types=sorted(set(r['page_type'] for r in S))
sales=f'''<section><div class="wrap"><h1 style="font-size:40px;margin:0 0 8px">All sales</h1><p class="meta">Every verified 1985–1995 original art sale in the index, with a link to the source we checked.</p>
<div class="filters"><input id="f" placeholder="Search artist, book, publisher…" aria-label="Search"><select id="t" aria-label="Type"><option value="">All types</option>{"".join(f"<option>{e(x)}</option>" for x in types)}</select><select id="o" aria-label="Sort"><option value="p">Highest price</option><option value="d">Newest sale</option><option value="y">Art year</option></select></div>
<p class="count" id="n"></p><div id="tbl">{table(S,"../")}</div>
<h2 id="top" style="margin-top:36px">Top 25 all time</h2>{table(S[:25],"../",rank=True)}</div></section>
<script>
const D={json.dumps([[r['artist'],r['credit'],r['title'],r['publisher'],r['page_type'],r['year'],r['price'],r['sale_date'],r['auction_house'],r['source']] for r in S],ensure_ascii=False)};
const f=document.getElementById('f'),t=document.getElementById('t'),o=document.getElementById('o'),n=document.getElementById('n'),tb=document.getElementById('tbl');
const es=s=>String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);const sl=s=>s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const fd=d=>new Date(d+'T12:00:00').toLocaleDateString('en-US',{{month:'short',day:'numeric',year:'numeric'}});
function go(){{const q=f.value.trim().toLowerCase();let m=D.filter(r=>(!t.value||r[4]==t.value)&&(!q||r.slice(0,6).join(' ').toLowerCase().includes(q)));
m.sort((a,b)=>o.value=='p'?b[6]-a[6]:o.value=='d'?b[7].localeCompare(a[7]):a[5]-b[5]);n.textContent=m.length+' sale'+(m.length==1?'':'s')+' · $'+Math.round(m.reduce((s,r)=>s+r[6],0)).toLocaleString()+' total';
tb.innerHTML='<div class="tablewrap"><table class="board"><thead><tr><th>Artwork</th><th class="hide-s">Type</th><th class="hide-s">Sold</th><th>Price</th></tr></thead><tbody>'+m.map(r=>'<tr><td><b><a href="../artists/'+sl(r[0])+'/">'+es(r[1])+'</a></b><br>'+es(r[2])+' <span class="meta">('+es(r[3])+', '+r[5]+')</span><div class="meta">'+es(r[8])+' · <a href="'+es(r[9])+'">source</a></div></td><td class="hide-s">'+es(r[4])+'</td><td class="hide-s">'+fd(r[7])+'</td><td class="num">$'+r[6].toLocaleString()+'</td></tr>').join('')+'</tbody></table></div>'}}
f.value=new URLSearchParams(location.search).get('q')||'';[f,t,o].forEach(x=>x.addEventListener('input',go));go();
</script>'''
w('sales/index.html',page('All sales · Comic Art Index','Searchable table of verified prime-era original comic art sales.',sales,1,'All sales'))
arts=sorted(by,key=lambda a:-sum(r['price'] for r in by[a]))
al=''.join(f'<a class="card" href="{slug(a)}/"><h3>{e(a)}</h3><div class="meta">{len(by[a])} sale{"s" if len(by[a])>1 else ""} · top {money(max(r["price"] for r in by[a]))}</div></a>' for a in arts)
w('artists/index.html',page('Artists · Comic Art Index','Prime-era comic artists with tracked original art sales.',f'<section><div class="wrap"><h1 style="font-size:40px;margin:0 0 16px">Artists</h1><div class="grid g3 tiles">{al}</div></div></section>',1,'Artists'))
for a in arts:
  rs=sorted(by[a],key=lambda r:-r['price'])
  b=f'''<section><div class="wrap"><div class="crumbs"><a href="../">← All artists</a></div><h1 style="font-size:44px;margin:4px 0 12px">{e(a)}</h1>
<div class="stats"><div><b>{len(rs)}</b>sales tracked</div><div><b>{money(rs[0]["price"])}</b>top sale</div><div><b>{money(sum(r["price"] for r in rs))}</b>total</div></div>
<h2>Price chart</h2>{chart(rs)}
<h2 style="margin-top:28px">Sales</h2>{"<div class='grid g4' style='margin-bottom:20px'>"+"".join(card(r,"../../") for r in rs if r.get("image"))+"</div>" if any(r.get("image") for r in rs) else ""}{table(rs,"../../")}</div></section>'''
  w(f'artists/{slug(a)}/index.html',page(f'{a} original art sale prices · Comic Art Index',f'Verified public sales of {a} original comic art from 1985–1995.',b,2,'Artists'))
srcs={}
for r in S: srcs.setdefault(r['source'],[r['source_name'],0]); srcs[r['source']][1]+=1
sl_=''.join(f'<li><a href="{e(u)}">{e(n)}</a> — {c} sale{"s" if c>1 else ""}<br><span class="meta">{e(u)}</span></li>' for u,(n,c) in sorted(srcs.items(),key=lambda x:-x[1][1]))
about=f'''<section><div class="wrap prose"><h1 style="font-size:44px;margin:0 0 12px">About &amp; methodology</h1>
<p><b>Comic Art Index</b> is a free price guide for original comic art from the "prime era," roughly 1985 to 1995: the years of Frank Miller's Dark Knight, Todd McFarlane's Spider-Man, Jim Lee's X-Men and the early Image boom.</p>
<h2>What counts</h2><ul><li>Original art (covers, interior pages, splashes, spreads) created between 1985 and 1995.</li><li>Sales that were publicly reported, with the price, the venue, and a date.</li><li>Every row links to the page we checked when adding it. No estimated, asking, or invented prices.</li></ul>
<h2>How prices are reported</h2><ul><li>Auction prices are shown as reported by the source. Heritage and ComicConnect results generally include the buyer's premium.</li><li>Rows from Heritage auction #7470 (Sept 25–27, 2026) are dated to the auction's closing day; the exact session day for each lot may differ by a day or two.</li><li>The Uncanny X-Men #268 cover sale is dated to the CBR report (Dec 4, 2020).</li><li>The Dark Knight Returns Joker spread is dated to Heritage's Oct 6–8, 2023 event.</li></ul>
<h2>Images</h2><p>We show only a few small, credited thumbnails, each linked to its Heritage Auctions listing. All artwork is © its creators and publishers.</p>
<h2>Sources ({len(srcs)})</h2><ul>{sl_}</ul>
<h2>Data</h2><p>The full dataset is available as <a href="../data/sales.json">sales.json</a> ({len(S)} rows). Spot a missing sale or an error? Corrections are welcome.</p></div></section>'''
w('about/index.html',page('About & methodology · Comic Art Index','How Comic Art Index sources and verifies prime-era comic art sale prices.',about,1,'About'))
print(len(S),len(arts))
