import asyncio
from playwright.async_api import async_playwright

async def html_to_pdf(html_content: str, output_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]  # Recomendado para Docker
        )
        page = await browser.new_page()
        await page.set_content(html_content, wait_until="networkidle")
        await page.pdf(path=output_path)
        await browser.close()

def generate_pdf_sync(html_content: str, output_path: str):
    asyncio.run(html_to_pdf(html_content, output_path))