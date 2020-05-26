# slack_statistics

あるワークスペースのいろいろなChannelにおけるランキングを取得できます。
ランキングは現状
- 発言数ランキング
- リアクション数ランキング
があります

# 準備
https://qiita.com/ykhirao/items/3b19ee6a1458cfb4ba21
を参考にするといい

1. アプリの作成 
https://api.slack.com/apps からアプリを作成する
2. スコープの設定
スコープの設定をします。`channels:history`,`channels:read`,`users:read`の三つのスコープを追加します。

3. Slackにアプリをインストール
[Install App To Team]を押してスラックにアプリをインストールします。また、そのページにあるOAuth Access Tokenを控えておきます。
4. Tokenの設定
本プロジェクトの`config.ini`にトークンを記述します。
