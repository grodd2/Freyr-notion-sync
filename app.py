from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests (CORS) so the test HTML can call this API

# Notion API keys from Replit Secrets
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

# Standard Notion API headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

@app.route("/sync", methods=["POST"])
def sync_to_notion():
    data = request.json

    notion_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": data.get("name")}}]},
            "Category": {"select": {"name": data.get("category")}},
            "Status": {"select": {"name": data.get("status", "Draft")}},
            "File Link": {"url": data.get("file_link")}  # only if a property by this name exists

        }
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=notion_data)

    if response.status_code == 200 or response.status_code == 201:
        return jsonify({"message": "Synced successfully!"}), 200
    else:
        return jsonify({"error": response.text}), 400

@app.route("/", methods=["GET"])
def home():
    return "Freyr Notion Sync is running.", 200

if __name__ == "__main__":
    app.run(debug=True)

