import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def search_wikipedia(query):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'utf8': 1
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract search results
    search_results = data['query']['search']
    return search_results


# Function to get latest news articles from The Guardian
def get_latest_news(topic):
    api_key = "8c202a88-78e2-4936-b5c7-f4b58299bcf1"  # Replace with your actual API key
    base_url = "https://content.guardianapis.com/search"
    params = {
        'q': topic,
        'api-key': api_key,
        'show-fields': 'headline,shortUrl',
        'order-by': 'newest'
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract news articles
    articles = data.get('response', {}).get('results', [])
    return articles

def display_news_articles(articles):
    if not articles:
        st.warning("No news articles found for this topic.")
    else:
        st.write("Latest News Articles:")
        for article in articles:
            st.write(f"- [{article['webTitle']}]({article['webUrl']})")


def get_wikipedia_content(page_id):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'pageids': page_id,
        'prop': 'extracts',
        'exintro': True
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract content from the response
    page = next(iter(data['query']['pages'].values()))
    if 'extract' in page:
        content = page['extract']
        
        # Use BeautifulSoup to remove HTML tags
        soup = BeautifulSoup(content, 'html.parser')
        clean_text = soup.get_text()
        
        return clean_text.strip()
    else:
        return None

# Main function
def main():
    st.title("🌐 Wikipedia Search and QA App")

    # User input for Wikipedia search
    user_query = st.text_input("🔍 Enter the name of anything you want to search on Wikipedia:")

    if user_query:
        search_results = search_wikipedia(user_query)

        if not search_results:
            st.warning(f"❌ No results found for '{user_query}' on Wikipedia.")
        else:
            st.write("Choose a Wikipedia page:")
            for i, result in enumerate(search_results, 1):
                st.write(f"{i}. {result['title']}")

            choice = st.number_input("👉 Enter the number corresponding to your choice:", min_value=1, max_value=len(search_results))

            if 1 <= choice <= len(search_results):
                selected_page_id = search_results[int(choice) - 1]['pageid']
                content = get_wikipedia_content(selected_page_id)

                if content:
                    st.write(content)

                    # BERT-based question answering
                    qa_model = pipeline("question-answering")
                    user_question = st.text_input("💬 Ask a question about the article:")
                    if user_question:
                        answer = qa_model(question=user_question, context=content)
                        st.write(f"**Question:** {user_question}")
                        st.write(f"**Answer:** {answer['answer']}")

                    # Ask the user if they want to read news articles
                    read_news = st.button("📰 Read Latest News Articles")
                    if read_news:
                        topic_for_news = user_query
                        news_articles = get_latest_news(topic_for_news)
                        display_news_articles(news_articles)

                else:
                    st.warning(f"❌ Failed to retrieve content for the selected page.")
            else:
                st.warning("❌ Invalid choice.")

if __name__ == "__main__":
    main()