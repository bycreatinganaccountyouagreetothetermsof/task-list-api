from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request
from datetime import datetime

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goal", __name__, url_prefix="/goals")


select_model = {"task": Task, "goal": Goal}


@tasks_bp.route("", methods=["GET"])
@goals_bp.route("", methods=["GET"])
def get_all_items():
    model = select_model[request.blueprint]
    sort = {"asc": model.title.asc(), "desc": model.title.desc()}.get(
        request.args.get("sort")
    )
    items = model.query.order_by(sort).all()
    return jsonify([item.to_dict() for item in items])


@tasks_bp.route("", methods=["POST"])
@goals_bp.route("", methods=["POST"])
def post_new_item():
    model = select_model[request.blueprint]
    label = request.blueprint
    request_body = request.get_json()
    if not all([field in request_body for field in model.fields_required]):
        return {"details": "Invalid data"}, 400
    new_item = model(**request_body)
    db.session.add(new_item)
    db.session.commit()
    return {f"{label}": new_item.to_dict()}, 201


@tasks_bp.route("/<item_id>", methods=["DELETE", "PUT", "GET"])
@goals_bp.route("/<item_id>", methods=["DELETE", "PUT", "GET"])
def single_item(item_id):
    model = select_model[request.blueprint]
    label = request.blueprint
    item = model.query.get_or_404(item_id)
    if request.method == "DELETE":
        db.session.delete(item)
        db.session.commit()
        return {
            "details": f'{label.capitalize()} {item_id} "{item.title}" successfully deleted'
        }
    if request.method == "PUT":
        request_body = request.get_json()
        item.update(request_body)
        db.session.commit()
    return {f"{label}": item.to_dict()}


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return f"Task {task_id} not found", 404
    task.completed_at = datetime.now()
    db.session.commit()
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return f"Task {task_id} not found", 404
        # return jsonify(None), 404
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}
