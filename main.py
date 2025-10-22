import tkinter as tk
from copy import deepcopy
from PIL import Image, ImageTk

import calculator

'''
---------
Variables
---------
'''
#Texto de saludo
SALUDO = "Seleccione una figura del menú desplegable para calcular su volumen"

#Los cuerpos se pueden obtener del modulo 'calculator'
bodies = calculator.bodies_data

#Elemento de ventana de tkinter
window = tk.Tk()

'''
------------------------
Elementos de la ventana
------------------------
'''
class CalculatorFrame:
    def __init__(self, root:tk.Tk):
        #Variable que contenga el cuerpo para los calculos
        self.body = None

        #Se crea un frame que ocupe toda la ventana. El contenido a editar se encuentra dentro de este frame.
        self.main_frame = tk.Frame(root, borderwidth=1, relief="groove")
        self.main_frame.configure(bg="lightblue")
        self.main_frame.pack(expand=True, fill='both', pady=20, padx=20)

        #Etiqueta de inicio
        self.etiqueta_1 = tk.Label(self.main_frame, text=SALUDO, font=("Arial", 12), bg="gray",wraplength=350) #mensaje principal
        self.etiqueta_1.pack(side='top', fill='x')

        #Registrar la function para validar que la nueva entrada sea un número
        self.entry_verification = (root.register(self.validate_number), '%P')
        #Almacenar las variables de las entradas en un diccionario para que no se borren al no ser referenciadas
        self.entries_var:dict[str, tk.StringVar] = {}
        #Almacenar la referencia a la entrada que será destinada al resultado
        self.var_volume = tk.StringVar()
        self.result_volume:tk.Entry = tk.Entry(master=self.main_frame, textvariable=self.var_volume, font=("Arial", 15), fg="blue", justify='center', width=25, state='readonly')
        self.var_surface = tk.StringVar()
        self.result_surface:tk.Entry = tk.Entry(master=self.main_frame, textvariable=self.var_surface, font=("Arial", 15), fg="blue", justify='center', width=25, state='readonly')

    #Comprobar que el valor a ingresar sea un numero
    def validate_number(self, value:str)->bool:
        if value != '': #Si no se borra el contenido
            try:
                float(value)
            except:
                return False
        return True
    
    #Variable que se llamará cuando se cambie alguna de las entradas de texto
    def change_value(self, name:str, value:str):
        #Si la entrada está vacía será 0. Convertir variable string --> float
        value = 0 if value == '' else float(value)
        #Cambiar el valor del parametro
        self.body.set(name, value)
        #Cambiar el valor del texto de volumen y superficie
        self.set_results()

    #Cambiar el valor del texto de volumen y superficie
    def set_results(self):
        self.var_volume.set("{:.4f}".format(self.body.volume()))
        self.var_surface.set("{:.4f}".format(self.body.surface()))

    #Cambiar el contenido del frame para que corresponda al cuerpo geométrico
    def load(self, body:calculator.Body):
        #Eliminar el contenido del frame
        self.clean_frame()
        #Guardar el cuerpo
        self.body = body
        #Modificar el título de la ventana para que sea el nombre del cuerpo
        self.etiqueta_1.config(text=body)
        #Cargar la imagen
        img = Image.open(f'images/{body.name.lower()}.png') #Se carga el archivo con el mismo nombre de la forma en la carpeta imagenes
        img = img.resize((150, 150))
        image = ImageTk.PhotoImage(img) #Convertir la imagen para utilizarla en tkinter
        etiqueta_img = tk.Label(self.main_frame, image=image) #Añadir la imagen en un Label
        etiqueta_img.image = image
        etiqueta_img.pack(pady=5) #Añadir el label al frame
        #Etiqueta para las instrucciones
        etiqueta_instruccion = tk.Label(self.main_frame, text="Ingrese los valores indicados:", font=("Arial", 10), justify='left', background='lightblue')
        etiqueta_instruccion.pack(fill='x', pady=5) #Añadir la etiqueta al frame

        #Crear las entradas de texto para cada parámetro
        
        for key, value in body.parameters.items():
            #Etiqueta con el nombre de la variable
            etiqueta_valor = tk.Label(self.main_frame, text=key[0].upper()+key[1:].lower(), font=("Arial", 10), background="gray")
            etiqueta_valor.pack(anchor='w', fill='x', pady=5)
            #Variable de la entrada de texto
            variable_valor = tk.StringVar(name=key, value=value)
            self.entries_var[key] = variable_valor
            #Entrada de texto
            entrada_valor = tk.Entry(self.main_frame, textvariable=variable_valor, validate='key', validatecommand=self.entry_verification)
            entrada_valor.pack(pady=5)
            #Evento en caso de modificación de la entrada de texto
            variable_valor.trace_add('write', lambda name, _index, _mode, v = variable_valor : self.change_value(name, v.get()))

        #Añadir entradas de solo lectura para mostrar los resultados del volumen y de la superficie del cuerpo
        etiqueta_volumen = tk.Label(self.main_frame, text=f"El volumen del {body.name.lower()} es:", font=("Arial", 15), fg="blue", bg='gray')
        etiqueta_volumen.pack(fill='x', pady=5)
        self.result_volume.pack(pady=5)
        etiqueta_superficie = tk.Label(self.main_frame, text=f"La superficie del {body.name.lower()} es:", font=("Arial", 15), fg="blue", bg='gray')
        etiqueta_superficie.pack(fill='x', pady=5)
        self.result_surface.pack(pady=5)
        #Cambiar los valores de los resultados si es necesario
        self.set_results()

    #Funcion para limpiar la pantalla cuando se cambia de opción de figura
    def clean_frame(self):
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
            

'''
----------------------------------
Funciones para el manejo de entradas
----------------------------------
'''
def select(body:calculator.Body):
    main_frame.load(deepcopy(body))

def clean_window():
    main_frame.clean_frame()

'''
---------------------
Configurar la ventana
---------------------
'''
#Título de la ventana
window.title('Calculadora de volumen')

#Tamaño
window.geometry("500x500")
window.minsize(400, 350)
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