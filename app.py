import datetime
import random
import uuid

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

from db import get_connection, init_db
from sentiment import score_text
from chatbot import response

st.set_page_config(page_title="Reframe", layout="centered", page_icon="✦")
init_db()

PAGE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;500&display=swap');

.stApp { background: linear-gradient(180deg, #FAF7F2 0%, #F5F0E8 100%); }

h1 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    transform: rotate(-0.5deg);
}

h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 600 !important;
    color: #2D2A26 !important;
}

p, span, label, div {
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stCaptionContainer"] {
    font-family: 'Cormorant Garamond', serif !important;
    font-style: italic;
    letter-spacing: 0.05em;
    color: #6B6560 !important;
}

.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 999px !important;
    font-weight: 500 !important;
    border: 1px solid #C17F59 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(193, 127, 89, 0.25);
}

div[data-testid="stVerticalBlock"] > div {
    border-radius: 12px;
}

/* Subtle chaos — slightly asymmetric blockquote feel for prompts */
div[data-testid="stMarkdownContainer"] {
    max-width: 42rem;
}

/* Refined input areas */
.stTextInput input, .stTextArea textarea {
    border-radius: 12px !important;
    border: 1px solid #E8E2D9 !important;
}

.stSelectbox > div {
    border-radius: 12px !important;
}
"""
st.markdown(f"<style>{PAGE_CSS}</style>", unsafe_allow_html=True)

names = ["Kara Deskin", "Test User"]
usernames = ["kara", "test"]
hashed_passwords = stauth.Hasher.hash_list(["123", "test"])  # demo only
credentials = {
    "usernames": {
        usernames[0]: {"name": names[0], "password": hashed_passwords[0]},
        usernames[1]: {"name": names[1], "password": hashed_passwords[1]},
    }
}
authenticator = stauth.Authenticate(
    credentials, "reframe_app", "abcdef", cookie_expiry_days=1
)
authenticator.login(location="main", key="Login")

name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")


def _get_mood_counts_for_user(conn, user):
    """Query mood_logs for current user and return counts."""
    df = pd.read_sql_query(
        "SELECT mood FROM mood_logs WHERE username = ?",
        conn,
        params=(user,),
    )
    return df["mood"].value_counts() if not df.empty else pd.Series(dtype=int)


def _get_sentiment_for_user(conn, user):
    """Query journal_entries for sentiment over time."""
    df = pd.read_sql_query(
        """
        SELECT timestamp, sentiment_score
        FROM journal_entries
        WHERE username = ? AND sentiment_score IS NOT NULL
        ORDER BY timestamp
        """,
        conn,
        params=(user,),
    )
    if df.empty:
        return None
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    return df.set_index("timestamp")


def _get_shared_entry(conn, shared_id):
    """Look up journal entry by shared_id."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT entry_text FROM journal_entries WHERE shared_id = ? LIMIT 1",
        (shared_id.strip(),),
    )
    row = cursor.fetchone()
    return row[0] if row else None


if authentication_status:
    st.markdown('<p style="font-size:0.9rem; color:#6B6560; margin-bottom:0;">✦</p>', unsafe_allow_html=True)
    st.title("Reframe")
    st.caption("— reframe your thoughts")
    st.write(f"Hey *{name}* — welcome back.")
    st.write(
        "I'm Reframe. I'm here to guide you with CBT techniques. How are you *really* feeling today?"
    )
    st.divider()

    user_input = st.text_input("You:", "", placeholder="Type anything... I'm listening.")
    if user_input:
        reply = response(user_input)
        st.markdown(f"**Reframe:** {reply}")

    prompts = [
        "What's something you're grateful for today?",
        "What challenged you today?",
        "Describe a moment that made you smile recently.",
        "What emotion are you feeling most strongly today?",
        "Write about something you're looking forward to.",
    ]
    st.subheader("Daily Prompt")
    st.markdown(f"*{random.choice(prompts)}*")
    st.divider()

    st.subheader("Your Journal")
    entry = st.text_area("Write about your day or how you are feeling:")
    if st.button("Save Entry"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sentiment_label, sentiment_score = score_text(entry)
        shared_id = str(uuid.uuid4())[:6]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO journal_entries
            (username, timestamp, entry_text, sentiment_label, sentiment_score, mood, shared_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (username, timestamp, entry, sentiment_label, sentiment_score, None, shared_id),
        )
        conn.commit()
        conn.close()

        st.success("Your journal entry has been saved.")
        st.info(f"Your shareable ID is: {shared_id}")

    st.divider()
    st.subheader("Mood Tracker")
    mood = st.selectbox(
        "How are you feeling right now?",
        ["Happy", "Sad", "Anxious", "Calm", "Frustrated", "Excited"],
    )
    if st.button("Log Mood"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mood_logs (username, timestamp, mood) VALUES (?, ?, ?)",
            (username, timestamp, mood),
        )
        conn.commit()
        conn.close()
        st.success("Your mood has been logged!")

    conn = get_connection()
    mood_counts = _get_mood_counts_for_user(conn, username)
    conn.close()

    if not mood_counts.empty:
        st.subheader("Mood Overview")
        st.bar_chart(mood_counts)

    conn = get_connection()
    df_sent = _get_sentiment_for_user(conn, username)
    conn.close()

    if df_sent is not None and not df_sent.empty:
        st.subheader("Sentiment Over Time")
        st.line_chart(df_sent)

    st.divider()
    st.subheader("View Shared Entry")
    view_id = st.text_input("Enter a shared entry ID:")
    if st.button("Load Shared Entry"):
        conn = get_connection()
        entry_text = _get_shared_entry(conn, view_id)
        conn.close()
        if entry_text:
            st.success(f"Shared Entry:\n\n{entry_text}")
        else:
            st.error("Entry not found. Please check the ID and try again.")

    authenticator.logout("Logout", "sidebar")

elif authentication_status is False:
    st.error("Username or password is incorrect")
else:
    st.warning("Please enter your username and password")
