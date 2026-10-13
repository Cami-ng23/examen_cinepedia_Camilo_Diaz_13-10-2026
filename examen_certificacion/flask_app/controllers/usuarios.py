from flask import Blueprint, render_template, request, redirect, session, flash
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

usuarios_bp = Blueprint("usuarios", __name__)
bcrypt = Bcrypt()

@usuarios_bp.route("/")
def inicio():
    if "usuario_id" in session:
        return redirect("/bienvenida")
    return render_template("registro.html")

@usuarios_bp.route("/registro", methods=["POST"])
def registro():
    nombre = request.form["nombre"].strip()
    apellido = request.form["apellido"].strip()
    email = request.form["email"].strip()
    password = request.form["password"]
    confirmar = request.form["confirmar"]

    if len(nombre) < 2 :
        flash("El nombre  debe tener al menos 2 caracteres.", "error")
        return redirect("/")

    if "@" not in email or "." not in email:
        flash("Ingresa un correo válido.", "error")
        return redirect("/")

    if Usuario.buscar_por_email(email):
        flash("Ese correo ya está registrado.", "error")
        return redirect("/")

    if len(password) < 8:
        flash("La contraseña debe tener al menos 8 caracteres.", "error")
        return redirect("/")

    if password != confirmar:
        flash("Las contraseñas no coinciden.", "error")
        return redirect("/")

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    id_usuario = Usuario.crear({
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password": password_hash
    })

    session["usuario_id"] = id_usuario
    session["usuario_nombre"] = nombre

    flash("Cuenta creada correctamente.", "success")
    return redirect("/bienvenida")

@usuarios_bp.route("/registro", methods=["POST"])
def login():
    email = request.form["email"].strip()
    password = request.form["password"]

    usuario = Usuario.buscar_por_email(email)

    if not usuario:
        flash("Correo o contraseña incorrectos.", "error")
        return redirect("/")

    if not bcrypt.check_password_hash(usuario["password"], password):
        flash("Correo o contraseña incorrectos.", "error")
        return redirect("/")

    session["usuario_id"] = usuario["id"]
    session["usuario_nombre"] = usuario["nombre"]

    return redirect("/bienvenida")

@usuarios_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
