from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    fields_required = ["title"]

    def update(self, updates):
        self.title = updates["title"]

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }
