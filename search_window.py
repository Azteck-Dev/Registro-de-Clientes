from Module.client import Client
from Module.dao import DaoClient
from tkinter import PhotoImage, Toplevel, messagebox, ttk
import tkinter as tk
import os


class SearchWin(Toplevel):
    def __init__(self):
        super().__init__()
        # Recursos de la ventana.
        icon_path = os.path.abspath("Sources/icons/search.ico")
        search_img = os.path.abspath("Sources/images/search_client_32x32.png")
        see_img = os.path.abspath("Sources/images/ver_48x48.png")
        cancel_img = os.path.abspath("Sources/images/cancel_48x48.png")
        self.s_img = PhotoImage(file=search_img)
        self.see_img = PhotoImage(file=see_img)
        self.cancel_img = PhotoImage(file=cancel_img)
        # Dimensiones de la ventana.
        ancho_ventana = 900
        alto_ventana = 550
        x_ventana = self.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.winfo_screenheight() // 2 - alto_ventana // 2
        position = f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}"
        # Propiedades de la ventana.
        self.title("Buscar Un Cliente")
        self.geometry(position)
        self.resizable(0, 0)
        self.iconbitmap(icon_path)
        # Variables
        self._results = []
        self._item= None
        # Contenido de la ventana.
        self._main_content()
        self.mainloop()

    @property
    def item(self):
        return self._item

    def _main_content(self):
        # Frame principal para el contenido.
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both")
        # Frame de busqueda de clientes.
        search_frame = tk.LabelFrame(main_frame, text="Busqueda", font="bold")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="EW")
        # Frame de resultado de la busqueda.
        result_frame = tk.LabelFrame(main_frame, text="Resultados", font="bold")
        result_frame.grid(row=1, column=0, padx=10, pady=3, sticky="NSEW")
        # Frame para los botones.
        btn_frame = tk.Frame(
            main_frame,
        )
        btn_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NSE")
        # Contenido del Frame de busqueda.
        # Nombre(s)
        l_search = tk.Label(search_frame, text="Nombre(s)", font=("arial", 10, "bold"))
        l_search.grid(row=0, column=0, padx=10, pady=10, sticky="SE")
        self.e_name = ttk.Entry(search_frame, width=20, justify="left")
        self.e_name.grid(row=0, column=1, padx=5, pady=10, sticky="SW")
        self.e_name.focus()
        # Apellido Paterno
        l_search = tk.Label(search_frame, text="A.Paterno", font=("arial", 10, "bold"))
        l_search.grid(row=0, column=2, padx=10, pady=10, sticky="SE")
        self.e_lastname = ttk.Entry(search_frame, width=20, justify="left")
        self.e_lastname.grid(row=0, column=3, padx=5, pady=10, sticky="SW")
        # Apellido Materno.
        l_search = tk.Label(search_frame, text="A.Materno", font=("arial", 10, "bold"))
        l_search.grid(row=0, column=4, padx=10, pady=10, sticky="SE")
        self.e_mothers = ttk.Entry(search_frame, width=20, justify="left")
        self.e_mothers.grid(row=0, column=5, padx=5, pady=10, sticky="SW")
        # Boton de busqueda.
        search_btn = ttk.Button(
            search_frame,
            text="Buscar",
            image=self.s_img,
            compound="left",
            command=self._search_client,
        )
        search_btn.grid(row=0, column=6, padx=5, pady=10, sticky="EW")
        # Información de ayuda.
        l_help = ttk.Label(
            search_frame,
            text="**Ingrese al menos un dato para la busqueda.",
            font="bold",
            justify="center",
        )
        l_help.grid(row=1, column=0, padx=20, pady=5, sticky="EW", columnspan=6)
        # Contenido de los resultados.
        self.result_table = ttk.Treeview(
            result_frame,
            columns=("id","clave", "name", "lastname", "mothers"),
            height=13,
            show="headings",
            selectmode='browse'
        )
        self.result_table.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        # Titulo de los campos de la tabla
        self.result_table.heading("id", text="Id")
        self.result_table.heading("clave", text="Clave")
        self.result_table.heading("name", text="Nombre")
        self.result_table.heading("lastname", text="A. Paterno")
        self.result_table.heading("mothers", text="A. Materno")
        # Dimensiones de las columnas
        self.result_table.column("id",width=60, anchor='center')
        self.result_table.column("clave",width=150, anchor='center')
        self.result_table.column("name", anchor='center')
        self.result_table.column("lastname", anchor='center')
        self.result_table.column("mothers", anchor='center')
        # Scrollbar para los resultados.
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_table.yview)
        self.result_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="NS")
        # Botones
        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancelar",
            image=self.cancel_img,
            compound="left",
            command=self.cancel,
        )
        cancel_btn.grid(row=0, column=0, padx=10, pady=5, sticky="WE")
        see_btn = ttk.Button(btn_frame, text="Ver", image=self.see_img, compound="left", command=self.see)
        see_btn.grid(row=0, column=1, padx=10, pady=5, sticky="WE")

    def _search_client(self):
        # Si la lista de resultados ya contiene información se resetea.
        if self._results:
            self._results = []
        # Si la tabla ya tiene información se limpia.
        for item in self.result_table.get_children():
            self.result_table.delete(item)
        # Obtención de los datos proporcionados.
        nombre = self.e_name.get()
        a_paterno = self.e_lastname.get()
        a_materno = self.e_mothers.get()
        if self._check_entry(nombre, a_paterno, a_materno):
            results = DaoClient.search(
                name=nombre.title(),
                lastname=a_paterno.strip().title(),
                mothers=a_materno.strip().title(),
            )
            if not results:
                messagebox.showinfo(
                    "Resultados", "No se encontró ninguna coincidencia."
                )
            else:
                # Lectura de resultados y creación del objeto tipo cliente.
                for data in results:
                    client = Client(
                        id=data[0],
                        image=data[1],
                        clave=data[2],
                        name=data[3],
                        lastname=data[4],
                        mothers=data[5],
                        phone=data[6],
                        type_client=data[7],
                        location=data[8],
                        debt=data[9],
                        balance=data[10],
                        date=data[11],
                    )
                    self._results.append(client)
        # Inserción de los resultados.
        self._table_insert(self._results)

    # Verificación de campos ingresados.
    def _check_entry(self, *args):
        if args[0] or args[1] or args[2]:
            return True
        else:
            messagebox.showerror("Campos Vacíos", "Debes introducir al menos un dato para la busqueda")
            return False

    # Inserta los resultados en la tabla.
    def _table_insert(self, clientes:tuple):
        for data in clientes:
            result = [data.id, data.clave, data.name, data.lastname, data.mothers]
            self.result_table.insert("", tk.END, values=result, text=data.id)

    # Obtenemos el cliente seleccionado y su objeto.
    def see(self):
        item = self.result_table.item(self.result_table.selection())
        self._item = item['text']
        self.cancel()

    def cancel(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    test = SearchWin()
