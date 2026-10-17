import re,html,json
RBH="https://www.rarebookhub.com/auctions/auction_detail?id=51635&size=500"
t=open('/workspace/comicartindex/raw/rbh.html').read()
rows=[]
EXCL=re.compile(r'Far Side|Playmates|Masters of the Universe|circa|c\. 19|Calendar|Trading Card|Concept Illustration|Character Study')
def ptype(s):
  s2=s.lower()
  if 'complete' in s2 and 'story' in s2: return 'Complete story'
  if 'double-page' in s2 or 'gatefold' in s2: return 'Double-page spread'
  if 'cover' in s2 and 'back cover' not in s2: return 'Cover'
  if 'splash' in s2: return 'Splash page'
  if 'illustration' in s2 or 'back cover' in s2: return 'Illustration'
  return 'Interior page'
def credit_and_book(title,authors):
  words=[w for a in authors for w in re.split(r'[ ;]+',a) if len(w)>1]
  end=0
  for w in words:
    i=title.find(w,0,90)
    if i>=0: end=max(end,i+len(w))
  cr=title[:end].strip(); bk=title[end:].strip(' -')
  m=re.match(r'\(([^)]*)\)\s*(.*)',bk)
  if m: cr+=' ('+m.group(1)+')'; bk=m.group(2)
  return cr,bk
for r in re.findall(r'<tr.*?</tr>',t,re.S):
  c=[html.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)]
  if len(c)<7 or not c[6].startswith('USD'): continue
  lot,auth,title,_,yr,_,price=c[:7]
  if not re.fullmatch(r'19(8[5-9]|9[0-5])',yr) or EXCL.search(title): continue
  authors=[a.strip() for a in auth.split(';') if a.strip()]
  cr,bk=credit_and_book(title,authors)
  m=re.search(r'\(([^,()]+), (\d{4})\)\.?$',bk); pub=m.group(1) if m else ''
  book=re.sub(r'\s*Original Art.*$','',bk).strip()
  primary=re.split(r' and |, | - | \(',cr)[0].strip()
  rows.append(dict(artist=primary,credit=cr,title=book,publisher=pub,page_type=ptype(title),year=int(yr),
    price=float(price.replace('USD','').replace(',','')),sale_date='2026-09-27',auction_house='Heritage Auctions',
    auction=f'Comic Art Signature Auction #7470, lot {lot} (Sept 25–27, 2026)',source=RBH,source_name='Rare Book Hub (Heritage #7470 results)'))
