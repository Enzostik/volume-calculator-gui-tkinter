'''
Conversión de unidades de longitud, superficie y volumen.
'''

# Funciones de longitud


def meters_to(value: int | float, unit_to: str) -> int | float:
    '''
    Método para convertir un valor de longitud de metros a otras unidades.
    '''
    match unit_to:
        case 'km' | 'kilometros':
            value /= 1000.0
        case 'hm' | 'hectometro':
            value /= 100.0
        case 'dam' | 'decametro':
            value /= 10.0
        case 'm' | 'metros':
            pass
        case 'dm' | 'decimetros':
            value *= 10
        case 'cm' | 'centimetros':
            value *= 100
        case 'mm' | 'milimetros':
            value *= 1000
        case 'inch' | 'pulgadas':
            value *= 39.37007874
        case _:
            raise IndexError('Unidad de medida no válida.')
    return value


def to_meters(value: int | float, unit_from: str) -> int | float:
    '''
    Método para convertir un valor de longitud cualquier unidad a metros.
    '''
    return value / meters_to(1.0, unit_from)


def length_from_to(value: int | float, unit_from: str, unit_to: str) -> int | float:
    '''
    Método para convertir un valor de longitud de una unidad a otra.
    '''
    # Primero convertir a metros
    value = value / meters_to(1.0, unit_from)
    # Y devolver la undiad deseada
    return meters_to(value, unit_to)

# Funciones de superficie


def meters2_to(value: int | float, unit_to: str) -> int | float:
    '''
    Método para convertir un valor de superficie de metros cuadrados a otras unidades.
    '''
    match unit_to:
        case 'm2' | 'metro cuadrado':
            pass
        case _:
            raise IndexError('Unidad de medida no válida.')
    return value


def to_meters2(value: int | float, unit_from: str) -> int | float:
    '''
    Método para convertir un valor de superficie cualquier unidad a metros cuadrados.
    '''
    return value / meters2_to(1.0, unit_from)

# Funciones de volumen


def meters3_to(value: int | float, unit_to: str) -> int | float:
    '''
    Método para convertir un valor de volumen de metros cúbicos a otras unidades.
    '''
    match unit_to:
        case 'm3' | 'metro cubico':
            pass
        case 'l' | 'litro' | 'dm3' | 'decimetro cubico':
            value *= 1000
        case 'ml' | 'mililitro' | 'cm3' | 'centimetro cubico':
            value *= 1000000
        case 'mm3' | 'milimetro cubico':
            value *= 1000000000
        case _:
            raise IndexError('Unidad de medida no válida.')
    return value


def to_meters3(value: int | float, unit_from: str) -> int | float:
    '''
    Método para convertir un valor de volumen cualquier unidad a metros cúbicos.
    '''
    return value / meters3_to(1.0, unit_from)
