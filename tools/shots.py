import sys,asyncio
from playwright.async_api import async_playwright
base=sys.argv[1]; pre=sys.argv[2]
sizes=[(390,844,True),(430,932,True),(1024,1366,True),(1366,1024,False)]
pages=['', 'sales/', 'artists/jim-lee/', 'about/']
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--host-resolver-rules=MAP comicartindex.com 185.199.108.153'])
    for w,h,m in sizes:
      c=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=2 if m else 1,is_mobile=m,has_touch=m)
      pg=await c.new_page()
      for u in pages:
        await pg.goto(base+u,wait_until='domcontentloaded');await pg.wait_for_timeout(2500)
        name=f"shots/{pre}{(u.strip('/').replace('/','-') or 'home')}-{w}x{h}.png"
        await pg.screenshot(path=name)
        # checks
        r=await pg.evaluate('''()=>{const sw=document.documentElement.scrollWidth>innerWidth+1;
          const small=[...document.querySelectorAll('a,button,input,select')].filter(e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0&&b.height<40&&getComputedStyle(e).display!='inline'}).map(e=>e.textContent.trim().slice(0,30)||e.tagName);
          const hb=document.querySelector('header.top').getBoundingClientRect().height;return {overflow:sw,small:small.slice(0,6),header:hb}}''')
        print(name,r)
      await c.close()
    await b.close()
asyncio.run(main())
