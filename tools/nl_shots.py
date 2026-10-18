import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--host-resolver-rules=MAP comicartindex.com 185.199.108.153'])
    for w,h,m in [(390,844,True),(430,932,True),(1366,1024,False)]:
      c=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=2 if m else 1,is_mobile=m,has_touch=m)
      pg=await c.new_page(); await pg.goto('https://comicartindex.com/',wait_until='networkidle'); await pg.wait_for_timeout(5000)
      el=pg.locator('#newsletter'); await el.scroll_into_view_if_needed()
      info=await pg.evaluate('''()=>{const n=document.querySelector('#newsletter .bh');const f=n.querySelector('iframe,form,input');
       const small=[...document.querySelectorAll('a,button,input,select')].filter(e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0&&b.height<40&&getComputedStyle(e).display!='inline'}).map(e=>e.textContent.trim().slice(0,30)||e.tagName);
       return {bhHeight:n.getBoundingClientRect().height,embed:f?f.tagName+' '+(f.src||'').slice(0,60):null,overflow:document.documentElement.scrollWidth>innerWidth+1,small,header:document.querySelector('header.top').getBoundingClientRect().height}}''')
      print(w,h,info)
      if w!=430: await el.screenshot(path=f'shots/newsletter-{w}x{h}.png')
      await c.close()
    await b.close()
asyncio.run(main())
