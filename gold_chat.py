# multi_source_finance_chatbot_selenium.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

cache = {}
CACHE_DURATION = timedelta(minutes=5)

# -----------------------------
# Selenium setup
# -----------------------------

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service('/usr/bin/chromedriver')  # Adjust path if needed
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# -----------------------------
# Scrape Wikipedia for general topics
# -----------------------------

def scrape_wikipedia(query, max_paragraphs=3):
    search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        import requests
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        summary_texts = []
        for p in paragraphs:
            text = p.text.strip()
            if text:
                summary_texts.append(text)
            if len(summary_texts) >= max_paragraphs:
                break
        if summary_texts:
            return '\n\n'.join(summary_texts)
        return None
    except:
        return None

# -----------------------------
# Scrape Gold Rate using Selenium
# -----------------------------

def scrape_gold_rate():
    key = 'gold_rate'
    if key in cache and datetime.now() - cache[key]['time'] < CACHE_DURATION:
        return cache[key]['data']

    try:
        driver = get_driver()
        driver.get('https://www.goodreturns.in/gold-rates.html')
        time.sleep(3)  # wait for JS content to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rate_elem = soup.select_one('div[class*="gold_rate"]')  # update selector manually
        driver.quit()
        if rate_elem:
            rate = rate_elem.text.strip()
            cache[key] = {'data': rate, 'time': datetime.now()}
            return rate
    except:
        pass
    return '⚠️ Could not fetch gold rate.'

# -----------------------------
# Scrape Vegetable Prices using Selenium
# -----------------------------

def scrape_vegetables():
    key = 'vegetables'
    if key in cache and datetime.now() - cache[key]['time'] < CACHE_DURATION:
        return cache[key]['data']

    try:
        driver = get_driver()
        driver.get('https://www.indiamart.com/vegetable-prices/')
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table')
        veg_prices = []
        if table:
            rows = table.find_all('tr')
            for row in rows[1:6]:  # first 5 rows
                cols = row.find_all('td')
                if len(cols) >= 2:
                    veg_prices.append(f"{cols[0].text.strip()}: {cols[1].text.strip()}")
        driver.quit()
        if veg_prices:
            result = '\n'.join(veg_prices)
            cache[key] = {'data': result, 'time': datetime.now()}
            return result
    except:
        pass
    return '⚠️ Could not fetch vegetable prices.'

# -----------------------------
# Chatbot reply function
# -----------------------------

def chatbot_reply(user_input):
    user_input = user_input.lower()
    if 'gold' in user_input:
        rate = scrape_gold_rate()
        return f"💰 Current gold rate: {rate}"
    elif 'vegetable' in user_input or 'market price' in user_input:
        veg_data = scrape_vegetables()
        return f"🥦 Current vegetable prices:\n{veg_data}"
    else:
        summary = scrape_wikipedia(user_input, max_paragraphs=3)
        if summary:
            return f"🤖 {summary}"
        return "🤖 Sorry, I could not find relevant information for your query."

# -----------------------------
# Console Test
# -----------------------------

if __name__ == '__main__':
    print("Welcome to Multi-Source Finance & Market Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        response = chatbot_reply(user_input)
        print("Chatbot:", response)