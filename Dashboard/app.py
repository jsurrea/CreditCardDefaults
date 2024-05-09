from dash import Dash, html, dcc, callback, Output, Input
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from os import path

app = Dash(__name__, external_stylesheets = [path.join('assets', 'styles.css')])
app.title = "CREDIT CARD DEFAULTS"


df = pd.read_csv(path.join('assets', 'data.csv'))

def create_treemap():
    temp_df = df.copy()
    temp_df['Age'] = pd.cut(
        temp_df['Age'], 
        bins=[20, 28, 35, 46, 80],
        labels=['Young Adult (20-27)', 'Adult (28-35)', 'Middle Aged (36-45)', 'Senior (46-80)'],
        include_lowest=True,
        ordered=True
    )
    temp_df['Defaulted Payment Next Month'] = temp_df['Defaulted Payment Next Month'].map({ 'Not Defaulted': 0, 'Defaulted': 1 }).astype(int)
    mean_defaulted = temp_df['Defaulted Payment Next Month'].mean()
    temp_df = temp_df.groupby(['Marriage', 'Sex', 'Age', 'Education'])['Defaulted Payment Next Month'].agg(['mean', 'count']).reset_index().rename(columns={'mean': 'Defaulted (%)', 'count': 'Number of Customers'})
    temp_df = temp_df[temp_df['Marriage'] != 'Others']
    temp_df = temp_df[temp_df['Education'] != 'Others']
    temp_df['Defaulted (%)'] = temp_df['Defaulted (%)'] * 100
    fig = px.treemap(
        temp_df, 
        path=[px.Constant("Customers"), 'Marriage', 'Sex', 'Age', 'Education'], 
        values='Number of Customers',
        color='Defaulted (%)', 
        color_continuous_scale="RdBu_r",
        color_continuous_midpoint=mean_defaulted * 100,
    )
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig


def create_parcoords():
    temp_df = df.copy()
    temp_df['Defaulted October Payment'] = temp_df['Defaulted Payment Next Month'].map({ 'Not Defaulted': 0, 'Defaulted': 1 }).astype(int)
    for column in ['Payed Status in September', 'Payed Status in August', 'Payed Status in July', 'Payed Status in June', 'Payed Status in May', 'Payed Status in April']:
        temp_df[column] = temp_df[column].map({
            'New Customer': 0,
            'Paid ahead': 0,
            'Paid on time': 0,
            'Delay 1 Month': 1,
            'Delay 2 Months': 1,
            'Delay 3 Months': 1,
            'Delay 4 Months': 1,
            'Delay 5 Months': 1,
            'Delay 6 Months': 1,
            'Delay 7 Months': 1,
            'Delay 8 Months': 1,
            'Delay 9+ Months': 1,
        }).astype(int)
        temp_df[column] = temp_df[column] + np.random.normal(0, 0.1, temp_df.shape[0])
    temp_df = temp_df.sample(500)
    fig = go.Figure(
        data=go.Parcoords(
            line = dict(
                color = temp_df['Defaulted October Payment'],
                colorscale = 'RdBu_r',
                showscale = False,
                cmin = -1,
                cmax = 2,
            ),
            dimensions = list([
                dict(label = "April", values = temp_df['Payed Status in April'], tickvals=[0, 1], ticktext=['Paid on Time', 'Delayed']),
                dict(label = "May", values = temp_df['Payed Status in May'], tickvals=[0, 1], ticktext=['Paid on Time', 'Delayed']),
                dict(label = "June", values = temp_df['Payed Status in June'], tickvals=[0, 1], ticktext=['Paid on Time', 'Delayed']),
                dict(label = "July", values = temp_df['Payed Status in July'], tickvals=[0, 1], ticktext=['Paid on Time', 'Delayed']),
                dict(label = "August", values = temp_df['Payed Status in August'], tickvals=[0, 1], ticktext=['Paid on Time', 'Delayed']),
                dict(label = "September", values = temp_df['Payed Status in September'], tickvals=[0, 1], ticktext=['Paid on Time', 'Delayed']),
                dict(label = "Defaulted October Payment", values = temp_df['Defaulted October Payment'], tickvals=[0, 1], ticktext=['Not Defaulted', 'Defaulted']),
            ]),
            unselected = dict(line = dict(opacity = 0)),
        )
    )
    return fig


