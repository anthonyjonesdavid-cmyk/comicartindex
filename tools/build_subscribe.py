# Subscribe landing page. exec'd from build_site.py (shares its globals).
# Sample issue uses the five highest sales from sent Issue #1 (Heritage #7470,
# Sept 25-27, 2026). Prices, titles, and images are read from sales.json.
_by_slug = {r['slug']: r for r in S}
_issue1 = [
    'x-men-6-psylocke-and-sabretooth-cover-jim-lee',
    'teenage-mutant-ninja-turtles-50-city-at-war-wraparound-cover-peter-laird',
    'the-crow-4-cover-painting-james-o-barr',
    'mad-289-batman-cover-richard-williams',
    'x-men-9-blue-team-story-page-1-jim-lee',
]
missing = [s for s in _issue1 if s not in _by_slug]
if missing:
    raise SystemExit('subscribe sample sales missing from sales.json: ' + ', '.join(missing))
sample = [_by_slug[s] for s in _issue1]
for r in sample:
    if not r.get('image'):
        raise SystemExit('subscribe sample sale has no image: ' + r['slug'])
top = sample[0]
lot = top.get('image_credit') or top['source']
p = '../'

def _sample_list(rows, p):
    o = '<ol class="salelist">'
    for r in rows:
        th = (
            f'<img class="sth" src="{p}{r["image"]}" alt="{e(r["credit"]+", "+r["title"])} original art">'
            if r.get('image') else '<span class="sth noimg"></span>'
        )
        o += (
            f'<li><a href="{p}sales/{r["slug"]}/">{th}'
            f'<span class="sp">{money(r["price"])}</span>'
            f'<span class="st"><b>{e(r["title"])}</b>'
            f'<span class="meta">{e(r["credit"])} · {e(r["publisher"])}, {r["year"]}</span>'
            f'</span></a></li>'
        )
    return o + '</ol>'

feat = (
    f'<article class="ifeat">'
    f'<a class="ifeatimg" href="{p}sales/{top["slug"]}/">'
    f'<img src="{p}{top["image"]}" alt="{e(top["credit"]+", "+top["title"])} original art"></a>'
    f'<div class="ifeattxt"><div class="price">{money(top["price"])}</div>'
    f'<h3><a href="{p}sales/{top["slug"]}/">{e(top["title"])}</a></h3>'
    f'<p class="meta"><a href="{p}artists/{slug(top["artist"])}/">{e(top["credit"])}</a>'
    f' · {e(top["publisher"])}, {top["year"]}</p>'
    f'<p class="meta">Sold {e(top["auction_house"])}, {fdate(top["sale_date"])}</p>'
    f'<p class="credit">Image: <a href="{e(lot)}">{icred(top)}</a></p>'
    f'<a class="view" href="{p}sales/{top["slug"]}/">See the sale page →</a>'
    f'</div></article>'
)

sog = ogimg(
    'subscribe',
    top['image'],
    'Every Friday',
    'The free newsletter',
    'FREE',
    'Sign up',
    e(top['credit']) + ' · ' + e(top['title']),
)

sub = f'''<div class="hero subhero"><div class="wrap"><div class="herotxt">
<h1>Great art.<br><span>Real prices.</span><br>Every Friday.</h1>
<p>The free weekly Comic Art Index newsletter. Each Friday issue covers the week&#x27;s biggest 1985–1995 original art sales, with prices, links to the lots, and one deep dive.</p></div>
<div class="kitbox" id="signup">{kitform(p)}<p class="kitnote">Free. One email every Friday. Unsubscribe anytime.</p></div></div></div>
<section><div class="wrap">
<div class="sh"><h2>What&#x27;s in each issue:</h2><span class="rule"></span></div>
<ul class="gets"><li>The week&#x27;s top Prime Era (1985–1995) original comic art sales</li><li>Verified prices and a link to every lot</li><li>One deep dive on an artist, sale, or market pattern</li></ul>
<div class="issueltr">
<div class="ih"><small>A sample issue</small><p>Issue #1 · Heritage Auctions #7470, Sept 25–27, 2026</p><h2>Jim Lee&#x27;s X-Men #6 cover just sold for {money(top["price"])}</h2></div>
<div class="ibody">
<p class="ilead">Issue #1 looked back at Heritage&#x27;s Comic Art Signature Auction, where these were the five biggest Prime Era sales. Every price and image is from the index, and each one links to its sale page.</p>
{feat}
<h3 class="sub">The rest of the top five</h3>
{_sample_list(sample[1:], p)}
<p class="allsales"><a class="more" href="{p}sales/">Browse all sales on Comic Art Index →</a></p>
</div></div>
</div></section>'''

w(
    'subscribe/index.html',
    page(
        'Subscribe · Comic Art Index',
        'Free Friday newsletter of the week’s biggest 1985–1995 original comic art sales, with verified prices and links to every lot.',
        sub,
        1,
        'Free newsletter',
        og=sog,
        url='subscribe/',
        band=False,
    ),
)
print('subscribe page', [r['title'] for r in sample], [money(r['price']) for r in sample])
