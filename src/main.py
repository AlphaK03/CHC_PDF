import tkinter as tk
from view.app_view import AppView
from controller.app_controller import AppController


def main():
    root = tk.Tk()

    # Inicializa la vista
    view = AppView(root)

    # Inicializa el controlador y pasa la vista
    controller = AppController(view)

    # Conectar las funciones del controlador a la vista
    view.iniciar_monitoreo = controller.iniciar_monitoreo
    view.detener_monitoreo = controller.detener_monitoreo
    view.seleccionar_carpeta = controller.seleccionar_carpeta
    view.seleccionar_salida = controller.seleccionar_salida
    view.restablecer_salida_por_defecto = controller.restablecer_salida_por_defecto

    root.mainloop()


if __name__ == '__main__':
    main()