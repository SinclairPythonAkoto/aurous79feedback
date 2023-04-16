from flask import Flask


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    # add configurations here
    return app


app = create_app()
