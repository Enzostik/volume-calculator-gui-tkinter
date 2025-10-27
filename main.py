'''
Implementación de interfáz gráfica tkinter para el cálculo de forma geométrica.
'''
import tkinter as tk
from copy import deepcopy
from PIL import Image, ImageTk

import calculator
from unit_handler import to_meters, length_from_to, meters2_to, meters3_to

# Texto de saludo
SALUDO = "Seleccione una figura del menú desplegable para calcular su volumen"

# Los cuerpos se pueden obtener del modulo 'calculator'
bodies = calculator.bodies_data

# Elemento de ventana de tkinter
window = tk.Tk()

# Unidades seleccionadas
u_length: list[str] = [
    'm-Metros',
    'km-Kilómetros',
    'hm-Hectómetros',
    'dam-Decámetros',
    'dm-Decímetros',
    'cm-Centímetros',
    'mm-Milímetros',
    'inch-Pulgadas'
]
u_surface: list[str] = [
    'm2-Metros cuadrados'
]
u_volume: list[str] = [
    'm3-Metros cúbicos',
    'dm3-decimetro cubico',
    'l-Litros',
    'ml-Mililitros',
    'cm3-centimetro cubico',
    'mm3-Milímetros cúbicos'
]

'''
--------------------
Funciones generales
--------------------
'''


def validate_number(value: str) -> bool:
    '''
    Verifica que el valor ingresado sea un número positivo.
    '''
    if value != '':  # Si no se borra el contenido
        try:
            # Tiene que ser un numero y debe ser mayor o igual a 0
            return float(value) >= 0
        except ValueError:
            return False
    return True


def string_to_float(value: str) -> float:
    '''
    Convierte una cadena de caracteres a su correspondiente número.
    '''
    return 0 if value == '' else float(value)


def format_value(value: float) -> str:
    '''
    Da formato a un número para facilitar su lectura si es mayor o menor a 0.001
    '''
    # Si el valor es menor a 0.001 utilizar exponente para poder leerlo
    if value == 0 or value > 0.001:
        return round(value, 4)
    return f"{value:.4e}"


# Elementos de tkinter
# Registrar la función para validar que la nueva entrada sea un número
entry_verification = (window.register(validate_number), '%P')


class CustomEntry:
    '''
    Objeto para guardar el objeto `tk.Widget` con su asociado `tk.StringVar`.
    '''

    def __init__(self, widget: tk.Widget, variable: tk.StringVar = None):
        self.widget = widget
        self.variable = variable

    def set(self, *args, **kwargs) -> None:
        '''
        Llama la función `self.variable.set()` de la clase `tk.StringVar`.
        '''
        self.variable.set(*args, **kwargs)

    def get(self) -> str:
        '''
        Llama la función `self.variable.get()` de la clase `tk.StringVar`.
        '''
        return self.variable.get()

    def trace_add(self, *args, **kwargs) -> None:
        '''
        Llama la función `self.variable.trace_add()` de la clase `tk.StringVar`.
        '''
        self.variable.trace_add(*args, **kwargs)

    def bind(self, *args, **kwargs) -> None:
        '''
        Llama la función `self.entry.bind()` del elemento `tkinter`.
        '''
        self.widget.bind(*args, **kwargs)

    def pack(self, *args, **kwargs) -> None:
        '''
        Llama la función `self.entry.pack()` del elemento `tkinter`.
        '''
        self.widget.pack(*args, **kwargs)


