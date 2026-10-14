from flask import Blueprint, request, redirect, session, flash, url_for
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

comentarios_bp = Blueprint("comentarios", __name__)

@comentarios_bp.route("/peliculas/<int:pelicula_id>/comentarios", methods=["POST"])
def crear(pelicula_id):
    if not session.get("usuario_id"):
        flash("Debes iniciar sesión para comentar.", "error")
        return redirect(url_for("usuarios.inicio"))
    contenido = request.form.get("contenido", "").strip()
    if contenido:
        Comentario.crear({"pelicula_id": pelicula_id,
                          "usuario_id": session["usuario_id"],
                          "contenido": contenido})
    return redirect(url_for("peliculas.detalle", pelicula_id=pelicula_id))

@comentarios_bp.route("/comentarios/eliminar/<int:comentario_id>/<int:pelicula_id>", methods=["POST"])
def eliminar(comentario_id, pelicula_id):
    if not session.get("usuario_id"):
        return redirect(url_for("usuarios.inicio"))
    Comentario.eliminar(comentario_id, session["usuario_id"])
    return redirect(url_for("peliculas.detalle", pelicula_id=pelicula_id))
