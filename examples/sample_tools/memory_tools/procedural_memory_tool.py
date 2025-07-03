
import json
import os
import datetime
from typing import List, Dict, Any, Optional

# Define path for the local JSON file that acts as our skill registry
SKILL_REGISTRY_FILE = os.path.join(os.path.dirname(__file__), "pm_skill_registry.json")

def _load_registry() -> Dict[str, Any]:
    """Loads the skill registry from the JSON file."""
    if not os.path.exists(SKILL_REGISTRY_FILE):
        return {}
    try:
        with open(SKILL_REGISTRY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_registry(data: Dict[str, Any]):
    """Saves the skill registry to the JSON file."""
    try:
        with open(SKILL_REGISTRY_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving registry: {e}")

def register_procedural_skill(
    skill_name: str,
    version: str,
    entry_point: str,
    description: str,
    permissions: Optional[List[str]] = None
):
    """
    Registers a new reusable skill or workflow in the procedural memory.
    This simulates adding a new versioned function to a Git repo + metadata DB.

    :param skill_name: The name of the skill (e.g., "format_document").
    :param version: The semantic version of the skill (e.g., "1.0.0").
    :param entry_point: The path or function name to call (e.g., "formatters.document.run").
    :param description: A brief explanation of what the skill does.
    :param permissions: Optional list of roles or users allowed to execute this skill.
    """
    print(f"PM-TOOL: Registering skill '{skill_name}' version '{version}'.")
    registry = _load_registry()
    
    if skill_name not in registry:
        registry[skill_name] = {"versions": {}}
    
    registry[skill_name]["versions"][version] = {
        "entry_point": entry_point,
        "description": description,
        "permissions": permissions or [],
        "checksum": hex(hash(f"{entry_point}@{version}")), # Mock checksum
        "registered_at": datetime.datetime.utcnow().isoformat()
    }
    # Keep track of the latest version
    registry[skill_name]["latest"] = version
    
    _save_registry(registry)
    return f"Skill '{skill_name}' version '{version}' has been registered."

def find_procedural_skill(skill_name: str, version: str = "latest") -> Dict[str, Any]:
    """
    Finds a specific version of a skill in the registry.

    :param skill_name: The name of the skill to find.
    :param version: The specific version to retrieve. Defaults to "latest".
    :return: A dictionary with the skill's metadata or a 'not found' message.
    """
    print(f"PM-TOOL: Looking up skill '{skill_name}' version '{version}'.")
    registry = _load_registry()
    skill = registry.get(skill_name)
    
    if not skill:
        return f"Skill '{skill_name}' not found."
        
    if version == "latest":
        version = skill.get("latest", "")
        
    skill_version_data = skill.get("versions", {}).get(version)
    
    if not skill_version_data:
        return f"Version '{version}' for skill '{skill_name}' not found."
        
    return {"skill_name": skill_name, "version": version, **skill_version_data}

def apply_procedural_skill(skill_name: str, version: str = "latest", **kwargs) -> str:
    """
    Applies or executes a learned skill, simulating a "muscle memory" action.
    
    :param skill_name: The name of the skill to execute.
    :param version: The version to execute. Defaults to "latest".
    :param kwargs: The arguments to pass to the skill.
    :return: A string indicating the result of the execution.
    """
    print(f"PM-TOOL: Applying skill '{skill_name}' with args: {kwargs}")
    skill_data = find_procedural_skill(skill_name, version)
    
    if isinstance(skill_data, str): # It returned an error message
        return f"Execution failed: {skill_data}"

    # In a real system, this would dynamically load and run the code at skill_data['entry_point']
    print(f"PM-TOOL:   -> SIMULATING EXECUTION of {skill_data['entry_point']}...")
    
    return f"Successfully applied skill '{skill_name}' version '{skill_data['version']}' with arguments {kwargs}."

