from flask_app.config.mysqlconnection import MySQLConnection


class Pelicula:

    @classmethod
    def crear(cls, datos):
        query = """
        INSERT INTO peliculas
        (nombre_pelicula, director, fecha_estreno, sinopsis, usuario_id)
        VALUES
        (%(nombre_pelicula)s, %(director)s, %(fecha_estreno)s,
         %(sinopsis)s, %(usuario_id)s)
        """

        return MySQLConnection("cinepedia").query_db(query, datos)

    @classmethod
    def listar(cls):
        query = """
        SELECT peliculas.*,
               usuarios.nombre AS autor_nombre,
               usuarios.apellido AS autor_apellido
        FROM peliculas
        JOIN usuarios ON peliculas.usuario_id = usuarios.id
        ORDER BY peliculas.nombre_pelicula
        """

        return MySQLConnection("cinepedia").query_db(query)

    @classmethod
    def buscar(cls, pelicula_id):
        query = """
        SELECT peliculas.*,
               usuarios.nombre AS autor_nombre,
               usuarios.apellido AS autor_apellido
        FROM peliculas
        JOIN usuarios ON peliculas.usuario_id = usuarios.id
        WHERE peliculas.id = %(id)s
        """

        resultado = MySQLConnection("cinepedia").query_db(
            query, {"id": pelicula_id}
        )

        return resultado[0] if resultado else None

    @classmethod
    def editar(cls, datos):
        query = """
        UPDATE peliculas
        SET nombre_pelicula = %(nombre_pelicula)s,
            director = %(director)s,
            fecha_estreno = %(fecha_estreno)s,
            sinopsis = %(sinopsis)s
        WHERE id = %(id)s
          AND usuario_id = %(usuario_id)s
        """

        return MySQLConnection("cinepedia").query_db(query, datos)

    @classmethod
    def eliminar(cls, pelicula_id, usuario_id):
        query = """
        DELETE FROM peliculas
        WHERE id = %(id)s AND usuario_id = %(usuario_id)s
        """

        return MySQLConnection("cinepedia").query_db(
            query,
            {
                "id": pelicula_id,
                "usuario_id": usuario_id
            }
        )