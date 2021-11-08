from flask import current_app
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")
    fields_required = ["title", "description", "completed_at"]

    def update(self, updates):
        self.title = updates["title"]
        self.description = updates["description"]

    def to_dict(self):
        return_dict = {
            "id": self.task_id,
            # "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None,
        }
        if self.goal_id is not None:
            return_dict["goal_id"] = self.goal_id
        return return_dict
