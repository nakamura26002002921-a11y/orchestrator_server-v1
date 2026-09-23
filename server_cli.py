# server_cli.py
# ============================================================
# orchestrator_server にリクエストを登録するCLI
#
# Usage:
#   python server_cli.py --id XXX --cmd "echo helloworld" --purpose "テスト" --approval-state False --url https://xxxx.trycloudflare.com
#
# ※ サーバ(server.py)を先に起動しておくこと
#   python3 server.py
# ============================================================

import argparse
import json
import sys
import requests

def str2bool(value: str) -> bool:
    if isinstance(value, bool):
        return value
    if value.lower() in ("true", "1", "yes", "y"):
        return True
    if value.lower() in ("false", "0", "no", "n"):
        return False
    raise argparse.ArgumentTypeError(f"boolとして解釈できません: {value}")


def create_request(
    server_id: str,
    cmd: str,
    purpose: str,
    approval_state: bool,
    base_url: str,
) -> dict:
    url = f"{base_url}/api/requests"
    payload = {
        "id": server_id,
        "command": cmd,
        "purpose": purpose,
    }
    response = requests.post(url, json=payload)
    if response.status_code not in (200, 201):
        return {
            "error": True,
            "status_code": response.status_code,
            "detail": response.json() if response.content else None,
        }

    result = response.json()
    if approval_state:
        approve_url = f"{base_url}/api/requests/{server_id}/approve"
        approve_response = requests.post(approve_url)
        if approve_response.status_code == 200:
            result = approve_response.json()
        else:
            result = {
                "error": True,
                "status_code": approve_response.status_code,
                "detail": approve_response.json() if approve_response.content else None,
            }
    return result


def parse_args():
    parser = argparse.ArgumentParser(
        description="orchestrator_server にリクエストを登録するCLI"
    )
    parser.add_argument("--id", required=True, help="登録するリクエストのID")
    parser.add_argument("--cmd", required=True, help='実行コマンド (例: "echo helloworld")')
    parser.add_argument("--purpose", required=True, help="目的 (例: サーバテスト)")
    parser.add_argument(
        "--approval-state",
        type=str2bool,
        default=False,
        help="True の場合は登録と同時に承認済みにする (デフォルト: False)",
    )
    parser.add_argument(
        "--url",
        required=True,
        help="サーバのベースURL (必須。例: https://xxxx.trycloudflare.com)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = create_request(
        server_id=args.id,
        cmd=args.cmd,
        purpose=args.purpose,
        approval_state=args.approval_state,
        base_url=args.url,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
