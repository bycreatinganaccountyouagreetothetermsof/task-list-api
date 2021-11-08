from flask import current_app
from app import db


class Goal(db.Model):
    """
    Model for goal records
    ---
    - attributes:
        goal_id: autoincrementing integer id
        title: string, required field on creation
        tasks: list of integers, foreign keys for Task model
    """

    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")
    fields_required = ["title"]

    def update(self, updates):
        """
        utility method for applying updates from provided dict
        """
        self.title = updates["title"]

    def to_dict(self):
        """
        utility method for generating json
        """
        return {
            "id": self.goal_id,
            "title": self.title,
        }
