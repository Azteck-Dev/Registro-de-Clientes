# Code by: J.Mesach Venegas
# email: mesach.venegas@gmail.com
from tkinter import PhotoImage, TclError, Tk, messagebox, scrolledtext, ttk, filedialog
from Module.productos import Producto
from search_window import SearchWin
from NewClient_window import NewClient
from Module.client import Client
from Module.notas import Notas
from Module.dao import DaoClient, DaoNotas, DaoProduct
from datetime import datetime
from img_handler import HandImg
import tkinter as tk
import os


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        # Recursos de la ventana.
        self.font_style = "arial",10,'bold'
        icon = os.path.abspath('Sources/icons/agenda_2.ico')
        add_img = os.path.abspath('Sources/images/add_client.png')
        search_img = os.path.abspath('Sources/images/search_client_64x64.png')
        edit_img = os.path.abspath('Sources/images/edit_client.png')
        del_img = os.path.abspath("Sources/images/delete_client.png")
        exit_img = os.path.abspath("Sources/images/exit_64x64.png")
        clear_img = os.path.abspath("Sources/images/clear_btn.png")
        see_img = os.path.abspath("Sources/images/ver_32x32.png")
        del_note_img = os.path.abspath("Sources/images/delete_32x32.png")
        new_note_img = os.path.abspath("Sources/images/add_note_32x32.png")
        edit_note_img = os.path.abspath("SOurces/images/edit_note_32x32.png")
        save_note_img = os.path.abspath("Sources/images/save_file.png")
        cancel_img = os.path.abspath("Sources/images/cancel_64x64.png")
        save_client_img = os.path.abspath("Sources/images/save_cliente_64x64.png")
        load_img = os.path.abspath("Sources/images/load_32x32.png")
        search_prod = os.path.abspath("Sources/images/search_client_32x32.png")
        new_prod = os.path.abspath("Sources/images/new_prod_32x32.png")
        delete_prod = os.path.abspath("Sources/images/delete_prod_32x32.png")
        update_prod = os.path.abspath("Sources/images/update_prod_32x32.png")
        save_prod = os.path.abspath("Sources/images/save_prod_32x32.png")
        self._new = PhotoImage(file= add_img)
        self._search = PhotoImage(file= search_img)
        self._edit = PhotoImage(file= edit_img)
        self._delete = PhotoImage(file= del_img)
        self._exit = PhotoImage(file= exit_img)
        self._clean = PhotoImage(file= clear_img)
        self._see = PhotoImage(file= see_img)
        self._del = PhotoImage(file= del_note_img)
        self._add_note = PhotoImage(file= new_note_img)
        self._edit_note = PhotoImage(file= edit_note_img)
        self._save_note = PhotoImage(file= save_note_img)
        self._cancel_update_client = PhotoImage(file= cancel_img)
        self._save_update_client = PhotoImage(file= save_client_img)
        self._load = PhotoImage(file= load_img)
        self._search_prod = PhotoImage(file= search_prod)
        self._new_prod = PhotoImage(file= new_prod)
        self._delete_prod = PhotoImage(file= delete_prod)
        self._update_prod = PhotoImage(file= update_prod)
        self._save_prod = PhotoImage(file= save_prod)
        # Variables.
        self._client = None
        self._products = None
        self.product = None
        self._head_notas = []
        self._cont_note = []
        self._content = None
        self._obj_note = None
        self._id = tk.StringVar(value= None)
        self._name = tk.StringVar(value= None)
        self._clave = tk.StringVar(value= None)
        self._lastname = tk.StringVar(value= None)
        self._mothers = tk.StringVar(value= None)
        self._phone = tk.StringVar(value= None)
        self._debt = tk.DoubleVar(value= None)
        self._balance = tk.DoubleVar(value= None)
        self._type = tk.StringVar(value= None)
        self._location = tk.StringVar(value= None)
        self._date = tk.StringVar(value= None)
        self._title = tk.StringVar(value= None)
        self._note_content = tk.StringVar(value= None)
        self._product_name = tk.StringVar(value= None)
        self._product_folio = tk.IntVar(value= None)
        self._product_key = tk.StringVar(value= None)
        self._product_description = tk.StringVar(value= None)
        self._product_price = tk.DoubleVar(value= None)
        self._product_in = tk.StringVar(value= None)
        self._product_out = tk.StringVar(value= None)
        self._product_lote = tk.StringVar(value= None)
        self._product_qty = tk.DoubleVar(value= None)
        # Dimensiones de la ventana.
        width = 750
        height = 670
        x = self.winfo_screenwidth() // 2 - width // 2
        y = self.winfo_screenheight() // 2 - height // 2 - 35
        position = f"{width}x{height}+{x}+{y}"
        # Propiedades de la ventana.
        self.geometry(position)
        self.title("Clientes")
        self.iconbitmap(icon)
        self.resizable(0,0)
        self.minsize(width,height)
        self.state('zoomed')
        # Propiedades del grid.
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self._side_buttons()
        self._data_client()
        self._tab_frame()
        self.mainloop()

    # Frame Con la botonera de interaccion principal
    def _side_buttons(self):
        """Frame donde se carga la botonera de interacion principal.
        """
        # Frame para la botonera de opciones del app.
        btn_frame = tk.Frame(self, relief=tk.RAISED, border=2)
        btn_frame.grid(row=0, column=0, sticky="NSEW")
        # Botones.
        # Agregar un cliente nuevo.
        self.add_btn = tk.Button(
            btn_frame,
            text="Nuevo Cliente",
            image= self._new,
            compound='top',
            relief= tk.GROOVE,
            border= 0,
            command= NewClient,
            font=('Arial',10,'bold')
        )
        self.add_btn.grid(row=0, column=0, padx=5, pady=10, sticky="NSEW")
        # Buscar un cliente.
        self.search_btn = tk.Button(
            btn_frame,
            text="Buscar Cliente",
            image= self._search,
            compound='top',
            relief= tk.GROOVE,
            border=0,
            command= self._load_client,
            font=('Arial',10,'bold')
        )
        self.search_btn.grid(row=1, column=0, padx=5, pady=10, sticky="NSEW")
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
        self.exit_btn = tk.Button(
            btn_frame,
            text="Salir",
            image= self._exit,
            compound='top',
            border=0,
            font=('Arial',10,'bold'),
            command= lambda: (self.quit, self.destroy()),
        )
        self.exit_btn.grid(row=5, column=0, padx=5, pady=10, sticky="NSEW")

    # Frame donde se carga la información del cliente.
    def _data_client(self, cliente: Client = None):
        """Encargada de crear el frame donde se visualizaran los datos del cliente.

        Args:
            cliente (Client, optional): Objeto con la información del cliente  a cargar. Defaults to None.
        """
        # Frame donde se cargaran los datos del cliente seleccionado.
        self.data_frame = tk.LabelFrame(self, text="Cliente")
        self.data_frame.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")
        # Si ya se selecciono un cliente se cargaran sus datos en las variables.
        if cliente:
            flag = True
            # Logo del cliente.
            logo_img = os.path.abspath(cliente.image)
            self._logo = PhotoImage(file= logo_img)
            # Variables.
            self._id = tk.StringVar(value= cliente.id)
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
            self.logo = tk.Label(self.data_frame, image= self._logo, compound='center' ,bg="#fff")
            self.logo.config(height=120, width=120)
            self.logo.grid(row=0, column=0, padx=5, pady=10, rowspan=3)
        else:
            flag = False
            # Logo o imagen del cliente.
            self.logo = tk.Label(self.data_frame, text="Not Aviable",bg="#fff")
            self.logo.config(height=6, width=16)
            self.logo.grid(row=0, column=0, padx=5, pady=10, rowspan=3)

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
        self._e_location = ttk.Entry(
            self.data_frame,
            textvariable= self._location,
            font=('arial',10,'bold'),
            state= tk.DISABLED,
            width=15
        )
        self._e_location.grid(row=5, column=1, padx=2, pady=5, sticky="NW")
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
        # carga de notas.
        lab = tk.Label(
            self.data_frame,
            text="Notas",
            font=('arial',10,'bold'),
            anchor='nw'
        )
        lab.grid(row=7, column=0, padx=5, sticky="EW", columnspan=4)
        # Tabla con las notas.
        self.tabla_notas = ttk.Treeview(self.data_frame, columns=("titulo","fecha"), show='headings', height=4, selectmode='browse')
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
        # Lector de eventos de selección en la tabla de notas.
        self.tabla_notas.bind("<Double 1>", self._text_note)
        # Funcion encargada de mostrar las notas del cliente.
        self._widget_notes(flag=flag)

    # Widget donde se carga la nota para su visualización y manipulación.
    def _widget_notes(self, flag: bool, note: Notas = None):
        """Encargada de generar la vista para las notas del cliente cada que se recarga el widget."""
        if note:
            new_state = tk.NORMAL
            del_state = tk.NORMAL
            edit_state = tk.NORMAL
            save_state = tk.DISABLED
            self._title = note.titulo
            self._content = note.nota
        elif flag:
            new_state = tk.NORMAL
            del_state = tk.DISABLED
            edit_state = tk.DISABLED
            save_state = tk.DISABLED
        else:
            new_state = tk.DISABLED
            del_state = tk.DISABLED
            edit_state = tk.DISABLED
            save_state = tk.DISABLED
        # Visualización de la nota.
        # Titulo.
        note_title = tk.Label(self.data_frame, text="Titulo", justify='right')
        note_title.grid(row=9, column=0,  padx=5, pady=5 , sticky="SE")
        self.e_note = ttk.Entry(self.data_frame, textvariable= self._title, width=30, font=('arial',10,'bold'), justify='left', state=tk.DISABLED)
        # Si se selecciono una nota se activa la caja de texto e inserta el titulo de la nota.
        if note:
            self.e_note.config(state=tk.NORMAL)
            if self.e_note.get():
                self.e_note.delete(0, tk.END)
            self.e_note.insert(tk.END,self._title)
            self.e_note.config(state= tk.DISABLED)
        self.e_note.grid(row=9, column=1, padx=5, pady=5, sticky='SEW', columnspan=2)
        # Contenido de la nota.
        self.note_box = scrolledtext.ScrolledText(
            self.data_frame,
            font = ('arial',10,'bold'),
            height = 10,
            width = 80,
            wrap = tk.WORD,
            state=tk.DISABLED,
            border = 0
        )
        self.note_box.grid(row=10, column=0, padx=5, pady=7, columnspan=4)
        # Carga de la nota en la caja de texto.
        if note:
            self.note_box.config(state='normal')
            if self.note_box.get('1.0', tk.END):
                self.note_box.delete('1.0',tk.END)
            self.note_box.insert(tk.INSERT, self._content)
            self.note_box.config(state=tk.DISABLED)
        # Boton de nueva nota.
        self.new_note_btn = ttk.Button(
            self.data_frame,
            text="Nueva",
            image= self._add_note,
            compound='left',
            state= new_state,
            command= self._create_note
        )
        self.new_note_btn.grid(row=11, column=0, padx=5, pady=5, sticky='EW')
        # Boton para eliminar una nota
        self.del_note_btn = ttk.Button(
            self.data_frame,
            text="Eliminar",
            image= self._del,
            compound='left',
            state= del_state,
            command= self._delete_note
        )
        self.del_note_btn.grid(row=11, column=1, padx=5, pady=5, sticky='EW')
        # Boton para editar la nota.
        self.edit_note_btn = ttk.Button(
            self.data_frame,
            text="Editar",
            image= self._edit_note,
            compound='left',
            state= edit_state,
            command= self._fun_edit_note
        )
        self.edit_note_btn.grid(row=11, column=2, padx=5, pady=5, sticky='EW')
        # Boton para guardar la nota
        self.save_note_btn = ttk.Button(
            self.data_frame,
            text="Guardar",
            image= self._save_note,
            compound='left',
            state= save_state,
            command= self._save_new_note
        )
        self.save_note_btn.grid(row=11, column=3, padx=5, pady=5, sticky='EW')

    # Frame para la visualización de los productos del cliente.
    def _tab_frame(self, cliente: Client = None):
        self.prod_frame = tk.LabelFrame(self, text="Productos")
        self.prod_frame.grid(row=0, column=2, padx=5, pady=5, sticky='NSEW')
        type_search = ["Seleccionar","Folio","Producto"]
        # Busqueda
        l_search_type = tk.Label(self.prod_frame, text="Buscar por", font=("arial",10,'bold'))
        l_search_type.grid(row=0, column=0, padx=5, pady=5, sticky='SE')
        self.e_type_box = ttk.Combobox(self.prod_frame, values=type_search, width=10)
        self.e_type_box.grid(row=0, column=1, padx=5, pady=5, sticky="SW")
        self.e_type_box.current(0)
        l_text_search = tk.Label(self.prod_frame, text="Folio/Producto", font=("arial",10,'bold'))
        l_text_search.grid(row=1, column=0, padx=5, pady=5, sticky='SE')
        self.e_text_search = ttk.Entry(self.prod_frame, width=30, justify='left')
        self.e_text_search.grid(row=1, column=1,padx=5, pady=5, sticky="SW")
        # Boton para la busqueda.
        self.product_search_btn = ttk.Button(
            self.prod_frame,
            text="Buscar",
            image= self._search_prod,
            compound='left',
            command= self._research_prod
        )
        self.product_search_btn.grid(row=1, column=2, padx=5, pady=5, sticky='NEW')
        # Tabla de productos.
        self.tabla_productos = ttk.Treeview(
            self.prod_frame,
            columns=("folio","name","cost","qty","in","out"),
            show='headings',
            height=13
        )
        self.tabla_productos.grid(row=2, column=0, padx=5, pady=5, sticky="NSEW",columnspan=3)
        # Columnas de la tabla.
        self.tabla_productos.heading("folio", text="Folio")
        self.tabla_productos.heading("name", text="Nombre")
        self.tabla_productos.heading("cost", text="Precio")
        self.tabla_productos.heading("qty",text="Cantidad")
        self.tabla_productos.heading("in", text="Ingreso")
        self.tabla_productos.heading("out",text="Salio")
        # Dimensiones de las columnas
        self.tabla_productos.column("folio", width=75, anchor= tk.CENTER)
        self.tabla_productos.column("name",width=130, anchor= tk.CENTER)
        self.tabla_productos.column("cost",width=80, anchor= tk.CENTER)
        self.tabla_productos.column("qty",width=80, anchor= tk.CENTER)
        self.tabla_productos.column("in",width=100, anchor= tk.CENTER)
        self.tabla_productos.column("out",width=100, anchor= tk.CENTER)
        # Scrollbar para la info de las notas
        scrollbar = ttk.Scrollbar(self.prod_frame, orient=tk.VERTICAL, command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=3, sticky="NS")
        self.tabla_productos.bind("<Double 1>", self._select_product)
        # Carga de productos en la tabla
        if cliente:
            self._load_products(cliente.clave)
        # Información detallada del producto.
        self._prod_info()

    # Frame donde se desglosan los datos del producto.
    def _prod_info(self, producto:Producto = None):
        # Frame contendor de la información.
        detail_frame = tk.Frame(self.prod_frame)
        detail_frame.grid(row=4, column=0, padx=5, pady=5, sticky="NSEW", columnspan=4)
        # Cambio de valores de las variables si se ha seleccionado un producto.
        if producto:
            self._product_name = tk.StringVar(value= producto.name)
            self._product_key = tk.StringVar(value= producto.id)
            self._product_lote = tk.StringVar(value= producto.prod_id)
            self._product_folio = tk.StringVar(value= producto.folio)
            self._product_qty = tk.StringVar(value= producto.cantidad)
            self._product_price = tk.StringVar(value= producto.cost)
            self._product_description = tk.StringVar(value= producto.description)
            self._product_in = tk.StringVar(value= producto.f_in)
            self._product_out = tk.StringVar(value= producto.f_out)
            index_currency = self.t_currency.index(producto.currency)
            index_size = self.t_size.index(producto.size)
            self._crud_product(producto)
        else:
            self._crud_product()
        self.t_currency = ["None", "dlls", "mxn"]
        self.t_size = ["None","kgs","pzs","lts","ton","lbs","oz","m","cm","g"]
        # Folio del producto.
        l_folio = tk.Label(detail_frame, text="Folio", justify=tk.RIGHT, font= self.font_style)
        l_folio.grid(row=0, column=0, padx=5, pady=10, sticky='NE')
        self.e_prod_folio = ttk.Entry(
            detail_frame,
            textvariable= self._product_folio,
            width=10,
            justify=tk.LEFT,
            font= self.font_style,
            state= tk.DISABLED
        )
        self.e_prod_folio.grid(row=0, column=1, padx=5, pady=10, sticky="NW")
        # Lote del producto
        l_lote = tk.Label(detail_frame, text="Lote", font= self.font_style)
        l_lote.grid(row=0, column=2, padx=5, pady=10, sticky='NW')
        self.e_prod_lote = ttk.Entry(
            detail_frame,
            textvariable= self._product_lote,
            width=15,
            justify=tk.LEFT,
            font= self.font_style,
            state= tk.DISABLED
        )
        self.e_prod_lote.grid(row=0, column=3, padx=5, pady=10, sticky="NW")
        # Clave de cliente.
        l_clave = tk.Label(detail_frame, text="Cod. Cliente", font= self.font_style)
        l_clave.grid(row=0, column=4, padx=5, pady=10, sticky='NW')
        self.e_prod_clave = ttk.Entry(
            detail_frame,
            textvariable= self._product_key,
            width=20,
            justify=tk.LEFT,
            font= self.font_style,
            state= tk.DISABLED
        )
        self.e_prod_clave.grid(row=0, column=5, padx=5, pady=10, sticky="NW")
        # Nombre del producto
        l_name = tk.Label(detail_frame, text="Nombre", font= self.font_style)
        l_name.grid(row=1, column=0, padx=5, pady=5, sticky="SE")
        self.e_prod_name = ttk.Entry(
            detail_frame,
            textvariable= self._product_name,
            font= self.font_style,
            state= tk.DISABLED
        )
        self.e_prod_name.grid(row=1, column=1, padx=5, pady=5, sticky="SW", columnspan=2)
        # Costo del producto.
        l_cost = tk.Label(detail_frame, text="Precio", font= self.font_style)
        l_cost.grid(row=2, column=0, padx=5, pady=5, sticky="SW")
        self.e_prod_cost = ttk.Entry(
            detail_frame,
            width=10,
            textvariable= self._product_price,
            font= self.font_style,
            state= tk.DISABLED
        )
        self.e_prod_cost.grid(row=2, column=1, padx=5, pady=5, sticky="SW")
        # Tipo de moneda.
        self.box_currency = ttk.Combobox(
            detail_frame,
            values= self.t_currency,
            width=5,
            font= self.font_style,
            state= tk.DISABLED
        )
        self.box_currency.grid(row=2, column=2, padx=5, pady=5, sticky="SW")
        # Cantidad del producto.
        l_qty = tk.Label(detail_frame, text="Cantidad", font= self.font_style)
        l_qty.grid(row=3, column=0, padx=5, pady=5, sticky="SW")
        self.e_prod_qty = ttk.Entry(
            detail_frame,
            width=10,
            textvariable= self._product_qty,
            font= self.font_style,
            state= tk.DISABLED
        )
        self.e_prod_qty.grid(row=3, column=1, padx=5, pady=5, sticky="SW")
        # Medicion del producto.
        self.box_size = ttk.Combobox(
            detail_frame,
            values= self.t_size,
            width=5,
            font= self.font_style,
            state= tk.DISABLED
        )
        self.box_size.grid(row=3, column=2, padx=5, pady=5, sticky="SW")
        if producto:
            self.box_currency.current(index_currency)
            self.box_size.current(index_size)
        else:
            self.box_currency.current(0)
            self.box_size.current(0)
        # Descripcion del producto.
        l_description = tk.Label(detail_frame, text="Descripcion", font= self.font_style)
        l_description.grid(row=1, column=3, padx=5, pady=5, sticky="SW")
        self.box_description = scrolledtext.ScrolledText(
            detail_frame,
            width=50,
            height= 5,
            font= self.font_style,
            state = tk.DISABLED,
            border = 0
        )
        self.box_description.grid(row=2,column=3, padx=5, pady=5, sticky="NW", rowspan=3, columnspan=3)
        if producto:
            self.box_description.config(state= tk.NORMAL)
            if producto.description:
                self.box_description.insert('1.0',producto.description)
            self.box_description.config(state= tk.DISABLED)

    # Botones de interacion CRUD de los productos.
    def _crud_product(self, producto: Producto = None):
        # Frame para los botones
        self.frame_crud = ttk.Frame(self.prod_frame)
        self.frame_crud.grid(row=5, column=0, padx=5, pady=5, columnspan=4, sticky="EW")
        # Estado de los botones según si hay producto o no.
        if self._client is None:
            state_new_btn = tk.DISABLED
            state_delete_btn = tk.DISABLED
            state_change_btn = tk.DISABLED
            state_save_btn = tk.DISABLED
        elif self._client and producto:
            state_new_btn = tk.NORMAL
            state_delete_btn = tk.NORMAL
            state_change_btn = tk.NORMAL
            state_save_btn = tk.DISABLED
        else:
            state_new_btn = tk.NORMAL
            state_delete_btn = tk.DISABLED
            state_change_btn = tk.DISABLED
            state_save_btn = tk.DISABLED
        # Boton de nuevo producto.
        self.btn_new_product = ttk.Button(
            self.frame_crud,
            text="Nuevo",
            state= state_new_btn,
            image= self._new_prod,
            compound='left',
            command= self._add_product
        )
        self.btn_new_product.grid(row=0, column=0, padx=7, pady=7, sticky="EW")
        # Boton de eliminar producto.
        self.btn_delete_product = ttk.Button(
            self.frame_crud,
            text="Eliminar",
            state= state_delete_btn,
            image= self._delete_prod,
            compound='left',
            command= self._delete_product
        )
        self.btn_delete_product.grid(row=0, column=1, padx=7, pady=7, sticky="EW")
        # Boton de edición de producto.
        self.btn_edit_product = ttk.Button(
            self.frame_crud,
            text="Actualizar",
            state= state_change_btn,
            image= self._update_prod,
            compound= 'left',
            command= self._update_product
        )
        self.btn_edit_product.grid(row=0, column=3, padx=7, pady=7, sticky="EW")
        # Boton de gardado de cambios.
        self.btn_save_changes_prod = ttk.Button(
            self.frame_crud,
            text="Guardar",
            state= state_save_btn,
            image= self._save_prod,
            compound='left',
            command= lambda: self._save_changes_product()
        )
        self.btn_save_changes_prod.grid(row=0, column=4, padx=7, pady=7, sticky="EW")

