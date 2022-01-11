from re import sub
from tkinter import Toplevel, messagebox, ttk, PhotoImage
from Module.client import Client
import tkinter as tk
import os

class NewClient(Toplevel):
    def __init__(self):
        super().__init__()
        icon = os.path.abspath('Sources/icons/add.ico')
        self.title('Agregar un cliente')
        self.iconbitmap(icon)
        self.geometry('500x350')
        self.resizable(0,0)
        self.config(bg='#3C3C3C')
        self._main_content()
        self._client_specs()
        self._buttons()
        self.mainloop()

    def _main_content(self):
        # Frame principal.
        main_frame = tk.LabelFrame(self, text='Datos del Cliente.', font='bold')
        main_frame.grid(row=0, column=0, padx=5, pady=7, sticky='NSEW', columnspan=2)
        main_frame.config(foreground='#FFF', background='#3C3C3C')
        # Formulario para el relleno de datos.
        # Nombres
        l_name = tk.Label(main_frame, text='Nombre(s):', justify=tk.RIGHT, font=("Arial",10,"bold"))
        l_name.grid(row=0, column=0, padx=5, pady=10, sticky='SW')
        l_name.config(foreground='#FFF', background='#3C3C3C')
        self.e_name = ttk.Entry(main_frame, width=40, justify='left', font=('Arial',10,'bold'))
        self.e_name.grid(row=0, column=1, padx=8, pady=10, sticky='NSE')
        self.e_name.focus()
        # Apellido Paterno.
        l_lastname = tk.Label(main_frame, text='A. Paterno:', justify=tk.RIGHT, font=("Arial",10,"bold"))
        l_lastname.grid(row=1, column=0, padx=5, pady=10, sticky='NSEW')
        l_lastname.config(foreground='#FFF', background='#3C3C3C')
        self.e_lastname = ttk.Entry(main_frame, width=40, justify='left', font=("Arial",10,"bold"))
        self.e_lastname.grid(row=1, column=1, padx=8, pady=10, sticky='NSE')
        # Apellido Materno
        l_mothers = tk.Label(main_frame, text='A. Materno:', justify=tk.RIGHT, font=("Arial",10,"bold"))
        l_mothers.grid(row=2, column=0, padx=5, pady=10, sticky='NSEW')
        l_mothers.config(foreground='#FFF', background='#3C3C3C')
        self.e_mothers = ttk.Entry(main_frame, width=40, justify='left', font=('arial',10,'bold'))
        self.e_mothers.grid(row=2, column=1, padx=8, pady=10, sticky='NSE')
        # Numero Telefónico.
        l_phone = tk.Label(main_frame, text='No. Telefono:', justify=tk.RIGHT, font=('arial',10,'bold'))
        l_phone.grid(row=3, column=0, padx=5, pady=10, sticky='NSEW')
        l_phone.config(foreground='#FFF', background='#3C3C3C')
        self.e_phone = ttk.Entry(main_frame, width=40, justify='left', font=('arial',10,'bold'))
        self.e_phone.grid(row=3, column=1, padx=8, pady=10, sticky='NSE')

    def _client_specs(self):
        # Variables de acceso.
        self.t_cliente = tk.StringVar()
        self.l_client = tk.StringVar()
        # Frame para el tipo de cliente.
        type_frame = tk.LabelFrame(self, text="Tipo de Cliente", font='bold')
        type_frame.grid(row=1,column=0, padx=5, pady=5, sticky='NSEW')
        type_frame.config(foreground='#FFF', background='#3C3C3C')
        # Frame para la localización del cliente.
        loc_frame = tk.LabelFrame(self, text='Localización Cliente', font='bold')
        loc_frame.grid(row=1, column=1, padx=5, pady=5, sticky='NSEW')
        loc_frame.config(foreground='#FFF', background='#3C3C3C')
        # Selección del tipo de cliente.
        t_one = tk.Radiobutton(type_frame, text='Proveedor', variable=self.t_cliente, value='Proveedor', font=('arial',10,'bold'))
        t_one.grid(row=0, column=0, padx=5, pady=5, sticky='NSW')
        t_one.config(foreground='#FFF', background='#3C3C3C',)
        t_two = tk.Radiobutton(type_frame, text='Comprador', variable=self.t_cliente, value='Comprador', font=('arial',10,'bold'))
        t_two.grid(row=1, column=0, padx=5, pady=5, sticky='NSW')
        t_two.config(foreground='#FFF', background='#3C3C3C')
        # Selección de localización.
        l_one = tk.Radiobutton(loc_frame, text='Local', variable=self.l_client, value='Local', font=('arial',10,'bold'))
        l_one.grid(row=0, column=0, padx=5, pady=5, sticky='NSW')
        l_one.config(foreground='#FFF', background='#3C3C3C')
        l_two = tk.Radiobutton(loc_frame, text='Nacional', variable=self.l_client, value='Nacional', font=('arial',10,'bold'))
        l_two.grid(row=1, column=0, padx=5, pady=5, sticky='NSW')
        l_two.config(foreground='#FFF', background='#3C3C3C')
        l_three = tk.Radiobutton(loc_frame, text='Internacional', variable=self.l_client, value='Internacional', font=('arial',10,'bold'))
        l_three.grid(row=2, column=0, padx=5, pady=5, sticky='NSW')
        l_three.config(foreground='#FFF', background='#3C3C3C')

    def _buttons(self):
        pass


if __name__ == "__main__":
    test = NewClient()