import requests

LANGUAGES = [
    'af',
    'sq',
    'am',
    'ar',
    'hy',
    'az',
    'eu',
    'be',
    'bn',
    'bs',
    'bg',
    'ca',
    'ceb',
    'ny',
    'zh-cn',
    'zh-tw',
    'co',
    'hr',
    'cs',
    'da',
    'nl',
    'en',
    'eo',
    'et',
    'tl',
    'fi',
    'fr',
    'fy',
    'gl',
    'ka',
    'de',
    'el',
    'gu',
    'ht',
    'ha',
    'haw',
    'iw',
    'he',
    'hi',
    'hmn',
    'hu',
    'is',
    'ig',
    'id',
    'ga',
    'it',
    'ja',
    'jw',
    'kn',
    'kk',
    'km',
    'ko',
    'ku',
    'ky',
    'lo',
    'la',
    'lv',
    'lt',
    'lb',
    'mk',
    'mg',
    'ms',
    'ml',
    'mt',
    'mi',
    'mr',
    'mn',
    'my',
    'ne',
    'no',
    'or',
    'ps',
    'fa',
    'pl',
    'pt',
    'pa',
    'ro',
    'ru',
    'sm',
    'gd',
    'sr',
    'st',
    'sn',
    'sd',
    'si',
    'sk',
    'sl',
    'so',
    'es',
    'su',
    'sw',
    'sv',
    'tg',
    'ta',
    'te',
    'th',
    'tr',
    'uk',
    'ur',
    'ug',
    'uz',
    'vi',
    'cy',
    'xh',
    'yi',
    'yo',
    'zu'
]

def trans(txt, langs):
    url = "https://script.google.com/macros/s/AKfycbybnefLnp6WsVP1Ju7EeN6L1O6BT3ed4Jwc7kOouosn6o6rQHt2EWVPn8vAQcZJ8s8O/exec?"+"txt="+txt+"&langs="+','.join(langs)+""
    r = requests.get(url)
    print(url)
    return r.text

# def trans_loop(text, langs):
#     tr = Translator()
#     txt = text
#     las = langs

#     prev_trans = tr.translate(txt, src="ja", dest=las[0]).text
#     for i in range(len(las)-1):
#         print(prev_trans)
#         next_trans = tr.translate(prev_trans, src=las[i], dest=las[i+1]).text
#         prev_trans = next_trans
#     print(prev_trans)
#     final_trans = tr.translate(prev_trans, src=las[len(las)-1], dest="ja").text

#     return final_trans
