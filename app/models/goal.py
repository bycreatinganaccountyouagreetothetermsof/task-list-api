from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")
    fields_required = ["title"]

    def update(self, updates):
        self.title = updates["title"]

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }

    def tasks_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    def id_and_tasks(self):
        return {"id": self.goal_id, "task_ids": [task.task_id for task in self.tasks]}
