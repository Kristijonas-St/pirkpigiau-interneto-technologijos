import streamlit as st
import requests

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    login_url = "http://localhost:5000/login"
    response = requests.post(login_url, json={"username": username, "password": password})
    
    if response.status_code == 200 and response.json().get("success"):
        st.success("Logged in!")
        st.title("Logged In")
    else:
        st.error("Login failed. Check your username and password.")
