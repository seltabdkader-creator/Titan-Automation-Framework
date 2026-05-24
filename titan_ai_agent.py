import asyncio
import os
import base64
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from openai import OpenAI
import random

# إعداد العميل (يستخدم المفتاح من البيئة تلقائياً)
client = OpenAI()

class TitanAIAgent:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.stealth = Stealth()

    async def launch(self):
        print("🚀 [AI] تشغيل المحرك الذكي...")
        pw = await async_playwright().start()
        self.browser = await pw.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        self.page = await self.context.new_page()
        await self.stealth.apply_stealth_async(self.page)
        print("✅ [AI] البيئة جاهزة.")

    async def get_ai_decision(self, prompt, take_screenshot=True):
        """يطلب من الذكاء الاصطناعي تحليل الصفحة واتخاذ قرار"""
        print(f"🧠 [AI] تحليل الموقف: {prompt}")
        
        messages = [{"role": "system", "content": "أنت خبير أتمتة متقدم. مهمتك هي تحليل حالة الصفحة واتخاذ القرار البرمجي الصحيح باستخدام Playwright."}]
        
        if take_screenshot:
            screenshot_path = "ai_vision.png"
            await self.page.screenshot(path=screenshot_path)
            with open(screenshot_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            })
        else:
            html = await self.page.content()
            messages.append({"role": "user", "content": f"HTML Snippet: {html[:2000]}\n\nTask: {prompt}"})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500
        )
        return response.choices[0].message.content

    async def autonomous_task(self, goal):
        """ينفذ مهمة بشكل ذاتي بالكامل"""
        print(f"🎯 [AI] الهدف النهائي: {goal}")
        await self.launch()
        
        try:
            # الخطوة الأولى: الانتقال للموقع المناسب (يقرره الذكاء الاصطناعي)
            decision = await self.get_ai_decision(f"ما هو أفضل رابط للبدء في تحقيق هذا الهدف: {goal}؟ أجب بالرابط فقط.")
            url = decision.strip()
            if not url.startswith("http"):
                url = "https://www.google.com/search?q=" + goal
            
            await self.page.goto(url, wait_until="networkidle")
            print(f"🌐 [AI] تم الدخول إلى: {url}")

            # دورة اتخاذ القرار (3 خطوات تجريبية)
            for i in range(3):
                action_plan = await self.get_ai_decision(f"الهدف: {goal}. بناءً على لقطة الشاشة، ما هي الخطوة التالية (كود Playwright بسيط)؟")
                print(f"🛠️ [AI] تنفيذ خطوة {i+1}: {action_plan}")
                
                # هنا يمكن تنفيذ الكود المقترح بشكل آمن (Sandbox)
                # للتبسيط في هذا النموذج، سنقوم بالتمرير والبحث
                await self.page.mouse.wheel(0, 500)
                await asyncio.sleep(2)

            print("✅ [AI] تم الانتهاء من المهمة الذاتية.")
        except Exception as e:
            print(f"❌ [AI] فشل في النظام: {e}")
        finally:
            await self.browser.close()

if __name__ == "__main__":
    agent = TitanAIAgent()
    asyncio.run(agent.autonomous_task("ابحث عن أحدث أخبار الذكاء الاصطناعي اليوم"))
