'''
Módulo encargado de definir las formas geométricas,
determinando sus parámetros y calculando sus propiedades.
'''
from abc import ABC, abstractmethod
from math import pi as PI

#Clase base para todo cuerpo geométrico
class Body(ABC):
    '''
    Clase base para definir los cuerpos geométricos.

    Definir
    ---
        - volume : return `float`
        - surface : return `float`
    '''
    def __init__(self, name:str, **kwargs:dict[str, int|float]):
        self.name:str = name
        self.__parameters:dict[str, int|float] = kwargs
    @property
    def parameters(self)->dict[str, int|float]:
        '''
        Obtiene una copia de los parámetros del cuerpo geométrico.

        Para obtener/modificar un valor específico llama:
        -   `Body.set(key, value)`:
        -   `Body.get(key)`.
        '''
        return self.__parameters.copy()
    @parameters.setter
    def parameters(self, data:dict[str, int|float])->None:
        if not isinstance(data, dict):
            raise TypeError("La variable 'data' debe ser un diccionario")
        if data.keys() == self.__parameters.keys():
            self.__parameters = data.copy()
        else:
            raise IndexError(f"Los índices no coinciden: {list(self.__parameters.keys())}")
    def set(self, key:str, value:int|float)->None:
        '''
        Cambia un valor de un parámetro ya definido del cuerpo geométrico.
        
        Si el parámetro no existe no hace nada.
        '''
        if key in self.__parameters:
            self.__parameters[key] = value
    def get(self, key:str)->int|float|None:
        '''
        Función para obtener los valores de los parámetros.

        Si el parámetro no existe provoca un error.
        '''
        try:
            return self.__parameters[key]
        except KeyError as e:
            raise KeyError('Parámetro no encontrado') from e
    @abstractmethod
    def volume(self)-> float:
        ''' Se debe declarar la fórmula de volumen '''
        return
    @abstractmethod
    def surface(self)-> float:
        ''' Se debe declarar la fórmula de superficie '''
        return
    def __str__(self):
        #Para obtener el nombre empezando con mayuscula y el resto en minúscula
        return self.name[0].upper()+self.name[1:].lower()

#Clases para cada nuevo cuerpo geométrico
class Sphere(Body):
    '''
    Cuerpo geométrico: Esfera
    '''
    def __init__(self, radius:int|float = 0):
        super().__init__(name='Esfera', radio = radius)
    def volume(self)->float:
        return (4/3) * PI * self.get('radio')**3
    def surface(self)->float:
        return 4 * PI * self.get('radio')**2

class Cube(Body):
    '''
    Cuerpo geométrico: Cubo
    '''
    def __init__(self, side:int|float = 0):
        super().__init__(name='Cubo', lado=side)
    def volume(self)->float:
        return self.get('lado')**3
    def surface(self)->float:
        return 6 * (self.get('lado')**2)

#Variable donde guardar los cuerpos creados/configurados
bodies_data:list[Body] = [Sphere(), Cube()]
