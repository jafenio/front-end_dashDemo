from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from styles import style_input, style_label, style_output, style_select, style_title
from utils import colums, colums_optiones, products, default_products
from math import ceil
import dash_bootstrap_components as dbc
import json
import requests
import os

url = str(os.environ['BACKEND_URL'])

def get_category_products():
    response = requests.get(f'{url}/category-products')
    print(f'Petition to: {url}/category-products, status code: {response.status_code}')
    data = list(response.json()['data'])
    return data

app = Dash(external_stylesheets=[dbc.themes.SIMPLEX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div(
                html.H2('Dashboard DEMO')
            ), style=style_title
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Dropdown(
                    id='category',
                    options=get_category_products(),
                    placeholder='Selecciona una categoría',
                    style=style_select
                )
            )
        ),
        dbc.Col(
            html.Div([
                dcc.Dropdown(
                    id='drop_product',
                    options=[],
                    value=[],
                    multi=False,
                    placeholder="Seleccione un producto",
                    style=style_select
                )
            ]), align='center'
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id='grafico',
                    figure={
                        'data': [
                        ]
                    }
                )
            ), style={'padding-top': '2%'}
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                html.H3("Datos para la predicción")
            ), align='center',  style=style_title
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5(colums_optiones[2], style=style_label),
                dcc.Input(
                    id='i_inv_actual',
                    placeholder='0',
                    type="number",
                    min=0,
                    style=style_input
                )]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums_optiones[3], style=style_label),
                dcc.Input(
                    id='minimo_compra',
                    placeholder='0',
                    type="number",
                    min=0,
                    style=style_input
                )]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums_optiones[1], style=style_label),
                dcc.Input(
                    id='i_tiem_entrega',
                    placeholder='0',
                    type="number",
                    min=1,
                    style=style_input
                )]
            )
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                html.H3('Unidades que se deben de comprar')
            ), align='center',  style=style_title
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5(colums[0], style=style_label),
                html.Div(id='codigo', style=style_output)
            ]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums[1], style=style_label),
                html.Div(id='inventario', style=style_output)
            ]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums[2], style=style_label),
                html.Div(id='tiempo_entrega', style=style_output)
            ]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums[3], style=style_label),
                html.Div(id='m_compra', style=style_output)
            ]
            )
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5(colums[4], style=style_label),
                html.Div(id='p_venta', style=style_output)
            ]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums[5], style=style_label),
                html.Div(id='u_comprar', style=style_output)
            ]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums[6], style=style_label),
                html.Div(id='r_vendido', style=style_output)
            ]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums[7], style=style_label),
                html.Div(id='d_predicion_real', style=style_output)
            ]
            )
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5(colums[8], style=style_label),
                html.Div(id='p_predicion_real', style=style_output)
            ]
            )
        ),
        dbc.Col(
            html.Div([
                html.H5(colums[9], style=style_label),
                html.Div(id='e_medio', style=style_output)
            ]
            )
        ),
        dbc.Col(
            dcc.Store(id='prediction_values')
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Store(id='real_values')
        ),
        dbc.Col(
            html.Div(
                html.P()
            ), style=style_title
        )
    ])
])

# Rellenado del select de productos.


@app.callback(
    Output('drop_product', 'options'),
    [Input('category', 'value')]
)
def update_product(p):
    print('update_product')
    if p is not None:
        response = requests.post(f'{url}/search-products', json={'product': p})
        print(f'Petition to: {url}/seacrh-products, status code: {response.status_code}')
        data = list(response.json()['data'])
    else:
        print(f'Not petition to: {url}/seacrh-products')
        data = []
    return [{'label': v, 'value': v} for v in data]

# Generamos la grafica de forma dinamica.


@app.callback(
    Output('grafico', 'figure'),
    Output('e_medio', component_property='children'),
    Output('prediction_values', 'data'),
    Output('real_values', 'data'),
    Input('drop_product', 'value'),
    Input('category', 'value')
)

