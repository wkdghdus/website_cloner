import os
import base64
import requests
from playwright.sync_api import sync_playwright
from browserbase import Browserbase
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from agent.states.state import State

load_dotenv()

def create_session():
    bb = Browserbase(api_key=os.environ["BROWSERBASE_API_KEY"])
    session = bb.sessions.create(
        project_id=os.environ["BROWSERBASE_PROJECT_ID"],
        # browser_settings={"advanced_stealth": True},  # only available in enterprise plan
    )
    return session

def web_scrape(state: State):
    try:
        print("\U0001F50D Scraping:", state.given_url)
        session = create_session()
        print(f"View session replay at https://browserbase.com/sessions/{session.id}")

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(session.connect_url)
            context = browser.contexts[0]
            page = context.pages[0]

            print("Processing:", state.given_url)
            page.goto(state.given_url, wait_until="domcontentloaded")

            # Remove unnecessary clutter
            page.evaluate("""
                () => {
                    const elementsToRemove = document.querySelectorAll('script, style, .ads, .popup, .cookie-banner, .tracking');
                    elementsToRemove.forEach(el => el.remove());
                }
            """)

            # Wait for meaningful content
            try:
                page.wait_for_selector('main', timeout=5000)
                main_content = page.query_selector('main')
            except:
                main_content = None

            # Fallback to body if <main> not found
            html_raw = main_content.inner_html() if main_content else page.content()

            # Minify HTML using BeautifulSoup
            soup = BeautifulSoup(html_raw, 'html.parser')
            minified_html = soup.prettify()

            # Extract stylesheet URLs
            stylesheet_urls = page.evaluate("""
                () => Array.from(document.styleSheets)
                    .map(s => s.href)
                    .filter(href => href !== null)
            """)

            stylesheets = {}
            for url in stylesheet_urls:
                try:
                    response = requests.get(url, timeout=5)
                    response.raise_for_status()
                    stylesheets[url] = response.text
                except Exception as e:
                    print(f"Failed to fetch stylesheet: {url} - {e}")

            images = page.eval_on_selector_all('img', 'imgs => imgs.map(img => img.src)')
            screenshot = page.screenshot(full_page=True)
            meta_tags = page.evaluate("""
                () => Array.from(document.querySelectorAll('meta'))
                        .map(meta => ({name: meta.name, content: meta.content}))
            """)
            fonts = page.evaluate("""
                () => getComputedStyle(document.body).getPropertyValue('font-family')
            """)

            print("Shutting down...")
            page.close()
            browser.close()

        return {
            "raw_html": minified_html,
            "stylesheets": stylesheets,
            "images": images,
            "screen_shot": base64.b64encode(screenshot).decode('utf-8'),
            "meta": meta_tags,
            "fonts": fonts,
        }
    except Exception as e:
        print("\u274c web_scrape failed:", e)
        raise
