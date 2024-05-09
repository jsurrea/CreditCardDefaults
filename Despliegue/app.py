from dash import Dash, html, dcc, callback, Output, Input
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from os import path
from dotenv import load_dotenv
from model import predict
import psycopg2
import os

app = Dash(__name__, external_stylesheets = [path.join('assets', 'styles.css')])
app.title = "Credit Card Defaults"

load_dotenv(dotenv_path='.env')
USER = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DBNAME = os.getenv('DBNAME')

engine = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)
cursor = engine.cursor()
query = "SELECT * FROM customer_data;"
df = pd.read_sql(query, engine)

df = df.rename(columns={
    'credit_limit': 'Credit Limit',
    'sex': 'Sex',
    'education': 'Education',
    'marriage': 'Marriage',
    'age': 'Age',
    'payed_status_in_september': 'Payed Status in September',
    'payed_status_in_august': 'Payed Status in August',
    'payed_status_in_july': 'Payed Status in July',
    'payed_status_in_june': 'Payed Status in June',
    'payed_status_in_may': 'Payed Status in May',
    'payed_status_in_april': 'Payed Status in April',
    'bill_amount_in_september': 'Bill Amount in September',
    'bill_amount_in_august': 'Bill Amount in August',
    'bill_amount_in_july': 'Bill Amount in July',
    'bill_amount_in_june': 'Bill Amount in June',
    'bill_amount_in_may': 'Bill Amount in May',
    'bill_amount_in_april': 'Bill Amount in April',
    'amount_paid_in_september': 'Amount Paid in September',
    'amount_paid_in_august': 'Amount Paid in August',
    'amount_paid_in_july': 'Amount Paid in July',
    'amount_paid_in_june': 'Amount Paid in June',
    'amount_paid_in_may': 'Amount Paid in May',
    'amount_paid_in_april': 'Amount Paid in April',
    'defaulted_payment_next_month': 'Defaulted Payment Next Month'
})

def create_treemap():
    temp_df = df.copy()
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
    for column in ['Payed Status in September', 'Payed Status in August', 'Payed Status in July', 'Payed Status in June', 'Payed Status in May', 'Payed Status in April']:
        temp_df[column] = temp_df[column] + np.random.normal(0, 0.1, temp_df.shape[0])
    temp_df = temp_df.sample(500)
    fig = go.Figure(
        data=go.Parcoords(
            line = dict(
                color = temp_df['Defaulted Payment Next Month'],
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
                dict(label = "Defaulted October Payment", values = temp_df['Defaulted Payment Next Month'], tickvals=[0, 1], ticktext=['Not Defaulted', 'Defaulted']),
            ]),
            unselected = dict(line = dict(opacity = 0)),
        )
    )
    return fig


def create_indicator():
    p = 0.03  # Margen de ganancia promedio (profit margin)
    r = 0.3  # Tasa de recuperación de catera (recovery rate)
    temp_df = df.copy()
    temp_df['Average Bill Amount'] = temp_df[['Bill Amount in April', 'Bill Amount in May', 'Bill Amount in June', 'Bill Amount in July', 'Bill Amount in August', 'Bill Amount in September']].median(axis=1)
    temp_df['Average Amount Paid'] = temp_df[['Amount Paid in April', 'Amount Paid in May', 'Amount Paid in June', 'Amount Paid in July', 'Amount Paid in August', 'Amount Paid in September']].median(axis=1)
    temp_df['Average Debt'] = temp_df['Average Bill Amount'] - temp_df['Average Amount Paid']
    temp_df['Income'] = temp_df['Average Bill Amount'] * 6 * p * (1 - temp_df['Defaulted Payment Next Month'])
    temp_df['Loses'] = temp_df['Average Debt'] * temp_df['Defaulted Payment Next Month'] * (1 - r)
    temp_df['Revenue'] = temp_df['Income'] - temp_df['Loses']
    income = temp_df['Income'].sum()
    loses = temp_df['Loses'].sum()
    revenue = temp_df['Revenue'].sum()

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number",
        value = income,
        number = {'prefix': "$", 'font': {'size': 50, 'color': '#3cb040'}},
        title = {"text": "Potential Income"},
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
        number = {'prefix': "$", 'font': {'size': 50, 'color': '#5eb4e6'}},
        title = {"text": "Current Revenue"},
        domain = {'row': 2, 'column': 0},
    ))
    fig.update_layout(
        grid = {'rows': 3, 'columns': 1, 'ygap': 0.5},
        margin = dict(t=50, l=25, r=25, b=25),
    )
    return fig

# modelooo