### Funciones para botonera crud de productos.
    def _add_product(self):
        # Activación de los campos.
        self.e_prod_name.config(state= tk.NORMAL)
        self.e_prod_lote.config(state= tk.NORMAL)
        self.e_prod_clave.config(state= tk.NORMAL)
        self.e_prod_qty.config(state= tk.NORMAL)
        self.e_prod_cost.config(state= tk.NORMAL)
        self.e_prod_folio.config(state= tk.NORMAL)
        self.box_description.config(state= tk.NORMAL)
        self.box_currency.config(state= tk.NORMAL)
        self.box_size.config(state= tk.NORMAL)
        # Limpieza del contenido de los campos.
        if not self.e_prod_clave.get():
            self.e_prod_clave.insert(0,self._client.clave)
            self.e_prod_clave.config(state= tk.DISABLED)
        else:
            self.e_prod_clave.config(state= tk.DISABLED)
        self.e_prod_name.delete(0,tk.END)
        self.e_prod_lote.delete(0,tk.END)
        self.e_prod_lote.config(state= tk.DISABLED)
        self.e_prod_qty.delete(0,tk.END)
        self.e_prod_cost.delete(0,tk.END)
        self.e_prod_folio.delete(0,tk.END)
        self.box_description.delete('1.0', tk.END)
        self.box_currency.current(0)
        self.box_size.current(0)
        self.e_prod_folio.focus()
        # Cambio de estado de la botonera.
        self.btn_new_product.config(state= tk.DISABLED)
        self.btn_delete_product.config(text="Cancelar", state= tk.NORMAL, command= self._cancel_create)
        self.btn_edit_product.config(state= tk.DISABLED)
        self.btn_save_changes_prod.config(state= tk.NORMAL)

    def _delete_product(self):
        try:
            DaoProduct.prodDel(self.product.prod_id)
            self._product_name = tk.StringVar(value= None)
            self._product_folio = tk.IntVar(value= None)
            self._product_key = tk.StringVar(value= None)
            self._product_description = tk.StringVar(value= None)
            self._product_price = tk.DoubleVar(value= None)
            self._product_in = tk.StringVar(value= None)
            self._product_out = tk.StringVar(value= None)
            self._product_lote = tk.StringVar(value= None)
            self._product_qty = tk.DoubleVar(value= None)
            self._tab_frame(self._client)
        except Exception as ex:
            messagebox.showerror("Error",ex)

    def _update_product(self):
        # Activación de los campos.
        self.e_prod_name.config(state= tk.NORMAL)
        self.e_prod_qty.config(state= tk.NORMAL)
        self.e_prod_cost.config(state= tk.NORMAL)
        self.e_prod_folio.config(state= tk.NORMAL)
        self.box_description.config(state= tk.NORMAL)
        self.box_currency.config(state= tk.NORMAL)
        self.box_size.config(state= tk.NORMAL)
        # Desactivacíon de botones no necesarios.
        self.btn_new_product.config(state= tk.DISABLED)
        self.btn_edit_product.config(state= tk.DISABLED)
        # Activación de guardado y cancelación de actualización.
        self.btn_save_changes_prod.config(state= tk.NORMAL, command= lambda: self._save_changes_product(False))
        self.btn_delete_product.config(text="Cancelar", command= lambda: self._cancel_create(create= False))

    def _save_changes_product(self, new = True):
        # Obtención de información en los campos
        nombre = self.e_prod_name.get()
        clave = self.e_prod_clave.get()
        qty = self.e_prod_qty.get()
        precio = self.e_prod_cost.get()
        folio = self.e_prod_folio.get()
        descripcion = self.box_description.get('1.0', tk.END)
        moneda = self.box_currency.get()
        qty_size = self.box_size.get()
        if new:
            if nombre and qty and folio and qty_size != "None":
                self.product = Producto(
                    name= nombre.title(),
                    folio= folio.strip(),
                    description= descripcion.capitalize(),
                    currency= moneda.strip(),
                    id= clave.strip(),
                    cost= precio.strip(),
                    cantidad= qty.strip(),
                    size= qty_size.strip(),
                )
                self.product.dateInOut('in')
                answer = messagebox.askyesnocancel("Nuevo Producto",f"Producto a ingresar esta seguro de la información?\n\n{self.product}")
                if answer:
                    try:
                        DaoProduct.prod_reg(self.product)
                        self._tab_frame(self._client)
                    except Exception as ex:
                        messagebox.showerror("Error",ex)
                elif answer is None:
                    self._cancel_create()
                else:
                    return
            else:
                messagebox.showwarning("Campos Obligatorios","Debe ingresar como mínimo el folio, nombre del producto y la cantidad")
        else:
            self.product.name = nombre
            self.product.cantidad = qty
            self.product.cost = precio
            self.product.folio = folio
            self.product.description = descripcion
            self.product.currency = moneda
            self.product.size = qty_size
            answer = messagebox.askokcancel("Confirmación", f"{self.product}")
            if answer:
                try:
                    DaoProduct.prodUpdate(self.product, 'all')
                    messagebox.showinfo("Correcto","Actualizado correctamente.")
                    self._tab_frame(self._client)
                except Exception as ex:
                    messagebox.showerror("Error",ex)
            else:
                self._cancel_create(False)

    def _cancel_create(self, create = True):
        if create:
            # Limpieza del contenido de los campos.
            self.e_prod_clave.config(state= tk.NORMAL)
            self.e_prod_clave.delete(0, tk.END)
            self.e_prod_name.delete(0,tk.END)
            self.e_prod_lote.delete(0,tk.END)
            self.e_prod_lote.config(state= tk.DISABLED)
            self.e_prod_qty.delete(0,tk.END)
            self.e_prod_cost.delete(0,tk.END)
            self.e_prod_folio.delete(0,tk.END)
            self.box_description.delete('1.0', tk.END)
            self.box_currency.current(0)
            self.box_size.current(0)
            self.e_prod_folio.focus()
            # Deshabilitacion de campos.
            self.e_prod_clave.config(state= tk.DISABLED)
            self.e_prod_name.config(state= tk.DISABLED)
            self.e_prod_lote.config(state= tk.DISABLED)
            self.e_prod_lote.config(state= tk.DISABLED)
            self.e_prod_qty.config(state= tk.DISABLED)
            self.e_prod_cost.config(state= tk.DISABLED)
            self.e_prod_folio.config(state= tk.DISABLED)
            self.box_description.config(state= tk.DISABLED)
            self.box_currency.config(state= tk.DISABLED)
            self.box_size.config(state= tk.DISABLED)
            # Cambio de estado de botonera
            self.btn_new_product.config(state= tk.NORMAL)
            self.btn_delete_product.config(state= tk.DISABLED, text="Eliminar", command= self._update_product)
            self.btn_edit_product.config(state= tk.DISABLED)
            self.btn_save_changes_prod.config(state= tk.DISABLED)
        else:
            # Deshabilitacion de campos.
            self.e_prod_clave.config(state= tk.DISABLED)
            self.e_prod_name.config(state= tk.DISABLED)
            self.e_prod_lote.config(state= tk.DISABLED)
            self.e_prod_lote.config(state= tk.DISABLED)
            self.e_prod_qty.config(state= tk.DISABLED)
            self.e_prod_cost.config(state= tk.DISABLED)
            self.e_prod_folio.config(state= tk.DISABLED)
            self.box_description.config(state= tk.DISABLED)
            self.box_currency.config(state= tk.DISABLED)
            self.box_size.config(state= tk.DISABLED)
            # Cambio de estado de botonera.
            self.btn_new_product.config(state= tk.NORMAL)
            self.btn_delete_product.config(state= tk.NORMAL, command= lambda: self._cancel_create(), text= "Eliminar")
            self.btn_edit_product.config(state= tk.NORMAL)
            self.btn_save_changes_prod.config(state= tk.DISABLED, command= lambda: self._save_changes_product())

