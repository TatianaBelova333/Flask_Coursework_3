from project.config import DevelopmentConfig
from project.dao.models import Genre, Director, Movie, User
from project.server import create_app, db

app = create_app(DevelopmentConfig)
app.app_context().push()


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Movie": Movie,
        "Director": Director,
        "User": User
    }


if __name__ == '__main__':
    app.run(port=25000)