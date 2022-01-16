from datetime import datetime


class Notas:
    def __init__(self,id:int = None, id_nota: str = None, titulo: str = None, nota: str = None, f_ingreso: str = None):
        self._id = id
        self._id_nota = id_nota
        self._titulo = titulo
        self._nota = nota
        self._f_ingreso = self._notaIn(f_ingreso)

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    @property
    def id_nota(self):
        return self._id_nota
    @id_nota.setter
    def id_nota(self, value):
        self._id_nota = value
    @property
    def titulo(self):
        return self._titulo
    @titulo.setter
    def titulo(self, value):
        self._titulo = value
    @property
    def nota(self):
        return self._nota
    @nota.setter
    def nota(self, value):
        self._nota = value
    @property
    def f_ingreso(self):
        return self._f_ingreso
    @f_ingreso.setter
    def f_ingreso(self, value):
        self._f_ingreso = value

    def _notaIn(self, f_ingreso):
        dat = datetime.now()
        fecha = dat.strftime('%d-%m-%Y')
        if not f_ingreso:
            return fecha
        else:
            return f_ingreso

    def __str__(self):
        return f'''
    ID Nota: {self._id}
    ID Cliente: {self._id_nota}
    Titulo: {self._titulo}
    Nota: {self._nota}
    Fecha: {self._f_ingreso}
    '''


if __name__ == '__main__':
    test =  Notas(
        id_nota='CN-1702JHVS8242',
        titulo='Nota de prueba', 
        nota='''That was Wintermute, manipulating the lock the way it had manipulated the drone micro and the drifting shoals of waste. Case felt the edge of the bright void beyond the chain link. Case had never seen him wear the same suit twice, although his wardrobe seemed to consist entirely of meticulous reconstruction’s of garments of the bright void beyond the chain link.'''
    )
    print(test)