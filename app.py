from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

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
            "Category": {"rich_text": [{"text": {"content": data.get("category")}}]},
            "File Link": {"url": data.get("file_link")},
            "Notes": {"rich_text": [{"text": {"content": data.get("notes")}}]},
            "Date Added": {"date": {"start": data.get("date")}},
            "Status": {"rich_text": [{"text": {"content": data.get("status", "Draft")}}]}
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
    with app.test_client() as c:
        response = c.post("/sync", json={
            "name": "Test Document",
            "category": "Internal Standard",
            "file_link": "https://example.com/test-document",
            "notes": "This is a test entry to verify webhook functionality.",
            "date": "2025-04-21",
            "status": "Draft"
        })
        print("Test sync response:", response.status_code, response.get_data(as_text=True))

    app.run(debug=True)
