# server.py
# ============================================================
# Usage:
#   pip install -r requirements.txt
#   python3 server.py
# ============================================================

import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

DATABASE = Path("data/server.db")


def get_db():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL CHECK (status IN ('承認待ち', '承認済み')),
            purpose TEXT NOT NULL,
            command TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()


@app.route("/api/requests", methods=["POST"])
def create_request():
    body = request.get_json()

    server_id = body["id"]
    purpose = body["purpose"]
    command = body["command"]

    db = get_db()
    db.execute(
        """
        INSERT INTO requests (id, status, purpose, command)
        VALUES (?, ?, ?, ?)
        """,
        (server_id, "承認待ち", purpose, command)
    )
    db.commit()
    db.close()

    return jsonify({
        "id": server_id,
        "status": "承認待ち",
        "purpose": purpose,
        "command": command
    }), 201


@app.route("/api/requests/<server_id>", methods=["GET"])
def get_request(server_id):
    db = get_db()
    row = db.execute(
        """
        SELECT id, status, purpose, command, created_at, updated_at
        FROM requests
        WHERE id = ?
        """,
        (server_id,)
    ).fetchone()
    db.close()

    if row is None:
        return jsonify({
            "error": "指定されたIDは存在しません"
        }), 404

    return jsonify(dict(row))


@app.route("/api/requests", methods=["GET"])
def get_requests():
    db = get_db()
    rows = db.execute(
        """
        SELECT id, status, purpose, command, created_at, updated_at
        FROM requests
        ORDER BY created_at DESC
        """
    ).fetchall()
    db.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/requests/<server_id>/approve", methods=["POST"])
def approve_request(server_id):
    db = get_db()

    db.execute(
        """
        UPDATE requests
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        ("承認済み", server_id)
    )

    db.commit()

    row = db.execute(
        """
        SELECT id, status, purpose, command, created_at, updated_at
        FROM requests
        WHERE id = ?
        """,
        (server_id,)
    ).fetchone()

    db.close()

    if row is None:
        return jsonify({
            "error": "指定されたIDは存在しません"
        }), 404

    return jsonify(dict(row))


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "Server Approval API",
        "status": "running"
    })


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)
