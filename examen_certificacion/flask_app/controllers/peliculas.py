from flask import Blueprint, render_template, request, redirect, session, flash
from flask_app.models.pelicula import pelicula

peliculas_bp = Blueprint("peliculas", __name__)

@peliculas_bp.route("/peliculas")
def listar():
    if "usuario_id" not in session:
        return redirect("/")

    peliculas = pelicula.listar_usuario(session["usuario_id"])
    return render_template("peliculas.html", peliculas=peliculas)

# Estamos creando una nueva pelicula

@peliculas_bp.route("/peliculas/crear", methods=["POST"])
def crear():
    if "usuario_id" not in session:
        return redirect("/")

    nombre = request.form["nombre"].strip()

    if len(nombre) < 2:
        flash("La categoría debe tener al menos 2 caracteres.", "error")
        return redirect("/peliculas")

    pelicula.crear({
        "nombre_pelicula": nombre_pelicula,
        "director": director,
        "fecha_estreno": fecha_estreno,
        "sinopsis": sinopsis,
        "usuario_id": session["usuario_id"]
    })

    flash("pelicula creada.", "success")
    return redirect("/peliculas")


@peliculas_bp.route("/peliculas/editar/<int:id>", methods=["POST"])
def editar(id):
    if "usuario_id" not in session:
        return redirect("/")

    nombre = request.form["nombre"].strip()

    if len(nombre) < 2:
        flash("La pelicula debe tener al menos 5 caracteres.", "error")
        return redirect("/peliculas")

    Categoria.editar({
        "nombre_pelicula": nombre_pelicula,
        "director": director,
        "fecha_estreno": fecha_estreno,
        "sinopsis": sinopsis,
        "usuario_id": session["usuario_id"]
    })

    return redirect("/peliculas")

@categorias_bp.route("/peliculas/eliminar/<int:id>")
def eliminar(id):
    if "usuario_id" not in session:
        return redirect("/")

    pelicula.eliminar(id, session["usuario_id"])
    flash("Pelicula eliminada.", "success")
    return redirect("/peliculas")
