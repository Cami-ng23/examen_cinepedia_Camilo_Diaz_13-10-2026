from flask_app.config.mysqlconnection import MySQLConnection

class Comentario:
    @classmethod
    def crear(cls, datos):
        query = "INSERT INTO comentarios (pelicula_id, usuario_id, contenido) VALUES (%(pelicula_id)s, %(usuario_id)s, %(contenido)s)"
        return MySQLConnection().query_db(query, datos)

    @classmethod
    def listar_por_pelicula(cls, pelicula_id):
        # Bono: los comentarios más nuevos aparecen primero.
        query = "SELECT comentarios.*, usuarios.nombre AS autor_nombre, usuarios.apellido AS autor_apellido FROM comentarios JOIN usuarios ON comentarios.usuario_id" \
        " = usuarios.id WHERE comentarios.pelicula_id = %(id)s ORDER BY comentarios.created_at DESC"
        return MySQLConnection().query_db(query, {"id": pelicula_id})

    @classmethod
    def eliminar(cls, comentario_id, usuario_id):
        query = "DELETE FROM comentarios WHERE id = %(id)s AND usuario_id = %(usuario_id)s"
        return MySQLConnection().query_db(query, {"id": comentario_id, "usuario_id": usuario_id})
