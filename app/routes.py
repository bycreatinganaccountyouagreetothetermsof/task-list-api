from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        return jsonify([task.to_dict() for task in Task.query.all()])
    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(
            title=request_body["title"], description=request_body["description"]
        )
        db.session.add(new_task)
        db.session.commit()
        return f"Task {new_task.title} successfully created", 201


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(task_id):
    task = Task.query.get(task_id)
    if not task:
        return f"Task {task_id} not found", 404
    if request.method == "GET":
        return {"task": task.to_dict()}
    elif request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()
        return f"Task {task_id} successfully updated"
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return f"Task {task_id} successfully deleted"
