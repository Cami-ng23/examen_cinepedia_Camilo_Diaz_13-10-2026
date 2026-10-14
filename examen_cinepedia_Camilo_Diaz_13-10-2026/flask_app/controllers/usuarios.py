from flask import (
    Blueprint, render_template, request,
    redirect, session, flash, url_for
)

from flask_app.models.usuario import Usuario
from flask_app import bcrypt

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/")
def inicio():
    if session.get("usuario_id"):
        return redirect(url_for("peliculas.listar"))

    return render_template("registro.html")


@usuarios_bp.route("/registro", methods=["POST"])
def registro():
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirmar = request.form.get("confirmar", "")

    if len(nombre) < 2 or len(apellido) < 2:
        flash("Nombre y apellido deben tener al menos 3 caracteres.", "error")
        return redirect(url_for("usuarios.inicio"))

    if "@" not in email or "." not in email.split("@")[-1]:
        flash("Ingresa un correo válido.", "error")
        return redirect(url_for("usuarios.inicio"))

    if Usuario.buscar_por_email(email):
        flash("Ese correo ya está registrado.", "error")
        return redirect(url_for("usuarios.inicio"))

    if len(password) < 8:
        flash("La contraseña debe tener al menos 8 caracteres.", "error")
        return redirect(url_for("usuarios.inicio"))

    if password != confirmar:
        flash("Las contraseñas no coinciden.", "error")
        return redirect(url_for("usuarios.inicio"))

    password_hash = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    usuario_id = Usuario.crear({
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password": password_hash
    })

    session["usuario_id"] = usuario_id
    session["usuario_nombre"] = nombre

    flash("Cuenta creada correctamente.", "success")

    return redirect(url_for("peliculas.listar"))


@usuarios_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("login_email", "").strip().lower()
    password = request.form.get("login_password", "")

    usuario = Usuario.buscar_por_email(email)

    if not usuario or not bcrypt.check_password_hash(
        usuario["password"], password
    ):
        flash("Correo o contraseña incorrectos.", "error")
        return redirect(url_for("usuarios.inicio"))

    session.clear()
    session["usuario_id"] = usuario["id"]
    session["usuario_nombre"] = usuario["nombre"]

    return redirect(url_for("peliculas.listar"))


@usuarios_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("usuarios.inicio"))