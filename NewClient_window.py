from tkinter import Toplevel, messagebox, ttk, PhotoImage
from Module.client import Client
from Module.dao import DaoClient
from datetime import datetime
import tkinter as tk
import os


class NewClient(Toplevel):
    def __init__(self):
        super().__init__()
        icon = os.path.abspath("Sources/icons/add.ico")
        self.title("Agregar un cliente")
        self.iconbitmap(icon)
        self.geometry("500x350")
        self.resizable(0, 0)
        # Variables de acceso.
        self.t_cliente = tk.StringVar(value='')
        self.l_cliente = tk.StringVar(value='')
        # Listas de valores.
        self.index_type = ["Comprador", "Proveedor"]
        self.index_loc = ["Local", "Nacional", "Internacional"]
        # Imágenes de los botones.
        path_save = os.path.abspath('Sources/images/save_cliente.png')
        path_cancel = os.path.abspath('Sources/images/close.png')
        self.save_img = PhotoImage(file= path_save)
        self.cancel_img = PhotoImage(file= path_cancel)
        # Fecha actual para el registro.
        dat = datetime.now()
        self._fecha = dat.strftime("%d-%m-%Y")
        # Contenido.
        self._main_content()
        self._client_specs()
        self._buttons()
        self.mainloop()

    def _main_content(self):
        # Frame principal.
        main_frame = tk.LabelFrame(self, text="Datos del Cliente.", font="bold")
        main_frame.grid(row=0, column=0, padx=5, pady=7, sticky="NSEW", columnspan=2)
        # Formulario para el relleno de datos.
        # Nombres
        l_name = tk.Label(
            main_frame, text="Nombre(s):", justify=tk.RIGHT, font=("Arial", 10, "bold")
        )
        l_name.grid(row=0, column=0, padx=5, pady=10, sticky="SW")
        self.e_name = ttk.Entry(
            main_frame, width=40, justify="left", font=("Arial", 10, "bold")
        )
        self.e_name.grid(row=0, column=1, padx=8, pady=10, sticky="NSE")
        self.e_name.focus()
        # Apellido Paterno.
        l_lastname = tk.Label(
            main_frame, text="A. Paterno:", justify=tk.RIGHT, font=("Arial", 10, "bold")
        )
        l_lastname.grid(row=1, column=0, padx=5, pady=10, sticky="NSEW")
        self.e_lastname = ttk.Entry(
            main_frame, width=40, justify="left", font=("Arial", 10, "bold")
        )
        self.e_lastname.grid(row=1, column=1, padx=8, pady=10, sticky="NSE")
        # Apellido Materno
        l_mothers = tk.Label(
            main_frame, text="A. Materno:", justify=tk.RIGHT, font=("Arial", 10, "bold")
        )
        l_mothers.grid(row=2, column=0, padx=5, pady=10, sticky="NSEW")
        self.e_mothers = ttk.Entry(
            main_frame, width=40, justify="left", font=("arial", 10, "bold")
        )
        self.e_mothers.grid(row=2, column=1, padx=8, pady=10, sticky="NSE")
        # Numero Telefónico.
        l_phone = tk.Label(
            main_frame,
            text="No. Telefono:",
            justify=tk.RIGHT,
            font=("arial", 10, "bold"),
        )
        l_phone.grid(row=3, column=0, padx=5, pady=10, sticky="NSEW")
        self.e_phone = ttk.Entry(
            main_frame, width=40, justify="left", font=("arial", 10, "bold")
        )
        self.e_phone.grid(row=3, column=1, padx=8, pady=10, sticky="NSE")

    def _client_specs(self):
        # Valor por defecto del radiobutton.
        self.l_cliente.set(0)
        self.t_cliente.set(0)
        # Frame para el tipo de cliente.
        type_frame = tk.LabelFrame(self, text="Tipo de Cliente", font="bold")
        type_frame.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")
        # Frame para la localización del cliente.
        loc_frame = tk.LabelFrame(self, text="Localización Cliente", font="bold")
        loc_frame.grid(row=1, column=1, padx=5, pady=5, sticky="NSEW")
        # Selección del tipo de cliente.
        t_one = tk.Radiobutton(
            type_frame,
            text="Proveedor",
            variable=self.t_cliente,
            value=1,
            font=("arial", 10, "bold"),
            command=lambda: self.t_cliente.get(),
        )
        t_one.grid(row=0, column=0, padx=5, pady=5, sticky="NSW")
        t_two = tk.Radiobutton(
            type_frame,
            text="Comprador",
            variable=self.t_cliente,
            value=0,
            font=("arial", 10, "bold"),
            command=lambda: self.t_cliente.get(),
        )
        t_two.grid(row=1, column=0, padx=5, pady=5, sticky="NSW")
        # Selección de localización.
        l_one = tk.Radiobutton(
            loc_frame,
            text="Local",
            variable=self.l_cliente,
            value=0,
            font=("arial", 10, "bold"),
            command= lambda: self.l_cliente.get()
        )
        l_one.grid(row=0, column=0, padx=5, pady=5, sticky="NSW")
        l_two = tk.Radiobutton(
            loc_frame,
            text="Nacional",
            variable=self.l_cliente,
            value=1,
            font=("arial", 10, "bold"),
            command= lambda: self.l_cliente.get()
        )
        l_two.grid(row=1, column=0, padx=5, pady=5, sticky="NSW")
        l_three = tk.Radiobutton(
            loc_frame,
            text="Internacional",
            variable=self.l_cliente,
            value=2,
            font=("arial", 10, "bold"),
            command= lambda: self.l_cliente.get()
        )
        l_three.grid(row=2, column=0, padx=5, pady=5, sticky="NSW")

    def _buttons(self):
        # frame botonera
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=0, column=2, padx=5,pady=12, sticky='NSEW')
        # Botones
        save_btn = tk.Button(
            btn_frame,
            text="Guardar",
            image= self.save_img,
            compound='top',
            command= self._save,
        )
        save_btn.grid(row=0, column=0, padx=2, pady=5, sticky='EW')
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancelar",
            image= self.cancel_img,
            compound='top',
            command= self._cancel
        )
        cancel_btn.grid(row=1, column=0, padx=2, pady=5, sticky='EW')

    def _save(self):
        # Obtención de los datos ingresados.
        nombre = self.e_name.get()
        a_paterno = self.e_lastname.get()
        a_materno = self.e_mothers.get()
        telefono = self.e_phone.get()
        tipo_cliente = self.index_type[int(self.t_cliente.get())]
        localization_cliente = self.index_loc[int(self.l_cliente.get())]
        # Verificación del formulario.
        titulo = "Campo Vació"
        if not nombre:
            messagebox.showwarning(titulo, "El campo de nombre esta vació")
        if not a_paterno and not a_materno:
            messagebox.showwarning(titulo, "El campo de Apellido esta vació debe ingresar al menos un apellido.")
        if not telefono:
            messagebox.showwarning(titulo, "El campo de Telefono esta vació")
        # Conversion a objeto tipo cliente.
        if nombre and telefono and a_paterno or a_materno:
            new_client = Client(
                name= nombre.title(),
                lastname= a_paterno.title(),
                mothers= a_materno.title(),
                phone= telefono.title(),
                type_client= tipo_cliente,
                location= localization_cliente,
                date= self._fecha
            )
            try:
                result = DaoClient.singup(new_client)
                if result:
                    messagebox.showinfo("Nuevo Cliente", f"Cliente Registrado con éxito\n Clave: {new_client.clave}")
                    self.quit()
            except Exception as ex:
                messagebox.showerror('Error', f"No se pudo registrar al cliente\nError: {ex}")

    def _cancel(self):
        self.quit()
        self.destroy()



if __name__ == "__main__":
    test = NewClient()
