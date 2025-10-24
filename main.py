'''
Implementación de interfáz gráfica tkinter para el cálculo de forma geométrica.
'''
import tkinter as tk
from copy import deepcopy
from PIL import Image, ImageTk

import calculator

#Texto de saludo
SALUDO = "Seleccione una figura del menú desplegable para calcular su volumen"

#Los cuerpos se pueden obtener del modulo 'calculator'
bodies = calculator.bodies_data

#Elemento de ventana de tkinter
window = tk.Tk()


'''
--------------------
Funciones generales
--------------------
'''
def validate_number(value:str)->bool:
    '''
    Verifica que el valor ingresado sea un número positivo.
    '''
    if value != '': #Si no se borra el contenido
        try:
            return float(value) >= 0 #Tiene que ser un numero y debe ser mayor o igual a 0
        except ValueError:
            return False
    return True

def string_to_float(value:str)->float:
    '''
    Convierte una cadena de caracteres a su correspondiente número.
    '''
    return 0 if value == '' else float(value)

def format_value(value:float)->str:
    '''
    Da formato a un número para facilitar su lectura si es mayor o menor a 0.001
    '''
    #Si el valor es menor a 0.001 utilizar exponente para poder leerlo
    if value == 0 or value > 0.001:
        return round(value, 4)
    return f"{value:.4e}"


#Elementos de tkinter
# Registrar la función para validar que la nueva entrada sea un número
entry_verification = (window.register(validate_number), '%P')

class CalculatorFrame:
    '''
    Cuadro principal donde colocar los elementos para la calculadora de cuerpos geométricos.
    '''
    def __init__(self, root:tk.Tk):
        # Variable que contenga el cuerpo para los calculos
        self.body = None

        # Se crea un frame que ocupe toda la ventana.
        # El contenido a editar se encuentra dentro de este frame.
        self.main_frame = tk.Frame(root)
        self.main_frame.configure(bg="lightblue")
        self.main_frame.pack(expand=True, fill='both')

        # Etiqueta de inicio
        self.etiqueta_1 = tk.Label(self.main_frame, text=SALUDO,
                                   font=("Arial", 12), bg="gray",wraplength=350) #mensaje principal
        self.etiqueta_1.pack(side='top', fill='x')

        # Almacenar las variables de las entradas en un diccionario
        # para que no se borren al no ser referenciadas
        self.entries_var:dict[str, tk.StringVar] = {}
        # Almacenar la referencia a la entrada que será destinada al resultado
        self.var_volume = tk.StringVar()
        self.result_volume:tk.Entry = tk.Entry(
            master=self.main_frame, textvariable=self.var_volume, font=("Arial", 15),
            fg="blue", justify='center', width=25, state='readonly'
        )
        self.var_surface = tk.StringVar()
        self.result_surface:tk.Entry = tk.Entry(
            master=self.main_frame, textvariable=self.var_surface, font=("Arial", 15),
            fg="blue", justify='center', width=25, state='readonly'
        )

        #Click derecho para copiar los resultados
        self.popup_menu = tk.Menu(master=root, tearoff=0)
        self.popup_menu.add_command(
            label='Copiar', command=lambda :
            [root.clipboard_clear(), root.clipboard_append(self.value_selected)]
        )
        self.result_volume.bind('<Button-3>', lambda event, result_var = self.var_volume :
                                self.__show_popupmenu(result_var, event))
        self.result_surface.bind('<Button-3>', lambda event, result_var = self.var_surface :
                                 self.__show_popupmenu(result_var, event))
        self.value_selected:float = None
    #Variable que se llamará cuando se cambie alguna de las entradas de texto
    def __change_value(self, name:str, value:str):
        #Si la entrada está vacía será 0. Convertir variable string --> float
        value = 0 if value == '' else float(value)
        #Cambiar el valor del parametro
        self.body.set(name, value)
        #Cambiar el valor del texto de volumen y superficie
        self.update_results()

    #Cambiar el valor del texto de volumen y superficie
    def update_results(self):
        '''
        Actualiza los valores de los resultados del volumen y superficie.
        Realizando sus respectivos cálculos nuevamente.
        '''
        self.var_volume.set(format_value(self.body.volume()))
        self.var_surface.set(format_value(self.body.surface()))

    #Cambiar el contenido del frame para que corresponda al cuerpo geométrico
    def load(self, new_body:calculator.Body):
        '''
        Carga un cuerpo geométrico para representarlo en la interfáz gráfica.
        '''
        #Eliminar el contenido del frame
        self.clean_frame()
        #Guardar el cuerpo
        self.body = new_body
        #Modificar el título de la ventana para que sea el nombre del cuerpo
        self.etiqueta_1.config(text=new_body)
        #Cargar la imagen
        try: #Intenta agregar imagenes de la figura
            #Se carga el archivo con el mismo nombre de la forma en la carpeta imagenes
            img = Image.open(f'images/{new_body.name.lower()}.png')
            img = img.resize((150, 150))
            image = ImageTk.PhotoImage(img) #Convertir la imagen para utilizarla en tkinter
            etiqueta_img = tk.Label(self.main_frame, image=image) #Añadir la imagen en un Label
            etiqueta_img.image = image
            etiqueta_img.pack(pady=5) #Añadir el label al frame
        except FileNotFoundError: #Si no hay imagenes que coincidan con el nombre no hace nada
            pass
        #Etiqueta para las instrucciones
        etiqueta_instruccion = tk.Label(self.main_frame, text="Ingrese los valores indicados:",
                                        font=("Arial", 10), justify='left', background='lightblue')
        etiqueta_instruccion.pack(fill='x', pady=5) #Añadir la etiqueta al frame

        #Crear las entradas de texto para cada parámetro
        for key, value in new_body.parameters.items():
            #Etiqueta con el nombre de la variable
            etiqueta_valor = tk.Label(self.main_frame, text=key[0].upper()+key[1:].lower(),
                                      font=("Arial", 10), background="gray")
            etiqueta_valor.pack(anchor='w', fill='x', pady=5)
            #Variable de la entrada de texto
            variable_valor = tk.StringVar(name=key, value=value)
            self.entries_var[key] = variable_valor
            #Entrada de texto
            entrada_valor = tk.Entry(self.main_frame, textvariable=variable_valor,
                                     validate='key', validatecommand=entry_verification)
            entrada_valor.pack(pady=5)
            #Evento en caso de modificación de la entrada de texto
            variable_valor.trace_add('write', lambda name, _index, _mode, v = variable_valor :
                                     self.__change_value(name, v.get()))

        #Añadir entradas de solo lectura para mostrar los resultados
        etiqueta_volumen = tk.Label(
            self.main_frame, text=f"El volumen del {new_body.name.lower()} es:",
            font=("Arial", 15), fg="blue", bg='gray'
        )
        etiqueta_volumen.pack(fill='x', pady=5)
        self.result_volume.pack(pady=5)
        etiqueta_superficie = tk.Label(
            self.main_frame, text=f"La superficie del {new_body.name.lower()} es:",
            font=("Arial", 15), fg="blue", bg='gray'
        )
        etiqueta_superficie.pack(fill='x', pady=5)
        self.result_surface.pack(pady=5)
        #Cambiar los valores de los resultados si es necesario
        self.update_results()

    #Funcion para limpiar la pantalla cuando se cambia de opción de figura
    def clean_frame(self):
        '''
        Elimina/limpia todos los elementos agregados a la ventana.
        '''
        self.body = None #Eliminar las variables previamente utilizadas
        self.entries_var.clear() #Eliminar las variables previamente utilizadas
        #Devolver la etiqueta principal al mensaje de entrada
        self.etiqueta_1.config(text=SALUDO)
        #Elementos a eliminar
        for widget in self.main_frame.winfo_children():
            if widget in [self.etiqueta_1, self.result_volume, self.result_surface]:
                #No destruir si es la etiqueta principal o las entradas de resultados
                widget.pack_forget()
                continue
            widget.destroy()
        #Volver a colocar le etiqueta principal
        self.etiqueta_1.pack(side='top', fill='x')

    def __show_popupmenu(self, value_string:tk.StringVar, event:tk.Event = None):
        try:
            self.value_selected = float(value_string.get())
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