### Funciones para la tabla de productos.
    def _load_products(self, key = None):
        if key:
            try:
                resultados = DaoProduct.search(search="client", id= key)
                if resultados:
                    for dat in resultados:
                        self._products = Producto(
                            id= dat[0],
                            prod_id= dat[1],
                            folio= dat[2],
                            name= dat[3],
                            description= dat[4],
                            cantidad= dat[5],
                            size= dat[6],
                            cost= dat[7],
                            currency= dat[8],
                            f_in= dat[9],
                            f_out= dat[10]
                        )
                        prod_info = [
                            self._products.folio,
                            self._products.name,
                            (self._products.cost, self._products.currency),
                            (self._products.cantidad,self._products.size),
                            self._products.f_in,
                            self._products.f_out
                        ]
                        self.tabla_productos.insert("", tk.END, values= prod_info, text= self._products.folio)
            except Exception as ex:
                messagebox.showerror("Error", ex)

    def _select_product(self, event):
        item = self.tabla_productos.item(self.tabla_productos.selection())
        if item:
            try:
                result = DaoProduct.search(search='product',folio=item["text"])
            except Exception as ex:
                messagebox.showerror("Error",ex)
            if result:
                    for dat in result:
                        self.product = Producto(
                                id= dat[0],
                                prod_id= dat[1],
                                folio= dat[2],
                                name= dat[3],
                                description= dat[4],
                                cantidad= dat[5],
                                size= dat[6],
                                cost= dat[7],
                                currency= dat[8],
                                f_in= dat[9],
                                f_out= dat[10]
                            )
                    self._prod_info(self.product)

    def _research_prod(self):
        tipo_busqueda = self.e_type_box.get()
        element = self.e_text_search.get()
        if tipo_busqueda != "Seleccionar" and element:
            match tipo_busqueda:
                case "Folio":
                    if element.isdigit():
                        # Busqueda de el producto por folio.
                        try:
                            resultado = DaoProduct.search_element(folio= element)
                        except Exception as ex:
                            messagebox.showerror("Error",ex)
                        if resultado:
                            # Limpieza de los elementos anteriores en la tabla.
                            for item in self.tabla_productos.get_children():
                                    self.tabla_productos.delete(item)
                            # Creación de objetos producto.
                            for dat in resultado:
                                self._products = Producto(
                                    id= dat[0],
                                    prod_id= dat[1],
                                    folio= dat[2],
                                    name= dat[3],
                                    description= dat[4],
                                    cantidad= dat[5],
                                    size= dat[6],
                                    cost= dat[7],
                                    currency= dat[8],
                                    f_in= dat[9],
                                    f_out= dat[10]
                                )
                                prod_info = [
                                    self._products.folio,
                                    self._products.name,
                                    (self._products.cost, self._products.currency),
                                    (self._products.cantidad,self._products.size),
                                    self._products.f_in,
                                    self._products.f_out
                                ]
                                self.tabla_productos.insert("", tk.END, values= prod_info, text= self._products.folio)
                    else:
                        messagebox.showerror("Valor invalido",f"Ingrese solo numero de folio")
                case "Producto":
                    if not element.isdigit():
                        # Busqueda del producto por nombre.
                        try:
                            resultado = DaoProduct.search_element(name=element)
                        except Exception as ex:
                            messagebox.showerror("Error",ex)
                        if resultado:
                            # Limpieza de los elementos anteriores en la tabla.
                            for item in self.tabla_productos.get_children():
                                    self.tabla_productos.delete(item)
                            # Creación de objetos producto.
                            for dat in resultado:
                                self._products = Producto(
                                    id= dat[0],
                                    prod_id= dat[1],
                                    folio= dat[2],
                                    name= dat[3],
                                    description= dat[4],
                                    cantidad= dat[5],
                                    size= dat[6],
                                    cost= dat[7],
                                    currency= dat[8],
                                    f_in= dat[9],
                                    f_out= dat[10]
                                )
                                prod_info = [
                                    self._products.folio,
                                    self._products.name,
                                    (self._products.cost, self._products.currency),
                                    (self._products.cantidad,self._products.size),
                                    self._products.f_in,
                                    self._products.f_out
                                ]
                                self.tabla_productos.insert("", tk.END, values= prod_info, text= self._products.folio)
                    else:
                        messagebox.showerror("Valor invalido",f"Ingresa solo el nombre del producto.")
        else:
            if tipo_busqueda == "Seleccionar":
                messagebox.showwarning("Selección","Seleccione el tipo de busqueda a realizar")
            elif not element:
                messagebox.showwarning("Campo vació","debe especificar la busqueda.")
            else:
                return

