import json

colums = ['Código', 'Inventario actual', 'Tiempo de entrega', 'Mínimo de compra', 'Pronóstico de venta',
          'Unidades a comprar', 'Real vendido', 'Diferencia entre prediccion vs real',
          'Diferencia entre prediccion vs real (porcentual)', 'Error medio cuadratico']

colums_optiones = ['Real vendido', 'Tiempo de entrega',
                   'Inventario actual', 'Minimo de compra']

products = ['BOTANA',
            'DULCES',
            'ABARROTES',
            'BEBIDAS',
            'PANADERIA Y REPORTERIA',
            'LACTEOS Y EMBUTIDOS',
            'SERVICIOS Y LIMPIEZA',
            'FRUTAS Y VERDURAS',
            'QUESOS',
            'CARNES Y AVES',
            'ALMACEN COCINA',
            'SECOS Y CEREALES',
            'CERVEZAS',
            'CIGARROS',
            'PESCADOS Y MARISCOS',
            'ESPECIAS',
            'HELADOS',
            'VINOS Y LICORES']


default_products = {
            'data': [
            ]
        }, 0, json.dumps({}, default=str), json.dumps({}, default=str)