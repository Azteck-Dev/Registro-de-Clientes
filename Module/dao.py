from Module.connexion import AccessDB
from datetime import datetime
from Module.log_gen import log
from Module.client import Client
from Module.notas import Notas
from Module.productos import Producto


# DAO para el control de los datos del cliente.
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
            name = f'%{name}%'
            cls._data_search = (name, lastname, mothers)
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Clientes WHERE Nombres LIKE ? AND (A_paterno= ? OR A_materno= ?)",cls._data_search)
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


# DAO para el manejo de las notas del cliente.
class DaoNotas:
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

    # Busqueda de Nota.
    @classmethod
    def getNote(cls, id_note):
        cls._data_search = (id_note,)
        with AccessDB() as cursor:
            cursor.execute("SELECT * FROM Notas WHERE id = ?", cls._data_search)
            cls._result = cursor.fetchone()
            return cls._check_point(cls._result)

    # Consulta de las notas existentes de un cliente.
    @classmethod
    def getNotas(cls, id_nota):
        """Obtener las notas de un cliente.

        Args:
            id_nota (str): Clave del cliente a quien pertenece la nota.

        Returns:
            tuple: Tupla de tuplas con los resultados de la consulta SQL, devolverá None si no se
            encontró ninguna coincidencia,
        """
        cls._data_search = (id_nota,)
        with AccessDB() as cursor:
            cursor.execute('SELECT * FROM Notas WHERE id_nota = ?', cls._data_search)
            cls._result = cursor.fetchall()
            return cls._check_point(cls._result)

    # Registrar una nota aun cliente.
    @classmethod
    def regNota(cls, nota: Notas):
        """Ingreso de notas para un cliente.

        Args:
            nota (Notas): Objeto de clase Notas a ingresar a la base de datos.
        """
        cls._data_in = (nota.titulo, nota.nota, nota.f_ingreso, nota.id_nota)
        try:
            with AccessDB() as cursor:
                cursor.execute('INSERT INTO Notas(Titulo, Nota, F_nota, id_nota) VALUES(?,?,?,?)', cls._data_in)
                log.info(f'{cursor.rowcount} registro fue ingresado.')
        except Exception as ex:
            log.error(f'No se pudo realizar el registro: {ex}')

    # Actualización de una nota de un cliente.
    @classmethod
    def noteUpdate(cls, nota: Notas):
        """Actualizar los datos de una nota.

        Args:
            nota (Notas): Objeto de clase notas a actualizar.
        """
        cls._data_in = (nota.titulo, nota.nota, nota.f_ingreso ,nota.id)
        with AccessDB() as cursor:
            cursor.execute('UPDATE Notas SET Titulo = ?, Nota = ?, F_nota = ? WHERE id = ?', cls._data_in)
            log.info(f'{cursor.rowcount} registro se actualizo correctamente.')


    # Eliminar una nota de un cliente.
    @classmethod
    def delNote(cls,id):
        """Eliminar una nota de un usurario.

        Args:
            id (str): Id de la nota a eliminar.
        """
        cls._data_search = (id,)
        with AccessDB() as cursor:
            cursor.execute('DELETE FROM Notas WHERE id = ?', cls._data_search)
            log.info(f'{cursor.rowcount} registro ha sido eliminado.')