def create_gauge_figure(display_value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = display_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Probabilidad de Incumplimiento"},
        gauge = {'axis': {'range': [0, 100], 'ticks': 'outside', 'dtick': 10}, 'bar': {'color': '#ff6347'}},
        number={'suffix': "%", 'font': {'color': '#ff6347'}},  # Color del número
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Color de fondo del lienzo
        plot_bgcolor='rgba(0,0,0,0)',   # Color de fondo del gráfico
        width=400,  # Ancho de la gráfica
        height=400,  # Altura de la gráfica
        margin={"t": 0, "b": 0, "l": 0, "r": 0},  # Ajustar los márgenes
        font={"color": '#ff6347'},
    )
    return fig

@callback(
    Output(component_id='gauge-model', component_property='figure'),
    [
        # Dropdowns
        Input(component_id='sex-dropdown', component_property='value'),
        Input(component_id='age-dropdown', component_property='value'),
        Input(component_id='education-dropdown', component_property='value'),
        Input(component_id='marital-status-dropdown', component_property='value'),
        # Sliders
        Input(component_id='credit-limit-slider', component_property='value'),
        Input(component_id='bill-amount-slider', component_property='value'),
        Input(component_id='pay-amount-slider', component_property='value'),
        # Switches
        Input(component_id='month-switch-April', component_property='on'),
        Input(component_id='month-switch-May', component_property='on'),
        Input(component_id='month-switch-June', component_property='on'),
        Input(component_id='month-switch-July', component_property='on'),
        Input(component_id='month-switch-August', component_property='on'),
        Input(component_id='month-switch-September', component_property='on'),
    ]
)
def create_gauge_figure_model(sex, age, education, marital_status, credit_limit, bill_amount, pay_amount, april, may, june, july, august, september):
    if any([
        sex is None,
        age is None,
        education is None,
        marital_status is None,
    ]):
        return create_gauge_figure(0)

    probability = predict(sex, age, education, marital_status, credit_limit, bill_amount, pay_amount, april, may, june, july, august, september)
    return create_gauge_figure(probability * 100)



