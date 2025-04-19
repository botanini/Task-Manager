from flask import Flask, request, render_template, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# File to store tasks
TASKS_FILE = 'tasks.txt'

def load_tasks():
    """
    Load tasks from the file.
    Returns a list of tasks, where each task is a tuple (task, due_date).
    """
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        tasks = file.readlines()
    return [task.strip().split('|') for task in tasks]

def save_tasks(tasks):
    """
    Save tasks to the file.
    Each task is a tuple (task, due_date).
    """
    with open(TASKS_FILE, 'w') as file:
        for task, due_date in tasks:
            file.write(f"{task}|{due_date}\n")

def format_date(date_str):
    """
    Format the date from 'YYYY-MM-DD' to 'Month Day, Year'.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%B %d, %Y')

@app.route('/')
def home():
    """
    Route for the home page.
    Displays the list of tasks.
    """
    tasks = load_tasks()
    formatted_tasks = [(task, format_date(due_date)) for task, due_date in tasks]
    return render_template('index.html', tasks=formatted_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """
    Route for adding a new task.
    """
    task = request.form.get('task')
    due_date = request.form.get('due_date')
    if task and due_date:
        tasks = load_tasks()
        tasks.append((task, due_date))
        save_tasks(tasks)
    return redirect(url_for('home'))

@app.route('/delete/<int:task_index>', methods=['POST'])
def delete_task(task_index):
    """
    Route for deleting a task.
    """
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        save_tasks(tasks)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)