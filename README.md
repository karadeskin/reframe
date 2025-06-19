# Reframe

Reframe is an AI mental health chatbot designed to support users through **Cognitive Behavioral Therapy (CBT)** techniques. It provides a space for reflection, emotion tracking, and journaling to help users reframe their thoughts and understand their emotions over time.

## Features

-  **Chatbot** using simple NLP to engage users in supportive conversation  
-  **Sentiment analysis** with TextBlob to monitor emotional trends  
-  **Daily journaling prompts** for guided self-reflection  
-  **Mood and sentiment visualizations** over time  
-  Local data logging 

## Tech Stack

- **Python**
- **Streamlit** – UI and app logic
- **TextBlob** – Sentiment analysis
- **pandas, matplotlib** – Data visualization and storage
- **CSV logging** – local data tracking

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

## Example Output

- mood_log.csv: Tracks the mood selected by the user each day
- sentiment_log.csv: Stores sentiment polarity scores of each journal entry
- journal_entries.txt: Saves daily journal responses
- Graphs generated using matplotlib for emotion trends over time

## Future Improvements 

- Add authentication for multiple users
- Integrate with GPT for more natural conversations
- Cloud-based storage for user data
- Exportable reports of mood trends

Created with care by Kara Deskin 🧡