def select(new_body:calculator.Body):
    '''
    Seleccionar un cuerpo geométrico para ser representado en la interfaz de la ventana principal.
    '''
    main_frame.load(deepcopy(new_body))

def clean_window():
    '''
    Borrar todo el contenido de la ventana principal y volver al mensaje por defecto.
    '''
    main_frame.clean_frame()

#Título de la ventana
window.title('Calculadora de volumen')

#Tamaño
window.geometry("500x600")
window.minsize(400, 450)
window.maxsize(600, 700)

#Icono
window.iconbitmap('icon.ico')

# Deshabilitar modo pantalla completa
window.attributes("-fullscreen", False)

#Color de fondo
window.configure(bg="lightblue")

#Menu desplegable
menu_bar = tk.Menu(window)
menu_principal =tk.Menu(menu_bar, tearoff=0)
submenu_figuras=tk.Menu(menu_principal, tearoff=0)
window.config(menu=menu_bar)

#Añadir las figuras al sub-menu figuras
for body in bodies:
    submenu_figuras.add_command(label=body, command=lambda x = body : select(x))
#Añadir el menu principal a la barra de menu
menu_bar.add_cascade(label="Inicio", menu=menu_principal)
#Añadir el menu figuras al menu principal
menu_principal.add_cascade(label='Figuras', menu = submenu_figuras)
#Añadir el menu figuras al menu principal
menu_principal.add_command(label='Reiniciar', command= clean_window)
#Añadir la opcion salir al menu principal
menu_principal.add_separator()
menu_principal.add_command(label='Salir', command=window.destroy)

#Ventana principal de la aplicación
main_frame = CalculatorFrame(window)

window.mainloop()
