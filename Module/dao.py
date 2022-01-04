from connexion import AccessDB
from datetime import datetime
from client import Client
from log_gen import log


class DaoClient:
    _result = None
    _data_search = None
    _data_in = None

    # Revision de el resultado de la busqueda.
    @classmethod
    def _check_point(cls, result: tuple):
        if result:
            log.info(f'Registros encontrados: {len(result)}')
            return result
        else:
            log.warning(f'No se encontró ningún registro')
            return None

    # Busqueda de registros.
    @classmethod
    def search(cls, name: str = None, lastname:str = None, mothers:str = None, type:str = None, location:str = None):
        """Search/Busqueda
        Permite la consulta de registros en la base de datos, en base a ciertos datos personales del cliente.

        Args:
            name (str, optional): Nombre. Defaults to None.
            lastname (str, optional): Apellido paterno. Defaults to None.
            mothers (str, optional): Apellido materno. Defaults to None.
            type (str, optional): Tipo de cliente.(Proveedor/ Comprador). Defaults to None.
            location (str, optional): Ubicación del cliente(Local-Nacional-Internacional). Defaults to None.

        Returns:
            resultados(tuple): Tupla de tuplas con los resultados de la busqueda.
        """
        # Busqueda por Nombre y Apellidos
        if name and lastname or mothers:
            cls._data_search = (name, lastname, mothers)
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Clientes WHERE Nombres= ? AND (A_paterno= ? OR A_materno= ?)",cls._data_search)
                cls._result = cursor.fetchall()
                return cls._check_point(cls._result)

        # Busqueda por nombre
        if name:
            cls._data_search = ('%' + name[0:4] + '%',)
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Clientes WHERE Nombres LIKE ? ", cls._data_search)
                cls._result = cursor.fetchall()
                return cls._check_point(cls._result)

        # Busqueda por apellidos.
        if lastname or mothers:
            cls._data_search = (lastname, mothers)
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Clientes WHERE A_paterno= ? OR A_materno= ?", cls._data_search)
                cls._result = cursor.fetchall()
                return cls._check_point(cls._result)

        # Busqueda por tipo de cliente.
        if type or location:
            cls._data_search = (type, location)
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Clientes WHERE T_cliente = ? OR L_cliente = ?", cls._data_search)
                cls._result = cursor.fetchall()
                return cls._check_point(cls._result)

    # Busqueda por id.
    @classmethod
    def load_client(cls, id_cliente:str = None, type:str = 'one'):
        """Busqueda de clientes por id

        Args:
            id_cliente (str, optional): Indica el id asignado del cliente a localizar en la database. Defaults to None.
            type (str, optional): Indica el tipo de busqueda, es decir si se buscara a un solo registro o se quieren traer a todos los registros disponibles ('one' / 'all'). Defaults to 'one'.

        Returns:
            Tuple: Devolverá un tuple con los datos de el(los) registro(s) solicitado(s).
        """
        if type == 'one':
            cls._data_search = (id_cliente,)
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Clientes WHERE ID = ?", cls._data_search)
                cls._result = cursor.fetchone()
                if cls._result:
                    log.info(f'Registe encontrado: {cls._result[2]}')
                    return cls._result
                else:
                    log.warning('No se encontró el registro.')
                    return None
        elif type == 'all':
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Clientes ORDER BY ID")
                cls._result = cursor.fetchall()
                return cls._check_point(cls._result)
        else:
            if not id_cliente:
                log.error('No se pudo realizar, debe proporcionar el id del cliente a buscar.')


    # Registro de nuevo usuario.
    @classmethod
    def singup(cls, cliente : Client):
        """SingUp/Registro de clientes en la base de datos.

        Args:
            cliente (Client): Objeto de tipo cliente con sus propiedades.

        Returns:
            bool: True / False.
        """
        fecha = datetime.now()
        cliente.date = fecha.strftime('%d-%m-%Y')
        cls._data_in = (
            cliente.clave,
            cliente.name,
            cliente.lastname,
            cliente.mothers,
            cliente.phone,
            cliente.type_client,
            cliente.location,
            cliente.date
        )
        try:
            with AccessDB() as cursor:
                cursor.execute('INSERT INTO Clientes(Clave, Nombres, A_paterno, A_materno, Telefono, T_cliente, L_cliente, F_registro) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', cls._data_in)
                log.info(f'Cliente: {cliente.clave} registrado.')
                return True
        except Exception:
            return False

    # Actualización de datos del cliente.
    @classmethod
    def update(cls, data: Client):
        """Update/Actualización de datos de un cliente.

        Args:
            data (Client): Objeto de tipo de cliente que sera modificado.

        Returns:
            Bool: True/False
        """
        cls._data_in = (
            data.name,
            data.lastname,
            data.mothers,
            data.phone,
            data.type_client,
            data.location,
            data.image,
            data.id
        )
        try:
            with AccessDB() as cursor:
                cursor.execute("UPDATE Clientes SET Nombres= ?, A_paterno= ?, A_materno= ?, Telefono= ?, T_cliente= ?, L_cliente= ?, C_img= ? WHERE ID = ?",cls._data_in)
                log.info(f'Cliente: {data.clave} actualizado')
                return True
        except Exception:
            return False

    # Método para la eliminación de un registro.
    @classmethod
    def delete(cls, id: Client.id):
        """Delete/ Eliminar un registro de la base de datos.

        Args:
            id (Client.id): Propiedad id del cliente a eliminar o el id a eliminar en formato string

        Returns:
            Bool: True / False
        """
        cls._data_search = (id,)
        try:
            with AccessDB() as cursor:
                cursor.execute('DELETE FROM Clientes WHERE ID = ?', cls._data_search)
                if cursor.rowcount:
                    log.info(f'Registro eliminado: {cursor.rowcount}')
                    return True
                else:
                    log.info('No se encontró el registro a eliminar')
                    return False
        except Exception:
            log.error(f"No se pudo borrar al registro: {id}")