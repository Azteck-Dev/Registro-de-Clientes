from datetime import datetime

class Producto:
    def __init__(self, id:str = None, folio: int = None, name:str = None, description:str = None, cost:float = 0, f_in:str = None, f_out: str = None, prod_id:str = None, cantidad:int = None, size:str = None, currency:float = None):
        self._id = id
        self._folio = folio
        self._name = name
        self._description = description
        self._cantidad = cantidad
        self._size = size
        self._cost = cost
        self._currency = currency
        self._f_in = f_in
        self._f_out = f_out
        self._prod_id = self._prod_code(prod_id)

    @property
    def id(self):
        return self._id
    @property
    def prod_id(self):
        return self._prod_id
    @property
    def folio(self):
        return self._folio
    @property
    def name(self):
        return self._name
    @property
    def description(self):
        return self._description
    @property
    def cost(self):
        return self._cost
    @property
    def f_in(self):
        return self._f_in
    @property
    def f_out(self):
        return self._f_out
    @property
    def cantidad(self):
        return self._cantidad
    @cantidad.setter
    def cantidad(self, value):
        self._cantidad = value
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        self._size = value
    @property
    def currency(self):
        return self._currency
    @currency.setter
    def currency(self, value):
        self._currency = value


    def _prod_code(self, prod_id:str):
        if prod_id:
            return prod_id
        else:
            key = str(self._name[0]) + '-' + str(self._id[:2])
            return key + str(self._folio)

    def dateInOut(self, type:str = 'in'):
        dat = datetime.now()
        fecha = dat.strftime('%d-%m-%Y')
        if type == 'in':
            if not self._f_in:
                self._f_in = fecha
        elif type == 'out':
            if not self._f_out:
                self._f_out =  fecha
            else:
                self._f_out =  f'{self._f_out},{fecha}'

    def __str__(self) :
        return f'''Producto:
ID: {self._id}
Folio: {self._folio}
Prod ID: {self._prod_id}
Nombre: {self._name}
Descripcion: {self._description}
Cantidad: {self._cantidad} {self._size}
Costo: {self._cost} {self._currency}
Ingreso: {self._f_in}
Salida: {self._f_out}
    '''

if __name__ == '__main__':
    prod = Producto('CN-1702JHVS8242','7044','Jalapeño', 'Chile verde',11.20,currency="mxn",size="kgs", cantidad=10)
    prod.dateInOut('in')
    prod.dateInOut('out')
    print(prod)

