import streamlit as st 
from chatbot import response
import datetime
import random
import pandas as pd
import os
from textblob import TextBlob

st.set_page_config(page_title="Reframe", layout="centered")
st.title("Reframe")
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
    st.success("Your journal entry has been saved.")
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