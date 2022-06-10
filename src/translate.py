import requests

def translate_via_GAS(txt, langs):
    gas_url = "https://script.google.com/macros/s/AKfycbybnefLnp6WsVP1Ju7EeN6L1O6BT3ed4Jwc7kOouosn6o6rQHt2EWVPn8vAQcZJ8s8O/exec?"+"txt="+txt+"&langs="+",".join(langs)
    gas_get_result = requests.get(gas_url)
    return gas_get_result.text
