from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# --- 1. DATOS REALES DEL STRESS TEST A PARABANK ---
data = {
    'Metrica': ['/billpay (Exitosas)', '/billpay (Errores)', 'Total Peticiones'],
    'Cantidad': [1664, 0, 1664], 
    'Usuarios_Virtuales': [20, 20, 20],
    'Tiempo_Promedio_ms': [250, 0, 250] 
}
df = pd.DataFrame(data)

# --- 2. CREACIÓN DE GRÁFICOS CORREGIDOS ---
# Gráfico 1: Distribución de Peticiones (Pastel)
fig_status = px.pie(df[df['Metrica'] != 'Total Peticiones'], 
                    names='Metrica', 
                    values='Cantidad',
                    title='Distribución de Peticiones (Éxito vs Errores)',
                    color_discrete_sequence=px.colors.qualitative.Pastel)

# Gráfico 2: Tiempos de Respuesta Promedio (Barras)
fig_time = px.bar(df[df['Metrica'] != 'Total Peticiones'], 
                  x='Metrica', 
                  y='Tiempo_Promedio_ms',
                  title='Latencia Promedio por Estado (ms)',
                  labels={'Tiempo_Promedio_ms': 'Tiempo (ms)', 'Metrica': 'Estado'},
                  color='Metrica',
                  color_discrete_sequence=['#2ecc71', '#e74c3c'])

# --- 3. DISEÑO DEL DASHBOARD (LAYOUT CORREGIDO) ---
app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    
    # Encabezado Principal centrado y limpio
    html.H1("Dashboard de QA - Stress Testing ParaBank API", style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.P("Evidencia analítica de carga simulada con 20 VUs activos (k6).", style={'textAlign': 'center', 'color': '#7f8c8d'}),
    
    # Contenedor de las Gráficas alineadas (50% de ancho cada una)
    html.Div(style={'display': 'flex', 'flex-wrap': 'wrap', 'marginTop': '30px'}, children=[
        html.Div(dcc.Graph(figure=fig_status), style={'width': '50%'}),
        html.Div(dcc.Graph(figure=fig_time), style={'width': '50%'})
    ]),
    
    # Sección de Conclusiones de Ingeniería de QA
    html.H3("Resumen Ejecutivo de la Prueba", style={'marginTop': '40px'}),
    html.P("Nota: El endpoint /billpay soportó exitosamente la carga simultánea sin reportar caídas en el servidor. Todas las iteraciones se completaron bajo los parámetros esperados.", 
           style={'color': '#27ae60', 'fontWeight': 'bold'})
])

if __name__ == '__main__':
    app.run(debug=True)