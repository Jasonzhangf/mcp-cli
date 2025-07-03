
import json
import os
import datetime
from typing import List, Dict, Any, Optional

# Define paths for the local JSON files
PREFERENCES_FILE = os.path.join(os.path.dirname(__file__), "ltm_preferences.json")
DOCUMENTS_FILE = os.path.join(os.path.dirname(__file__), "ltm_documents.json")

def _load_json_file(file_path: str) -> Dict:
    """Loads data from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_json_file(file_path: str, data: Dict):
    """Saves data to a JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving file {file_path}: {e}")

def save_user_preference(user_id: str, key: str, value: Any):
    """
    Saves a persistent user preference, simulating a write to a SQL table.
    This represents storing durable, structured knowledge.

    :param user_id: The unique identifier for the user.
    :param key: The preference key (e.g., "language", "theme").
    :param value: The value of the preference (can be a string, number, dict, etc.).
    """
    print(f"LTM-TOOL: Saving preference for user {user_id}: {key} = {value}")
    preferences = _load_json_file(PREFERENCES_FILE)
    
    if user_id not in preferences:
        preferences[user_id] = {}
        
    preferences[user_id][key] = {
        "value": value,
        "updated_at": datetime.datetime.utcnow().isoformat()
    }
    _save_json_file(PREFERENCES_FILE, preferences)
    return f"Preference '{key}' for user {user_id} has been saved to long-term memory."

def retrieve_user_preference(user_id: str, key: str) -> Any:
    """
    Retrieves a specific user preference from long-term memory.

    :param user_id: The unique identifier for the user.
    :param key: The preference key to retrieve.
    :return: The value of the preference or a 'not found' message.
    """
    print(f"LTM-TOOL: Retrieving preference for user {user_id}: {key}")
    preferences = _load_json_file(PREFERENCES_FILE)
    return preferences.get(user_id, {}).get(key, f"Preference '{key}' not found for user {user_id}.")

def store_learned_document(doc_id: str, s3_uri: str, summary: str, user_id: Optional[str] = None):
    """
    Stores a reference to a learned document, simulating an entry in a document index.

    :param doc_id: A unique ID for the document.
    :param s3_uri: The URI of the document in an object store like S3.
    :param summary: A summary of the document's content.
    :param user_id: Optional user ID if the document is user-specific.
    """
    print(f"LTM-TOOL: Storing learned document {doc_id} in document index.")
    documents = _load_json_file(DOCUMENTS_FILE)
    
    # Mock embedding for the summary
    embedding = [float(ord(c)) for c in summary[:16].ljust(16, ' ')]
    
    documents[doc_id] = {
        "s3_uri": s3_uri,
        "summary": summary,
        "embedding": embedding,
        "user_id": user_id,
        "indexed_at": datetime.datetime.utcnow().isoformat()
    }
    _save_json_file(DOCUMENTS_FILE, documents)
    return f"Document {doc_id} has been indexed in long-term memory."

def find_relevant_documents(query: str, user_id: Optional[str] = None) -> List[Dict]:
    """
    Finds relevant documents from LTM based on a semantic query.

    :param query: The search query to find relevant documents.
    :param user_id: Optional user ID to restrict the search.
    :return: A list of relevant document records.
    """
    print(f"LTM-TOOL: Searching for documents relevant to '{query}'")
    documents = _load_json_file(DOCUMENTS_FILE)
    results = []
    
    for doc_id, data in documents.items():
        # Filter by user if provided
        if user_id and data.get("user_id") and data.get("user_id") != user_id:
            continue
        
        # Simple keyword search in summary
        if query.lower() in data.get("summary", "").lower():
            results.append({"doc_id": doc_id, **data})
            
    return results if results else "No relevant documents found in long-term memory."

