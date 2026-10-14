import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "cambia-esta-clave-en-tu-env")
    bcrypt.init_app(app)

    from flask_app.controllers.usuarios import usuarios_bp
    from flask_app.controllers.peliculas import peliculas_bp
    from flask_app.controllers.comentarios import comentarios_bp

    app.register_blueprint(usuarios_bp)
    app.register_blueprint(peliculas_bp)
    app.register_blueprint(comentarios_bp)
    return app
