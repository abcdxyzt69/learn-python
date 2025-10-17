import streamlit as st

st.title("AI app")
st.header("Super AI Title")

user_name = st.text_input("Enter your name:", "type here")

if st.button("Hello"):
    st.write(f"Hello, {user_name}!")
