from Module.client import Client
from Module.dao import DaoClient
from tkinter import Toplevel, messagebox
import os

class SearchWin(Toplevel):
    def __init__(self):
        super().__init__()
        icon_path = os.path.abspath('Sources/icons/search.ico')
        ancho_ventana = 600
        alto_ventana = 300
        x_ventana = self.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.winfo_screenheight() // 2 - alto_ventana // 2
        position = f'{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}'
        self.title("Buscar Un Cliente")
        self.geometry(position)
        self.resizable(0,0)
        self.iconbitmap(icon_path)
        self.mainloop()





if __name__ == "__main__":
    test = SearchWin()