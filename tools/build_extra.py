# Per-sale pages and character pages. exec'd from build_site.py (shares its globals).
EXTRA_URLS=[]
CHARS=[('Batman',r'\bBatman\b'),('Superman',r'\bSuperman\b'),('Spider-Man',r'Spider-Man|\bSpidey\b'),('X-Men',r'\bX-Men\b'),
 ('Wolverine',r'\bWolverine\b'),('Teenage Mutant Ninja Turtles',r'Teenage Mutant Ninja Turtles'),('Ghost Rider',r'Ghost Rider'),
 ('Uncle Scrooge',r'Uncle Scrooge'),('Green Lantern',r'Green Lantern'),('Doctor Strange',r'\bDr\. Strange\b'),('The Punisher',r'Punisher'),
 ('Sabretooth',r'Sabretooth'),('Silver Surfer',r'Silver Surfer'),('John Constantine',r'Constantine'),('Deathlok',r'Deathlok')]
CH={}
for n,rx in CHARS:
  m=sorted([r for r in S if re.search(rx,r['title'])],key=lambda r:-r['price'])
  if len(m)>=2: CH[n]=m
def rowlist(rows,p):
  return '<ol class="salelist">'+''.join(f'<li><a href="{p}sales/{r["slug"]}/"><span class="sp">{money(r["price"])}</span><span class="st"><b>{e(r["title"])}</b><span class="meta">{e(r["credit"])} · {e(r["publisher"])}, {r["year"]} · {e(r["auction_house"])}, {fdate(r["sale_date"])}</span></span></a></li>' for r in rows)+'</ol>'
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False).replace('</','<\\/')+'</script>'
for r in S:
  p='../../'; lot=r.get('image_credit') or r['source']
  same=[x for x in sorted(by[r['artist']],key=lambda x:-x['price']) if x is not r]
  sim=same[:5]
  if len(sim)<3:
    others=sorted([x for x in S if x is not r and x not in sim],key=lambda x:abs(math.log(x['price']/r['price'])))
    sim+=others[:4-len(sim)]
  simlabel='More by '+e(r['artist']) if same and len(sim)==len(same[:5]) else ('More by '+e(r['artist'])+' &amp; similar prices' if same else 'Sales at similar prices')
  if r.get('image'):
    img=f'<figure class="saleimg"><a href="{e(lot)}"><img src="{p}{r["image"]}" alt="{e(r["credit"]+", "+r["title"])} original art"></a><figcaption>Image: <a href="{e(lot)}">{icred(r)}</a></figcaption></figure>'
  else: img=f'<div class="saleimg noimg"><span>{e(r["page_type"])}</span><small>No image on file</small></div>'
  chs=[n for n in CH if r in CH[n]]
  chh=('<p class="meta">Characters: '+' · '.join(f'<a href="{p}characters/{slug(n)}/">{e(n)}</a>' for n in chs)+'</p>') if chs else ''
  approx='<p class="meta">Sale date is approximate; see <a href="'+p+'about/">methodology</a>.</p>' if r.get('date_approx') else ''
  links=f'<a class="btn" href="{e(r["source"])}">Source: {e(r["source_name"])} →</a>'
  if r.get('image_credit') and r['image_credit']!=r['source']: links=f'<a class="btn" href="{e(r["image_credit"])}">View the original lot →</a>'+links
  b=f'''<section><div class="wrap"><div class="crumbs"><a href="../">← All sales</a></div>
<div class="sale">{img}<div class="saleinfo"><span class="tag2">{e(r["page_type"])}</span><h1>{e(r["title"])}</h1>
<div class="bigprice">{money(r["price"])}</div>
<dl class="facts"><dt>Artist</dt><dd><a href="{p}artists/{slug(r["artist"])}/">{e(r["credit"])}</a></dd><dt>Publisher</dt><dd>{e(r["publisher"])}, {r["year"]}</dd><dt>Sold</dt><dd>{fdate(r["sale_date"])}</dd><dt>Auction house</dt><dd>{e(r["auction_house"])}{(" · "+e(r["auction"])) if r.get("auction") else ""}</dd></dl>
{chh}<div class="lotlinks">{links}</div>{approx}<p class="meta">Price as reported by the source (generally including buyer's premium).</p></div></div>
{sponsor(p)}<h2 class=sub>{simlabel}</h2>{rowlist(sim,p)}</div></section>'''
  t=f'{r["title"]} Original Art Price | {r["artist"]}'
  d=f'{r["credit"]}\'s {r["title"]} ({r["publisher"]}, {r["year"]}) original {r["page_type"].lower()} art sold for {money(r["price"])} at {r["auction_house"]} on {fdate(r["sale_date"])}. Sourced price, lot link and similar sales.'
  og='img/og/default.png'
  if r.get('image'): og=ogimg('s-'+r['slug'][:60]+'-'+str(r['id']),r['image'],e(r['title'][:60]),e(r['credit']),'SOLD',money(r['price']),f"{e(r['auction_house'])}, {fdate(r['sale_date'])}")
  sch={'@context':'https://schema.org','@type':'VisualArtwork','name':r['title'],'artform':'Original comic art','artworkSurface':'Paper','creator':{'@type':'Person','name':r['artist']},'dateCreated':str(r['year']),'publisher':{'@type':'Organization','name':r['publisher']},'url':f'https://comicartindex.com/sales/{r["slug"]}/'}
  if r.get('image'): sch['image']='https://comicartindex.com/'+r['image']
  bc={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'All sales','item':'https://comicartindex.com/sales/'},{'@type':'ListItem','position':2,'name':r['title']}]}
  w(f'sales/{r["slug"]}/index.html',page(t,d,b,2,'All sales',og=og,url=f'sales/{r["slug"]}/',head=ld(sch)+ld(bc),ogtype='article'))
  EXTRA_URLS.append(f'sales/{r["slug"]}/')
