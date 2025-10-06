# wiki_chatbot_gold.py

import requests
from bs4 import BeautifulSoup

# -----------------------------
# Function to scrape Wikipedia
# -----------------------------
def scrape_wikipedia(query, max_paragraphs=3):
    """
    Returns a summary of a Wikipedia page for the query.
    max_paragraphs: Number of paragraphs to return (default 3)
    """
    search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            return f"⚠️ Could not find Wikipedia page for '{query}'."

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
        else:
            return f"⚠️ No summary found for '{query}'."

    except Exception as e:
        return f"⚠️ Error fetching Wikipedia page: {str(e)}"

# -----------------------------
# Chatbot response function
# -----------------------------
def chatbot_reply(user_input):
    user_input_lower = user_input.lower()

    # Special case for gold rate
    if 'gold rate' in user_input_lower:
        return "💰 Sorry, I cannot provide live gold prices. Please check a finance website or API."

    # Otherwise, use Wikipedia
    query = user_input_lower.replace('tell me about', '').replace('what is', '').strip()

    if query:
        summary = scrape_wikipedia(query, max_paragraphs=3)
        return f"🤖 {summary}"
    else:
        return "🤖 Please ask me about something."

# -----------------------------
# Console test
# -----------------------------
if __name__ == "__main__":
    print("Welcome to Wikipedia Chatbot! Type 'exit' to quit.")
    while True:
        user_question = input("You: ")
        if user_question.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        response = chatbot_reply(user_question)
        print("Chatbot:", response)