import json,re,os,html,math,datetime
R='/workspace/comicartindex'
S=json.load(open(f'{R}/data/sales.json'))
HI=json.load(open(f'{R}/data/heritage_images.json'))
for r in S:
  if r['title'] in HI and not r.get('image'): r['image'],r['image_credit']=HI[r['title']]
def _sl(n): return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
_seen=set()
for r in S:
  b=_sl(r['title']+' '+r['artist'])[:90].strip('-'); k=b
  if k in _seen: k=f"{b}-{r['id']}"
  _seen.add(k); r['slug']=k
json.dump(S,open(f'{R}/data/sales.json','w'),indent=1,ensure_ascii=False)
def sh(t,link='',lt='',tag='h2'): return f'<div class="sh"><{tag}>{t}</{tag}><span class="rule"></span>'+(f'<a class="more" href="{link}">{lt} →</a>' if link else '')+'</div>'
e=html.escape
from og import ogimg
XH='DavidJonesXacct'
def sponsor(p): return f'<aside class="sponsor"><span>Sponsor</span><b>Your gallery here. Reach Prime Era collectors.</b><a href="{p}advertise/">Advertise →</a></aside>'
def money(p): return '$'+format(int(round(p)),',') if p==int(p) else '$'+format(p,',.2f')
def slug(n): return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
def fdate(d):
  return datetime.date.fromisoformat(d).strftime('%b %-d, %Y')
FEATURED=['Jim Lee','Todd McFarlane','Frank Miller','Rob Liefeld','Dan Jurgens','Arthur Adams','Sam Kieth','Mike Mignola','Bill Sienkiewicz','John Romita Jr.','George Perez','Ron Lim']
by={}
for r in S: by.setdefault(r['artist'],[]).append(r)
def page(title,desc,body,depth,cur='',og='img/og/default.png',url='',head='',ogtype='website'):
  p='../'*depth
  nav=[('Home',''),('All sales','sales/'),('Artists','artists/'),('Characters','characters/'),('Years','years/'),('About','about/'),('Free newsletter','#newsletter')]
  navh=''.join(f'<a href="{"" if u.startswith("#") else p}{u}"{" aria-current=page" if cur==n else ""}{" class=nl" if u.startswith("#") else ""}>{n}</a>' for n,u in nav)
  return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#111111"><title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta property="og:type" content="{ogtype}"><link rel="canonical" href="https://comicartindex.com/{url}"><meta property="og:site_name" content="Comic Art Index"><meta property="og:url" content="https://comicartindex.com/{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="https://comicartindex.com/{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="https://comicartindex.com/{og}">{head}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" sizes="32x32" href="{p}img/stamp-icon-32.png"><link rel="icon" type="image/png" sizes="512x512" href="{p}img/stamp-icon-512.png"><link rel="apple-touch-icon" href="{p}img/stamp-icon-180.png"><link rel="stylesheet" href="{p}assets/style.css?v=10"></head><body>
