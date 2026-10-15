import os
import pdfplumber
import pandas as pd
import re
from .config_manager import guardar_archivos_procesados

# Lista de patrones para diferentes casos
patrones = [
    re.compile(r'\b\d{4}[a-zA-Z]{8}\b'),  # Caso sin espacios: 1234ABCDEFGH
    re.compile(r'\b\d{4} [a-zA-Z]{8}\b')  # Caso con espacio entre números y letras: 1234 ABCDEFGH
]

def procesar_pdf(ruta_pdf, archivo_csv, processed_files, config_dir):
    archivo_nombre = os.path.basename(ruta_pdf)

    # Verificar si el archivo ya ha sido procesado
    if archivo_nombre in processed_files:
        print(f"El archivo {archivo_nombre} ya ha sido procesado, omitiendo...")
        return  # Omitimos el procesamiento si ya fue procesado

    try:
        print(f"Procesando el archivo: {ruta_pdf}")
        with pdfplumber.open(ruta_pdf) as pdf:
            resultados = []
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    # Intentamos encontrar palabras con las expresiones regulares definidas
                    palabras_encontradas = []
                    for patron in patrones:
                        palabras_encontradas.extend(patron.findall(texto))

                    # Si se encuentran palabras, las añadimos a los resultados
                    if palabras_encontradas:
                        for palabra in palabras_encontradas:
                            # Limpiamos la palabra si es necesario (por ejemplo, quitamos espacios si es el caso con espacio)
                            palabra_limpia = palabra.replace(' ', '')
                            resultados.append([archivo_nombre, palabra_limpia])

            # Guardar los resultados en un archivo CSV
            if resultados:
                df_resultados = pd.DataFrame(resultados, columns=["Nombre del archivo", "Palabra"])

                # Escribir los resultados en el CSV, agregando si ya existe el archivo
                if os.path.exists(archivo_csv):
                    df_resultados.to_csv(archivo_csv, mode='a', header=False, index=False)
                else:
                    df_resultados.to_csv(archivo_csv, mode='w', header=True, index=False)

                # Añadir el archivo procesado al conjunto y guardar la lista de procesados
                processed_files.add(archivo_nombre)
                guardar_archivos_procesados(processed_files, config_dir)

    except Exception as e:
        print(f"Error al procesar {ruta_pdf}: {e}")


def procesar_archivos_existentes(carpeta, archivo_csv, processed_files, config_dir):
    """
    Procesa todos los archivos PDF existentes en la carpeta que aún no hayan sido procesados.
    """
    print("Procesando archivos PDF existentes en la carpeta...")
    for archivo_nombre in os.listdir(carpeta):
        if archivo_nombre.endswith(".pdf"):
            ruta_pdf = os.path.join(carpeta, archivo_nombre)
            procesar_pdf(ruta_pdf, archivo_csv, processed_files, config_dir)