CAT="https://comicarttracker.com/auctions/top-prices"
BC1="https://bleedingcool.com/comics/one-page-of-jim-lee-x-men-art-sold-for-over-1-3-of-a-million-last-week/"
H=[
("Frank Miller","Frank Miller & Lynn Varley","Batman: The Dark Knight Returns #1","DC","Cover",1986,2400000,"2022-06-16","Heritage Auctions",CAT,"ComicArtTracker top prices"),
("Dan Jurgens","Dan Jurgens","Superman #75 (Death of Superman)","DC","Cover",1992,1874673,"2026-04-13","ComicConnect",CAT,"ComicArtTracker top prices"),
("Rob Liefeld","Rob Liefeld","The New Mutants #98 (first Deadpool) Story Page 14","Marvel","Interior page",1991,960000,"2024-11-22","Heritage Auctions",CAT,"ComicArtTracker top prices"),
("Dan Jurgens","Dan Jurgens","Superman #75 Pages 25, 27–28 Triple Gatefold Splash","DC","Double-page spread",1992,828115,"2026-04-13","ComicConnect",CAT,"ComicArtTracker top prices"),
("Dan Jurgens","Dan Jurgens","Superman #75 Page 26 Splash","DC","Splash page",1992,797332,"2026-04-13","ComicConnect",CAT,"ComicArtTracker top prices"),
("Todd McFarlane","Todd McFarlane","Batman #423","DC","Cover",1988,781250,"2025-10-17","Heritage Auctions",CAT,"ComicArtTracker top prices"),
("Todd McFarlane","Todd McFarlane","The Amazing Spider-Man #328","Marvel","Cover",1990,657250,"2012-07-26","Heritage Auctions","https://bleedingcool.com/comics/todd-mcfarlane-amazing-spider-man-328-original-cover-art-sells-for-record-675250/","Bleeding Cool"),
("Todd McFarlane","Todd McFarlane","Spider-Man #1","Marvel","Cover",1990,358500,"2012-07-26","Heritage Auctions","https://archive.nytimes.com/artsbeat.blogs.nytimes.com/2012/07/27/collector-sense-tingling-comic-book-sale-yields-powerful-prices/","New York Times"),
("Frank Miller","Frank Miller & Klaus Janson","Batman: The Dark Knight Returns (Joker's death) Two-Page Sequence","DC","Double-page spread",1986,550000,"2023-10-07","Heritage Auctions","https://www.overstreetaccess.com/frank-miller-dark-knight-returns-pages-reach-550k-at-heritage/","Overstreet Access"),
("Frank Miller","Frank Miller & Klaus Janson","Batman: The Dark Knight Returns #3 Page 10 (Batman & Robin splash)","DC","Splash page",1986,448125,"2011-05-05","Heritage Auctions","https://icv2.com/articles/comics/view/20019/miller-page-goes-448-125","ICv2"),
("Frank Miller","Frank Miller & Klaus Janson","Batman: The Dark Knight Returns (Carrie Kelley as Robin) Story Page","DC","Interior page",1986,288000,"2024-11-22","Heritage Auctions","https://artdaily.com/news/175930/Deadpool-s-debut-slices-up-the-record-books-as-Rob-Liefeld-s-original-art-from--New-Mutants--No--98-sells-for--960-000-","Artdaily (Heritage release)"),
("Jim Lee","Jim Lee & Scott Williams","The Uncanny X-Men #271 Story Page 4","Marvel","Interior page",1990,360000,"2022-04-08","Heritage Auctions",BC1,"Bleeding Cool"),
("Jim Lee","Jim Lee & Scott Williams","The Uncanny X-Men #268","Marvel","Cover",1990,300000,"2020-12-04","Heritage Auctions","https://www.cbr.com/jim-lee-uncanny-x-men-original-art-auctioned-300k/","CBR"),
("Jim Lee","Jim Lee & Scott Williams","The Uncanny X-Men #274 Savage Land Double-Page Spread 2–3","Marvel","Double-page spread",1991,180000,"2022-04-08","Heritage Auctions",BC1,"Bleeding Cool"),
("Jim Lee","Jim Lee","Wolverine #24","Marvel","Cover",1990,144000,"2022-04-08","Heritage Auctions",BC1,"Bleeding Cool"),
]
for a,cr,b,p,pt,y,pr,d,h,s,sn in H:
  rows.append(dict(artist=a,credit=cr,title=b,publisher=p,page_type=pt,year=y,price=float(pr),sale_date=d,auction_house=h,auction='',source=s,source_name=sn,date_approx=(sn=='CBR')))
IMG={("The Uncanny X-Men #271 Story Page 4"):("img/lee-uxm-271-p4.jpg","https://www.ha.com/itm/original-comic-art/jim-lee-and-scott-williams-uncanny-x-men-271-story-page-4-original-art-marvel-1990-/a/7270-94121.s"),
 "Batman #423":("img/mcfarlane-batman-423-cover.jpg","https://comics.ha.com/itm/original-comic-art/covers/todd-mcfarlane-batman-423-cover-original-art-dc-1988-/a/7443-94047.s"),
 "The Uncanny X-Men #274 Savage Land Double-Page Spread 2–3":("img/lee-uxm-274-dps.jpg","https://www.ha.com/itm/original-comic-art/jim-lee-and-scott-williams-uncanny-x-men-274-double-page-spread-2-3-savage-land-original-art-marvel-1991-/a/7270-91037.s"),
 "Wolverine #24":("img/lee-wolverine-24-cover.jpg","https://www.ha.com/itm/original-comic-art/jim-lee-wolverine-24-cover-original-art-marvel-1990-/a/7270-91036.s")}
for i,r in enumerate(sorted(rows,key=lambda r:-r['price'])):
  r['id']=i+1
  if r['title'] in IMG: r['image'],r['image_credit']=IMG[r['title']]
rows.sort(key=lambda r:-r['price'])
json.dump(rows,open('/workspace/comicartindex/data/sales.json','w'),indent=1,ensure_ascii=False)
print(len(rows)); import collections; print(collections.Counter(r['artist'] for r in rows).most_common(15))
for r in rows[:5]+rows[-3:]: print(r['credit'],'|',r['title'],'|',r['page_type'],r['price'])