### Funciones para la carga de las notas en la tabla.
    def _text_note(self, event):
        # obtengo el id de la columna seleccionada.
        linea = self.tabla_notas.identify_row(event.y)
        elemento = self.tabla_notas.item(linea)
        id_nota = elemento['text']
        # Obtengo los datos de la nota
        data = DaoNotas.getNote(id_nota)
        if data:
            # Objeto nota
            self._obj_note = Notas(
                id= data[0],
                id_nota= data[1],
                f_ingreso= data[2],
                titulo= data[3],
                nota= data[4]
            )
            # Se carga la nota
            self._widget_notes(note=self._obj_note, flag=True)
        else:
            return False

    def _notes_table(self, key: str):
        """Encargado de obtener las notas existentes del cliente y cargar info básica en la tabla para su elección.

        Args:
            key (str): clave del cliente
        """
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
                    self.tabla_notas.insert("", tk.END, values= self._head_notas, text=info.id)

### Funciones Botonera de acciones para las notas ###
    def _create_note(self):
        # Activación de las casillas para el ingreso de la nota.
        self.e_note.config(state=tk.NORMAL)
        self.note_box.config(state= tk.NORMAL)
        # limpieza de las casillas para el nuevo contenido.
        self.e_note.delete(0, tk.END)
        self.e_note.focus()
        self.note_box.delete('1.0', tk.END)
        # Cambio de estado de la botonera de interaccion e la nota.
        self.new_note_btn.config(state= tk.DISABLED)
        self.save_note_btn.config(state= tk.NORMAL)
        self.del_note_btn.config(state= tk.NORMAL)
        self.edit_note_btn.config(state= tk.DISABLED)

    def _save_new_note(self, new = True):
        # Obtención de los datos de la nota.
        titulo = self.e_note.get()
        nota = self.note_box.get('1.0', tk.END)
        cliente = self._clave.get()
        if new:
            # Se verifica que se ingreso información.
            if titulo and nota:
                # Objeto nota
                nueva_nota = Notas(
                    id_nota= cliente,
                    titulo= titulo.capitalize(),
                    nota= nota
                )
                # limpieza de las casillas
                self.e_note.delete(0, tk.END)
                self.note_box.delete('1.0', tk.END)
                # Ingreso de la nota en la base de datos.
                try:
                    DaoNotas.regNota(nueva_nota)
                    messagebox.showinfo("Guardado", "Nota Guardada")
                    self._data_client(self._client)
                except Exception as ex:
                    messagebox.showerror("Error!", f"Ocurrió un problema:\n{ex}")
            else:
                messagebox.showinfo("Nota vaciá", "Nose pueden guardar notas vaciás")
        else:
            fecha = datetime.now()
            update_date = fecha.strftime("%d-%m-%Y")
            try:
                self._obj_note.titulo = self.e_note.get()
                self._obj_note.nota = self.note_box.get('1.0', tk.END)
                self._obj_note.f_ingreso = update_date
                DaoNotas.noteUpdate(self._obj_note)
                self._data_client(self._client)
            except Exception as ex:
                messagebox.showerror(self.e_note.get(),f"error:\n{ex}")

    def _delete_note(self):
        try:
            DaoNotas.delNote(self._obj_note.id)
            self._data_client(self._client)
        except Exception as ex:
            messagebox.showerror("Error",f"No se pudo borrar la nota:\n{ex}")

    def _fun_edit_note(self):
        try:
            # Reactiva las casillas para su edición.
            self.e_note.config(state= tk.ACTIVE)
            self.note_box.config(state= tk.NORMAL)
            # Deshabilita botones u habilitación
            self.new_note_btn.config(state= tk.DISABLED)
            self.del_note_btn.config(state= tk.DISABLED)
            self.edit_note_btn.config(state= tk.DISABLED)
            self.save_note_btn.config(state= tk.NORMAL, command= lambda: self._save_new_note(False))
        except Exception as ex:
            messagebox.showinfo("Error",f"{ex}")

