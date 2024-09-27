import os
from tkinter import messagebox
from src.model.config_manager import cargar_configuraciones, guardar_configuraciones, cargar_archivos_procesados
from src.model.file_observer import iniciar_observador
from src.model.pdf_processor import procesar_archivos_existentes
import tkinter as tk
from tkinter import filedialog

class AppController:
    def __init__(self, view):
        self.view = view

        # Directorio raíz del proyecto (no subimos niveles)
        self.base_dir = os.getcwd()  # Nos aseguramos de estar en el directorio del proyecto

        # Directorios importantes
        self.config_dir = os.path.join(self.base_dir, 'config')  # Carpeta config en el nivel raíz del proyecto
        self.output_dir = os.path.join(self.base_dir, 'output')  # Carpeta output en el nivel raíz del proyecto

        # Asegurarse de que las carpetas existan
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            print(f"Carpeta de configuración creada en: {self.config_dir}")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Carpeta de salida creada en: {self.output_dir}")

        print(f"Base directory: {self.base_dir}")
        print(f"Config directory: {self.config_dir}")
        print(f"Output directory: {self.output_dir}")

        # Cargar configuraciones desde el archivo JSON en la nueva carpeta config
        self.config = cargar_configuraciones(self.config_dir)
        self.processed_files = cargar_archivos_procesados(self.config_dir)
        self.observer = None

        # Si no se ha definido una carpeta de salida en el archivo de configuración, usamos la carpeta por defecto
        if not self.config.get('output_folder'):
            self.config['output_folder'] = self.output_dir
            guardar_configuraciones(self.config, self.config_dir)

        # Si existe una carpeta de monitoreo en el archivo de configuración, la cargamos en la interfaz
        input_folder = self.config.get('input_folder', '')

        if input_folder:
            print(f"Carpeta de monitoreo cargada desde el archivo de configuración: {input_folder}")
            self.view.carpeta_entry.config(state='normal')  # Habilitar edición temporalmente
            self.view.carpeta_entry.delete(0, tk.END)  # Borrar cualquier valor actual
            self.view.carpeta_entry.insert(0, input_folder)  # Insertar la carpeta cargada
            self.view.carpeta_entry.config(state='readonly')  # Volver a deshabilitar la entrada para que sea solo lectura
        else:
            print("No se ha encontrado una carpeta de monitoreo en la configuración.")

    def iniciar_monitoreo(self):
        carpeta = self.view.carpeta_entry.get()

        # Verificar si la carpeta seleccionada está vacía
        if not carpeta:
            messagebox.showerror("Error", "Por favor selecciona una carpeta para monitorear.")
            return

        # Verificar si la carpeta existe en el sistema
        if not os.path.exists(carpeta):
            messagebox.showerror("Error", "La carpeta seleccionada no existe.")
            return

        output_folder = self.config['output_folder']

        archivo_csv = f"{output_folder}/resultados.csv"
        procesar_archivos_existentes(carpeta, archivo_csv, self.processed_files, self.config_dir)

        # Iniciar el observador de archivos (asegurarse de pasar config_dir)
        self.observer = iniciar_observador(carpeta, archivo_csv, self.processed_files, self.view.lista_archivos,
                                           self.config_dir)

        # Actualizamos la lista con el estado
        self.view.lista_archivos.insert(tk.END, "Monitoreo iniciado...")
        print("Monitoreo iniciado...")

    def detener_monitoreo(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.view.lista_archivos.insert(tk.END, "Monitoreo detenido.")
            print("Monitoreo detenido.")
        else:
            self.view.lista_archivos.insert(tk.END, "No hay monitoreo en ejecución.")
            print("No hay monitoreo en ejecución.")

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            # Actualizamos la carpeta en la interfaz y la configuración
            self.view.carpeta_entry.config(state='normal')  # Habilitar edición temporalmente
            self.view.carpeta_entry.delete(0, tk.END)
            self.view.carpeta_entry.insert(0, carpeta)
            self.view.carpeta_entry.config(state='readonly')  # Volver a deshabilitar la entrada
            self.config['input_folder'] = carpeta
            guardar_configuraciones(self.config, self.config_dir)
            print(f"Carpeta de monitoreo seleccionada: {carpeta}")

    def seleccionar_salida(self):
        carpeta_salida = filedialog.askdirectory()
        if carpeta_salida:
            self.config['output_folder'] = carpeta_salida
            guardar_configuraciones(self.config, self.config_dir)
            print(f"Carpeta de salida cambiada a: {carpeta_salida}")

    # Metodo para restablecer la carpeta de salida a la por defecto
    def restablecer_salida_por_defecto(self):
        default_output_folder = self.output_dir
        self.config['output_folder'] = default_output_folder
        guardar_configuraciones(self.config, self.config_dir)
        print(f"Carpeta de salida restablecida a: {default_output_folder}")