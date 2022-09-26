from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output
from styles import style_input, style_label, style_output, style_select, style_title, colorsFigure
from utils import colums, colums_optiones, default_products, clean_values_pronostic, validation_none, validation_cero
from math import ceil
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
import requests
import os

url = str(os.environ['BACKEND_URL'])


def get_category_products():
    response = requests.get(f'{url}/category-products')
    print(
        f'Petition to: {url}/category-products, status code: {response.status_code}')
    data = list(response.json()['data'])
    output = []
    for i in data:
        output.append({"label": i, "value": i})
    return output


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
            html.Div([
                dbc.Select(
                    id='category',
                    options=get_category_products(),
                    style=style_select
                )
            ]), align='center'
        ),
        dbc.Col(
            html.Div([
                dbc.Select(
                    id='drop_product',
                    options=[],
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
                dbc.Input(
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
                dbc.Input(
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
                dbc.Input(
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
    result = [{'label': 'Selecciona una de las siguientes opciones', 'value': ''}]
    if p is None:
        data = []
    response = requests.post(f'{url}/search-products', json={'product': p})
    print(
        f'Petition to: {url}/seacrh-products, status code: {response.status_code}')
    data = list(response.json()['data'])

    for v in data:
        result.append({'label': v, 'value': v})
    return result

# Generamos la grafica de forma dinamica.


@app.callback(
    Output('grafico', 'figure'),
    Output('e_medio', component_property='children'),
    Output('prediction_values', 'data'),
    Output('real_values', 'data'),
    Output('codigo', component_property='children'),
    Input('drop_product', 'value'),
    Input('category', 'value')
)
def grah_update(drop_product, category):
    triggered_id = ctx.triggered_id
    if triggered_id == 'drop_product':
        return draw_graph(drop_product)
    return reset_graph(category)


def draw_graph(drop_product):
    response = requests.post(
        f'{url}/prediction-product', json={'product': drop_product})
    print(
        f'Petition to: {url}/prediction-product, status code: {response.status_code}')
    data = response.json()['data']
    clean_ceros = {'data': list(
        filter(lambda x: x != 0.0, list(data['prediction-values'])))}
    data_real = {'data': list(data['real-values'])}
    # Comienza el proceso de graficacion
    values_day = data['days'][:-3]
    values_real = data['real-values']
    values_prediction = [0, 0] + data['prediction-values']
    post_training = [0 for v in range(
        len(data['prediction-values']) - len(data['training-values']))]
    values_trainin = data['training-values'] + post_training
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=values_day, y=values_prediction,
                             mode='lines', name='Prediccion'))
    fig.add_trace(go.Scatter(x=values_day, y=values_trainin,
                             mode='lines', name='Entrenamiento'))
    fig.add_trace(go.Scatter(x=values_day, y=values_real,
                             mode='lines', name='Real'))
    fig.update_layout(
        plot_bgcolor=colorsFigure['background'],
        paper_bgcolor=colorsFigure['background'],
        font_color=colorsFigure['text']
    )
    return fig, data['mean-square-error'], json.dumps(clean_ceros, default=str), json.dumps(data_real, default=str), drop_product


def reset_graph(category):
    print('reset_graph, option: ', category)
    return default_products

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

# Detonante de Unidades que se deben de comprar.


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
    real_vendido = 0
    pronostic = 0
    por_per_real = 0
    # Verificamos que ninguna entrada este en None.
    validation = {
        'i_tiem_entrega': i_tiem_entrega,
        'drop_product': drop_product,
        'i_inv_actual': i_inv_actual,
        'minimo_compra': minimo_compra
    }
    comprobation_none = validation_none(validation)
    if comprobation_none:
        return clean_values_pronostic()
    get_real_values = json.loads(real_values)['data']
    clean_ceros = json.loads(prediction_values)['data']
    # Verificamos que los datos reales y las predicciones no esten vacias.
    comprobation_cero = validation_cero(
        [len(get_real_values), len(clean_ceros)])
    if comprobation_cero:
        return clean_values_pronostic()
    diferentia = len(get_real_values) - len(clean_ceros) - 2
    # Calculamos el real vendido
    for i in range(diferentia, diferentia + i_tiem_entrega):
        real_vendido += int(float(get_real_values[i]))
    real_vendido = int(float(real_vendido))
    # Calculamos el pronostico de venta
    for i in range(i_tiem_entrega):
        pronostic += clean_ceros[i]
    pronostic = ceil(round(pronostic, 6))
    if int(pronostic) < int(minimo_compra):
        pronostic = minimo_compra
    # Calculamos las unidades a comprar
    unidad = pronostic - i_inv_actual
    unidad = round(unidad, 6)
    if int(unidad) < int(minimo_compra):
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
    app.run_server(debug=True, host='0.0.0.0', port=3000)