#### Funciones de Botonera principal ###
    def _load_client(self):
        """Encargada de la busqueda de clientes, para obtener su información, crear el objeto cliente y cargar
        su información el widget para su manipulación.
        """
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
            self._data_client(self._client)
            self._tab_frame(self._client)

    def _edit_client(self):
        tipos_cliente = ["Comprador","Proveedor"]
        loca_cliente = ["Local","Nacional","Internacional"]
        # Desactivacíon de botones de interaccion innecesarios.
        self.add_btn.config(state= tk.DISABLED)
        self.search_btn.config(state = tk.DISABLED)
        self.delete_btn.config(state= tk.DISABLED)
        # Cambio de estado de botones necesarios.
        self.edit_btn.config(image= self._save_update_client,text="Guardar cambios", command= self._save_changes)
        self.clean_btn.config(image= self._cancel_update_client, text="Cancelar cambios", command= self._not_update)
        # Activación de casillas de Info del cliente para su edición.
        self._e_name.config(state= tk.ACTIVE)
        self._e_name.focus()
        self._e_lastname.config(state = tk.NORMAL)
        self._e_mothers.config(state = tk.NORMAL)
        self._e_phone.config(state = tk.NORMAL)
        self._e_debt.config(state = tk.NORMAL)
        self._e_balance.config(state = tk.NORMAL)
        self._box_type = ttk.Combobox(
            self.data_frame,
            width=15,
            values= tipos_cliente
        )
        self._box_type.grid(row=4, column=1, padx=2, pady=5, sticky="NW")
        self._box_location = ttk.Combobox(
            self.data_frame,
            width= 15,
            values= loca_cliente
        )
        self._box_location.grid(row=5, column=1, padx=2, pady=5, sticky="NW")
        index_client = tipos_cliente.index(self._client.type_client)
        self._box_type.current(index_client)
        index_location = loca_cliente.index(self._client.location)
        self._box_location.current(index_location)
        # Boton para carga de nueva imagen de cliente.
        self._change_img_btn = ttk.Button(
            self.data_frame,
            text="Cargar Imagen",
            image= self._load,
            compound= tk.LEFT,
            command= self._load_imagen
        )
        self._change_img_btn.grid(row=3, column=0, padx=5, pady=5, sticky="NSEW")

    def _save_changes(self):
        self._client.name=  self._e_name.get()
        self._client.lastname = self._e_lastname.get()
        self._client.mothers = self._e_mothers.get()
        self._client.phone = self._e_phone.get()
        self._client.debt = self._e_debt.get()
        self._client.balance = self._e_balance.get()
        self._client.type_client = self._box_type.get()
        self._client.location = self._box_location.get()
        try:
            DaoClient.update(self._client)
            self._data_client(self._client)
            self._side_buttons()
            self.edit_btn.config(state= tk.NORMAL)
            self.clean_btn.config(state= tk.NORMAL)
            self.delete_btn.config(state= tk.NORMAL)
        except Exception as ex:
            messagebox.showerror("Error!", f"No se pudo actualizar:\n{ex}")

    def _not_update(self):
        # recarga de widgets de botones e info del cliente.
        self._side_buttons()
        self._e_name.config(state= tk.DISABLED)
        self._e_lastname.config(state = tk.DISABLED)
        self._e_mothers.config(state = tk.DISABLED)
        self._e_phone.config(state = tk.DISABLED)
        self._e_debt.config(state = tk.DISABLED)
        self._e_balance.config(state = tk.DISABLED)
        # Eliminación de elementos innecesarios.
        self._box_location.destroy()
        self._box_type.destroy()
        self._change_img_btn.destroy()
        # Reactivación de botones de interacion.
        self.edit_btn.config(state= tk.NORMAL)
        self.clean_btn.config(state= tk.NORMAL)
        self.delete_btn.config(state= tk.NORMAL)
        # restablecimiento de la imagen.
        self.logo.config(image= self._logo)

    def _delete_client(self):
        id_client = self._id.get()
        DaoClient.delete(id_client)
        self._clean_data()

    def _clean_data(self):
        """Encargada de la limpieza de los datos en las variables y recargar los widgets.
        """
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
        self._product_name = tk.StringVar(value= None)
        self._product_folio = tk.IntVar(value= None)
        self._product_key = tk.StringVar(value= None)
        self._product_description = tk.StringVar(value= None)
        self._product_price = tk.DoubleVar(value= None)
        self._product_in = tk.StringVar(value= None)
        self._product_out = tk.StringVar(value= None)
        self._product_lote = tk.StringVar(value= None)
        self._product_qty = tk.DoubleVar(value= None)
        self._data_client()
        self._tab_frame()
        self.edit_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')
        self.clean_btn.config(state='disabled')

    def _load_imagen(self):
        try:
            main_dir = os.path.abspath("Sources/clients")
            img_path = filedialog.askopenfilename(
                initialdir=main_dir,
                title="Cartera - Subir Imagen",
                filetypes= (("","*.png"),("all","*"))
            )
            if img_path:
                image = HandImg(img_path, self._client.name).prepare_img()
                self._client.image = image
                self.new_img = PhotoImage(file= self._client.image)
                self.logo.config(image= self.new_img)
        except TclError:
            messagebox.showerror("Error",f"Solo se permiten archivos en formato png\nno mayores 200x150 pixels")

if __name__ == '__main__':
    main_app = MainWindow()