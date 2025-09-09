import streamlit as st
from chatbot import response
import datetime, random, pandas as pd, os, uuid
from pathlib import Path
from textblob import TextBlob
import streamlit_authenticator as stauth

st.set_page_config(page_title="Reframe", layout="centered")
names = ['Kara Deskin', 'Test User']
usernames = ['kara', 'test']
hashed_passwords = stauth.Hasher.hash_list(['123', 'test'])  # demo only
credentials = {
    "usernames": {
        usernames[0]: {"name": names[0], "password": hashed_passwords[0]},
        usernames[1]: {"name": names[1], "password": hashed_passwords[1]},
    }
}
authenticator = stauth.Authenticate(credentials, 'reframe_app', 'abcdef', cookie_expiry_days=1)
authenticator.login(location='main', key='Login')
name = st.session_state.get('name')
authentication_status = st.session_state.get('authentication_status')
username = st.session_state.get('username')
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
journal_path   = DATA_DIR / "journal_entries.txt"
sentiment_path = DATA_DIR / "sentiment_log.csv"
mood_path      = DATA_DIR / "mood_log.csv"
shared_path    = DATA_DIR / "shared_entries.txt"
if authentication_status:
    st.title("Reframe")
    st.write(f'Welcome *{name}*')
    st.write("Hi! My name is Reframe. I am here to guide you using CBT techniques. How are you feeling today?")
    user_input = st.text_input("You:", "")
    if user_input:
        reply = response(user_input)
        st.markdown(f"**Reframe:** {reply}")
    prompts = [
        "What's something you're grateful for today?",
        "What challenged you today?",
        "Describe a moment that made you smile recently.",
        "What emotion are you feeling most strongly today?",
        "Write about something you’re looking forward to."
    ]
    st.subheader("Daily Prompt")
    st.write(random.choice(prompts))
    st.subheader("Your Journal")
    entry = st.text_area("Write about your day or how you are feeling:")
    if st.button("Save Entry"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sentiment_score = TextBlob(entry).sentiment.polarity
        with open(journal_path, "a") as f:
            f.write(f"{timestamp} - {entry} | Sentiment: {sentiment_score:.2f}\n")
        with open(sentiment_path, "a") as f:
            f.write(f"{timestamp},{sentiment_score:.2f}\n")
        shared_id = str(uuid.uuid4())[:6]
        with open(shared_path, "a") as f:
            f.write(f"{shared_id}|{entry}\n")
        st.success("Your journal entry has been saved.")
        st.info(f"Your shareable ID is: {shared_id}")
    st.subheader("Mood Tracker")
    mood = st.selectbox("How are you feeling right now?", ["Happy", "Sad", "Anxious", "Calm", "Frustrated", "Excited"])
    if st.button("Log Mood"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(mood_path, "a") as f:
            f.write(f"{timestamp},{mood}\n")
        st.success("Your mood has been logged!")
    if mood_path.exists():
        df = pd.read_csv(mood_path, names=["Date", "Mood"])
        mood_counts = df["Mood"].value_counts()
        st.subheader("Mood Overview")
        st.bar_chart(mood_counts)
    if sentiment_path.exists():
        st.subheader("Sentiment Over Time")
        df_sent = pd.read_csv(sentiment_path, names=["Date", "Sentiment"])
        df_sent["Date"] = pd.to_datetime(df_sent["Date"], errors="coerce")
        df_sent = df_sent.dropna(subset=["Date"]).sort_values("Date")
        st.line_chart(df_sent.set_index("Date"))
    st.subheader("View Shared Entry")
    view_id = st.text_input("Enter a shared entry ID:")
    if st.button("Load Shared Entry"):
        if shared_path.exists():
            with open(shared_path, "r") as f:
                entries = f.readlines()
            for e in entries:
                parts = e.strip().split("|", 1)
                if len(parts) == 2 and parts[0] == view_id:
                    st.success(f"Shared Entry:\n\n{parts[1]}")
                    break
            else:
                st.error("Entry not found. Please check the ID and try again.")
    authenticator.logout('Logout', 'sidebar')
elif authentication_status is False:
    st.error('Username or password is incorrect')
else:
    st.warning('Please enter your username and password')