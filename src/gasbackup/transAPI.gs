function doGet(e) {
  var p = e.parameter;
  txt = p.txt;
  langs = p.langs.split(",");

  prev_trans = LanguageApp.translate(txt, "ja", langs[0]);
    for(let i=0; i < langs.length-1; i++){
      next_trans = LanguageApp.translate(prev_trans, src=langs[i], dest=langs[i+1])
      prev_trans = next_trans
    }
  final_trans = LanguageApp.translate(prev_trans, src=langs[langs.length-1], "ja")
  return ContentService.createTextOutput(final_trans);
}