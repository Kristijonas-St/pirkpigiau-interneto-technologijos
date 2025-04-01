import streamlit as st
import requests

#TODO: clean code

session = requests.Session()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


login_placeholder = st.empty()

def load_search_page():
    from scraping_feature.scraping_feature import ScrapingRequest
    from speech_response_feature.speech_response import say_formatted_response
    from voice_recognition.voice_recognition import VoiceRecognizer

    def perform_scraping(item_name, shops):
        data = []
        results = dict()
        voice_responses = []
        index = 0
        is_found = False

        for shop in shops:
            request = ScrapingRequest(shop, item_name)
            data.append(request.scrape_price())

            if data[index]:
                is_found = True
                price = float(data[index].cheapest_item)
                message = f"{shop.upper()}: Pigiausias variantas: [{data[index].item_name}]({data[index].item_url}) už "
                results[message] = price
                voice_responses.append((is_found, data[index].item_name, shop, data[index].cheapest_item))
            else:
                is_found = False
                price = float('inf')
                message = f"{shop.upper()}: Prekė {item_name} nerasta."
                results[message] = price
                voice_responses.append((is_found, item_name, shop, None))

            index += 1

        sorted_results = sorted(results.items(), key=lambda x: x[1])

        return sorted_results, voice_responses


    app = VoiceRecognizer()
    shops = ["Rimi", "Maxima", "IKI"]
    st.title("🎙️ Pigiausių prekių paieška balsu")


    if "recognized_text" not in st.session_state:
        st.session_state.recognized_text = ""
    if "scrape_result" not in st.session_state:
        st.session_state.scrape_result = ""
    if "voice_responses" not in st.session_state:
        st.session_state.voice_responses = []

    input_method = st.radio("Pasirinkite įvedimo būdą:", ("Įvesti ranka", "Įrašyti balsu"))


    if input_method == "Įvesti ranka":
        st.session_state.recognized_text = st.text_input("Įveskite prekės pavadinimą:", value=st.session_state.recognized_text)
        if st.session_state.recognized_text:
            st.session_state.scrape_result, st.session_state.voice_responses = perform_scraping(st.session_state.recognized_text, shops)

    if st.button("🎤 Pasakyti prekę"):
        st.session_state.recognized_text = app.recognize_speech_whisper()
        if st.session_state.recognized_text:
            st.session_state.scrape_result, st.session_state.voice_responses = perform_scraping(st.session_state.recognized_text, shops)


    if st.session_state.recognized_text:
        edited_text = st.text_input("Atpažintas žodis:", value=st.session_state.recognized_text)
        if edited_text != st.session_state.recognized_text:
            st.session_state.recognized_text = edited_text
            st.session_state.scrape_result, st.session_state.voice_responses = perform_scraping(edited_text, shops)


    for result in st.session_state.scrape_result:
        if result[1] != float('inf'):
            st.markdown(f"{result[0]}{result[1]}€", unsafe_allow_html=True)
        else:
            st.markdown(f"{result[0]}", unsafe_allow_html=True)


    if st.session_state.voice_responses:
        cheapest_response = None
        for response in st.session_state.voice_responses:
            if response[0]:
                if cheapest_response is None or float(response[3]) < float(cheapest_response[3]):
                    cheapest_response = response

        if cheapest_response:
            say_formatted_response(*cheapest_response)
        else:
            say_formatted_response(False, st.session_state.recognized_text, "", None)


def handle_permissions():
    protected_url = "http://localhost:5000/protected"
    response = session.get(protected_url)

    if response.status_code == 200 and response.json().get("access"):
        st.session_state.logged_in = True
        load_search_page()
    else:
        st.error("Access Denied. Please log in again.")



if not st.session_state.logged_in:
    with login_placeholder.container():
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

    if login_button:
        login_url = "http://localhost:5000/login"
        response = session.post(login_url, json={"username": username, "password": password}) 

        if response.status_code == 200 and response.json().get("success"):
            login_placeholder.empty()
            handle_permissions()
        else:
            st.error("Login failed. Check your username and password.")
else:
    load_search_page() 
