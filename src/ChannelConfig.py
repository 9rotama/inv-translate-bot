class ChannelConfig:
  def __init__(self, id):
    self.channel_id = id
    self.started: bool = False
    self.langs: list[str] = ["en"] #中継言語
    self.show_origin_text: bool = True #原文を表示するかどうか
    self.origin_lang: str = "ja" #原文の言語
