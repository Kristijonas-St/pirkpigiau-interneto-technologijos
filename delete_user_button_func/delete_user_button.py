import streamlit as st
import requests

def delete_user_button(session):
    st.subheader("🗑️ Ištrinti mano paskyrą")

    if st.button("Ištrinti mano paskyrą"):
        try:
            response = session.delete("http://127.0.0.1:5000/delete_logged_user")

            if response.status_code == 200:
                st.success(response.json().get("message"))
                st.session_state.clear()
                st.rerun()
            else:
                st.error(response.json().get("message"))

        except requests.exceptions.ConnectionError:
            st.error("❌ Nepavyko prisijungti prie serverio. Ar `backend.py` veikia?")