cl=''.join(f'<a class="atile" href="{slug(n)}/"><h3>{e(n)}</h3><div class="meta">{len(m)} sales · top {money(m[0]["price"])}</div></a>' for n,m in sorted(CH.items(),key=lambda x:-x[1][0]['price']))
w('characters/index.html',page('Original Comic Art Prices by Character | Comic Art Index',f'Prime Era (1985–1995) original comic art sale prices for {len(CH)} characters, including Batman, Spider-Man, X-Men and the Teenage Mutant Ninja Turtles.',f'<section><div class="wrap"><div class="sh"><h1>Characters:</h1><span class="rule"></span></div><p class="meta">Characters named in the titles of sales in the index, with at least two sales each.</p><div class="grid g3">{cl}</div></div></section>',1,'Characters',url='characters/'))
EXTRA_URLS.append('characters/')
for n,m in CH.items():
  p='../../'
  b=f'''<section><div class="wrap"><div class="crumbs"><a href="../">← All characters</a></div><div class="sh"><h1>{e(n)}</h1><span class="rule"></span></div>
<p class="meta">Prime Era original art sales whose title names {e(n)}, highest price first.</p>
<div class="stats s4"><div><b>{len(m)}</b>sales tracked</div><div><b>{money(m[-1]["price"])}</b>lowest</div><div><b>{money(m[0]["price"])}</b>highest</div><div><b>{money(sum(r["price"] for r in m))}</b>total</div></div>
{sponsor(p)}<h2 class=sub>Sales by price</h2>{rowlist(m,p)}</div></section>'''
  ti=[r for r in m if r.get('image')]
  og=ogimg('c-'+slug(n),ti[0]['image'],e(n),'Original comic art prices',f'{len(m)} SALES',money(m[-1]['price'])+'–'+money(m[0]['price']),e(ti[0]['title'][:60])) if ti else 'img/og/default.png'
  w(f'characters/{slug(n)}/index.html',page(f'{n} Original Comic Art Prices (1985–1995) | Comic Art Index',f'{n} original comic art prices: {len(m)} verified Prime Era auction sales from {money(m[-1]["price"])} to {money(m[0]["price"])}, with links to each sale.',b,2,'Characters',og=og,url=f'characters/{slug(n)}/'))
  EXTRA_URLS.append(f'characters/{slug(n)}/')
print('sales',len(S),'chars',{n:len(m) for n,m in CH.items()})