<header class="top"><div class="wrap"><a class="logo" href="{p}"><img src="{p}img/stamp-logo-128.png" alt="" width="36" height="36"><span>Comic Art Index</span></a><nav class="main" aria-label="Main">{navh}</nav></div></header>
<main>{body}</main>
<section class="band" id="newsletter"><div class="wrap">
<div class="bandtxt"><h2>Great art. <span>Real prices.</span> Every Friday.</h2>
<p>Each free Friday issue covers the week's biggest 1985–1995 original art sales, with prices, links to the lots, and one deep dive.</p></div>
<div class="kit"><script async data-uid="5e118f0c3a" src="https://unique-painter-8002.kit.com/5e118f0c3a/index.js"></script></div>
</div></section>
<footer><div class="wrap">© 2026 Comic Art Index · Prices are public auction results (generally including buyer's premium) as reported by the linked sources. Artwork © its creators and publishers; images credited to and linked to the auction house that sold them (Heritage Auctions or Hake&#x27;s). Not affiliated with any auction house or publisher. <a href="{p}about/">Methodology &amp; sources</a> · <a href="{p}advertise/">Advertise</a></div></footer>
</body></html>'''
def icred(r): return "Hake&#x27;s" if r.get('auction_house')=="Hake's" else 'Heritage Auctions (HA.com)'
def card(r,p):
  lot=r.get('image_credit') or r['source']
  if r.get('image'):
    th=f'<a class="thumb" href="{e(lot)}"><img loading="lazy" src="{p}{r["image"]}" alt="{e(r["credit"]+", "+r["title"])} original art"></a><div class="credit">Image: <a href="{e(lot)}">{icred(r)}</a></div>'
  else: th=f'<div class="thumb noimg">{e(r["page_type"])}</div>'
  return f'''<article class="card"><span class="tag">{e(r["page_type"])}</span>{th}<div class="body"><div class="price">{money(r["price"])}</div><h3><a href="{p}sales/{r["slug"]}/">{e(r["title"])}</a></h3><div class="meta"><a href="{p}artists/{slug(r["artist"])}/">{e(r["credit"])}</a> · {e(r["publisher"])}, {r["year"]}</div><div class="meta">Sold {e(r["auction_house"])}, {fdate(r["sale_date"])}</div><a class="view" href="{e(lot)}">View sale →</a></div></article>'''
def table(rows,p,rank=False,tid=''):
  h=f'<div class="tablewrap"><table class="board"{" id="+tid if tid else ""}><thead><tr>{"<th>#</th>" if rank else ""}<th>Artwork</th><th class="hide-s">Type</th><th class="hide-s">Sold</th><th>Price</th></tr></thead><tbody>'
  for i,r in enumerate(rows):
    h+=f'<tr>{f"<td class=rank>{i+1}</td>" if rank else ""}<td><b><a href="{p}artists/{slug(r["artist"])}/">{e(r["credit"])}</a></b><br><a href="{p}sales/{r["slug"]}/">{e(r["title"])}</a> <span class="meta">({e(r["publisher"])}, {r["year"]})</span><div class="meta">{e(r["auction_house"])} · <a href="{e(r["source"])}">source</a></div></td><td class="hide-s">{e(r["page_type"])}</td><td class="hide-s">{fdate(r["sale_date"])}</td><td class="num">{money(r["price"])}</td></tr>'
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
pol=[x for x in withimg if x['image'].startswith('img/ha-7470-')][:2]
herof=''.join(f'<figure class="pol p{i}"><a href="{e(r["image_credit"])}"><img src="{r["image"]}" alt="{e(r["credit"]+", "+r["title"])} original art"></a><figcaption>{money(r["price"])} · {e(r["title"])}<br><small>Image: {icred(r)}</small></figcaption></figure>' for i,r in enumerate(pol))
pills=''.join(f'<a class="pill" href="artists/{slug(a)}/">{e(a)}</a>' for a in FEATURED if a in by)
home=f'''<div class="hero"><div class="wrap"><div class="herotxt">
<h1>What 80s &amp; 90s <span>comic art</span> actually sells for.</h1>
<p>Sourced auction results for original art from 1985–1995. {len(S)} verified sales, {money(round(total))} total.</p>
<form class="search" role="search" action="sales/" onsubmit="event.preventDefault();location.href='sales/?q='+encodeURIComponent(this.q.value)"><input name="q" id="q" type="search" placeholder="Search by artist, title, year…" aria-label="Search sales" autocomplete="off"><button>Search</button></form>
<div id="hits" class="hits"></div>
<a class="sample" href="#newsletter">Get the free Friday issue →</a></div>
<div class="pols">{herof}</div></div></div>
<section><div class="wrap">{sh("Recent sales:","sales/?o=d","View all sales")}<div class="grid g4">{"".join(card(r,"") for r in recent[:4])}</div></div></section>
<section><div class="wrap">{sh("Browse by artist:","artists/","View all artists")}<div class="pills">{pills}</div></div></section>
<section><div class="wrap">{sh("All-time top 10:","sales/#top","Top 25")}{table(S[:10],"",rank=True)}</div></section>
<script>
const P=location.pathname.replace(/[^/]*$/,'');let D=null;const q=document.getElementById('q'),h=document.getElementById('hits');
q.addEventListener('input',async()=>{{if(!D)D=await (await fetch('data/sales.json')).json();const t=q.value.trim().toLowerCase();if(t.length<2){{h.innerHTML='';return}}
const m=D.filter(r=>[r.artist,r.credit,r.title,r.publisher,r.page_type,String(r.year)].join(' ').toLowerCase().includes(t));
h.innerHTML='<b>'+m.length+' match'+(m.length==1?'':'es')+'</b>'+m.slice(0,5).map(r=>'<div class=hit><a href="sales/'+r.slug+'/"><b>$'+Math.round(r.price).toLocaleString()+'</b> · '+r.credit+' · '+r.title+'</a></div>').join('')+(m.length>5?'<div><a href="sales/?q='+encodeURIComponent(q.value)+'">See all '+m.length+' →</a></div>':'')}});
</script>'''
ld=max(r['sale_date'] for r in S); lo_=(datetime.date.fromisoformat(ld)-datetime.timedelta(days=6)).isoformat()
wk=sorted([r for r in S if lo_<=r['sale_date']<=ld and r.get('image')],key=lambda r:-r['price'])
hog=ogimg('home',wk[0]['image'],"This week's #1 sale",'Prime Era original art, 1985–1995','#1',money(wk[0]['price']),f"{wk[0]['credit']} · {wk[0]['title']}<br>{wk[0]['auction_house']}, {fdate(wk[0]['sale_date'])} · {len(S)} sales tracked") if wk else 'img/og/default.png'
w('index.html',page('Comic Art Index · What prime-era comic art sells for','Free, sourced sale prices for 1985–1995 original comic art: Jim Lee, Todd McFarlane, Frank Miller, Rob Liefeld and more.',home,0,'Home',og=hog))
types=sorted(set(r['page_type'] for r in S))
sales=f'''<section><div class="wrap"><div class="sh"><h1>All sales:</h1><span class="rule"></span></div><p class="meta">Every verified 1985–1995 original art sale in the index, with a link to the source we checked.</p>
<div class="filters"><input id="f" placeholder="Search artist, book, publisher…" aria-label="Search"><select id="t" aria-label="Type"><option value="">All types</option>{"".join(f"<option>{e(x)}</option>" for x in types)}</select><select id="o" aria-label="Sort"><option value="p">Highest price</option><option value="d">Newest sale</option><option value="y">Art year</option></select></div>
{sponsor("../")}<p class="count" id="n"></p><div id="tbl">{table(S,"../")}</div>
<div class="sh" id="top"><h2>Top 25 all time:</h2><span class="rule"></span></div>{table(S[:25],"../",rank=True)}</div></section>
<script>
const D={json.dumps([[r['artist'],r['credit'],r['title'],r['publisher'],r['page_type'],r['year'],r['price'],r['sale_date'],r['auction_house'],r['source'],r['slug']] for r in S],ensure_ascii=False)};
const f=document.getElementById('f'),t=document.getElementById('t'),o=document.getElementById('o'),n=document.getElementById('n'),tb=document.getElementById('tbl');
const es=s=>String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);const sl=s=>s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const fd=d=>new Date(d+'T12:00:00').toLocaleDateString('en-US',{{month:'short',day:'numeric',year:'numeric'}});
function go(){{const q=f.value.trim().toLowerCase();let m=D.filter(r=>(!t.value||r[4]==t.value)&&(!q||r.slice(0,6).join(' ').toLowerCase().includes(q)));
m.sort((a,b)=>o.value=='p'?b[6]-a[6]:o.value=='d'?b[7].localeCompare(a[7]):a[5]-b[5]);n.textContent=m.length+' sale'+(m.length==1?'':'s')+' · $'+Math.round(m.reduce((s,r)=>s+r[6],0)).toLocaleString()+' total';
tb.innerHTML='<div class="tablewrap"><table class="board"><thead><tr><th>Artwork</th><th class="hide-s">Type</th><th class="hide-s">Sold</th><th>Price</th></tr></thead><tbody>'+m.map(r=>'<tr><td><b><a href="../artists/'+sl(r[0])+'/">'+es(r[1])+'</a></b><br><a href="'+r[10]+'/">'+es(r[2])+'</a> <span class="meta">('+es(r[3])+', '+r[5]+')</span><div class="meta">'+es(r[8])+' · <a href="'+es(r[9])+'">source</a></div></td><td class="hide-s">'+es(r[4])+'</td><td class="hide-s">'+fd(r[7])+'</td><td class="num">$'+r[6].toLocaleString()+'</td></tr>').join('')+'</tbody></table></div>'}}
const U=new URLSearchParams(location.search);f.value=U.get('q')||'';if(U.get('o'))o.value=U.get('o');[f,t,o].forEach(x=>x.addEventListener('input',go));go();
</script>'''
w('sales/index.html',page('All sales · Comic Art Index','Searchable table of verified prime-era original comic art sales.',sales,1,'All sales',url='sales/'))
arts=sorted(by,key=lambda a:-sum(r['price'] for r in by[a]))
al=''.join(f'<a class="atile" href="{slug(a)}/"><h3>{e(a)}</h3><div class="meta">{len(by[a])} sale{"s" if len(by[a])>1 else ""} · top {money(max(r["price"] for r in by[a]))}</div></a>' for a in arts)
w('artists/index.html',page('Original Comic Art Prices by Artist | Comic Art Index',f'Original comic art sale prices for {len(arts)} artists of the 1985–1995 prime era, from verified public auction results.',f'<section><div class="wrap"><div class="sh"><h1>Artists:</h1><span class="rule"></span></div><div class="grid g3">{al}</div></div></section>',1,'Artists',url='artists/'))
for a in arts:
  rs=sorted(by[a],key=lambda r:-r['price'])
  b=f'''<section><div class="wrap"><div class="crumbs"><a href="../">← All artists</a></div><div class="sh"><h1>{e(a)}</h1><span class="rule"></span></div>
