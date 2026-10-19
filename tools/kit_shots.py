import asyncio,sys
from playwright.async_api import async_playwright
base=sys.argv[1]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--host-resolver-rules=MAP comicartindex.com 185.199.108.153'])
    for w,h,m in [(390,844,True),(1366,1024,False)]:
      c=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=2 if m else 1,is_mobile=m,has_touch=m)
      async def guard(route):
        if route.request.method!='GET': print(' BLOCKED',route.request.method,route.request.url); await route.abort()
        else: await route.continue_()
      await c.route('**/*',guard)
      pg=await c.new_page(); await pg.goto(base,wait_until='domcontentloaded'); await pg.wait_for_timeout(8000)
      await pg.add_style_tag(content='header.top{position:static!important}'); el=pg.locator('#newsletter'); await el.scroll_into_view_if_needed()
      info=await pg.evaluate('''()=>{const k=document.querySelector('.kit');const f=k.querySelector('form');
        const s=[...k.querySelectorAll('a,button,input,select')].filter(e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0&&b.height<40}).map(e=>e.outerHTML.slice(0,80));
        return {form:!!f,kitH:k.getBoundingClientRect().height,kitW:k.getBoundingClientRect().width,fields:[...k.querySelectorAll('input,button')].map(e=>e.tagName+':'+(e.type||'')+':'+Math.round(e.getBoundingClientRect().height)),small:s,overflow:document.documentElement.scrollWidth>innerWidth+1}}''')
      print(w,info)
      await el.screenshot(path=f'shots/kit-{w}x{h}.png'); await c.close()
    await b.close()
asyncio.run(main())
