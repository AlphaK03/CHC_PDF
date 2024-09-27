import tkinter as tk
from tkinter import ttk, Menu

class AppView:
    def __init__(self, root):
        self.root = root

        # Estas funciones serán asignadas más tarde en main.py
        self.iniciar_monitoreo = None
        self.detener_monitoreo = None
        self.seleccionar_carpeta = None
        self.seleccionar_salida = None
        self.restablecer_salida_por_defecto = None

        # Construimos la interfaz
        self.build_interface()

    def build_interface(self):
        self.root.title("Monitoreo de Archivos PDF")
        self.root.geometry("700x500")  # Ajustamos el tamaño de la ventana
        self.root.resizable(False, False)  # Deshabilitamos el cambio de tamaño

        # Aplicamos un tema más moderno usando ttk
        style = ttk.Style()
        style.theme_use("clam")  # Puedes probar con otros temas: "clam", "alt", "default"

        # Definir los estilos personalizados para los botones
        style.configure("TButton", padding=6, relief="flat", font=("Helvetica", 10))
        style.configure("Blue.TButton", foreground="white", background="#007bff", borderwidth=1)
        style.map("Blue.TButton", background=[("active", "#0056b3")])
        style.configure("Green.TButton", foreground="white", background="#28a745", borderwidth=1)
        style.map("Green.TButton", background=[("active", "#218838")])
        style.configure("Red.TButton", foreground="white", background="#dc3545", borderwidth=1)
        style.map("Red.TButton", background=[("active", "#c82333")])

        # Menú superior
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Añadimos la opción de "Opciones" en el menú
        opciones_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=opciones_menu)
        opciones_menu.add_command(label="Cambiar ruta de guardado", command=self.handle_seleccionar_salida)
        opciones_menu.add_command(label="Restablecer ruta de guardado por defecto",
                                  command=self.handle_restablecer_salida_por_defecto)

        # Frame principal para mayor organización
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Carpeta a monitorear (solo lectura)
        ttk.Label(main_frame, text="Carpeta a monitorear:", style="TLabel").grid(column=0, row=0, sticky=tk.W, pady=5)

        self.carpeta_entry = ttk.Entry(main_frame, width=50, state='readonly')  # Deshabilitar edición
        self.carpeta_entry.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        # Botón para seleccionar carpeta (azul)
        self.carpeta_boton = ttk.Button(main_frame, text="Seleccionar Carpeta", style="Blue.TButton", command=self.handle_seleccionar_carpeta)
        self.carpeta_boton.grid(column=3, row=0, padx=10, pady=5)

        # Botón para iniciar monitoreo (verde)
        self.iniciar_boton = ttk.Button(main_frame, text="Iniciar Monitoreo", style="Green.TButton", command=self.handle_iniciar_monitoreo)
        self.iniciar_boton.grid(column=1, row=1, pady=10, padx=10, sticky=tk.E)

        # Botón para detener monitoreo (rojo)
        self.detener_boton = ttk.Button(main_frame, text="Detener Monitoreo", style="Red.TButton", command=self.handle_detener_monitoreo)
        self.detener_boton.grid(column=2, row=1, pady=10, padx=10, sticky=tk.W)

        # Lista de archivos procesados
        ttk.Label(main_frame, text="Archivos Procesados:", style="TLabel").grid(column=0, row=2, sticky=tk.W, pady=10)
        self.lista_archivos = tk.Listbox(main_frame, width=100, height=15)
        self.lista_archivos.grid(column=0, row=3, columnspan=4, pady=10, padx=10)

        # Añadir scroll vertical a la lista de archivos procesados
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.lista_archivos.yview)
        self.lista_archivos.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(column=4, row=3, sticky=tk.NS)

        # Añadimos padding a todos los elementos del main_frame
        for child in main_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

    def handle_iniciar_monitoreo(self):
        if self.iniciar_monitoreo:
            self.iniciar_monitoreo()

    def handle_detener_monitoreo(self):
        if self.detener_monitoreo:
            self.detener_monitoreo()

    def handle_seleccionar_carpeta(self):
        if self.seleccionar_carpeta:
            self.seleccionar_carpeta()

    def handle_seleccionar_salida(self):
        if self.seleccionar_salida:
            self.seleccionar_salida()

    def handle_restablecer_salida_por_defecto(self):
        if self.restablecer_salida_por_defecto:
            self.restablecer_salida_por_defecto()