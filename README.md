# Server Approval API

## 1. 必要なもの

Python 3 と `cloudflared` をインストールしてください。

```bash
python3 --version
cloudflared --version
```

## 2. プロジェクトへ移動

```
cd server-approval
```

## 3. 仮想環境を作成

```
python3 -m venv .venv
source .venv/bin/activate
```

## 4. パッケージをインストール

```
pip install -r requirements.txt
```

## 5. Flaskサーバーを起動

ターミナル1で実行します。

```
python3 server.py
```

サーバーは `http://127.0.0.1:5000` で起動します。

## 6. Cloudflare Tunnelを起動

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

## 7. 動作確認

公開URLにアクセスします。

```
curl https://xxxxx.trycloudflare.com/
```

以下が返れば起動成功です。

```json
{
  "name": "orchestrator_server",
  "status": "ok"
}
```

## 8. 起動時の最終形

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

## 9. CLIツールの使い方

サーバー起動後、別のターミナルから以下のCLIでリクエストの登録・取得ができます。
（仮想環境を有効化した状態で実行してください）

どちらのCLIも `--url` でサーバのベースURLを指定します。**`--url` は必須オプションです。省略するとエラーになります。**
ローカルで動かしている場合は `--url http://127.0.0.1:5000` を、Cloudflare Tunnel経由の場合は手順6で表示された `https://xxxxx.trycloudflare.com` を指定してください。

### 9-1. リクエストを登録する (`server_cli.py`)

```
python server_cli.py --id XXX --cmd "echo helloworld" --purpose "テスト" --approval-state False --url "https://xxxxx.trycloudflare.com"
```

| オプション | 内容 |
| --- | --- |
| `--id` | リクエストの一意なID（必須） |
| `--cmd` | 実行コマンド（必須） |
| `--purpose` | 目的（必須） |
| `--approval-state` | `True` を指定すると登録と同時に承認済みにする（デフォルト: `False`） |
| `--url` | サーバのベースURL（**必須**。例: `https://xxxxx.trycloudflare.com` または `http://127.0.0.1:5000`） |

実行すると以下のようなJSONが表示されます。

```json
{
  "id": "XXX",
  "status": "承認待ち",
  "purpose": "テスト",
  "command": "echo helloworld"
}
```

`--url` を指定しなかった場合は、以下のようにエラーになり実行されません。

```
server_cli.py: error: the following arguments are required: --url
```

### 9-2. リクエストを取得する (`server_get.py`)

```
python server_get.py --id XXX --url "https://xxxxx.trycloudflare.com"
```

| オプション | 内容 |
| --- | --- |
| `--id` | 取得するリクエストのID（必須） |
| `--url` | サーバのベースURL（**必須**。例: `https://xxxxx.trycloudflare.com` または `http://127.0.0.1:5000`） |

実行すると以下のようなJSONが表示されます。

```json
{
  "XXX": {
    "実行コマンド": "echo helloworld",
    "目的": "テスト",
    "承認": false
  }
}
```

`"承認"` はサーバー上の `status` を変換したものです。`"承認待ち"` の場合は `false`、`"承認済み"` の場合は `true` になります。

`--url` を指定しなかった場合は、以下のようにエラーになり実行されません。

```
server_get.py: error: the following arguments are required: --url
```

## 10. 停止

FlaskとCloudflare Tunnelをそれぞれ起動しているターミナルで `Ctrl + C` を押すと停止できます。