def grah_update(drop_product, category):
    print('grah_update')
    if isinstance(drop_product, str) and isinstance(category, str):
        response = requests.post(f'{url}/prediction-product', json={'product': drop_product})
        print(f'Petition to: {url}/prediction-product, status code: {response.status_code}')
        data = response.json()['data']
        clean_ceros = {'data': list(
            filter(lambda x: x != 0.0, list(data['prediction-values'])))}
        data_real = {'data': list(data['real-values'])}
        return {
            'data': [
                {'x': data['days'], 'y': data['real-values'], 'type': 'line', 'name': 'Datos'},
                {'x': data['days'], 'y': data['prediction-values'], 'type': 'line', 'name': 'Predicción'},
                {'x': data['days'], 'y': data['training-values'], 'type': 'line', 'name': 'Entrenamiento'}
            ],
            'layout': {
                'title': data['name']
            }
        }, data['mean-square-error'], json.dumps(clean_ceros, default=str), json.dumps(data_real, default=str)
    else:
        print(f'Not petition to: {url}/prediction-product')
        return default_products
        

# Rellenado de forma dinamica el codigo.


@app.callback(
    Output('codigo', component_property='children'),
    Input('drop_product', 'value')
)
def update_codigo(value):
    return value

# Detonante de Tiempo de entrega.


@app.callback(
    Output('tiempo_entrega', component_property='children'),
    Input('i_tiem_entrega', 'value')
)
def procces_tiempo_entrega(value):
    return value

# Detonante de Inventario actual.


@app.callback(
    Output('inventario', component_property='children'),
    Input('i_inv_actual', 'value')
)
def procces_inventario_actual(value):
    return value

# Detonante de Minimo de compra.


@app.callback(
    Output('m_compra', component_property='children'),
    Input('minimo_compra', 'value')
)
def procces_minimo_compra(value):
    if value is None:
        value = 0
    return value

# Detonante de Pronostico de venta.


@app.callback(
    Output('p_venta', component_property='children'),
    Output('u_comprar', component_property='children'),
    Output('d_predicion_real', component_property='children'),
    Output('p_predicion_real', component_property='children'),
    Output('r_vendido', component_property='children'),
    Input('i_tiem_entrega', 'value'),
    Input('drop_product', 'value'),
    Input('i_inv_actual', 'value'),
    Input('minimo_compra', 'value'),
    Input('real_values', 'data'),
    Input('prediction_values', 'data')
)
def procces_pronostico_venta(i_tiem_entrega, drop_product, i_inv_actual, minimo_compra, real_values, prediction_values):
    # Variables a retonar
    pronostic = 0
    unidad = 0
    dif_pre_real = 0
    por_per_real = 0
    real_vendido = 0
    # Verificador
    if i_tiem_entrega is None or i_inv_actual is None or real_values is None or drop_product is None or prediction_values is None or minimo_compra is None:
        return pronostic, unidad, dif_pre_real, por_per_real, real_vendido
    else:
        get_real_values = json.loads(real_values)['data']
        clean_ceros = json.loads(prediction_values)['data']
        diferentia = len(get_real_values) - len(clean_ceros) - 2
        # Calculamos el real vendido
        for i in range(diferentia, diferentia + i_tiem_entrega):
            real_vendido += int(float(get_real_values[i]))
        real_vendido = int(float(real_vendido))
        # Calculamos el pronostico de venta
        for i in range(i_tiem_entrega):
            pronostic += clean_ceros[i]
        pronostic = ceil(round(pronostic, 6))
        if(int(pronostic) < int(minimo_compra)):
            pronostic = minimo_compra
        # Calculamos las unidades a comprar
        unidad = pronostic - i_inv_actual
        unidad = round(unidad, 6)
        if(int(unidad) < int(minimo_compra)):
            unidad = minimo_compra
        # Calculamos la diferencia entre lo predecido y lo real
        dif_pre_real = pronostic - real_vendido
        dif_pre_real = round(dif_pre_real, 6)
        # Calculamos el porcentaje entre lo predecido y lo real
        try:
            diferentia = ((pronostic * 100) / real_vendido) - 100
            por_per_real = round(diferentia, 2)
        except ZeroDivisionError:
            por_per_real = 0
        por_per_real = f'{por_per_real}%'
        return pronostic, unidad, dif_pre_real, por_per_real, real_vendido

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=3000)
