from random import randint

class Client:
    """Client es el encargado de generar los objetos de tipo cliente para el manejo de los datos del cliente.

    Returns:
        Client: Objeto clase cliente, con las siguientes propiedades.

            clave = Clave del cliente.
            name = Nombre.
            lastname / mothers = Apellidos del cliente.
            phone = Telefono de contacto del cliente.
            type_client = Tipo de cliente.(Proveedor / Comprador).
            location = Tipo de cliente por ubicación.(Local, Nacional, Internacional).
            debt = Si hay un adeudo pendiente y el monto.
            balance = Si tiene saldo a favor y el monto.
            date = Fecha en la que se registro como cliente.
    """
    def __init__(self,
        id:int = None,
        clave:str = None,
        name:str = None,
        lastname:str = None,
        mothers: str = None,
        phone: str = None,
        type_client:str = None,
        location:str = None,
        debt:float = 0,
        balance:float  = 0,
        date: str = None,
        image: str = None
    ):
        self._id = id
        self._name = name.title()
        self._lastname = lastname.title()
        self._mothers = mothers.title()
        self._phone = phone
        self._type_client = type_client
        self._location = location
        self._debt = debt
        self._balance = balance
        self._date = date
        self._image = image
        self._clave = self.key_gen(clave)

    def key_gen(self, clave: str):
        """Key Gen:
        Se encarga de generar la clave del cliente.

        Returns:
            Clave(str): Devuelve una cadena de texto, con la clave del cliente.
        """
        if not clave:
            dig = randint(0,2000)
            key = str(self._type_client[0]) + str(self._location[0]) + '-' + str(dig)
            code= str(self._name[0]) + str(self._name[-1].upper()) + str(self._lastname[0]) + str(self._mothers[0]) + str(self._phone[0:2]) + str(self._phone[-2:])
            self._clave =  key + code
            return self._clave
        else:
            return clave

    def __str__(self):
        return f'''
    ID: {self._id}
    Clave: {self._clave}
    Clase de cliente: {self._type_client}
    Tipo de cliente: {self._location}
    Cliente: {self._name} {self._lastname} {self._mothers}
    Telefono: {self._phone}
    Adeudo: ${self._debt}
    Balance a Favor: ${self._balance}
    Fecha de Registro: {self._date}
    '''

    # Set & Get atributo ID
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, key):
        self._id = key
    # Set & Get atributo Clave.
    @property
    def clave(self):
        return self._clave
    @clave.setter
    def clave(self, key):
        self._clave = key
    # Set & Get atributo Name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, nombre):
        self._name = nombre
    # Set & Get atributo Last Name
    @property
    def lastname(self):
        return self._lastname
    @lastname.setter
    def lastname(self, a_paterno):
        self._lastname = a_paterno
    # Set & Get atributo Mothers Last Name
    @property
    def mothers(self):
        return self._mothers
    @mothers.setter
    def mothers(self, a_materno):
        self._mothers = a_materno
    # Set & Get atributo Phone
    @property
    def phone(self):
        return self._phone
    @phone.setter
    def phone(self, telefono):
        self._phone = telefono
    # Set & Get atributo Type Client
    @property
    def type_client(self):
        return self._type_client
    @type_client.setter
    def type_client(self, tipo_cliente):
        self._type_client = tipo_cliente
    # Set & Get atributo Location Client
    @property
    def location(self):
        return self._location
    @location.setter
    def location(self, localization):
        self._location = localization
    # Set & Get atributo Debt
    @property
    def debt(self):
        return self._debt
    @debt.setter
    def debt(self, adeudo):
        self._debt = adeudo
    # Set & Get atributo Positive Balance
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, positive_balance):
        self._balance = positive_balance
    # Set & Get atributo Date
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, reg_date):
        self._date = reg_date
    # Set & Get Cliente Imagen/ Logo
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, path_img: str):
        self._image = path_img

if __name__ == '__main__':
    test = Client(
        name='Juan Carlos',
        lastname='Perez',
        mothers='Mendoza',
        phone= '6641213819',
        date='22-10-2021',
        type_client='Proveedor',
        location='Local'
    )
    print(test)