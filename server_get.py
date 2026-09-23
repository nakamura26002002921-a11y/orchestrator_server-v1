# server_get.py
# ============================================================
# orchestrator_server から指定IDのリクエストを取得するCLI
#
# Usage:
#   python server_get.py --id XXX
#
# 出力例:
#   {
#     "XXX": {
#       "実行コマンド": "echo helloworld",
#       "目的": "テスト",
#       "承認": false
#     }
#   }
#
# ※ サーバ(server.py)を先に起動しておくこと
#   python3 server.py
# ============================================================

import argparse
import json

import requests

DEFAULT_BASE_URL = "http://127.0.0.1:5000"


def get_request(server_id: str, base_url: str = DEFAULT_BASE_URL) -> dict:
    url = f"{base_url}/api/requests/{server_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return {
            "error": True,
            "status_code": response.status_code,
            "detail": response.json() if response.content else None,
        }
    data = response.json()
    return {
        server_id: {
            "実行コマンド": data.get("command"),
            "目的": data.get("purpose"),
            "承認": data.get("status") == "承認済み",
        }
    }

def parse_args():
    parser = argparse.ArgumentParser(
        description="orchestrator_server から指定IDのリクエストを取得するCLI"
    )
    parser.add_argument("--id", required=True, help="取得するリクエストのID")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"サーバのベースURL (デフォルト: {DEFAULT_BASE_URL})",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    result = get_request(server_id=args.id, base_url=args.base_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
