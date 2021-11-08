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
