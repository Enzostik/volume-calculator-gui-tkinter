
#Clase base para todo cuerpo geométrico
class Body:
    def __init__(self, name:str, **kwargs:dict[str, int|float]):
        self.name:str = name
        self.parameters:dict[str, int|float] = kwargs
        self.volume = 0

#Variable donde guardar los cuerpos creados/configurados
BODIES_DATA = (Body('ejemplo', longitud=10))