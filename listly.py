import os
import json
from datetime import datetime
import csv

listly = "listly.json"
tasks = []
history = []

def exists():
    global tasks
    if not os.path.exists(listly):
        with open (listly, "w") as file:
            json.dump(tasks, file, indent= 4)
    return

def load():
    global tasks
    try:
        with open(listly, "r") as file:
            loaded = json.load(file)
            tasks = [
                {
                    **task,
                    "due_date": datetime.strptime(task["due_date"], "%Y-%m-%d") if task["due_date"] != "not-set" else "not-set"
                }
                for task in loaded
            ]
    except FileNotFoundError:
        print("File was not found. Creating a new file...")
        exists()
        tasks = []
    except json.JSONDecodeError:
        print("The file is corrupted. Resetting its data....")
        tasks = []
        save()

def save():
    global tasks
    try:
        tasks_to_save = [
            {
                **task,
                "due_date": task["due_date"].strftime("%Y-%m-%d") if isinstance(task["due_date"], datetime) else task["due_date"]
            }
            for task in tasks
        ]
        with open(listly, "w") as file:
            json.dump(tasks_to_save, file, indent=4)
    except PermissionError:
        print("Permission denied. Unable to save the file.")

def saved_state():
    global tasks, history
    history.append([task.copy() for task in tasks])

def generate_id():
    global tasks
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def add(description):
    global tasks
    saved_state()
    task = {
        "id" : generate_id(),
        "description" : description,
        "status" : "in-progress",
        "due_date": "not-set",
        "priority": "low"
    }
    tasks.append(task)
    save()
    print(f"Task added successfully (ID: {task['id']})")
    return 

def update(task_id, new_desc):
    global tasks
    saved_state()
    for task in tasks:
        if int(task_id) == int(task["id"]):  
            task["description"] = new_desc
            print(f"Task updated successfully (ID: {task['id']})")  
            save()
            return
    print("Task not found") 

def view():
    global tasks
    if not tasks:
        print("Task not found")
    for task in tasks:
        print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Priority: {task['priority']} | Due Date: {task['due_date']}")
    return

def done(task_id):
    global tasks
    saved_state()
    for task in tasks:
        if int(task["id"]) == int(task_id):
            task["status"] = "done"
            save()
            print(f"Task marked as done (ID: {task_id})")
            return

def remove(task_id):
    global tasks
    saved_state()
    for task in tasks:
        if int(task_id) == int(task["id"]):
            tasks.remove(task)
            print(f"Task removed successfully.")
            save()
            return
    print("Task not found")

def date(task_id, date_str):
    global tasks
    saved_state()
    try:
        due_date = datetime.strptime(date_str, "%Y-%m-%d")
        for task in tasks:
            if int(task_id) == task["id"]:
                task["due_date"] = due_date  
                print(f"Due date added successfully (ID: {task_id})")
                save()
                return
        print("Task not found")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

def priority(task_id, priority):
    global tasks
    saved_state()
    for task in tasks:
        if int(task_id == task["id"]):
            if task["priority"] == priority:
                print(f"task is already set to {priority} priority.")
            else:   
                task["priority"] = priority
                print("priority added successfully")
                save()
                return

def sort_priority(reverse=False):
    global tasks
    priority_order = {"high": 1, "medium": 2, "low": 3}
    sorted_tasks = sorted(
        tasks,
        key=lambda task: priority_order.get(task.get("priority", "low"), 3),
        reverse=reverse
    )
    display_sorted_tasks(sorted_tasks)

def sort_due_date(reverse=False):
    global tasks
    sorted_tasks = sorted(
        tasks,
        key=lambda task: task["due_date"] if isinstance(task["due_date"], datetime) else datetime(9999, 12, 31),
        reverse=reverse
    )
    display_sorted_tasks(sorted_tasks)

def display_sorted_tasks(sorted_tasks):
    if not sorted_tasks:
        print("No tasks to display.")
        return
    for task in sorted_tasks:
        print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Priority: {task['priority']} | Due Date: {task['due_date']}")

def filter(choice):
    global tasks
    if not tasks:
        print("no tasks found")
    if choice == "in-progress":
        for task in tasks:
            if task["status"] == "in-progress":
                print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Priority: {task['priority']} | Due Date: {task['due_date']}")
    elif choice == "done":
        for task in tasks:
            if task["status"] == "done":
                print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Priority: {task['priority']} | Due Date: {task['due_date']}")
    elif choice == "low":
        for task in tasks:
            if task["priority"] == "low":
                print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Priority: {task['priority']} | Due Date: {task['due_date']}")
    elif choice == "medium":
        for task in tasks:
            if task["priority"] == "medium":
                print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Priority: {task['priority']} | Due Date: {task['due_date']}")
    elif choice == "high":
        for task in tasks:
            if task["priority"] == "high":
                print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Priority: {task['priority']} | Due Date: {task['due_date']}")

def undo():
    global tasks, history
    if not history:
        print("Nothing to undo")
        save
        return
    tasks = history.pop()
    save()

