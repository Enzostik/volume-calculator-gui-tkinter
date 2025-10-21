from abc import ABC, abstractmethod
from math import pi as PI

#Clase base para todo cuerpo geométrico
class Body(ABC):
    def __init__(self, name:str, **kwargs:dict[str, int|float]):
        self.name:str = name
        self._parameters:dict[str, int|float] = kwargs
    
    @property
    def parameters(self)->dict[str, int|float]:
        return self._parameters.copy()
    
    @parameters.setter
    def parameters(self, data:dict[str, int|float])->None:
        if not isinstance(data, dict):
            raise TypeError("La variable 'data' debe ser un diccionario")
        if data.keys() == self._parameters.keys():
            self._parameters = data.copy()
        else:
            raise Exception(f"Las llaves de 'data' deben coincidir con las de 'parameters': {list(self._parameters.keys())}")

    def set(self, key:str, value:int|float)->None:
        if key in self._parameters:
            self._parameters[key] = value
    
    def get(self, key:str)->int|float|None:
        try:
            return self._parameters[key]
        except:
            return None

    @abstractmethod
    def volume(self)-> float:
        ''' Se debe declarar la fórmula de volumen '''
        pass

    @abstractmethod
    def surface(self)-> float:
        ''' Se debe declarar la fórmula de superficie '''
        pass

    def __str__(self):
        #Para obtener el nombre empezando con mayuscula y el resto en minúscula
        return self.name[0].upper()+self.name[1:].lower()

#Clases para cada nuevo cuerpo geométrico
class Sphere(Body):
    def __init__(self, radius:int|float = 0):
        super().__init__(name='Esfera', radio = radius)

    def volume(self)->float:
        return (4/3) * PI * self._parameters['radio']**3

    def surface(self)->float:
        return 4 * PI * self._parameters['radio']**2

class Cube(Body):
    def __init__(self, side:int|float = 0):
        super().__init__(name='Cubo', lado=side)
    
    def volume(self):
        return self._parameters['lado']**3
    
    def surface(self):
        return 6 * (self._parameters['lado']**2)

'''
-------------------------------------------
    Creación de los cuerpos geométricos
-------------------------------------------
'''
#Variable donde guardar los cuerpos creados/configurados
bodies_data:list[Body] = [Sphere(), Cube()]

# selected_body = BODIES_DATA[0]
# print('Esfera 1')
# #Para modificar los parametros al mismo tiempo
# print(selected_body.parameters)
# selected_body.parameters = {'radio': 29}
# print(selected_body.parameters)

# #Caso para modificar los valores
# selected_body.set('radio', 100)
# print(selected_body.get('radio'))
# #Si no existe el parametro no hace nada
# selected_body.set('abdcs', 100)
# print(selected_body.get('abdcs'))
# #Mostrar volumen y superficie del cuerpo
# print('Volumen:',selected_body.volume)
# print('Superficie:',selected_body.surface)

# #Ahora se cambia el cuerpo a la segunda esfera
# selected_body = BODIES_DATA[1]
# print('Esfera 2')
# #Mostrar volumen y superficie de la otra esfera
# print('Volumen:',selected_body.volume)
# print('Superficie:',selected_body.surface)