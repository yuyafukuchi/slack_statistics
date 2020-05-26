# slack_statistics

あるワークスペースのいろいろなChannelにおけるランキングを取得できます。

ランキングは現状
- 発言数ランキング
- リアクション数ランキング

があります

## 準備
https://qiita.com/ykhirao/items/3b19ee6a1458cfb4ba21
を参考にするといい

1. アプリの作成

https://api.slack.com/apps からランキングを取得したいワークスペースのアプリを作成する

2. スコープの設定
   
スコープの設定をします。`channels:history`,`channels:read`,`users:profile:read`の三つのスコープを追加します。

3. Slackにアプリをインストール

[Install App To Team]を押してスラックにアプリをインストールします。また、そのページにあるOAuth Access Tokenを控えておきます。

4. Tokenの設定

本プロジェクトの`config.ini`にトークンを記述します。

`config.ini`ではトークンの他にターゲットのチャンネルや何位までランキングするかを設定することができます

## requirements
python 3.7.0+

## Install
```
git clone https://github.com/yuyafukuchi/slack_statistics
cd slack_statistics
pip install -r requirements.txt
```

## Usage
```
python main.py
```

すると以下のようなWindowが出てきます
<img width="638" alt="スクリーンショット 2020-05-22 22 41 48" src="https://user-images.githubusercontent.com/36098400/82908721-5606e700-9fa3-11ea-9c5c-42a3ba5553fb.png">

oldestday - latestdayの範囲のランキングを表示します

2020-01-01のようにゼロ埋めで日付を記述してください

「実行」ボタンを押すとランキングが表示されます
