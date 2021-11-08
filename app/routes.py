from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    sort = {"asc": Task.title.asc(), "desc": Task.title.desc()}.get(
        request.args.get("sort")
    )
    tasks = Task.query.order_by(sort).all()
    return jsonify([task.to_dict() for task in tasks])


@goals_bp.route("", methods=["GET"])
def get_goals():
    sort = {"asc": Goal.title.asc(), "desc": Goal.title.desc()}.get(
        request.args.get("sort")
    )
    goals = Goal.query.order_by(sort).all()
    return jsonify([goal.to_dict() for goal in goals])


@tasks_bp.route("", methods=["POST"])
def post_new_task():
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


@goals_bp.route("", methods=["POST"])
def post_new_goal():
    request_body = request.get_json()

    fields_required = ["title"]
    if not all([field in request_body for field in fields_required]):
        return {"details": "Invalid data"}, 400

    new_goal = Goal(
        title=request_body["title"],
    )
    db.session.add(new_goal)
    db.session.commit()
    return {"goal": new_goal.to_dict()}, 201


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def single_task(task_id):
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


@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def single_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return f"Goal {goal_id} not found", 404
    if request.method == "GET":
        return {"goal": goal.to_dict()}
    elif request.method == "PUT":
        request_body = request.get_json()
        goal.title = request_body["title"]
        db.session.commit()
        return {"goal": goal.to_dict()}
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    task.completed_at = datetime.now()
    db.session.commit()
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}
