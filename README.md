# Server Approval API

## 1. 必要なもの

Python 3 と `cloudflared` をインストールしてください。

```bash
python3 --version
cloudflared --version
````

 ## 2\. プロジェクトへ移動

```
cd server-approval
```

 ## 3\. 仮想環境を作成

```
python3 -m venv .venv
source .venv/bin/activate
```

 ## 4\. パッケージをインストール

```
pip install -r requirements.txt
```

 ## 5\. Flaskサーバーを起動

 ターミナル1で実行します。

```
python3 server.py
```

 サーバーは `http://127.0.0.1:5000` で起動します。

 ## 6\. Cloudflare Tunnelを起動

 別のターミナルを開き、以下を実行します。

```
cd server-approval
cloudflared tunnel --url http://127.0.0.1:5000
```

 表示された、

```
https://xxxxx.trycloudflare.com
```

 が公開URLです。

 ## 7\. 動作確認

 公開URLにアクセスします。

```
curl https://xxxxx.trycloudflare.com/
```

 以下が返れば起動成功です。

```
{
  "name": "Server Approval API",
  "status": "running"
}
```

 ## 8\. 起動時の最終形

 ターミナル1：

```
cd server-approval
source .venv/bin/activate
python3 server.py
```

 ターミナル2：

```
cd server-approval
cloudflared tunnel --url http://127.0.0.1:5000
```

 Cloudflare Tunnelに表示された `https://xxxxx.trycloudflare.com` をPWAのAPI URLとして使用します。

 ## 9\. 停止

 FlaskとCloudflare Tunnelをそれぞれ起動しているターミナルで `Ctrl + C` を押すと停止できます。

```

```
