import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--host-resolver-rules=MAP comicartindex.com 185.199.108.153'])
    for w,h,m in [(390,844,True),(1366,1024,False)]:
      c=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=2 if m else 1,is_mobile=m,has_touch=m)
      posted=[]
      async def rt(route):
        posted.append(route.request.post_data); await route.fulfill(status=200,body='ok')
      await c.route('https://subscribe-forms.beehiiv.com/api/submit',rt)
      pg=await c.new_page(); await pg.goto('https://comicartindex.com/',wait_until='networkidle')
      el=pg.locator('#newsletter'); await el.scroll_into_view_if_needed()
      info=await pg.evaluate('''()=>{const s=[...document.querySelectorAll('a,button,input,select')].filter(e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0&&b.height<40&&getComputedStyle(e).display!='inline'}).map(e=>e.outerHTML.slice(0,60));
        const f=document.querySelector('form.nl').getBoundingClientRect();return {overflow:document.documentElement.scrollWidth>innerWidth+1,small:s,formW:f.width,inputH:document.querySelector('#nl-email').getBoundingClientRect().height,btnH:document.querySelector('form.nl button').getBoundingClientRect().height}}''')
      print(w,info)
      await el.screenshot(path=f'shots/newsletter-native-{w}x{h}.png')
      await pg.fill('#nl-email','mock@example.com'); await pg.click('form.nl button'); await pg.wait_for_timeout(1200)
      print(' posted(mocked):',posted, 'thanks visible:',await pg.locator('.nl-thanks').is_visible())
      await el.screenshot(path=f'shots/newsletter-native-thanks-{w}x{h}.png')
      await c.close()
    await b.close()
asyncio.run(main())
