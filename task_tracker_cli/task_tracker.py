import json
import sys
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

def initialize_tasks_file():
    if not os.path.exists(TASKS_FILE) or os.stat(TASKS_FILE).st_size == 0:
        # Create the file and initialize it with an empty list if it doesn't exist or is empty
        with open(TASKS_FILE, 'w') as file:
            json.dump([], file)

def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # If the file is corrupted or empty, reinitialize it
        print("The tasks file is corrupted or empty. Reinitializing the file.")
        initialize_tasks_file()
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)
def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")

def list_tasks(status=None):
    tasks = load_tasks()
    for task in tasks:
        if not status or task["status"] == status:
            print(f"{task['id']}: {task['description']} [{task['status']}]")
def mark_task(task_id, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}.")
            return
    print(f"Task with ID {task_id} not found.")
def main():
    initialize_tasks_file()
    
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == "add":
        description = " ".join(sys.argv[2:])
        add_task(description)
    elif command == "update":
        task_id = int(sys.argv[2])
        description = " ".join(sys.argv[3:])
        update_task(task_id, description)
    elif command == "delete":
        task_id = int(sys.argv[2])
        delete_task(task_id)
    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)
    elif command == "mark-in-progress":
        task_id = int(sys.argv[2])
        mark_task(task_id, "in-progress")
    elif command == "mark-done":
        task_id = int(sys.argv[2])
        mark_task(task_id, "done")
    else:
        print("Unknown command. Available commands: add, update, delete, list, mark-in-progress, mark-done")

if __name__ == "__main__":
    main()
