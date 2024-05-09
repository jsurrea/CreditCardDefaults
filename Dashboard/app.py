from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from os import path

app = Dash(__name__, external_stylesheets = [path.join('assets', 'styles.css')])
app.title = "CREDIT CARD DEFAULTS"


df = pd.read_csv(path.join('assets', 'data.csv'))
df["productivity_difference"] = df["actual_productivity"] - df["targeted_productivity"]


def create_boxplot_figure():
    filtered_df = df[df.department == "sweing"].copy()
    # Crear una nueva columna categorica dividiendo según el valor de incentive
    filtered_df["incentive_category"] = pd.cut(filtered_df.incentive, bins=[-1, 20, 40, 60, 80, 100, 120], labels=["0-20", "20-40", "40-60", "60-80", "80-100", "100-120"])
    fig = px.box(filtered_df, x="incentive_category", y="actual_productivity", points="all", 
                  category_orders={"incentive_category": ["0-20", "20-40", "40-60", "60-80", "80-100", "100-120"]})
    fig.update_layout(font=dict(color='#FCFDFE'), xaxis=dict(gridcolor='#373A40', title_text="Incentivo"), yaxis=dict(gridcolor='#373A40', title_text="Productividad"))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def create_sunburst_figure():
    pivot_df = df.pivot_table(index=['department', 'team'], values=['actual_productivity', 'productivity_difference'], aggfunc='mean').reset_index()
    pivot_df.team = pivot_df.team.apply(lambda x: f"Equipo {x}")
    fig = px.sunburst(pivot_df, path=['department', 'team'], values='actual_productivity', color="productivity_difference", color_continuous_scale='Plotly3_r')
    fig.update_layout(coloraxis_colorbar=dict(yanchor="bottom", y=-0.1, xanchor="center", x=0.5, orientation='h', title='', tickfont={"color": '#FCFDFE'}))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def create_scatter_figure():
    filtered_df = df[df.department == "finishing"].copy()
    fig = px.scatter(filtered_df, x="smv", y="actual_productivity", trendline="ols")
    fig.update_layout(font=dict(color='#FCFDFE'), xaxis=dict(gridcolor='#373A40', title_text="Tiempo asignado a la tarea"), yaxis=dict(gridcolor='#373A40', title_text="Productividad"))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin={"r":0,"t":0,"l":0,"b":0})
    return fig


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



app.layout = html.Div([
    html.Header([
        html.Section([
            html.H1("CREDIT CARD DEFAULTS"),
            html.P("Data Analysis for the Manufacturing Industry"),
        ], className="header-title"),
        html.Section([
            html.Img(src=path.join('assets', 'logo.png'), alt="Uniandes Logo"),
        ], className="header-logo"),
    ], className="header-container"),
    html.Main([
        html.Section([
            html.Div([
                html.H2("Incentivos en Sweing Department"),
                dcc.Graph(id="graph-boxplot", figure=create_boxplot_figure()),
                html.P("Este gráfico muestra la distribución de la productividad real en el departamento de Sweing. Cada caja representa un rango de incentivos. A mayor incentivo, mayor productividad."),
            ], className="card"),
            html.Div([
                html.H2("Equipos más productivos"),
                dcc.Graph(id="graph-sunburst", figure=create_sunburst_figure()),
                html.P("Este gráfico muestra la diferencia entre la productividad real y la productividad esperada de cada equipo."),
            ], className="card"),
            html.Div([
                html.H2("Tiempo extra en Finishing Department"),
                dcc.Graph(id="graph-scatter", figure=create_scatter_figure()),
                html.P("Este gráfico muestra la relación entre el tiempo asignado a la tarea y la productividad real en el departamento de Finishing."),
            ], className="card"),
        ], className="main-graphs"),
        html.Section([
            html.H2("Modelos de Machine Learning"),
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
