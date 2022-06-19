from project.setup_db import db
from project.dao.models.base import BaseMixin
from sqlalchemy import Table

user_movie = Table(
    "user_movie",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("movie_id", db.ForeignKey("movie.id"), primary_key=True),
)

class User(BaseMixin, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    favourite_genre = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    favourite_movies = db.relationship(
        "Movie", secondary=user_movie, back_populates="users"
    )

    def __repr__(self):
        return "<User_email {}>".format(self.email)


