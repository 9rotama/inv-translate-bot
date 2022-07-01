function doGet(e) {
  var p = e.parameter;
  txt = p.txt;
  langs = p.langs.split(",");
  origin_lang = p.origin_lang

  prev_trans = LanguageApp.translate(txt, origin_lang, langs[0]);
    for(let i=0; i < langs.length-1; i++){
      next_trans = LanguageApp.translate(prev_trans, src=langs[i], dest=langs[i+1])
      prev_trans = next_trans
    }
  final_trans = LanguageApp.translate(prev_trans, src=langs[langs.length-1], origin_lang)
  return ContentService.createTextOutput(final_trans);
}