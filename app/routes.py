from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        sort = request.args.get("sort") or ""
        order = {"": None, "asc": Task.title.asc(), "desc": Task.title.desc()}
        query = Task.query.order_by(order[sort]).all()
        return jsonify([task.to_dict() for task in query])
    elif request.method == "POST":
        request_body = request.get_json()
        fields_required = ["title", "description", "completed_at"]
        if not all([field in request_body for field in fields_required]):
            return {"details": "Invalid data"}, 400
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"],
        )
        db.session.add(new_task)
        db.session.commit()
        return {"task": new_task.to_dict()}, 201


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
        return {"task": task.to_dict()}
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {"details": f'Task {task_id} "{task.title}" successfully deleted'}
