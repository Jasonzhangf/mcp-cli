
import json
import os
import datetime
from typing import List, Dict, Any, Optional

# Define paths for the local JSON files
EVENT_LOG_FILE = os.path.join(os.path.dirname(__file__), "em_event_log.json")
VECTOR_INDEX_FILE = os.path.join(os.path.dirname(__file__), "em_vector_index.json")

def _load_json_file(file_path: str) -> List[Dict] or Dict:
    """Loads data from a JSON file."""
    if not os.path.exists(file_path):
        return [] if file_path.endswith("log.json") else {}
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return [] if file_path.endswith("log.json") else {}

def _save_json_file(file_path: str, data: Any):
    """Saves data to a JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving file {file_path}: {e}")

def _generate_mock_embedding(text: str) -> List[float]:
    """Generates a simplistic, deterministic mock embedding for simulation purposes."""
    # In a real scenario, this would be a call to an embedding model.
    # Here, we use character codes to create a pseudo-vector.
    return [float(ord(c)) for c in text[:16].ljust(16, ' ')] # Mock a 16-dim vector

def record_episodic_event(
    event_id: str,
    agent_id: str,
    user_id: str,
    text: str,
    meta: Optional[Dict[str, Any]] = None
):
    """
    Records a detailed, event-specific experience, simulating a dual-write to an event log and a vector DB.
    This represents the 'Experience -> Encode -> Store' flow.

    :param event_id: A unique ID for the event.
    :param agent_id: The ID of the agent in the interaction.
    :param user_id: The ID of the user in the interaction.
    :param text: The content of the event/interaction.
    :param meta: Optional dictionary for additional metadata.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"EM-TOOL: Recording event {event_id} for user {user_id}.")

    # 1. Append to the event log (simulating ClickHouse/TimescaleDB)
    print("EM-TOOL:   -> Writing to append-only event log...")
    event_log = _load_json_file(EVENT_LOG_FILE)
    event_log.append({
        "event_id": event_id,
        "agent_id": agent_id,
        "user_id": user_id,
        "timestamp": timestamp,
        "text": text,
        "meta": meta or {}
    })
    _save_json_file(EVENT_LOG_FILE, event_log)

    # 2. Add to the vector index (simulating Milvus/Weaviate)
    print("EM-TOOL:   -> Updating vector index...")
    vector_index = _load_json_file(VECTOR_INDEX_FILE)
    vector_index[event_id] = {
        "embedding": _generate_mock_embedding(text),
        "user_id": user_id,
        "timestamp": timestamp
    }
    _save_json_file(VECTOR_INDEX_FILE, vector_index)

    return f"Successfully recorded episodic event {event_id}."

def recall_episodic_events(
    user_id: str,
    query_text: str,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Recalls relevant past events based on semantic similarity and metadata filters.
    This represents the 'Recall' process, simulating a hybrid search.

    :param user_id: The user ID to filter events for ('who').
    :param query_text: The text to search for semantically ('what').
    :param limit: The maximum number of events to return.
    :return: A list of matching event log entries.
    """
    print(f"EM-TOOL: Recalling events for user {user_id} with query: '{query_text}'")

    # 1. Simulate semantic search
    print("EM-TOOL:   -> Performing mock vector similarity search...")
    query_embedding = _generate_mock_embedding(query_text)
    vector_index = _load_json_file(VECTOR_INDEX_FILE)
    
    # Filter by user_id and calculate mock similarity (dot product)
    candidates = []
    for event_id, data in vector_index.items():
        if data.get("user_id") == user_id:
            sim = sum(q*v for q, v in zip(query_embedding, data.get("embedding", [])))
            candidates.append({"event_id": event_id, "similarity": sim})

    # Sort by similarity and get top N
    candidates.sort(key=lambda x: x["similarity"], reverse=True)
    top_event_ids = [c["event_id"] for c in candidates[:limit]]
    print(f"EM-TOOL:   -> Found top candidates by similarity: {top_event_ids}")

    # 2. Retrieve full event data from the log
    event_log = _load_json_file(EVENT_LOG_FILE)
    results = [event for event in event_log if event["event_id"] in top_event_ids]
    
    return results

