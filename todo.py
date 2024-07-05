import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


TASKS_FILE = 'tasks.json'


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)


def add_task():
    title = simpledialog.askstring("Task Title", "Enter task title:")
    if title:
        desc = simpledialog.askstring("Task Description", "Enter task description:")
        priority = simpledialog.askstring("Task Priority", "Enter task priority (low, medium, high):")
        due_date = simpledialog.askstring("Task Due Date", "Enter due date (YYYY-MM-DD):")
        task = {
            'title': title,
            'description': desc,
            'priority': priority,
            'due_date': due_date,
            'completed': False
        }
        tasks.append(task)
        save_tasks(tasks)
        render_tasks()


def edit_task(index):
    task = tasks[index]
    task['title'] = simpledialog.askstring("Edit Task Title", "Edit task title:", initialvalue=task['title'])
    task['description'] = simpledialog.askstring("Edit Task Description", "Edit task description:", initialvalue=task['description'])
    task['priority'] = simpledialog.askstring("Edit Task Priority", "Edit task priority (low, medium, high):", initialvalue=task['priority'])
    task['due_date'] = simpledialog.askstring("Edit Task Due Date", "Edit task due date (YYYY-MM-DD):", initialvalue=task['due_date'])
    save_tasks(tasks)
    render_tasks()


def delete_task(index):
    tasks.pop(index)
    save_tasks(tasks)
    render_tasks()

def toggle_task(index):
    tasks[index]['completed'] = not tasks[index]['completed']
    save_tasks(tasks)
    render_tasks()


def render_tasks():
    listbox.delete(0, tk.END)
    for index, task in enumerate(tasks):
        task_text = f"{'[x]' if task['completed'] else '[ ]'} {task['title']} - {task['priority']} (Due: {task['due_date']})"
        listbox.insert(tk.END, task_text)


tasks = load_tasks()


root = tk.Tk()
root.title("To-Do List App")

listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(pady=20)


btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="Add Task", command=add_task)
add_btn.grid(row=0, column=0, padx=5)

edit_btn = tk.Button(btn_frame, text="Edit Task", command=lambda: edit_task(listbox.curselection()[0]))
edit_btn.grid(row=0, column=1, padx=5)

complete_btn = tk.Button(btn_frame, text="Complete/Uncomplete Task", command=lambda: toggle_task(listbox.curselection()[0]))
complete_btn.grid(row=0, column=2, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete Task", command=lambda: delete_task(listbox.curselection()[0]))
delete_btn.grid(row=0, column=3, padx=5)


render_tasks()
root.mainloop()
