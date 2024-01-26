from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config["SECRET"] = "THIS IS A SUPER SECRET KEY FOR THE APP"
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["DOWNLOAD_FOLDER"] = "downloads"

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
