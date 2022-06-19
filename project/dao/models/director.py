from project.dao.models.base import BaseMixin
from project.setup_db import db


class Director(BaseMixin, db.Model):
    __tablename__ = "director"

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "<Director {}>".format(self.name)