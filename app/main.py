from flask import Flask, request, jsonify
from uuid import uuid4
from threading import Thread
from app.tasks import enqueue_batches, scheduler_loop, ingestion_store
import os

app = Flask(__name__)

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.json
    ids = data.get("ids")
    priority = data.get("priority")

    if not ids or priority not in ["HIGH", "MEDIUM", "LOW"]:
        return jsonify({"error": "Invalid payload"}), 400

    ingestion_id = str(uuid4())
    enqueue_batches(ingestion_id, ids, priority)

    # Run scheduler in background thread
    t = Thread(target=scheduler_loop)
    t.start()

    return jsonify({"ingestion_id": ingestion_id})

@app.route('/status/<ingestion_id>', methods=['GET'])
def get_status(ingestion_id):
    if ingestion_id not in ingestion_store:
        return jsonify({"error": "Invalid ingestion_id"}), 404

    data = ingestion_store[ingestion_id]
    return jsonify({
        "ingestion_id": ingestion_id,
        "status": data["status"],
        "batches": [
            {
                "batch_id": b_id,
                "ids": b_data["ids"],
                "status": b_data["status"]
            } for b_id, b_data in data["batch_status"].items()
        ]
    })

if __name__ == "__main__" or __name__ == "app.main":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)