from tkinter import  PhotoImage, Tk, messagebox, scrolledtext, ttk
from search_window import SearchWin
from NewClient_window import NewClient
from Module.client import Client
from Module.notas import Notas
from Module.dao import DaoClient, DaoNotas, DaoProduct
from Module.log_gen import log
import tkinter as tk
import os


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        # Recursos de la ventana.
        icon = os.path.abspath('Sources/icons/agenda_2.ico')
        add_img = os.path.abspath('Sources/images/add_client.png')
        search_img = os.path.abspath('Sources/images/search_client_64x64.png')
        edit_img = os.path.abspath('Sources/images/edit_client.png')
        del_img = os.path.abspath("Sources/images/delete_client.png")
        prod_img = os.path.abspath("Sources/images/prods_64x64.png")
        clear_img = os.path.abspath("Sources/images/clear_btn.png")
        see_img = os.path.abspath("Sources/images/ver_32x32.png")
        del_note_img = os.path.abspath("Sources/images/delete_32x32.png")
        new_note_img = os.path.abspath("Sources/images/add_note_32x32.png")
        edit_note_img = os.path.abspath("SOurces/images/edit_note_32x32.png")
        save_note_img = os.path.abspath("Sources/images/save_file.png")
        self._new = PhotoImage(file= add_img)
        self._search = PhotoImage(file= search_img)
        self._edit = PhotoImage(file= edit_img)
        self._delete = PhotoImage(file= del_img)
        self._prod = PhotoImage(file= prod_img)
        self._clean = PhotoImage(file= clear_img)
        self._see = PhotoImage(file= see_img)
        self._del = PhotoImage(file= del_note_img)
        self._add_note = PhotoImage(file= new_note_img)
        self._edit_note = PhotoImage(file= edit_note_img)
        self._save_note = PhotoImage(file= save_note_img)
        # Variables.
        self._client = None
        self._head_notas = []
        self._cont_note = []
        self._content = None
        self._name = tk.StringVar(value= None)
        self._clave = tk.StringVar(value= None)
        self._lastname = tk.StringVar(value= None)
        self._mothers = tk.StringVar(value= None)
        self._phone = tk.StringVar(value= None)
        self._debt = tk.DoubleVar(value= 0)
        self._balance = tk.DoubleVar(value= 0)
        self._type = tk.StringVar(value= None)
        self._location = tk.StringVar(value= None)
        self._date = tk.StringVar(value= None)
        self._title = tk.StringVar(value= None)
        self._note_content = tk.StringVar(value= None)
        # Dimensiones de la ventana.
        width = 900
        height = 540
        x = self.winfo_screenwidth() // 2 - width // 2
        y = self.winfo_screenheight() // 2 - height // 2
        position = f"{width}x{height}+{x}+{y}"
        # Propiedades de la ventana.
        self.geometry(position)
        self.title("Clientes")
        self.iconbitmap(icon)
        self.resizable(1,1)
        self.state('zoomed')
        self.wm_minsize(width, height)
        # Propiedades del grid.
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self._side_buttons()
        self._data_client()
        self.mainloop()

    def _side_buttons(self):
        # Frame para la botonera de opciones del app.
        btn_frame = tk.Frame(self, relief=tk.RAISED, border=2)
        btn_frame.grid(row=0, column=0, sticky="NSEW")
        # Botones.
        # Agregar un cliente nuevo.
        add_btn = tk.Button(
            btn_frame,
            text="Nuevo Cliente",
            image= self._new,
            compound='top',
            relief= tk.GROOVE,
            border= 0,
            command= NewClient,
            font=('Arial',10,'bold')
        )
        add_btn.grid(row=0, column=0, padx=5, pady=10, sticky="NSEW")
        # Buscar un cliente.
        search_btn = tk.Button(
            btn_frame,
            text="Buscar Cliente",
            image= self._search,
            compound='top',
            relief= tk.GROOVE,
            border=0,
            command= self._load_client,
            font=('Arial',10,'bold')
        )
        search_btn.grid(row=1, column=0, padx=5, pady=10, sticky="NSEW")
        # Editar un cliente.
        self.edit_btn = tk.Button(
            btn_frame,
            text="Editar Cliente",
            image= self._edit,
            compound= 'top',
            border= 0,
            font=('Arial',10,'bold'),
            command= self._edit_client,
            state= tk.DISABLED
        )
        self.edit_btn.grid(row=2, column=0, padx=5, pady=10, sticky="NSEW")
        # Eliminar a un cliente.
        self.delete_btn = tk.Button(
            btn_frame,
            text="Eliminar Cliente",
            image= self._delete,
            compound='top',
            border=0,
            font=('Arial',10,'bold'),
            command= self._delete_client,
            state= tk.DISABLED
        )
        self.delete_btn.grid(row=3, column=0, padx=5, pady=10, sticky="NSEW")
        # Limpiar datos del cliente.
        self.clean_btn = tk.Button(
            btn_frame,
            text="Limpiar",
            image= self._clean,
            compound='top',
            border=0,
            font=('Arial',10,'bold'),
            command= self._clean_data,
            state= tk.DISABLED
        )
        self.clean_btn.grid(row=4, column=0, padx=5, pady=10, sticky="NSEW")
        # Cargar productos del cliente.
        self.prods_btn = tk.Button(
            btn_frame,
            text="Productos",
            image= self._prod,
            compound='top',
            border=0,
            font=('Arial',10,'bold'),
            command= self._load_prods,
            state= tk.DISABLED
        )
        self.prods_btn.grid(row=5, column=0, padx=5, pady=10, sticky="NSEW")

    def _data_client(self, cliente: Client = None):
        # Frame donde se cargaran los datos del cliente seleccionado.
        self.data_frame = tk.LabelFrame(self, text="Cliente")
        self.data_frame.grid(row=0, column=1, padx=5, pady=10, sticky="NSEW")
        # Si ya se selecciono un cliente se cargaran sus datos en las variables.
        if cliente:
            # Logo del cliente.
            logo_img = os.path.abspath(cliente.image)
            self._logo = PhotoImage(file= logo_img)
            # Variables.
            self._clave = tk.StringVar(value= cliente.clave)
            self._name = tk.StringVar(value= cliente.name)
            self._lastname = tk.StringVar(value= cliente.lastname)
            self._mothers = tk.StringVar(value= cliente.mothers)
            self._phone = tk.StringVar(value= cliente.phone)
            self._debt = tk.DoubleVar(value= cliente.debt)
            self._balance = tk.DoubleVar(value= cliente.balance)
            self._date = tk.StringVar(value= cliente.date)
            self._type = tk.StringVar(value= cliente.type_client)
            self._location = tk.StringVar(value= cliente.location)
            # Logo o imagen del cliente.
            logo = tk.Label(self.data_frame, image= self._logo, compound='center' ,bg="#fff")
            logo.config(height=120, width=120)
            logo.grid(row=0, column=0, padx=5, pady=10, rowspan=3)
            new_state = 'active'
            see_state = 'active'
            del_state = 'active'
            edit_state = 'active'
            save_state = 'active'
        else:
            # Logo o imagen del cliente.
            logo = tk.Label(self.data_frame, text="Not Aviable",bg="#fff")
            logo.config(height=6, width=16)
            logo.grid(row=0, column=0, padx=5, pady=10, rowspan=3)
            new_state = 'disabled'
            see_state = 'disabled'
            del_state = 'disabled'
            edit_state = 'disabled'
            save_state = 'disabled'
        # Datos personales del cliente.
        # Nombre(s).
        l_name = tk.Label(self.data_frame, text="Nombre(s)", font=('arial',10,'bold'), justify='right')
        l_name.grid(row=0, column=1, padx=5, pady=5, sticky='NE')
        self._e_name = ttk.Entry(
            self.data_frame,
            textvariable= self._name,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=25)
        self._e_name.grid(row=0, column=2, padx=10,pady=5, sticky="NW", columnspan=2)
        # Apellido Paterno.
        l_lastname = tk.Label(self.data_frame, text='A.Paterno', font=('arial',10,'bold'), justify='right')
        l_lastname.grid(row=1, column=1, padx=5, pady=5, sticky='NE')
        self._e_lastname = ttk.Entry(
            self.data_frame,
            textvariable= self._lastname,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=25
        )
        self._e_lastname.grid(row=1, column=2, padx=10,pady=5, sticky="NW", columnspan=2)
        # Apellido materno.
        l_mothers = tk.Label(self.data_frame, text='A.Materno', font=('arial',10,'bold'), justify='right')
        l_mothers.grid(row=2, column=1, padx=5, pady=5, sticky='NE')
        self._e_mothers = ttk.Entry(
            self.data_frame,
            textvariable= self._mothers,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=25
        )
        self._e_mothers.grid(row=2, column=2, padx=10,pady=5, sticky="NW", columnspan=2)
        # Telefono.
        l_phone = tk.Label(self.data_frame, text="Telefono", font=('arial',10,'bold'), justify='right')
        l_phone.grid(row=3, column=1, padx=5, pady=5, sticky="NE")
        self._e_phone = ttk.Entry(
            self.data_frame,
            textvariable= self._phone,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=25
        )
        self._e_phone.grid(row=3, column=2, padx=10,pady=5, sticky="NW", columnspan=2)
        # Tipo de cliente.
        l_type = tk.Label(self.data_frame, text="Tipo de Cliente", font=('arial',10,'bold'), justify='right')
        l_type.grid(row=4, column=0, padx=5, pady=5, sticky="NW")
        self._e_type = ttk.Entry(
            self.data_frame,
            textvariable= self._type,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=15
        )
        self._e_type.grid(row=4, column=1, padx=2, pady=5, sticky="NW")
        # Localización del cliente.
        l_local = tk.Label(self.data_frame, text="Localización", font=('arial',10,'bold'), justify='right')
        l_local.grid(row=5, column=0, padx=5, pady=5, sticky="NW")
        self._e_type = ttk.Entry(
            self.data_frame,
            textvariable= self._location,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=15
        )
        self._e_type.grid(row=5, column=1, padx=2, pady=5, sticky="NW")
        # Adeudo.
        l_debt = tk.Label(self.data_frame, text="Adeudo", font=('arial',10,'bold'), justify='right')
        l_debt.grid(row=4, column=2, padx=5, pady=5, sticky="NW")
        self._e_debt = ttk.Entry(
            self.data_frame,
            textvariable= self._debt,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=15
        )
        self._e_debt.grid(row=4, column=3, padx=2, pady=5, sticky="NW")
        # Balance a favor.
        l_balance = tk.Label(self.data_frame, text="A Favor", font=('arial',10,'bold'), justify='right')
        l_balance.grid(row=5, column=2, padx=5, pady=5, sticky="NW")
        self._e_balance = ttk.Entry(
            self.data_frame,
            textvariable= self._balance,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=15
        )
        self._e_balance.grid(row=5, column=3, padx=2, pady=5, sticky="NW")
        # Separador
        sep = ttk.Separator(self.data_frame, orient='horizontal')
        sep.grid(row=6, column=0, padx=3,pady=5, sticky='EW', columnspan=4)
        # carga de notas.
        lab = tk.Label(
            self.data_frame,
            text="Notas",
            font=('arial',10,'bold'),
            anchor='nw'
        )
        lab.grid(row=7, column=0, padx=5, sticky="EW", columnspan=4)
        # Tabla con las notas.
        self.tabla_notas = ttk.Treeview(self.data_frame, columns=("titulo","fecha"), show='headings', height=4)
        self.tabla_notas.grid(row=8, column=0,padx=7, sticky='NSEW', columnspan=4)
        # Nombre de las columnas.
        self.tabla_notas.heading("titulo", text="Titulo")
        self.tabla_notas.heading("fecha", text="Fecha de ingreso")
        # Dimensiones y configuración de la columna.
        self.tabla_notas.column("titulo", anchor='center')
        self.tabla_notas.column("fecha", width=70, anchor='center')
        # Scrollbar para la info de las notas
        scrollbar = ttk.Scrollbar(self.data_frame, orient=tk.VERTICAL, command=self.tabla_notas.yview)
        self.tabla_notas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=8, column=4, sticky="NS")
        # Carga de la info de las notas
        self._notes_table(self._clave.get())
        # Botones de interacion.
        self.see_btn = ttk.Button(self.data_frame, text="Ver", image= self._see, compound='left', state= see_state)
        self.see_btn.grid(row=9, column=3, padx=5, pady=5, sticky='NW')
        # Visualización de la nota.
        # Titulo.
        note_title = tk.Label(self.data_frame, text="Titulo", justify='right')
        note_title.grid(row=10, column=0,  padx=5, pady=5 , sticky="NE")
        self.e_note = ttk.Entry(self.data_frame, textvariable= self._title, width=30, font=('arial',10,'bold'), justify='left', state=tk.DISABLED)
        self.e_note.grid(row=10, column=1, padx=5, pady=5, sticky='NEW', columnspan=2)
        # Contenido de la nota.
        self.note_box = scrolledtext.ScrolledText(
            self.data_frame,
            font = ('arial',10,'bold'),
            height = 8,
            width = 80,
            wrap = tk.WORD,
            state=tk.DISABLED,
            border = 0
        )
        self.note_box.grid(row=11, column=0, padx=5, pady=7, columnspan=4)
        # Boton de nueva nota.
        new_note = ttk.Button(
            self.data_frame,
            text="Nueva",
            image= self._add_note,
            compound='left',
            state= new_state
        )
        new_note.grid(row=12, column=0, padx=5, pady=5, sticky='EW')
        # Boton para eliminar una nota
        del_btn = ttk.Button(
            self.data_frame,
            text="Eliminar",
            image= self._del,
            compound='left',
            state= del_state
        )
        del_btn.grid(row=12, column=1, padx=5, pady=5, sticky='EW')
        # Boton para editar la nota.
        edit_btn = ttk.Button(
            self.data_frame,
            text="Editar",
            image= self._edit_note,
            compound='left',
            state= edit_state
        )
        edit_btn.grid(row=12, column=2, padx=5, pady=5, sticky='EW')
        # Boton para guardar la nota
        save_btn = ttk.Button(
            self.data_frame,
            text="Guardar",
            image= self._save_note,
            compound='left',
            state= save_state
        )
        save_btn.grid(row=12, column=3, padx=5, pady=5, sticky='EW')

    def _notes_table(self, key: str):
        if self._head_notas:
            self._head_notas = []
            it = self.tabla_notas.get_children()
            for item in it:
                self.tabla_notas.delete(item)
        if key:
            notes = DaoNotas.getNotas(key)
            if notes:
                for note in notes:
                    info = Notas(
                        id = note[0],
                        id_nota= note[1],
                        f_ingreso= note[2],
                        titulo= note[3],
                        nota= note[4]
                    )
                    self._cont_note.append(info)
                    self._head_notas = [info.titulo, info.f_ingreso]
                    self.tabla_notas.insert("", tk.END, values= self._head_notas)

    def _load_client(self):
        search = SearchWin()
        id_client = search.item
        # Si se selecciono un cliente se activan los botones para su manejo.
        if id_client:
            data = DaoClient.load_client(id_cliente= id_client)
            self._client = Client(
                id= data[0],
                image= data[1],
                clave= data[2],
                name= data[3],
                lastname= data[4],
                mothers= data[5],
                phone= data[6],
                type_client= data[7],
                location= data[8],
                debt= data[9],
                balance= data[10],
                date= data[11],
            )
            self.edit_btn.config(state='active')
            self.delete_btn.config(state='active')
            self.clean_btn.config(state='active')
            self.prods_btn.config(state='active')
            self._data_client(self._client)

    def _edit_client(self):
        pass

    def _delete_client(self):
        pass

    def _load_prods(self):
        pass

    def _load_content(self, id:int):
        if id:
            print(id)
            # note = self._cont_note[id]
            # print(note)

    def _clean_data(self):
        self._name = tk.StringVar(value= None)
        self._clave = tk.StringVar(value= None)
        self._lastname = tk.StringVar(value= None)
        self._mothers = tk.StringVar(value= None)
        self._phone = tk.StringVar(value= None)
        self._debt = tk.DoubleVar(value= 0)
        self._balance = tk.DoubleVar(value= 0)
        self._type = tk.StringVar(value= None)
        self._location = tk.StringVar(value= None)
        self._date = tk.StringVar(value= None)
        self._data_client()
        self.edit_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')
        self.clean_btn.config(state='disabled')
        self.prods_btn.config(state='disabled')



if __name__ == '__main__':
    test = MainWindow()