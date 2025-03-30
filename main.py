import streamlit as st
from scraping_feature.scraping_feature import ScrapingRequest
from speech_response_feature.speech_response import say_formatted_response
from voice_recognition.voice_recognition import VoiceRecognizer


def perform_scraping(item_name, shops):
    data = []
    results = dict()
    index = 0
    for shop in shops:
        request = ScrapingRequest(shop, item_name)
        data.append(request.scrape_price())
        if data[index]:
            message = f"{shop.upper()}: Pigiausias variantas: [{data[index].item_name}]({data[index].item_url}) už "
            price = float(data[index].cheapest_item)
            results[message] = price
            say_formatted_response(data[index].item_name, shop, data[index].cheapest_item)
        else:
            message = f"{shop.upper()}: Prekė {item_name} nerasta."
            price = float('inf')
            results[message] = price
        index += 1

    sorted_results = sorted(results.items(), key=lambda x: x[1])

    return sorted_results


app = VoiceRecognizer()
shops = ["Rimi", "Maxima", "IKI"]
st.title("🎙️ Pigiausių prekių paieška balsu")

if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""
if "scrape_result" not in st.session_state:
    st.session_state.scrape_result = ""

input_method = st.radio("Pasirinkite įvedimo būdą:", ("Įvesti ranka", "Įrašyti balsu"))

try:

    if input_method == "Įvesti ranka":
        st.session_state.recognized_text = st.text_input("Įveskite prekės pavadinimą:",
                                                         value=st.session_state.recognized_text)
        if st.session_state.recognized_text:
            st.session_state.scrape_result = perform_scraping(st.session_state.recognized_text, shops)

    if st.button("🎤 Pasakyti prekę"):
        st.session_state.recognized_text = app.recognize_speech_whisper()
        if st.session_state.recognized_text:
            st.session_state.scrape_result = perform_scraping(st.session_state.recognized_text, shops)

    if st.session_state.recognized_text:
        edited_text = st.text_input("Atpažintas žodis:", value=st.session_state.recognized_text)
        if edited_text != st.session_state.recognized_text:
            st.session_state.recognized_text = edited_text
            st.session_state.scrape_result = perform_scraping(edited_text, shops)

    for result in st.session_state.scrape_result:
        if result[1] != float('inf'):
            st.markdown(f"{result[0]}{result[1]}€", unsafe_allow_html=True)
        else:
            st.markdown(f"{result[0]}", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Klaida :( Pataisykite atpažintą žodį arba pabandykite dar kartą. Klaidos pranešimas: {str(e)}")

    edited_text = st.text_input("Atpažintas žodis:", value=st.session_state.recognized_text)

    if edited_text != st.session_state.recognized_text:
        st.session_state.recognized_text = edited_text
        st.session_state.scrape_result = perform_scraping(edited_text, shops)

    if st.session_state.scrape_result:
        for result in st.session_state.scrape_result:
            if result[1] != float('inf'):
                st.markdown(f"{result[0]}{result[1]}€", unsafe_allow_html=True)
            else:
                st.markdown(f"{result[0]}", unsafe_allow_html=True)