def create_indicator():
    p = 0.05  # Margen de ganancia promedio (profit margin)
    r = 0.3  # Tasa de recuperación de catera (recovery rate)
    temp_df = df.copy()
    temp_df['Defaulted October Payment'] = temp_df['Defaulted Payment Next Month'].map({ 'Not Defaulted': 0, 'Defaulted': 1 }).astype(int)
    temp_df['Average Bill Amount'] = temp_df[['Bill Amount in April', 'Bill Amount in May', 'Bill Amount in June', 'Bill Amount in July', 'Bill Amount in August', 'Bill Amount in September']].median(axis=1)
    temp_df['Average Amount Paid'] = temp_df[['Amount Paid in April', 'Amount Paid in May', 'Amount Paid in June', 'Amount Paid in July', 'Amount Paid in August', 'Amount Paid in September']].median(axis=1)
    temp_df['Average Debt'] = temp_df['Average Bill Amount'] - temp_df['Average Amount Paid']
    temp_df['Income'] = temp_df['Average Bill Amount'] * 6 * p * (1 - temp_df['Defaulted October Payment'])
    temp_df['Loses'] = temp_df['Average Debt'] * temp_df['Defaulted October Payment'] * (1 - r)
    temp_df['Revenue'] = temp_df['Income'] - temp_df['Loses']
    income = temp_df['Income'].sum()
    loses = temp_df['Loses'].sum()
    revenue = temp_df['Revenue'].sum()
    print(f"income={income:.0f}, loses={loses:.0f}, revenue={revenue:.0f}")

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number",
        value = income,
        number = {'prefix': "$", 'font': {'size': 50, 'color': '#3cb040'}},
        title = {"text": "Income"},
        domain = {'row': 0, 'column': 0},
        delta = {}
    ))
    fig.add_trace(go.Indicator(
        mode = "number",
        value = loses,
        number = {'prefix': "$", 'font': {'size': 50, 'color': '#f06454'}},
        title = {"text": "Unpaid Debt"},
        domain = {'row': 1, 'column': 0},
    ))
    fig.add_trace(go.Indicator(
        mode = "number",
        value = revenue,
        number = {'prefix': "$", 'font': {'size': 80, 'color': '#5eb4e6'}},
        title = {"text": "Revenue"},
        domain = {'row': 2, 'column': 0},
    ))
    fig.update_layout(
        grid = {'rows': 3, 'columns': 1, 'ygap': 0.5},
        margin = dict(t=50, l=25, r=25, b=25),
    )
    return fig

#modelooo

def create_gauge_figure(display_value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = display_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Productividad Esperada"},
        gauge = {'axis': {'range': [0, 100], 'ticks': 'outside', 'dtick': 10}, 'bar': {'color': '#9775FA'}},
        number={'suffix': "%", 'font': {'color': '#9775FA'}},  # Color del número
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Color de fondo del lienzo
        plot_bgcolor='rgba(0,0,0,0)',   # Color de fondo del gráfico
        width=300,  # Ancho de la gráfica
        height=300,  # Altura de la gráfica
        margin={"t": 0, "b": 0, "l": 0, "r": 0},  # Ajustar los márgenes
        font={"color": '#FCFDFE'},
    )
    return fig



@callback(
    Output(component_id='gauge-sweing', component_property='figure'),
    Input(component_id='sweing-slider', component_property='value')
)
def create_gauge_figure_sweing(incentive):
    productivity = 80 * 100
    return create_gauge_figure(productivity)

