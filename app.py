import streamlit as st
from chatbot import response
import datetime
import random
import pandas as pd
import os
from textblob import TextBlob
import streamlit_authenticator as stauth
import uuid

st.set_page_config(page_title="Reframe", layout="centered")
names = ['Kara Deskin', 'Test User']
usernames = ['kara', 'test']
hashed_passwords = stauth.Hasher(['123', 'test']).generate()
authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords, 'reframe_app', 'abcdef', cookie_expiry_days=1
)
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    st.title("Reframe")
    st.write(f'Welcome *{name}*')
    st.write("Hi! My name is Reframe. I am here to guide you using CBT (Cognitive Behavioral Therapy) techniques. How are you feeling today?")
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
        with open("journal_entries.txt", "a") as f:
            f.write(f"{timestamp} - {entry} | Sentiment: {sentiment_score:.2f}\n")
        with open("sentiment_log.csv", "a") as f:
            f.write(f"{timestamp},{sentiment_score:.2f}\n")
        shared_id = str(uuid.uuid4())[:6]
        with open("shared_entries.txt", "a") as f:
            f.write(f"{shared_id}|{entry}\n")
        st.success("Your journal entry has been saved.")
        st.info(f"Your shareable ID is: {shared_id}")
        st.write("Share this ID with someone to let them view your entry!")
    st.subheader("Mood Tracker")
    mood = st.selectbox("How are you feeling right now?", ["Happy", "Sad", "Anxious", "Calm", "Frustrated", "Excited"])
    if st.button("Log Mood"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("mood_log.csv", "a") as f:
            f.write(f"{timestamp},{mood}\n")
        st.success("Your mood has been logged!")
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date", "Mood"])
        mood_counts = df["Mood"].value_counts()
        st.subheader("Mood Overview")
        st.bar_chart(mood_counts)
    if os.path.exists("sentiment_log.csv"):
        st.subheader("Sentiment Over Time")
        df_sent = pd.read_csv("sentiment_log.csv", names=["Date", "Sentiment"])
        df_sent["Date"] = pd.to_datetime(df_sent["Date"])
        df_sent = df_sent.sort_values("Date")
        st.line_chart(df_sent.set_index("Date"))
    st.subheader("View Shared Entry")
    view_id = st.text_input("Enter a shared entry ID:")
    if st.button("Load Shared Entry"):
        if os.path.exists("shared_entries.txt"):
            with open("shared_entries.txt", "r") as f:
                entries = f.readlines()
            found = False
            for e in entries:
                saved_id, saved_entry = e.strip().split("|", 1)
                if saved_id == view_id:
                    st.success(f"Shared Entry:\n\n{saved_entry}")
                    found = True
                    break
            if not found:
                st.error("Entry not found. Please check the ID and try again.")
    authenticator.logout('Logout', 'sidebar')
elif authentication_status == False:
    st.error('Username or password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')