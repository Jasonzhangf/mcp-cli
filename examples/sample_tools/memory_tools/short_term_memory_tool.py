
import json
import os
from typing import List, Dict, Any

# Define the path for the local JSON file that acts as our cache
# This file will be created in the same directory as the tool script.
CACHE_FILE = os.path.join(os.path.dirname(__file__), "stm_cache.json")

def _load_cache() -> Dict[str, Any]:
    """Loads the cache from the JSON file."""
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_cache(data: Dict[str, Any]):
    """Saves the cache to the JSON file."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving cache: {e}")

def store_short_term_memory(conversation_id: str, interactions: List[Dict[str, str]]):
    """
    Stores temporary details for a conversation, simulating a write to a KV store like Redis.
    This represents the 'Encode' and 'Store' process in STM.

    :param conversation_id: The unique identifier for the conversation.
    :param interactions: A list of interaction dicts, e.g., [{'role': 'user', 'content': 'Hello', 'ts': '...'}].
    """
    print(f"STM-TOOL: Simulating write to Redis for conversation_id: {conversation_id}")
    cache = _load_cache()
    cache[conversation_id] = interactions
    _save_cache(cache)
    return f"Successfully stored {len(interactions)} interactions in short-term memory for conversation {conversation_id}."

def retrieve_short_term_memory(conversation_id: str) -> List[Dict[str, str]]:
    """
    Retrieves the recent interactions for a given conversation.
    This represents the 'Retrieve' aspect before it's erased.

    :param conversation_id: The unique identifier for the conversation.
    :return: A list of interaction dicts or an empty list if not found.
    """
    print(f"STM-TOOL: Simulating read from Redis for conversation_id: {conversation_id}")
    cache = _load_cache()
    return cache.get(conversation_id, [])

def clear_short_term_memory(conversation_id: str):
    """
    Clears the memory for a conversation, simulating TTL expiration or explicit deletion at the end of a task.
    This represents the 'Erase' process.

    :param conversation_id: The unique identifier for the conversation to clear.
    """
    print(f"STM-TOOL: Simulating cache eviction (DEL/EXPIRE) for conversation_id: {conversation_id}")
    cache = _load_cache()
    if conversation_id in cache:
        del cache[conversation_id]
        _save_cache(cache)
        return f"Short-term memory for conversation {conversation_id} has been cleared."
    return f"No short-term memory found for conversation {conversation_id}."

