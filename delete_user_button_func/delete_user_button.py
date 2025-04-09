import streamlit as st
import requests

def delete_user_button(session):
    st.subheader("🗑️ Ištrinti mano paskyrą")
    token = session.cookies.get("token")

    if st.button("Ištrinti mano paskyrą") and token:
        try:
            delete_url = "http://localhost:5000/delete_logged_user"
            headers = {
                "Cookie": f"token={token}"
            }
            response = session.delete(delete_url, headers=headers)

            if response.status_code == 200:
                st.success(response.json().get("message"))
                st.session_state.clear()
                st.rerun()
            else:
                st.error(response.json().get("message"))

        except requests.exceptions.ConnectionError:
            st.error("❌ Nepavyko prisijungti prie serverio. Ar `backend.py` veikia?")
