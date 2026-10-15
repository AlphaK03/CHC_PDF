from flask import Flask, render_template, request, redirect, url_for, flash
import os
from src.controller.app_controller import AppController

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para usar sesiones y mensajes flash

# Instanciar el controlador
controller = AppController()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-monitoring', methods=['POST'])
def start_monitoring():
    carpeta = request.form['carpeta']
    if not carpeta:
        flash('Por favor, ingresa una carpeta para monitorear.')
        return redirect(url_for('index'))
    else:
        controller.seleccionar_carpeta(carpeta)
        controller.iniciar_monitoreo()
        flash(f'Monitoreo iniciado en la carpeta: {carpeta}')
        return redirect(url_for('index'))

@app.route('/stop-monitoring')
def stop_monitoring():
    controller.detener_monitoreo()
    flash('Monitoreo detenido.')
    return redirect(url_for('index'))

@app.route('/results')
def results():
    # Leer los resultados desde el archivo CSV
    resultados = []
    archivo_csv = os.path.join(controller.config['output_folder'], 'resultados.csv')
    if os.path.exists(archivo_csv):
        import pandas as pd
        df = pd.read_csv(archivo_csv)
        resultados = df.values.tolist()
    return render_template('results.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
