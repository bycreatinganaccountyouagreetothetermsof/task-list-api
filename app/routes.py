"""
# project notes

started 7 nov

finished 7 nov, heroku 8 nov

wave 4 unimplemented. may implement on mastodon instead of slack, later


# optional enhancements

## edge cases

what should happen if...

- when creating a task, the value of completed_at is a string that is not a datetime?
    - return 400 and an error detail json. not implemented.
- when updating a task, the value of completed_at is a string that is not a datetime?
    - return 400 and an error detail json. not implemented.
- when getting all tasks, and using query params, the value of sort is not "desc" or "asc"?
    - fall back to unsorted. this is implemented by the dict.get call that returns None.

## re-organize routes

some routes are genericized and switch on dict provided by select_model and blueprint name

## model instance methods

as much as possible, json rendering is kept out of models and performed in route functions, aside from the typical to_dict.
i think this is appropriate as the correct implementation would be to have this behavior in a "view" but this was not in the lesson

## list comprehensions

list comprehensions are used where appropriate.

## more query params

not implemented
"""

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
    """
    This route will return all records of a model.
    ---
    parameters:
        - name: sort
            in: path
            type: string
            required: false
            description: sort by title asc or desc
    responses:
        200:
            description: Successful response containing all records of model. May be empty.
    """
    model = select_model[request.blueprint]
    sort = {"asc": model.title.asc(), "desc": model.title.desc()}.get(
        request.args.get("sort")
    )
    items = model.query.order_by(sort).all()
    return jsonify([item.to_dict() for item in items])


@tasks_bp.route("", methods=["POST"])
@goals_bp.route("", methods=["POST"])
def post_new_item():
    """
    This route will accept a new record via POST.
    ---
    responses:
        200:
            description: Successfully added new record.
        400:
            description: Post body did not include all fields required to create record.
    """
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
    """
    This route will read or modify a record.
    ---
    responses:
        200:
            description: Successfully read or modified record.
        404:
            description: Requested record does not exist.
    """
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
    """
    This route will mark a task complete.
    ---
    responses:
        200:
            description: Successfully completed task.
        404:
            description: Requested task does not exist.
    """
    task = Task.query.get_or_404(task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    """
    This route will mark a task incomplete.
    ---
    responses:
        200:
            description: Successfully un-completed task.
        404:
            description: Requested task does not exist.
    """
    task = Task.query.get_or_404(task_id)
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks(goal_id):
    """
    This route will add tasks to a goal.
    ---
    responses:
        200:
            description: Successfully added tasks to goal.
        404:
            description: Requested goal does not exist.
    """
    goal = Goal.query.get_or_404(goal_id)
    request_body = request.get_json()
    goal.tasks = [Task.query.get(task_id) for task_id in request_body["task_ids"]]
    db.session.commit()
    return {"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def goal_tasks(goal_id):
    """
    This route will retrieve tasks associated with a goal.
    ---
    responses:
        200:
            description: Successfully retrieved goal tasks.
        404:
            description: Requested goal does not exist.
    """
    goal = Goal.query.get_or_404(goal_id)
    response = goal.to_dict()
    response["tasks"] = [task.to_dict() for task in goal.tasks]
    return response
