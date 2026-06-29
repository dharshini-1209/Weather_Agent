import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    """
    Load previous conversation from memory.json.
    """

    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_memory(messages):
    """
    Save conversation into memory.json.
    """

    with open(MEMORY_FILE, "w") as file:
        json.dump(messages, file, indent=4)


def clear_memory():
    """
    Clear the conversation history.
    """

    with open(MEMORY_FILE, "w") as file:
        json.dump([], file, indent=4)


# -----------------------------
# Test memory.py
# -----------------------------
if __name__ == "__main__":

    print("Current Memory:\n")

    print(load_memory())