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

                else:
                    st.warning(f"❌ Failed to retrieve content for the selected page.")
            else:
                st.warning("❌ Invalid choice.")

if __name__ == "__main__":
    main()
