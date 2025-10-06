# finance_chatbot.py

import requests
from bs4 import BeautifulSoup

# -----------------------------
# Function to scrape Wikipedia or investopedia for finance terms
# -----------------------------
def scrape_finance_topic(query, max_paragraphs=3):
    """
    Returns a summary of a finance topic from Wikipedia or Investopedia.
    """
    # First try Wikipedia
    search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
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

        # If Wikipedia fails, try Investopedia search
        investopedia_url = f"https://www.investopedia.com/terms/{query[0].lower()}/{query.replace(' ', '-')}.asp"
        response = requests.get(investopedia_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
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

        return f"⚠️ Could not find finance info for '{query}'."

    except Exception as e:
        return f"⚠️ Error fetching finance topic: {str(e)}"

# -----------------------------
# Chatbot response function
# -----------------------------
def chatbot_reply(user_input):
    user_input = user_input.lower()
    user_input = user_input.replace('tell me about', '').strip()
    user_input = user_input.replace('what is', '').strip()

    if user_input:
        summary = scrape_finance_topic(user_input, max_paragraphs=3)
        return f"🤖 {summary}"
    else:
        return "🤖 Please ask me about a finance topic."

# -----------------------------
# Console test
# -----------------------------
if __name__ == "__main__":
    print("Welcome to Finance Chatbot! Type 'exit' to quit.")
    while True:
        user_question = input("You: ")
        if user_question.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        response = chatbot_reply(user_question)
        print("Chatbot:", response)