<div class="stats s4"><div><b>{len(rs)}</b>sale{"s" if len(rs)>1 else ""} tracked</div><div><b>{money(rs[-1]["price"])}</b>lowest</div><div><b>{money(rs[0]["price"])}</b>highest</div><div><b>{money(sum(r["price"] for r in rs))}</b>total</div></div>
{sponsor('../../')}<h2 class=sub>Price chart</h2>{chart(rs)}
<h2 class=sub>Sales</h2>{"<div class='grid g4' style='margin-bottom:20px'>"+"".join(card(r,"../../") for r in rs if r.get("image"))+"</div>" if any(r.get("image") for r in rs) else ""}{table(rs,"../../")}</div></section>'''
  ti=[r for r in rs if r.get('image')]
  aog=ogimg('a-'+slug(a),ti[0]['image'],e(a),'Original comic art prices',f'{len(rs)} SALE'+('S' if len(rs)>1 else ''),money(rs[0]['price']) if len(rs)==1 else money(rs[-1]['price'])+'–'+money(rs[0]['price']),e(ti[0]['title'])+f" · {ti[0]['auction_house']}, {fdate(ti[0]['sale_date'])}") if ti else 'img/og/default.png'
  w(f'artists/{slug(a)}/index.html',page(f'{a} Original Comic Art Prices | Comic Art Index',f'{a} original comic art prices: {len(rs)} verified auction sale{"s" if len(rs)>1 else ""} from 1985–1995 work, '+(f'ranging {money(rs[-1]["price"])} to {money(rs[0]["price"])}' if len(rs)>1 else f'sold for {money(rs[0]["price"])}')+', with links to each lot.',b,2,'Artists',og=aog,url=f'artists/{slug(a)}/'))
srcs={}
for r in S: srcs.setdefault(r['source'],[r['source_name'],0]); srcs[r['source']][1]+=1
sl_=''.join(f'<li><a href="{e(u)}">{e(n)}</a> — {c} sale{"s" if c>1 else ""}<br><span class="meta">{e(u)}</span></li>' for u,(n,c) in sorted(srcs.items(),key=lambda x:-x[1][1]))
about=f'''<section><div class="wrap prose"><div class="sh"><h1>About &amp; methodology</h1><span class="rule"></span></div>
<p><b>Comic Art Index</b> is a free price guide for original comic art from the "prime era," roughly 1985 to 1995: the years of Frank Miller's Dark Knight, Todd McFarlane's Spider-Man, Jim Lee's X-Men and the early Image boom.</p>
<h2>What counts</h2><ul><li>Original art (covers, interior pages, splashes, spreads) created between 1985 and 1995.</li><li>Sales that were publicly reported, with the price, the venue, and a date.</li><li>Every row links to the page we checked when adding it. No estimated, asking, or invented prices.</li></ul>
<h2>How prices are reported</h2><ul><li>Auction prices are shown as reported by the source. Heritage and ComicConnect results generally include the buyer's premium.</li><li>Rows from Heritage auction #7470 (Sept 25–27, 2026) are dated to the auction's closing day; the exact session day for each lot may differ by a day or two.</li><li>The Uncanny X-Men #268 cover sale is dated to the CBR report (Dec 4, 2020).</li><li>The Dark Knight Returns Joker spread is dated to Heritage's Oct 6–8, 2023 event.</li></ul>
<h2>Images</h2><p>We show only small, credited thumbnails, each credited to and linked to its auction listing at Heritage Auctions (HA.com) or Hake&#x27;s. All artwork is © its creators and publishers.</p>
<h2>Sources ({len(srcs)})</h2><ul>{sl_}</ul>
<h2>Data</h2><p>The full dataset is available as <a href="../data/sales.json">sales.json</a> ({len(S)} rows). Spot a missing sale or an error? Corrections are welcome.</p></div></section>'''
w('about/index.html',page('About & methodology · Comic Art Index','How Comic Art Index sources and verifies prime-era comic art sale prices.',about,1,'About',url='about/'))
adv=f'''<section><div class="wrap prose"><div class="sh"><h1>Advertise with Comic Art Index</h1><span class="rule"></span></div>
<p>Comic Art Index tracks verified auction prices for 1985–1995 ("Prime Era") original comic art, and sends a free newsletter every Friday with the week's top sales.</p>
<h2>Who reads it</h2><ul><li>Collectors of original pages, covers and splashes from 1985–1995</li><li>Buyers researching what an artist's work actually sells for before they bid</li><li>Dealers and consignors watching the market week to week</li></ul>
<p class="meta">We're new and growing. We'd rather tell you that than quote numbers we don't have.</p>
<h2>Available spots</h2><ul><li><b>Newsletter sponsor:</b> one slim sponsor box in the Friday issue.</li><li><b>Site sponsor box:</b> a slim "Sponsor" box on the sales and artist pages.</li><li><b>Artist page sponsor:</b> your box on the page for the artist you deal in.</li></ul>
<p class="meta">One sponsor per spot, always clearly labeled "Sponsor". Sponsors never affect prices or rankings.</p>
<h2>Get in touch</h2><p>Email <a href="mailto:hello@comicartindex.com">hello@comicartindex.com</a> or message us on X at <a href="https://x.com/{XH}">@{XH}</a>. You can also subscribe to the free newsletter below and reply to any issue.</p></div></section>'''
w('advertise/index.html',page('Advertise · Comic Art Index','Sponsor spots on Comic Art Index and its free Friday newsletter, reaching collectors of 1985–1995 original comic art.',adv,1,url='advertise/'))
exec(open(f'{R}/tools/build_extra.py').read())
B='https://comicartindex.com/'
urls=['','sales/','artists/','about/','advertise/']+[f'artists/{slug(a)}/' for a in arts]+EXTRA_URLS
open(f'{R}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{B}{u}</loc></url>\n' for u in urls)+'</urlset>\n')
open(f'{R}/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {B}sitemap.xml\n')
print(len(S),len(arts))
