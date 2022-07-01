import requests

api_url = "https://script.google.com/macros/s/AKfycbybnefLnp6WsVP1Ju7EeN6L1O6BT3ed4Jwc7kOouosn6o6rQHt2EWVPn8vAQcZJ8s8O/exec?"

def translate_GAS(txt, langs, origin_lang):
    req_url = api_url + "txt=" + txt + "&langs=" + ",".join(langs) + "&origin_lang=" + origin_lang
    req_get_result = requests.get(req_url)
    return req_get_result.text

