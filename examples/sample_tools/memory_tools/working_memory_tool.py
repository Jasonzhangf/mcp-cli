
import json
import os
from typing import List, Dict, Any

# Define the path for the local JSON file that acts as our scratchpad
CACHE_FILE = os.path.join(os.path.dirname(__file__), "wm_scratchpad.json")

def _load_scratchpad() -> Dict[str, Any]:
    """Loads the scratchpad from the JSON file."""
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_scratchpad(data: Dict[str, Any]):
    """Saves the scratchpad to the JSON file."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving scratchpad: {e}")

def update_working_memory(task_id: str, goal: str, current_step: int, intermediate_results: List[Any]):
    """
    Updates the scratchpad for a task, holding immediate information for decision-making.
    This represents the 'Temp Ops Area' for 'Real-Time Ops'.

    :param task_id: The unique identifier for the current task or reasoning chain.
    :param goal: The overall objective of the task.
    :param current_step: The current step number in the reasoning process.
    :param intermediate_results: A list of thoughts, calculations, or partial results.
    """
    print(f"WM-TOOL: Updating scratchpad for task_id: {task_id}")
    scratchpad = _load_scratchpad()
    scratchpad[task_id] = {
        "goal": goal,
        "current_step": current_step,
        "intermediate_results": intermediate_results,
    }
    _save_scratchpad(scratchpad)
    return f"Working memory for task {task_id} updated at step {current_step}."

def retrieve_working_memory(task_id: str) -> Dict[str, Any]:
    """
    Retrieves the current state of the scratchpad for a task.

    :param task_id: The unique identifier for the task.
    :return: A dictionary with the task's goal, step, and results, or an empty dict.
    """
    print(f"WM-TOOL: Retrieving scratchpad for task_id: {task_id}")
    scratchpad = _load_scratchpad()
    return scratchpad.get(task_id, {})

def discard_working_memory(task_id: str):
    """
    Discards the scratchpad for a task once it's completed or no longer needed.
    This represents the 'Discard' process.

    :param task_id: The unique identifier for the task to discard.
    """
    print(f"WM-TOOL: Discarding scratchpad for task_id: {task_id}")
    scratchpad = _load_scratchpad()
    if task_id in scratchpad:
        del scratchpad[task_id]
        _save_scratchpad(scratchpad)
        return f"Working memory for task {task_id} has been discarded."
    return f"No working memory found for task {task_id}."

