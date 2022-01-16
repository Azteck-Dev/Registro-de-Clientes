### Code by: J.Mesach Venegas
### email: mesach.venegas@gmail.com
from tkinter import PhotoImage, TclError, Tk, dialog, messagebox, scrolledtext, ttk, filedialog
from search_window import SearchWin
from NewClient_window import NewClient
from Module.client import Client
from Module.notas import Notas
from Module.dao import DaoClient, DaoNotas, DaoProduct
from datetime import datetime
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
        # Variables.
        self._client = None
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
        self._side_buttons()
        self._data_client()
        self.mainloop()

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
        """Encargada de la limpieza de los datos en las variables y recargar el widget.
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
        self._data_client()
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
                self._client.image = os.path.abspath(img_path)
                self.new_img = PhotoImage(file= self._client.image)
                self.logo.config(image= self.new_img)
        except TclError:
            messagebox.showerror("Error",f"Solo se permiten archivos en formato png\nno mayores 200x150 pixels")

if __name__ == '__main__':
    test = MainWindow()