from datetime import date
from flask import (
    Blueprint, render_template, request,
    redirect, session, flash, url_for
)

from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

peliculas_bp = Blueprint("peliculas", __name__)


def validar_pelicula(datos):
    if len(datos["nombre_pelicula"]) < 3:
        return "El nombre debe tener al menos 3 caracteres."

    if len(datos["director"]) < 2:
        return "El director debe tener al menos 2 caracteres."

    if not datos["fecha_estreno"]:
        return "La fecha de estreno no puede estar vacía."

    try:
        date.fromisoformat(datos["fecha_estreno"])
    except ValueError:
        return "La fecha de estreno no es válida."

    if not datos["sinopsis"]:
        return "La sinopsis no puede estar vacía."

    return None


def datos_formulario():
    return {
        "nombre_pelicula": request.form.get(
            "nombre_pelicula", ""
        ).strip(),
        "director": request.form.get("director", "").strip(),
        "fecha_estreno": request.form.get(
            "fecha_estreno", ""
        ).strip(),
        "sinopsis": request.form.get("sinopsis", "").strip()
    }


@peliculas_bp.route("/peliculas")
def listar():
    if not session.get("usuario_id"):
        return redirect(url_for("usuarios.inicio"))

    peliculas = Pelicula.listar()

    return render_template(
        "bienvenida.html",
        peliculas=peliculas
    )


@peliculas_bp.route("/peliculas/nueva")
def nueva():
    if not session.get("usuario_id"):
        return redirect(url_for("usuarios.inicio"))

    return render_template("nueva_pelicula.html", datos={})


@peliculas_bp.route("/peliculas/crear", methods=["POST"])
def crear():
    if not session.get("usuario_id"):
        return redirect(url_for("usuarios.inicio"))

    datos = datos_formulario()
    error = validar_pelicula(datos)

    if error:
        flash(error, "error")
        return render_template(
            "nueva_pelicula.html",
            datos=datos
        )

    datos["usuario_id"] = session["usuario_id"]

    Pelicula.crear(datos)

    flash("Película creada correctamente.", "success")

    return redirect(url_for("peliculas.listar"))


@peliculas_bp.route("/peliculas/<int:pelicula_id>")
def detalle(pelicula_id):
    if not session.get("usuario_id"):
        return redirect(url_for("usuarios.inicio"))

    pelicula = Pelicula.buscar(pelicula_id)

    if not pelicula:
        flash("La película no existe.", "error")
        return redirect(url_for("peliculas.listar"))

    comentarios = Comentario.listar_por_pelicula(pelicula_id)

    return render_template(
        "pelicula.html",
        pelicula=pelicula,
        comentarios=comentarios
    )


@peliculas_bp.route(
    "/peliculas/editar/<int:pelicula_id>",
    methods=["GET", "POST"]
)
def editar(pelicula_id):
    if not session.get("usuario_id"):
        return redirect(url_for("usuarios.inicio"))

    pelicula = Pelicula.buscar(pelicula_id)

    if not pelicula:
        flash("La película no existe.", "error")
        return redirect(url_for("peliculas.listar"))

    if pelicula["usuario_id"] != session["usuario_id"]:
        flash("Solo puedes editar tus propias películas.", "error")
        return redirect(url_for("peliculas.listar"))

    if request.method == "GET":
        return render_template(
            "editar_pelicula.html",
            pelicula=pelicula,
            datos=pelicula
        )

    datos = datos_formulario()
    error = validar_pelicula(datos)

    if error:
        flash(error, "error")
        return render_template(
            "editar_pelicula.html",
            pelicula=pelicula,
            datos=datos
        )

    datos["id"] = pelicula_id
    datos["usuario_id"] = session["usuario_id"]

    Pelicula.editar(datos)

    flash("Película actualizada correctamente.", "success")

    return redirect(
        url_for("peliculas.detalle", pelicula_id=pelicula_id)
    )


@peliculas_bp.route(
    "/peliculas/eliminar/<int:pelicula_id>",
    methods=["POST"]
)
def eliminar(pelicula_id):
    if not session.get("usuario_id"):
        return redirect(url_for("usuarios.inicio"))

    pelicula = Pelicula.buscar(pelicula_id)

    if not pelicula:
        flash("La película no existe.", "error")
        return redirect(url_for("peliculas.listar"))

    if pelicula["usuario_id"] != session["usuario_id"]:
        flash("Solo puedes borrar tus propias películas.", "error")
        return redirect(url_for("peliculas.listar"))

    Pelicula.eliminar(
        pelicula_id,
        session["usuario_id"]
    )

    flash("Película eliminada correctamente.", "success")

    return redirect(url_for("peliculas.listar"))