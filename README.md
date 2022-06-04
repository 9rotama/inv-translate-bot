# 無駄翻訳bot

![Frame 2](https://user-images.githubusercontent.com/65887771/171993445-42c0909b-fd47-4283-b719-16b94dd7838c.png)

Discordで送信された日本語のメッセージを勝手に再翻訳してくれるbot

## 使い方

```^start```


翻訳開始

```^set```

現在設定されている中継言語を表示

```^set [1番目の言語コード] [2番めの言語コード] ...```

中継する言語を設定

※10ヶ国語まで設定できます

言語コードの表 → https://cloud.google.com/translate/docs/languages?hl=ja

```^stop```

翻訳を終了

## 使ったもの

- discord.py 1.7.3
- Google App Script (翻訳部分)
- Heroku

# discordpy-startup

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

- Herokuでdiscord.pyを始めるテンプレートです。
- Use Template からご利用ください。
- 使い方はこちら： [Discord Bot 最速チュートリアル【Python&Heroku&GitHub】 - Qiita](https://qiita.com/1ntegrale9/items/aa4b373e8895273875a8)

## 各種ファイル情報

### discordbot.py
PythonによるDiscordBotのアプリケーションファイルです。

### requirements.txt
使用しているPythonのライブラリ情報の設定ファイルです。

### Procfile
Herokuでのプロセス実行コマンドの設定ファイルです。

### runtime.txt
Herokuでの実行環境の設定ファイルです。

### app.json
Herokuデプロイボタンの設定ファイルです。

### .github/workflows/flake8.yaml
GitHub Actions による自動構文チェックの設定ファイルです。

### .gitignore
Git管理が不要なファイル/ディレクトリの設定ファイルです。

### LICENSE
このリポジトリのコードの権利情報です。MITライセンスの範囲でご自由にご利用ください。

### README.md
このドキュメントです。