app.layout = html.Div([
    html.Header([
        html.Section([
            html.H1("Credit Card Defaults"),
            html.P("Herramienta analítica para prever y gestionar el riesgo de incumplimiento en tarjetas de crédito."),
        ], className="header-title"),
        html.Section([
            html.Img(src=path.join('assets', 'logo.png'), alt="Uniandes Logo"),
        ], className="header-logo"),
    ], className="header-container"),
    html.Main([
        html.Section([
            html.Div([
                html.H2("Incidencia de Factores Demográficos en la Probabilidad de Incumplimiento de Pago", style={'marginTop': '10px'}),
                dcc.Graph(id="graph-treemap", figure=create_treemap()),  # primera graficaaaa
                html.P("Visualiza la probabilidad de incumplimiento de pagos por factores demográficos como estado civil, sexo, edad y educación."),
            ], className="card", style={'width': '100%'}),  # Ocupa toda la fila
        ], className="main-graphs"),
        html.Section([
            html.Div([
                html.H2("Análisis del Historial de Comportamiento de Pago"),
                dcc.Graph(id="graph-parcoords", figure=create_parcoords()),
                html.P("Muestra patrones de pago y estados de cuentas de los clientes mes a mes, destacando los incumplimientos."),
            ], className="card", style={'width': '60%', 'height': '100%'}),  # 60% del ancho
            html.Div([
                html.H2("Indicadores Financieros Estimados"),
                dcc.Graph(id="graph-indicator", figure=create_indicator()),
                html.P("Exhibe ingresos, pérdidas por deudas impagas y ganancias netas, enfatizando el rendimiento financiero."),
            ], className="card", style={'width': '40%', 'height': '100%'}),  # 40% del ancho
        ], className="main-graphs", style={'height': '560px'}),
        html.Section([
            html.H2("Predicción de Incumplimiento de Pago"),
            html.Div([
                html.Section([
                    html.Section([
                        html.H3("Demografía"),

                        # Dropdowns para sexo, edad, educación, estado civil
                        html.Div([
                            html.Div([
                                html.P("Sex:"), 
                                dcc.Dropdown(
                                    id='sex-dropdown',
                                    options=[
                                        {'label': 'Male', 'value': 1},
                                        {'label': 'Female', 'value': 0}
                                    ],
                                    value=1,
                                    placeholder="Select sex of the customer...",
                                ),
                            ], style={'display': 'grid', 'justifyContent': 'space-between', 'gap': '5px', 'gridTemplateColumns': '140px 1fr', 'alignItems': 'center'}),
                            html.Div([
                                html.P("Age Group:"), 
                                dcc.Dropdown(
                                    id='age-dropdown',
                                    options=[
                                        {'label': 'Young Adult (20-27)', 'value': 'Young Adult (20-27)'},
                                        {'label': 'Adult (28-35)', 'value': 'Adult (28-35)'},
                                        {'label': 'Middle Aged (36-45)', 'value': 'Middle Aged (36-45)'},
                                        {'label': 'Senior (46-80)', 'value': 'Senior (46-80)'}
                                    ],
                                    value='Young Adult (20-27)',
                                    placeholder="Select age group of the customer...",
                                ),                        
                            ], style={'display': 'grid', 'justifyContent': 'space-between', 'gap': '5px', 'gridTemplateColumns': '140px 1fr', 'alignItems': 'center'}),
                            html.Div([
                                html.P("Education:"), 
                                dcc.Dropdown(
                                    id='education-dropdown',
                                    options=[
                                        {'label': 'Graduate School', 'value': 'Graduate School'},
                                        {'label': 'University', 'value': 'University'},
                                        {'label': 'High School', 'value': 'High School'},
                                        {'label': 'Others', 'value': 'Others'}
                                    ],
                                    value='Graduate School',
                                    placeholder="Select education level of the customer...",
                                ),
                            ], style={'display': 'grid', 'justifyContent': 'space-between', 'gap': '5px', 'gridTemplateColumns': '140px 1fr', 'alignItems': 'center'}),
                            html.Div([
                                html.P("Marital Status:"), 
                                dcc.Dropdown(
                                    id='marital-status-dropdown',
                                    options=[
                                        {'label': 'Married', 'value': 'Married'},
                                        {'label': 'Single', 'value': 'Single'},
                                        {'label': 'Others', 'value': 'Others'}
                                    ],
                                    placeholder="Select marital status of the customer...",
                                    value='Married',
                                )
                            ], style={'display': 'grid', 'justifyContent': 'space-between', 'gap': '5px', 'gridTemplateColumns': '140px 1fr', 'alignItems': 'center'}),
                        ], style={'padding': '20px', 'display': 'flex', 'flex-direction': 'column', 'justifyContent': 'space-between', 'gap': '5px'}),
                    ]),
                    html.Section([
                        html.H3("Crédito"),
                        # Sliders para Bill Amount, Pay Amount y Credit Limit
                        html.Div([
                            html.Div([
                                html.P("Credit Limit:"),    
                                dcc.Slider(
                                    id='credit-limit-slider',
                                    min=10_000,
                                    max=250_000,
                                    step=30_000,
                                    value=60_000,
                                    tooltip={"placement": "bottom", "always_visible": False}
                                )
                            ], style={'display': 'grid', 'justifyContent': 'space-between', 'gap': '5px', 'gridTemplateColumns': '100px 1fr'}),
                            html.Div([
                                html.P("Bill Amount:"),    
                                dcc.Slider(
                                    id='bill-amount-slider',
                                    min=0,
                                    max=100_000,
                                    step=10_000,
                                    value=50_000,
                                    tooltip={"placement": "bottom", "always_visible": False}
                                ),
                            ], style={'display': 'grid', 'justifyContent': 'space-between', 'gap': '5px', 'gridTemplateColumns': '100px 1fr'}),
                            html.Div([
                                html.P("Amount Paid:"),    
                                dcc.Slider(
                                    id='pay-amount-slider',
                                    min=0,
                                    max=10_000,
                                    step=1_000,
                                    value=8_000,
                                    tooltip={"placement": "bottom", "always_visible": False}
                                ),
                            ], style={'display': 'grid', 'justifyContent': 'space-between', 'gap': '5px', 'gridTemplateColumns': '100px 1fr'}),
                        ], style={'padding': '20px', 'display': 'flex', 'flex-direction': 'column', 'justifyContent': 'space-between', 'gap': '10px'}),
                    ]),
                    html.Section([
                        html.H3("Historial de Pagos"),
                        # Switches para los meses de abril a septiembre
                        html.Div([
                                daq.BooleanSwitch(
                                id=f'month-switch-{month}',
                                label=f'{month}',
                                labelPosition="top",
                                on=False
                            ) for month in ['April', 'May', 'June', 'July', 'August', 'September']
                        ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px', 'min-width': '80px'}),
                    ]),
                ], style={'width': '100%', 'padding': '40px 80px', 'display': 'flex', 'justifyContent': 'space-between', 'gap': '20px', 'flex-direction': 'column'}),
                html.Section([
                    html.Div([
                        dcc.Graph(id="gauge-model"),
                        html.H3("Predicción de Default", style={'textAlign': 'center'}),
                        html.P("Este modelo predice la probabilidad de incumplimiento en el próximo mes basado en la información ingresada. Utilice los controles para ajustar los valores y obtener una predicción."),
                    ], className="model-container"),
                ]),
            ], className="ml-container"),
        ], className="card main-models-container"),
    ], className="main-container"),
    html.Footer([
        html.P("Desarrollado por Haider Fonseca, Daniela Arenas y Sebastian Urrea"),
        html.P("Analítica Computacional para la Toma de Decisiones - Universidad de los Andes - 2024"),
    ], className="footer-container"),
], className="root-container")




if __name__ == '__main__':
    app.run_server(host = "localhost", port=8050, debug=True)
