from flask_app.config.mysqlconnection import MySQLConnection

class pelicula:

    @classmethod
    def crear(cls, datos):
        query = """
        INSERT INTO peliculas (nombre_pelicula, director, sipnosis, usuario_id)
        VALUES (%(nombre_pelicula)s,%(director)s, %(sinopsis)s, %(usuario_id)s)
        """
        return MySQLConnection("cinepedia").query_db(query, datos)

    @classmethod
    def listar_usuario(cls, usuario_id):
        query = """
        SELECT * FROM peliculas
        WHERE usuario_id = %(usuario_id)s
        ORDER BY nombre
        """
        return MySQLConnection("cinepedia").query_db(query, {"usuario_id": usuario_id})

    @classmethod
    def buscar(cls, id, usuario_id):
        query = """
        SELECT * FROM peliculas
        WHERE id = %(id)s AND usuario_id = %(usuario_id)s
        """
        resultado = MySQLConnection("cinepedia").query_db(
            query, {"id": id, "usuario_id": usuario_id}
        )
        return resultado[0] if resultado else None

    @classmethod
    def editar(cls, datos):
        query = """
        UPDATE peliculas
        SET nombre = %(nombre)s
        WHERE id = %(id)s AND usuario_id = %(usuario_id)s
        """
        return MySQLConnection("cinepedia").query_db(query, datos)

    @classmethod
    def eliminar(cls, id, usuario_id):
        query = """
        DELETE FROM peliculas
        WHERE id = %(id)s AND usuario_id = %(usuario_id)s
        """
        return MySQLConnection("cinepedia").query_db(
            query, {"id": id, "usuario_id": usuario_id}
        )
