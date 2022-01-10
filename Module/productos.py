from datetime import datetime

class Producto:
    def __init__(self, id:str = None, folio: int = None, name:str = None, description:str = None, cost:float = 0, f_in:str = None, f_out: str = None, prod_id:str = None):
        self._id = id
        self._folio = folio
        self._name = name
        self._description = description
        self._cost = cost
        self._f_in = f_in
        self._f_out = f_out
        self._prod_id = self._prod_code(prod_id)

    @property
    def id(self):
        return self._id
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


    def _prod_code(self, prod_id:str):
        if prod_id:
            return prod_id
        else:
            key = str(self._name[0]) + '-' + str(self._id[:2])
            return key + str(self._folio)

    def _dateInOut(self, type:str = 'in'):
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
Costo: {self._cost}
Ingreso: {self._f_in}
Salida: {self._f_out}
    '''

if __name__ == '__main__':
    prod = Producto('CN-1702JHVS8242','7044','Jalapeño', 'Chile verde',11.20)
    prod._dateInOut('in')
    prod._dateInOut('out')
    print(prod)

