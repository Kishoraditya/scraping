import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
from selenium import webdriver
import requests

async def execute_javascript_pyppeteer(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    rendered_content = await page.content()
    await browser.close()
    return rendered_content

def execute_javascript_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    rendered_content = driver.page_source
    driver.quit()
    return rendered_content

def execute_javascript_requests(url):
    response = requests.get(url)
    rendered_content = response.content
    return rendered_content

def execute_javascript(url, method='pyppeteer'):
    if method == 'pyppeteer':
        loop = asyncio.get_event_loop()
        rendered_content = loop.run_until_complete(execute_javascript_pyppeteer(url))
    elif method == 'selenium':
        rendered_content = execute_javascript_selenium(url)
    elif method == 'requests':
        rendered_content = execute_javascript_requests(url)
    else:
        raise ValueError("Invalid execution method specified.")

    return rendered_content

def scrape_data(rendered_content):
    # Use BeautifulSoup or Scrapy to scrape data from the rendered content
    soup = BeautifulSoup(rendered_content, 'html.parser')
    # Perform scraping operations using BeautifulSoup or Scrapy

    # Example: Extract all links from the rendered content
    links = [a.get('href') for a in soup.find_all('a') if 'href' in a.attrs]
    return links

