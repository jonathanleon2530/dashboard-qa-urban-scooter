from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# --- DATOS DE TUS PRUEBAS (Simulando resultados de Urban Scooter) ---
data = {
    'Caso de Prueba': ['Login', 'Registro', 'Pago Tarjeta', 'Mapa GPS', 'Cerrar Sesión'],
    'Estado': ['Pasó', 'Falló', 'Pasó', 'Error 500', 'Pasó'],
    'Tiempo_ms': [120, 450, 890, 2500, 105], # Útil para medir performance
    'Severidad': ['N/A', 'Alta', 'N/A', 'Crítica', 'N/A']
}
df = pd.DataFrame(data)

# Gráfico 1: Estado de las pruebas (Pastel)
fig_status = px.pie(df, names='Estado', title='Estado General de Ejecución',
                    color_discrete_sequence=px.colors.qualitative.Pastel)

# Gráfico 2: Tiempos de respuesta (Barras)
fig_time = px.bar(df, x='Caso de Prueba', y='Tiempo_ms', color='Estado',
                  title='Latencia por Endpoint (ms)',
                  labels={'Tiempo_ms': 'Tiempo (ms)'})

# --- DISEÑO DEL DASHBOARD ---
app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1("Dashboard de QA - Proyecto Urban Scooter", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div(style={'display': 'flex', 'flex-wrap': 'wrap'}, children=[
        html.Div(dcc.Graph(figure=fig_status), style={'width': '50%'}),
        html.Div(dcc.Graph(figure=fig_time), style={'width': '50%'})
    ]),
    
    html.H3("Detalle de Defectos Críticos"),
    html.P("Nota: El endpoint de Mapa GPS está devolviendo Error 500 bajo carga (visto en Postman).", 
           style={'color': 'red', 'fontWeight': 'bold'})
])

if __name__ == '__main__':
    app.run(debug=True)