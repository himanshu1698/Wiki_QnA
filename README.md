# Wikipedia Search and QA App

Welcome to the Wikipedia Search and Question Answering (QA) App! This Streamlit application allows users to search for topics on Wikipedia, explore detailed content from selected pages, and ask questions related to the articles using a BERT-based QA model. Additionally, users can read the latest news articles related to their search topic.

## Getting Started

### Prerequisites
Make sure you have the following dependencies installed:
- `streamlit`
- `requests`
- `beautifulsoup4`
- `transformers`

You can install them using the following command:
```bash
pip install streamlit requests beautifulsoup4 transformers
```

### How to Run
1. Save the provided code in a file, e.g., `wikipedia_app.py`.
2. Open a terminal and navigate to the directory containing the file.
3. Run the Streamlit app using the command:
   ```bash
   streamlit run wikipedia_app.py
   ```
4. The app will open in your default web browser.

## Features

1. **Wikipedia Search:**
   - Enter the name of anything you want to search on Wikipedia.
   - Choose from the search results and explore detailed content.

2. **Question Answering (QA):**
   - Utilizes a BERT-based QA model to answer questions related to the selected Wikipedia page.
   - Simply ask a question about the article, and the app will provide relevant answers.

3. **Latest News Articles:**
   - Optionally read the latest news articles related to the chosen Wikipedia search topic.
   - Powered by The Guardian API (replace the placeholder API key with your actual key).

## Usage

1. Enter a search query in the text input field.
2. Explore the search results and select a Wikipedia page.
3. Read detailed content and ask questions about the article.
4. Optionally, click the "Read Latest News Articles" button to discover recent news related to the topic.

Feel free to customize the app according to your needs and preferences. Happy exploring!

**Note:** Make sure to replace the placeholder API key with your actual API key for The Guardian API to enable the latest news feature.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Disclaimer: This app is for educational and exploratory purposes only. The developers are not responsible for the accuracy of the information retrieved or any misuse of the application.*