# DAO para el manejo de los productos por cliente.
class DaoProduct:
    _product_in = None
    _products = None
    _result = None

    # Revision de el resultado de la busqueda.
    @classmethod
    def _check_point(cls, result: tuple):
        if result:
            log.info(f'Registros encontrados: {len(result)}')
            return result
        else:
            log.warning(f'No se encontró ningún registro')
            return None

    # Registro de un producto en la base de datos.
    @classmethod
    def prod_reg(cls, prod: Producto):
        cls._product_in = (
            prod.id,
            prod.prod_id,
            prod.folio,
            prod.name,
            prod.description,
            prod.cantidad,
            prod.cost,
            prod.f_in,
            prod.f_out
        )
        with AccessDB() as cursor:
            cursor.execute('''INSERT INTO
                Productos(id_clave, prod_id, folio, nombre, descripcion, cantidad, costo, F_ingreso, F_out)
                VALUES(?,?,?,?,?,?,?,?,?)''', cls._product_in
            )
            log.info(f'{cursor.rowcount} producto ha sido registrado')

    # Busqueda de productos.
    @classmethod
    def search(cls, search:str = 'product', id: str = None):
        """Busqueda de productos en la base de datos.

        Args:
            search (str, optional): Define el tipo de busqueda por producto o por cliente.(client/product). Defaults to 'product'.
            id (str, optional): Ingresa el id correspondiente al tipo de busqueda seleccionado.. Defaults to None.

        Returns:
            (Tuple): Tupla de tuplas con los resultados obtenidos.
        """
        # Busqueda por producto
        if search == 'product' and id:
            cls._products = (id,)
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Productos WHERE nombre = ?", cls._products)
                cls._result = cursor.fetchall()
                return cls._check_point(cls._result)
        # Busqueda por cliente.
        elif search == 'client'  and id:
            cls._products = (id,)
            with AccessDB() as cursor:
                cursor.execute("SELECT * FROM Productos WHERE id_clave = ?", cls._products)
                cls._result = cursor.fetchall()
                return cls._check_point(cls._result)

    # Actualizar un producto o modificarlo.
    @classmethod
    def prodUpdate(cls, prod: Producto, *fields):
        """Actualización de los datos de un producto.

        Args:
            prod (Producto): Objeto de clase producto a modificar.
            *fields: Elementos a modificar. all/name/cost/description/cantidad/out
                ejem:
                prodUpdate(prod,'all','cost')
        """
        mns = 'Registro actualizado: '
        # Actualización de un campo en especifico.
        for field in fields:
            match field:
                # Actualizar todos los campos.
                case 'all':
                    cls._products = (prod.name, prod.description, prod.cantidad, prod.cost, prod.f_out, prod.prod_id)
                    with AccessDB() as cursor:
                        cursor.execute("UPDATE Productos SET nombre = ?, descripcion = ?, cantidad = ?, costo = ?, F_out = ? WHERE prod_id = ?", cls._products)
                        log.info(f'{cursor.rowcount} {mns} {field}')
                # Actualizar la cantidad en inventario.
                case 'cantidad':
                    cls._products = (prod.cantidad, prod.prod_id)
                    with AccessDB() as cursor:
                        cursor.execute("UPDATE Productos SET cantidad = ? WHERE prod_id = ?", cls._products)
                        log.info(f'{cursor.rowcount} {mns}{field}')
                # Actualizar el precio.
                case 'cost':
                    cls._products = (prod.cost, prod.prod_id)
                    with AccessDB() as cursor:
                        cursor.execute("UPDATE Productos SET costo = ? WHERE prod_id = ?", cls._products)
                        log.info(f'{cursor.rowcount} {mns}{field}')
                # Actualizar la fecha de salida del producto.
                case 'out':
                    cls._products = (prod.f_out, prod.cantidad, prod.prod_id)
                    with AccessDB() as cursor:
                        cursor.execute("UPDATE Productos SET F_out = ?, cantidad = ? WHERE prod_id = ?", cls._products)
                        log.info(f'{cursor.rowcount} {mns}{field}')
                # Actualizar la descripcion del producto.
                case 'description':
                    cls._products = (prod.description, prod.prod_id)
                    with AccessDB() as cursor:
                        cursor.execute("UPDATE Productos SET descripcion = ? WHERE prod_id = ?", cls._products)
                        log.info(f'{cursor.rowcount} {mns}{field}')
                # Actualizar el nombre del producto.
                case 'name':
                    cls._products = (prod.name, prod.prod_id)
                    with AccessDB() as cursor:
                        cursor.execute("UPDATE Productos SET nombre = ? WHERE prod_id = ?", cls._products)
                        log.info(f'{cursor.rowcount} {mns}{field}')
                # En caso de una opción invalida.
                case _:
                    if field:
                        log.warning(f'{field} no es una opción valida.')

    # Eliminación de un producto.
    @classmethod
    def prodDel(cls, prod_id: str):
        cls._products = (prod_id,)
        with AccessDB() as cursor:
            cursor.execute("DELETE FROM Productos WHERE prod_id = ?", cls._products)
            log.info(f'{cursor.rowcount} registro ha sido eliminado.')
