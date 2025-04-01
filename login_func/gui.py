import streamlit as st
import requests

session = requests.Session()

login_placeholder = st.empty()
with login_placeholder.container():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

def switch_to_main():

    protected_url = "http://localhost:5000/protected"
    response = session.get(protected_url)

    if response.status_code == 200 and response.json().get("access"):
        st.title("Search for Cheapest Products")
        query = st.text_input("Enter product name")

        if st.button("Search"):
            st.write(f"Searching for: {query} in three shops...")

    else:
        st.error("Access Denied. Please log in again.")

if login_button:
    login_url = "http://localhost:5000/login"
    response = session.post(login_url, json={"username": username, "password": password})  # Use session

    if response.status_code == 200 and response.json().get("success"):
        login_placeholder.empty()
        switch_to_main()
    else:
        st.error("Login failed. Check your username and password.")
