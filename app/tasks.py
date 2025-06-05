import time
import threading
from collections import defaultdict
from uuid import uuid4
import queue

PRIORITY_MAP = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
BATCH_SIZE = 3
RATE_LIMIT_SECONDS = 5

task_queue = queue.PriorityQueue()
ingestion_store = {}
processing_lock = threading.Lock()

def split_into_batches(ids):
    for i in range(0, len(ids), BATCH_SIZE):
        yield ids[i:i + BATCH_SIZE]

def simulate_external_fetch(id):
    time.sleep(1)
    return {"id": id, "data": "processed"}

def process_batch(ingestion_id, batch_id, ids):
    ingestion_store[ingestion_id]['batch_status'][batch_id]['status'] = "triggered"
    for i in ids:
        simulate_external_fetch(i)
    ingestion_store[ingestion_id]['batch_status'][batch_id]['status'] = "completed"

def get_overall_status(batch_status):
    statuses = [b['status'] for b in batch_status.values()]
    if all(s == "yet_to_start" for s in statuses):
        return "yet_to_start"
    elif all(s == "completed" for s in statuses):
        return "completed"
    return "triggered"

def scheduler_loop():
    with processing_lock:
        while not task_queue.empty():
            priority, timestamp, ingestion_id, batch_id, ids = task_queue.get()
            process_batch(ingestion_id, batch_id, ids)
            ingestion_store[ingestion_id]['status'] = get_overall_status(
                ingestion_store[ingestion_id]['batch_status']
            )
            time.sleep(RATE_LIMIT_SECONDS)

def enqueue_batches(ingestion_id, ids, priority):
    ingestion_store[ingestion_id] = {
        "status": "yet_to_start",
        "batch_status": {}
    }

    for batch_ids in split_into_batches(ids):
        batch_id = str(uuid4())
        ingestion_store[ingestion_id]["batch_status"][batch_id] = {
            "ids": batch_ids,
            "status": "yet_to_start"
        }
        task_queue.put((
            PRIORITY_MAP[priority],
            time.time(),
            ingestion_id,
            batch_id,
            batch_ids
        ))
