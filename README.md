# Reframe

Reframe is an AI mental health chatbot designed to support users through **Cognitive Behavioral Therapy (CBT)** techniques. It provides a space for reflection, emotion tracking, and journaling to help users reframe their thoughts and understand their emotions over time.
## Try it Live!!

https://reframe.streamlit.app/ 
------ login with test/test

## Features

- **ML-backed chatbot** – Uses sentiment analysis to tailor CBT-style responses (supportive for negative feelings, reflective for positive)
- **Sentiment analysis** – Pre-trained Hugging Face model (DistilBERT) to monitor emotional trends
- **Multi-user authentication** – Secure login for personal journals
- Daily journaling prompts for guided self-reflection
- Mood and sentiment visualizations over time
- Shareable journal entries with unique IDs for easy reflection and collaboration
- Shared entry viewer for loading and reading journal entries by ID
- SQLite-based data storage for privacy-first local logging

## Tech Stack

- **Python**
- **Streamlit** – UI and app logic
- **Hugging Face Transformers** – Pre-trained sentiment analysis
- **SQLite** – Journal entries, mood logs, and shared entries
- **pandas** – Data analysis and chart generation
- **streamlit-authenticator** – User authentication

## Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/karadeskin/reframe.git
   cd reframe
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Data & Visualizations

- **reframe.db** – SQLite database with `journal_entries` (text, sentiment, timestamps) and `mood_logs` (mood, timestamp) per user
- **Mood Overview** – Bar chart of mood distribution
- **Sentiment Over Time** – Line chart of emotional trends from journal entries
- Shareable IDs let you load any journal entry by ID

## Future Improvements

- Integrate with GPT for more natural conversations
- Cloud-based storage for user data
- Exportable reports of mood trends

Created with care by Kara Deskin 🧡