def export_csv(name = "tasks.csv"):
    global tasks
    if not name.endswith(".csv"):
        name +=".csv"
    with open (name, "w", newline= "", encoding= "utf-8") as file:
        writer = csv.DictWriter(
        file,
        fieldnames=["id", "description", "status", "due_date", "priority"]
        )
        writer.writeheader
        for task in tasks:
            task_write = task.copy()
            if isinstance(task_write["due_date"], datetime):
                task_write["due-date"] = task_write["due_date"].strftime("%Y-%m-%d")
            writer.writerow(task_write)
    print(f"Task exported successfully to {name}")

def main():
    exists()
    load()
    print("welcome to listly! type 'help' to see a list of commands!: ")
    while True:
        command = input("command:")
        if command.lower() == "help":
            print("add: add a task")
            print("update: update an existing task")
            print("remove: remove an existing task")
            print("done: mark a task as done")
            print("view: lets you see a list of all tasks")
            print("date: adds a due date")
            print("priority: changes task priority")
            print("sort: sort your list by priority or due date")
            print("filter: filter your list by priority or status")
            print("undo: deletes the last task added.")
            print("export: exports your tasks to a CSV file.")
            print("Exit: exits the program")
            continue
        elif command.lower() == "add":
            while True:
                try:
                 desc = input("task:")
                 if not desc.isspace:
                     raise NameError
                 else:
                    add(desc)
                    break
                except NameError:
                    print("Task cannot be empty.")
                    continue
        elif command.lower() == "update":
            try:
                upd_id = input("Enter the id of the task you want to update: ")
                descrip = input("new task: ")
                if not  descrip.isspace:
                    raise NameError
                update(upd_id, descrip)
            except ValueError:
                print("id must be a number.")
                continue
            except NameError:
                print("Task cannot be empty")
                continue
        elif command.lower() == "remove":
            try:
             rem_id = input("Enter the id of the task you want to remove: ")
             remove(rem_id)
            except ValueError:
                print("id must be a number.")
                continue
        elif command.lower() == "done":
            while True:
                try:
                    sure = input("Are you sure you want to mark task as done? (y/n)")
                    if sure.lower() == "y":
                        try:
                            don_id = input("Enter task id: ")
                            done(don_id)
                        except ValueError:
                            print("id must be a number.")
                            continue
                    elif sure.lower() == "n":
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Answer with y for yes and n for no only")
                    continue
        elif command.lower() == "view":
            view()
        elif command.lower() == "date":
            while True:
                try:
                    dat_id = int(input("Enter your id: "))
                    break
                except ValueError:
                    print("id must be an integer")
                    continue
            data = input("Enter the due date:")
            date(dat_id, data)
        elif command.lower() =="priority":
            while True:
                try:
                    prio_id = int(input("Enter your id: "))
                    type = input("Enter your priority: ")
                    if type.lower() not in ["low", "medium", "high"]:
                        raise NameError
                    priority(prio_id, type)
                    break
                except ValueError:
                    print("id must be an integer")
                    continue            
                except NameError:
                    print("Priority can only be low, medium, or high.")
        elif command.lower() == "sort":
            while True:
                try:
                    choice = input("sort by priority or date?: ")
                    if choice == "priority":
                        order = input("ascending (low to high) or descending (high to low): ")
                        if order == "descending":
                            reverse = True
                        elif order == "ascending":
                            reverse = False
                        else:
                            raise  ValueError
                        reverse = True if order == "descending" else False
                        sort_priority(reverse)
                    elif choice == "date":
                        order = input("ascending (low to high) or descending (high to low):")
                        if order == "descending":
                            reverse = True
                        elif order == "ascending":
                            reverse = False
                        else:
                            raise  ValueError                   
                        sort_due_date(reverse)
                    else:
                        raise ValueError
                except ValueError:
                    print("Invalid choice.")
                    continue
        elif command.lower() == "filter":
            while True:
                try:
                    choice = input("filter by status or priority: ")
                    if choice.lower() not in ["status", "priority"]:
                        raise ValueError
                    break
                except ValueError:
                    print("you can only filter by status or priority")
                    continue
            if choice.lower() == "status":
                while True:
                    try:
                        filtered = input("filter by in-progress or done: ") 
                        if filtered not in ["in-progress", "done"]:
                            raise ValueError
                        filter(filtered)
                        break
                    except ValueError:
                        print("You can only use in-progress or done as filter.")
            elif choice.lower()== "priority":
                while True:
                    try:
                        filtered = input("filter by low, medium, or high: ")
                        if filtered not in ["low", "medium", "high"]:
                            raise ValueError
                        filter(filtered)
                        break
                    except ValueError:
                        print("You can only filter by low, medium or high.")
                        continue
        elif command.lower() == "undo":
            undo()
            print("undo done successfully!")
        elif command.lower() == "export":
            name = input("Enter the name of the new file: ")
            export_csv(name)
        elif command.lower() == "exit":
            break
        else:
            print("command not found")


if __name__ == "__main__":
    main()