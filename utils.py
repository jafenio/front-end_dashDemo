import json

colums = ['Código', 'Inventario actual', 'Tiempo de entrega', 'Mínimo de compra', 'Pronóstico de venta',
          'Unidades a comprar', 'Real vendido', 'Diferencia entre prediccion vs real',
          'Diferencia entre prediccion vs real (porcentual)', 'Error medio cuadratico']

colums_optiones = ['Real vendido', 'Tiempo de entrega',
                   'Inventario actual', 'Minimo de compra']

default_products = {
    'data': [
    ]
}, 0, json.dumps({'data': []}, default=str), json.dumps({'data': []}, default=str), ''


def clean_values_pronostic():
    return 0, 0, 0, 0, 0


def validation_none(comprobation):
    return None in comprobation.values()

def validation_cero(values):
    return 0 in values
