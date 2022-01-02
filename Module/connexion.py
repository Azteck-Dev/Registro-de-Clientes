from log_gen import log
import sqlite3 as SQL

# Clase encargada de obtener la conexion con la base de datos.
class ConnSQL:
    """Clase encargada de conectar con la base de datos.

    Returns:
        Connection: Devuelve una conexion a la base de datos.
    """
    _conn = None

    @classmethod
    def getconn(cls):
        try:
            cls._conn = SQL.connect('DataBase/wallet.db3')
            return cls._conn
        except Exception as error:
            print(error)

class AccessDB:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def __enter__(self):
        self._connection = ConnSQL.getconn()
        log.info(f'Conexion Exitosa {self._connection}')
        self._cursor = self._connection.cursor()
        log.info(f'Cursor generado {self._cursor}')
        return self._cursor

    def __exit__(self, except_type, except_val, details):
        if except_val:
            self._connection.rollback()
            log.warning(f'Ocurrió un error se genero un Rollback')
            log.error(f'{except_val}\n{except_type}')
        else:
            log.info('Operacion exitosa')
            self._connection.commit()

        self._cursor.close()
        self._connection.close()


if __name__ == '__main__':
    with AccessDB() as cursor:
        cursor.execute('SELECT * FROM Clientes')
        data = cursor.fetchall()
        print(data)
