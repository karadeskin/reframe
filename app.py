import streamlit as st 
from chatbot import response

st.set_page_config(page_title="Reframe", layout="centered")
st.title("Reframe")
st.write("Hi! My name is Reframe. I am here to guide you using CBT (Cognitive Behavioral Therapy) techniques. How are you feeling today?")
user_input = st.text_input("You:", "")
if user_input:
    reply = response(user_input)
    st.markdown(f"**Reframe:** {reply}")

