import requests

def trans(txt, langs):
    url = "https://script.google.com/macros/s/AKfycbybnefLnp6WsVP1Ju7EeN6L1O6BT3ed4Jwc7kOouosn6o6rQHt2EWVPn8vAQcZJ8s8O/exec?"+"txt="+txt+"&langs="+",".join(langs)
    r = requests.get(url)
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
