import tkinter as tk  # Asegúrate de importar tkinter aquí
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from .pdf_processor import procesar_pdf

class MonitorArchivosPDF(FileSystemEventHandler):
    def __init__(self, archivo_csv, lista_archivos, processed_files, config_dir):
        self.archivo_csv = archivo_csv
        self.lista_archivos = lista_archivos
        self.processed_files = processed_files
        self.config_dir = config_dir  # Asegúrate de pasar config_dir

    def on_created(self, event):
        if event.src_path.endswith(".pdf"):
            time.sleep(1)  # Espera 1 segundo antes de procesar el archivo
            print(f"Nuevo archivo PDF detectado: {event.src_path}")
            procesar_pdf(event.src_path, self.archivo_csv, self.processed_files, self.config_dir)  # Pasar config_dir aquí
            self.lista_archivos.insert(tk.END, f"Procesado: {event.src_path}")

def iniciar_observador(carpeta, archivo_csv, processed_files, lista_archivos, config_dir):
    event_handler = MonitorArchivosPDF(archivo_csv, lista_archivos, processed_files, config_dir)  # Pasar config_dir
    observer = Observer()
    observer.schedule(event_handler, carpeta, recursive=False)
    observer.start()
    return observer