@callback(
    Output(component_id='gauge-finishing', component_property='figure'),
    Input(component_id='finishing-slider', component_property='value')
)
def create_gauge_figure_finishing(smv):
    productivity = 80 * 100
    return create_gauge_figure(productivity)

# Callbacks para los componentes de Dash
@app.callback(
    Output('dropdown-output', 'children'),
    Input('categorical-dropdown', 'value')
)
def display_dropdown_value(value):
    return f'Selected option: {value}'

@callback(
    Output('boolean-switch-output-1', 'children'),
    Input('my-boolean-switch', 'on')
)
def update_output(on):
    return f'The switch is {on}.'



app.layout = html.Div([
    html.Header([
        html.Section([
            html.H1("CREDIT CARD DEFAULTS"),
            html.P("Herramienta analítica para prever y gestionar el riesgo de incumplimiento en tarjetas de crédito."),
        ], className="header-title"),
        html.Section([
            html.Img(src=path.join('assets', 'logo.png'), alt="Uniandes Logo"),
        ], className="header-logo"),
    ], className="header-container"),
    html.Main([
        html.Section([
            html.Div([
                html.H2("Treemap de Riesgo de Default"),
                dcc.Graph(id="graph-treemap", figure=create_treemap()),  # primera graficaaaa
                html.P("Visualiza la probabilidad de incumplimiento de pagos por factores demográficos como estado civil, sexo, edad y educación."),
            ], className="card", style={'width': '100%'}),  # Ocupa toda la fila
        ], className="main-graphs"),
        html.Section([
            html.Div([
                html.H2("Análisis de Comportamiento de Pago"),
                dcc.Graph(id="graph-parcoords", figure=create_parcoords()),
                html.P("Muestra patrones de pago y estados de cuentas de los clientes mes a mes, destacando los incumplimientos."),
            ], className="card", style={'width': '60%', 'height': '100%'}),  # 60% del ancho
            html.Div([
                html.H2("Indicadores Financieros"),
                dcc.Graph(id="graph-indicator", figure=create_indicator()),
                html.P("Exhibe ingresos, pérdidas por deudas impagas y ganancias netas, enfatizando el rendimiento financiero."),
            ], className="card", style={'width': '40%', 'height': '100%'}),  # 40% del ancho
        ], className="main-graphs"),
        html.Section([
            html.H2("Modelos de Machine Learning"),

            #prueba de componentes
            dcc.Dropdown(
                id='categorical-dropdown',
                options=[
                    {'label': 'Option 1', 'value': 'option1'},
                    {'label': 'Option 2', 'value': 'option2'},
                    {'label': 'Option 3', 'value': 'option3'}
                ],
                value='option1'
            ),
            html.Div(id='dropdown-output'),

            daq.BooleanSwitch(id='my-boolean-switch', on=False),
            #-----------

            html.Div(id='boolean-switch-output-1'),
            html.Div([
                html.Div([
                    html.H3("Sweing Department"),
                    html.P("Este modelo predice la productividad en el departamento de Sweing."),
                    html.P("Seleccione el incentivo para obtener una predicción."),
                    dcc.Slider(0, 120, 5, value=20, id='sweing-slider'),
                    dcc.Graph(id="gauge-sweing", figure=create_gauge_figure_sweing(0)),
                ], className="model-container"),
                html.Div([
                    html.H3("Finishing Department"),
                    html.P("Este modelo predice la productividad en el departamento de Finishing."),
                    html.P("Seleccione el tiempo asignado para obtener una predicción."),
                    dcc.Slider(2, 6, 0.25, value=3, id='finishing-slider'),
                    dcc.Graph(id="gauge-finishing", figure=create_gauge_figure_sweing(0)),
                ], className="model-container")
            ], className="main-models"),
        ], className="card main-models-container"),
    ], className="main-container"),
], className="root-container")




if __name__ == '__main__':
    app.run_server(host = "localhost", port=8050, debug=True)
