import tempfile
import os
import time
import subprocess
import gtts


def say_formatted_response(is_found, item_to_search, shop_name, price):
    
    if is_found:
        price_value = float(price.replace(" €", "").replace(",", "."))
        
        euro_case, cent_case, shop_case = form_price_and_shop_cases(price_value, shop_name)
        speech_response = f"Preke, {item_to_search}, pigiausia, {shop_case}, {int(price_value)} {euro_case}, {round((price_value % 1) * 100)} {cent_case}"
    else:
        speech_response = f"Prekė {item_to_search} nerasta"
    
    speak(speech_response)

def form_price_and_shop_cases(price_value, shop_name):
    euro = int(price_value)
    if euro == 1 or str(euro)[-1] == "1":
        euro_case = "euras"
    elif euro == 0 or str(euro)[-1] == "0":
        euro_case = "eurų"
    else:
        euro_case = "eurai"

    cents = round((price_value % 1) * 100)
    if cents == 1 or str(cents)[-1] == "1":
        cent_case = "centas"
    elif cents == 0 or str(cents)[-1] == "0":
        cent_case = "centų"
    else:
        cent_case = "centai"

    if shop_name == "Maxima":
        shop_case = "Maximoje"
    else:
        shop_case = shop_name


    return euro_case, cent_case, shop_case

def speak(text, lang="lt"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        filename = temp_file.name

    tts = gtts.gTTS(text, lang=lang)
    tts.save(filename)

    if os.name == "nt":
        os.startfile(filename)
    else:
        subprocess.Popen(["mpg321", filename])

    time.sleep(5)
    for _ in range(3):
        try:
            os.remove(filename)
            break
        except PermissionError:
            time.sleep(2)