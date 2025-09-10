from flask import Flask, render_template, request, jsonify
import json
import requests

app = Flask(__name__)

# File to store tasks
TASKS_FILE = 'tasks.json'

# Load tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

# Get AI task suggestion from Ollama
def get_ai_suggestion():
    try:
        prompt = "Suggest one short, motivating to-do task for a woman building her career (max 8 words):"
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b-instruct-q4_0",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            task = result["response"].strip().strip('"').strip("'")
            return task[:50]  # Limit length
        else:
            return "Plan your weekly goals"
    except Exception as e:
        return "Reflect on your progress"

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    tasks = load_tasks()
    new_task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "title": data["title"]
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task)

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data["title"]
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"success": True})

@app.route("/ai-suggestion", methods=["GET"])
def ai_suggestion():
    suggestion = get_ai_suggestion()
    return jsonify({"suggestion": suggestion})

if __name__ == "__main__":
    app.run(debug=True)