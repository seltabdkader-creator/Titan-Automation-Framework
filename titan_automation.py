import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import random

class TitanAutomation:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def launch_browser(self, headless=True):
        print("🚀 تشغيل المتصفح...")
        pw = await async_playwright().start()
        self.browser = await pw.chromium.launch(headless=headless)
        
        # إعداد وضع التخفي
        stealth = Stealth()
        
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = await self.context.new_page()
        
        # تطبيق التخفي على الصفحة
        await stealth.apply_stealth_async(self.page)
        
        print("✅ تم تشغيل المتصفح بنجاح مع وضع التخفي.")

    async def navigate(self, url):
        print(f"🌐 الانتقال إلى: {url}")
        await self.page.goto(url, wait_until="networkidle")
        print(f"✅ تم الدخول إلى: {await self.page.title()}")

    async def human_like_scroll(self):
        print("⬇️ التمرير بشكل يحاكي الإنسان...")
        scroll_height = await self.page.evaluate("document.body.scrollHeight")
        current_scroll = 0
        while current_scroll < scroll_height:
            scroll_amount = random.randint(100, 300)
            await self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            current_scroll += scroll_amount
            await asyncio.sleep(random.uniform(0.5, 1.5))
            # تحديث ارتفاع الصفحة في حال كان هناك تحميل ديناميكي
            scroll_height = await self.page.evaluate("document.body.scrollHeight")
        print("✅ انتهى التمرير.")

    async def take_screenshot(self, path="screenshot.png"):
        print(f"📸 التقاط لقطة شاشة: {path}")
        await self.page.screenshot(path=path)
        print("✅ تم التقاط لقطة الشاشة.")

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            print("❌ تم إغلاق المتصفح.")

    async def run_example_task(self, url="https://www.google.com/"):
        try:
            await self.launch_browser()
            await self.navigate(url)
            await self.human_like_scroll()
            await self.take_screenshot("titan_example.png")
        except Exception as e:
            print(f"❌ حدث خطأ أثناء تنفيذ المهمة: {e}")
        finally:
            await self.close_browser()

async def main():
    titan = TitanAutomation()
    await titan.run_example_task()

if __name__ == "__main__":
    asyncio.run(main())
