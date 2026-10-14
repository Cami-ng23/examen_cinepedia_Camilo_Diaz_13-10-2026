from flask_app.config.mysqlconnection import MySQLConnection

class Usuario:

    @classmethod
    def crear(cls, datos):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password)
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s)
        """
        return MySQLConnection("cinepedia").query_db(query, datos)

    @classmethod
    def buscar_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s"
        resultado = MySQLConnection("cinepedia").query_db(query, {"email": email})
        return resultado[0] if resultado else None

    @classmethod
    def buscar_por_id(cls, id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s"
        resultado = MySQLConnection("cinepedia").query_db(query, {"id": id})
        return resultado[0] if resultado else None
