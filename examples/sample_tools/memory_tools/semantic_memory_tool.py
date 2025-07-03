
import json
import os
from typing import List, Dict, Any, Tuple

# Define paths for the local JSON files
GRAPH_FILE = os.path.join(os.path.dirname(__file__), "sm_knowledge_graph.json")
ENTITY_INDEX_FILE = os.path.join(os.path.dirname(__file__), "sm_entity_index.json")

def _load_json_file(file_path: str) -> List or Dict:
    """Loads data from a JSON file."""
    if not os.path.exists(file_path):
        return [] if file_path.endswith("graph.json") else {}
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return [] if file_path.endswith("graph.json") else {}

def _save_json_file(file_path: str, data: Any):
    """Saves data to a JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving file {file_path}: {e}")

def add_semantic_fact(subject: str, relation: str, obj: str):
    """
    Stores a new fact as a triple in the knowledge graph.
    This represents storing concepts and relationships.

    :param subject: The subject entity of the fact (e.g., "London").
    :param relation: The relationship (e.g., "is the capital of").
    :param obj: The object entity of the fact (e.g., "United Kingdom").
    """
    print(f"SM-TOOL: Adding fact to knowledge graph: ({subject}, {relation}, {obj})")
    graph = _load_json_file(GRAPH_FILE)
    
    # Avoid duplicate facts
    new_fact = {"subject": subject, "relation": relation, "object": obj}
    if new_fact not in graph:
        graph.append(new_fact)
        _save_json_file(GRAPH_FILE, graph)
        return f"Fact ({subject}, {relation}, {obj}) added to Semantic Memory."
    return f"Fact ({subject}, {relation}, {obj}) already exists."

def add_entity_details(entity_name: str, description: str, metadata: Dict[str, Any] = None):
    """
    Adds descriptive details for an entity, simulating indexing in Elasticsearch or a vector DB.

    :param entity_name: The name of the entity to describe.
    :param description: A text description of the entity.
    :param metadata: Optional additional structured data.
    """
    print(f"SM-TOOL: Indexing details for entity: {entity_name}")
    entity_index = _load_json_file(ENTITY_INDEX_FILE)
    
    # Mock embedding generation
    embedding = [float(ord(c)) for c in description[:16].ljust(16, ' ')]
    
    entity_index[entity_name] = {
        "description": description,
        "embedding": embedding,
        "metadata": metadata or {}
    }
    _save_json_file(ENTITY_INDEX_FILE, entity_index)
    return f"Details for entity '{entity_name}' have been indexed."

def query_semantic_memory(query: str) -> List[Dict[str, str]]:
    """
    Retrieves facts and concepts from memory.
    This simulates a hybrid query (e.g., keyword + graph traversal).

    :param query: The search query, which can be a keyword or a simple question.
    :return: A list of relevant facts or entity descriptions.
    """
    print(f"SM-TOOL: Querying semantic memory with: '{query}'")
    results = []
    
    # 1. Simple keyword search in entity descriptions (simulating Elasticsearch)
    entity_index = _load_json_file(ENTITY_INDEX_FILE)
    for name, data in entity_index.items():
        if query.lower() in data.get("description", "").lower() or query.lower() in name.lower():
            results.append({"type": "entity_description", "entity": name, "details": data})

    # 2. Simple graph pattern matching (simulating Neo4j/SPARQL)
    graph = _load_json_file(GRAPH_FILE)
    for fact in graph:
        if query.lower() in fact["subject"].lower() or query.lower() in fact["object"].lower():
            results.append({"type": "fact", "data": fact})
            
    return results if results else "No semantic information found."