class CalculatorFrame:
    '''
    Cuadro principal donde colocar los elementos para la calculadora de cuerpos geométricos.
    '''

    def __init__(self, root: tk.Tk):
        # Variable que contenga el cuerpo para los calculos
        self.body = None

        # Se crea un frame que ocupe toda la ventana.
        canvas = tk.Canvas(root, bg="lightblue")
        canvas.pack(expand=True, fill='both')

        # El contenido a editar se encuentra dentro de este frame.
        self.main_frame = tk.Frame(canvas)
        self.main_frame.configure(bg="lightblue")
        # self.main_frame.pack(side=tk.LEFT, expand=True, fill='both')

        # Scrollbar
        yscroll = tk.Scrollbar(canvas, orient=tk.VERTICAL,
                               command=canvas.yview, width=20)
        canvas.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)

        window_id = canvas.create_window(
            (0, 0), window=self.main_frame, anchor='nw')

        # Cuando se cambia el tamaño de la ventana o el contenido del main_frame
        self.main_frame.bind("<Configure>", lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind('<Configure>', lambda event: canvas.itemconfig(
            window_id, width=event.width))
        # Cuando se mueve la rueda del ratón
        canvas.bind_all("<MouseWheel>", lambda event: None if
                      (canvas.yview()[0] == 0.0 and canvas.yview()[1] == 1.0) else
                      canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # Etiqueta de inicio
        self.etiqueta_1 = tk.Label(self.main_frame, text=SALUDO,
                                   font=("Arial", 12), bg="gray", wraplength=350)
        self.etiqueta_1.pack(side='top', fill='x')

        # Unidades a emplear (siempre toma la primera de la lista por defecto)
        # Para la unidad de longitud: m-Metros
        self.unit_selector: dict[str, CustomEntry] = {}
        for key, values in {'length': u_length,  'surface': u_surface, 'volume': u_volume}.items():
            _variable = tk.StringVar(value=values[0])
            # Para los selectores de unidad de superficie y volumen se tendrá que recalcular los valores
            # pero con las nuevas unidades. --> Agregar comando cuando se cambie el menu
            _optionmenu = tk.OptionMenu(self.main_frame, _variable, *values,
                                        command=None if key == 'length' else lambda *args: self.update_results())
            _optionmenu.config(width=35)
            self.unit_selector[key] = CustomEntry(
                _optionmenu,
                _variable
            )
        # Guardar cual era la unidad de longitud anterior
        self.__previus_unit_length = u_length[0]
        # Ejecutar un comando que convierta el valor de la longitud al cambiarse su unidad
        self.unit_selector['length'].trace_add(
            'write', lambda *args: self.__set_unit_length(self.unit_selector['length'].get()))

        # Almacenar las variables de las entradas en un diccionario
        # para que no se borren al no ser referenciadas
        self.entries_var: dict[str, tk.StringVar] = {}
        # Almacenar la referencia a la entrada que será destinada al resultado
        self.result_entries: dict[str, CustomEntry] = {}
        for key in ['volume', 'surface']:
            _variable = tk.StringVar()
            self.result_entries[key] = CustomEntry(
                tk.Entry(master=self.main_frame, textvariable=_variable, font=("Arial", 15),
                         fg="blue", justify='center', width=25, state='readonly'),
                _variable
            )

        # Click derecho para copiar los resultados
        self.popup_menu = tk.Menu(master=root, tearoff=0)
        self.popup_menu.add_command(
            label='Copiar', command=lambda: [root.clipboard_clear(), root.clipboard_append(self.value_selected)])
        self.result_entries['volume'].bind(
            '<Button-3>', lambda event, result_var=self.result_entries['volume'].variable: self.__show_popupmenu(result_var, event))
        self.result_entries['surface'].bind(
            '<Button-3>', lambda event, result_var=self.result_entries['surface'].variable: self.__show_popupmenu(result_var, event))
        self.value_selected: float = None
    # Variable que se llamará cuando se cambie alguna de las entradas de texto

    def set_unit(self, name: str, unit: str):
        '''
        Cambiar los valores de la unidad `unit` para el parámetro `name` seleccionado.

        Al cambiar la unidad automáticamente intenta convertir el valor ya ingresado a la nueva unidad.
        '''
        _options = list(key for key in self.unit_selector)
        if name not in _options:
            raise IndexError(
                f'{name} no es un parametro válido, intente: {_options}')
        # Cambiar a la unidad seleccionada
        self.unit_selector[name].set(unit)
        # Si el parametro era longitud no hacer nada mas
        if name == 'length':
            return
        # Si era superficie o volumen se tiene que actualizar el valor con la nueva unidad
        if self.body:  # Solo hacerlo si hay un cuerpo seleccionado
            self.update_results()

    def __set_unit_length(self, unit_to: str) -> bool:
        # Si se selecciona la misma unidad no hacer nada --> Regresar falso
        if unit_to == self.__previus_unit_length:
            return False
        # Convertir los valores ya ingresados a la nueva unidad
        for val in self.entries_var.values():
            # Obtener el valor y convertirlo en número
            value = val.get()
            value = 0 if value == '' else float(value)
            # Convertir el valor a la unidad deseada
            value = length_from_to(
                value, self.__previus_unit_length.split('-', maxsplit=1)[0], unit_to.split('-')[0])
            val.set(format_value(value))
        # Actualizar el valor anterior
        self.__previus_unit_length = unit_to
        # Regresar True para indicar que si se realizaron cambios
        return True

    def __change_value(self, name: str, value: str):
        # Si la entrada está vacía será 0. Convertir variable string --> float
        value = 0 if value == '' else float(value)
        # El parametro en el Body siempre se guardará en las unidades por defecto
        # Convertirlas en m - Metros
        value = to_meters(
            value, self.unit_selector['length'].get().split('-')[0])
        # Cambiar el valor del parametro
        self.body.set(name, value)
        # Cambiar el valor del texto de volumen y superficie
        self.update_results()

    # Cambiar el valor del texto de volumen y superficie
    def update_results(self):
        '''
        Actualiza los valores de los resultados del volumen y superficie.

        Realizando sus respectivos cálculos nuevamente.
        '''
        # Obtener la unidad del volumen y convertirla de la unidad por defecto (m3) a la deseada
        vol_value = meters3_to(
            self.body.volume(), self.unit_selector['volume'].get().split('-')[0])
        # Y cambiarla en el resultado
        self.result_entries['volume'].set(format_value(vol_value))

        # Obtener la unidad del volumen y convertirla de la unidad por defecto (m3) a la deseada
        surf_value = meters2_to(
            self.body.surface(), self.unit_selector['surface'].get().split('-')[0])
        self.result_entries['surface'].set(format_value(surf_value))

    # Cambiar el contenido del frame para que corresponda al cuerpo geométrico
    def load(self, new_body: calculator.Body):
        '''
        Carga un cuerpo geométrico para representarlo en la interfáz gráfica.
        '''
        # Eliminar el contenido del frame
        self.clean_frame()
        # Guardar el cuerpo
        self.body = new_body
        # Modificar el título de la ventana para que sea el nombre del cuerpo
        self.etiqueta_1.config(text=new_body)
        # Cargar la imagen
        try:  # Intenta agregar imagenes de la figura
            # Se carga el archivo con el mismo nombre de la forma en la carpeta imagenes
            img = Image.open(f'images/{new_body.name.lower()}.png')
            img = img.resize((150, 150))
            # Convertir la imagen para utilizarla en tkinter
            image = ImageTk.PhotoImage(img)
            # Añadir la imagen en un Label
            etiqueta_img = tk.Label(self.main_frame, image=image)
            etiqueta_img.image = image
            etiqueta_img.pack(pady=5)  # Añadir el label al frame
        except FileNotFoundError:  # Si no hay imagenes que coincidan con el nombre no hace nada
            pass
        # Etiqueta para las instrucciones
        etiqueta_instruccion = tk.Label(self.main_frame, text="Ingrese los valores indicados:",
                                        font=("Arial", 10), justify='left', background='lightblue')
        # Añadir la etiqueta al frame
        etiqueta_instruccion.pack(fill='x', pady=5)

        # Añade el selector de unidades de longitud
        self.unit_selector['length'].pack(pady=5)

        # Crear las entradas de texto para cada parámetro
        for key, value in new_body.parameters.items():
            # Etiqueta con el nombre de la variable
            etiqueta_valor = tk.Label(self.main_frame, text=key[0].upper()+key[1:].lower(),
                                      font=("Arial", 10), background="gray")
            etiqueta_valor.pack(anchor='w', fill='x', pady=5)
            # Variable de la entrada de texto
            variable_valor = tk.StringVar(name=key, value=value)
            self.entries_var[key] = variable_valor
            # Entrada de texto
            entrada_valor = tk.Entry(self.main_frame, textvariable=variable_valor,
                                     validate='key', validatecommand=entry_verification)
            entrada_valor.pack(pady=5)
            # Evento en caso de modificación de la entrada de texto
            variable_valor.trace_add('write', lambda name, _index, _mode, v=variable_valor:
                                     self.__change_value(name, v.get()))

        # Añadir entradas de solo lectura para mostrar los resultados
        # Etiqueta del volumen
        etiqueta_volumen = tk.Label(
            self.main_frame, text=f"El volumen del {new_body.name.lower()} es:",
            font=("Arial", 15), fg="blue", bg='gray'
        )
        etiqueta_volumen.pack(fill='x', pady=5)
        # Selector de unidades del volumen
        self.unit_selector['volume'].pack(pady=5)
        # El resultado del volumen
        self.result_entries['volume'].pack(pady=5)

        # Etiqueta de la superficie
        etiqueta_superficie = tk.Label(
            self.main_frame, text=f"La superficie del {new_body.name.lower()} es:",
            font=("Arial", 15), fg="blue", bg='gray'
        )
        etiqueta_superficie.pack(fill='x', pady=5)
        # Selector de unidades de la superficie
        self.unit_selector['surface'].pack(pady=5)
        # Resultado de la superficie
        self.result_entries['surface'].pack(pady=5)

        # Cambiar los valores de los resultados si es necesario
        self.update_results()

    # Funcion para limpiar la pantalla cuando se cambia de opción de figura
    def clean_frame(self):
        '''
        Elimina/limpia todos los elementos agregados a la ventana.
        '''
        self.body = None  # Eliminar las variables previamente utilizadas
        self.entries_var.clear()  # Eliminar las variables previamente utilizadas
        # Devolver la etiqueta principal al mensaje de entrada
        self.etiqueta_1.config(text=SALUDO)
        # Elementos a eliminar
        for widget in self.main_frame.winfo_children():
            if widget in [self.etiqueta_1] + [element.widget for element in list(self.result_entries.values()) + list(self.unit_selector.values())]:
                # No destruir si es la etiqueta principal o las entradas de resultados
                widget.pack_forget()
                continue
            widget.destroy()
        # Volver a colocar le etiqueta principal
        self.etiqueta_1.pack(side='top', fill='x')

    def __show_popupmenu(self, value_string: tk.StringVar, event: tk.Event = None):
        try:
            self.value_selected = float(value_string.get())
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()


def select(new_body: calculator.Body):
    '''
    Seleccionar un cuerpo geométrico para ser representado en la interfaz de la ventana principal.
    '''
    main_frame.load(deepcopy(new_body))


def clean_window():
    '''
    Borrar todo el contenido de la ventana principal y volver a los valores por defecto.
    '''
    # Eliminar elementos del frame
    main_frame.clean_frame()
    # Regresar los valores de unidades a los valores por defecto
    main_frame.set_unit('length', u_length[0])
    main_frame.set_unit('surface', u_surface[0])
    main_frame.set_unit('volume', u_volume[0])


# Título de la ventana
window.title('Calculadora de volumen')

# Tamaño
window.geometry("500x600")
window.minsize(400, 450)
window.maxsize(600, 700)

# Icono
window.iconbitmap('icon.ico')

# Color de fondo
window.configure(bg="lightblue")

# Menu desplegable
menu_bar = tk.Menu(window)
menu_principal = tk.Menu(menu_bar, tearoff=0)
submenu_figuras = tk.Menu(menu_principal, tearoff=0)
menu_unidades = tk.Menu(menu_bar, tearoff=0)
submenu_longitud = tk.Menu(menu_unidades, tearoff=0)
submenu_volumen = tk.Menu(menu_unidades, tearoff=0)
submenu_superficie = tk.Menu(menu_unidades, tearoff=0)
window.config(menu=menu_bar)

# Añadir las figuras al sub-menu figuras
for body in bodies:
    submenu_figuras.add_command(label=body, command=lambda x=body: select(x))
# Añadir el menu figuras al menu principal
menu_principal.add_cascade(label='Figuras', menu=submenu_figuras)
# Añadir el menu figuras al menu principal
menu_principal.add_command(label='Reiniciar', command=clean_window)
# Añadir la opcion salir al menu principal
menu_principal.add_separator()
menu_principal.add_command(label='Salir', command=window.destroy)
# Añadir el menu principal a la barra de menu
menu_bar.add_cascade(label="Inicio", menu=menu_principal)

# Añadir unidades al sub-menu longitud
for l in u_length:
    submenu_longitud.add_command(
        label=l, command=lambda x=l: main_frame.set_unit('length', x))
# Añadir unidades al sub-menu superficie
for surf in u_surface:
    submenu_superficie.add_command(
        label=surf, command=lambda x=surf: main_frame.set_unit('surface', x))
# Añadir unidades al sub-menu volumen
for vol in u_volume:
    submenu_volumen.add_command(
        label=vol, command=lambda x=vol: main_frame.set_unit('volume', x))
# Añadir los sub-menus
menu_unidades.add_cascade(label='Longitud', menu=submenu_longitud)
menu_unidades.add_cascade(label='Volumen', menu=submenu_volumen)
menu_unidades.add_cascade(label='Superficie', menu=submenu_superficie)
# Añadir el menu unidades a la barra de menu
menu_bar.add_cascade(label='Unidades', menu=menu_unidades)

# Ventana principal de la aplicación
main_frame = CalculatorFrame(window)

window.update()
window.mainloop()
