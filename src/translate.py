import requests
from os import getenv

api_url = getenv("TRANS_API_URL")

def translate_GAS(txt, langs, origin_lang):
    req_url = api_url + "txt=" + txt + "&langs=" + ",".join(langs) + "&origin_lang=" + origin_lang
    req_get_result = requests.get(req_url)
    return req_get_result.text

