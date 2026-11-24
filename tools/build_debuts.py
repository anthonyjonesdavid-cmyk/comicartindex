# First appearances index page. exec'd from build_site.py (shares its globals,
# and runs after build_extra.py, so `ld` is available).
# Data: data/debuts.json — one group per debut issue. Each group lists the
# tracked sales in data/sales.json of original art from that issue, by sale id.
# The builder refuses to build if a listed sale's title does not name the
# group's issue, so the page can never claim a sale belongs to the wrong book.
DEBUTS = json.load(open(f'{R}/data/debuts.json'))
_by_id = {r['id']: r for r in S}
p = '../'
groups = ''
for g in DEBUTS:
    rows = []
    for i in g['sale_ids']:
        r = _by_id.get(i)
        if r is None:
            raise SystemExit(f"debuts.json: sale id {i} not in sales.json")
        if g['match'].lower() not in r['title'].lower():
            raise SystemExit(f"debuts.json: sale id {i} title {r['title']!r} does not name {g['match']!r}")
        rows.append(r)
    rows = sorted(rows, key=lambda r: -r['price'])
    if rows:
        stats = (
            f'<div class="stats s4"><div><b>{len(rows)}</b>sale{"s" if len(rows) > 1 else ""} tracked</div>'
            f'<div><b>{money(rows[-1]["price"])}</b>lowest</div>'
            f'<div><b>{money(rows[0]["price"])}</b>highest</div>'
            f'<div><b>{money(sum(r["price"] for r in rows))}</b>total</div></div>'
        )
        listing = f'<div class="grid g4">{"".join(card(r, p) for r in rows)}</div>'
    else:
        stats = ''
        listing = '<p class="meta">No sales of original art from this issue are tracked yet.</p>'
    groups += (
        f'<h2 class="sub">{e(g["character"])}</h2>'
        f'<p class="meta"><b>{e(g["debut"])}</b> · {e(g["issue"])} · {e(g["publisher"])}, {g["year"]}</p>'
        f'<p>{e(g["note"])}</p>'
        f'{stats}{listing}'
    )
body = (
    '<section><div class="wrap"><div class="sh"><h1>First appearances:</h1><span class="rule"></span></div>'
    '<p class="meta">Landmark Prime Era debut issues, and the original art from them that the index tracks. '
    'Every price is a verified public auction result, linked to the source we checked.</p>'
    + groups +
    '</div></section>'
)
bc = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://comicartindex.com/'},
    {'@type': 'ListItem', 'position': 2, 'name': 'First appearances'}]}
w('first-appearances/index.html', page(
    'First Appearances · Comic Art Index',
    'First-appearance issues tracked by Comic Art Index: Deadpool in The New Mutants #98, John Constantine in The Saga of the Swamp Thing #37, and Carrie Kelley in Batman: The Dark Knight Returns #1 — with verified auction prices for original art from each issue.',
    body, 1, 'First appearances', url='first-appearances/', head=ld(bc)))
EXTRA_URLS.append('first-appearances/')
print('first appearances', [(g['character'], g['sale_ids']) for g in DEBUTS])
