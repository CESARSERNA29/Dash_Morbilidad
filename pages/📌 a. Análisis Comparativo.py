import streamlit as st
import pandas as pd 
import plotly.express as px

#config page layout to wide
st.set_page_config(page_title="Home",page_icon="",layout="wide")

st.success("**TABLA DE DISTRIBUCIÓN DE FRECUENCIAS**")

#load css
theme_plotly = None 

# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#load dataframe
# df=pd.read_csv("sales.csv")
df = pd.read_excel('Tasas_Morbilidad.xlsx', sheet_name='Hoja1')

# Convirtiendo la columna Anio a Categórica:
    # Opción 2: Convertir a categórica (más eficiente)
df['anio'] = df['anio'].astype(str)



# Para Mostrar el Dataset:
# with st.expander("🔎 VER CONJUNTO DE DATOS ORIGINAL"):
# showData=st.multiselect("",df.columns,default=["OrderDate","Region","City","Category","Product","Quantity","UnitPrice","TotalPrice"]) 
# st.dataframe(df[showData],use_container_width=True)

#side navigation 
st.sidebar.image("data/logo1.png")

#calculate a frequency
frequency=df.nombre_cat_edad.value_counts().sort_index()

#calculate percentage frequency %
percentage_frequency=frequency/len(df.nombre_cat_edad)*100

#calculate cumulative frequency
cumulative_frequency=frequency.cumsum()

#relative frequency
relative_frequency=frequency/len(df.nombre_cat_edad)

#cumulative relative frequency
cumulative_relative_frequency=relative_frequency.cumsum()

#create summarized table
summary_table=pd.DataFrame({
  'Freq.':frequency,
  '% Freq.':percentage_frequency,
  'Freq. Acum.':cumulative_frequency,
  'Freq. Relat.':relative_frequency,
  'Freq. Relat. Acum.':cumulative_relative_frequency

 }
)
showData=st.multiselect("### FILTRO",summary_table.columns,default=["Freq.","% Freq.","Freq. Acum.","Freq. Relat.","Freq. Relat. Acum."]) 
st.dataframe(summary_table[showData],use_container_width=True)

# df   nombre_cat_edad


##3

# 1.  BARRAS COMPARATIVAS:
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# === SIMULACIÓN DE DATOS DE EJEMPLO ===
# Puedes reemplazar esta parte por tu propio DataFrame real
import numpy as np
np.random.seed(42)

fechas = pd.date_range('2022-01-01', '2025-12-01', freq='MS')
departamentos = ['Antioquia', 'Cundinamarca', 'Valle', 'Santander']
grupos_edad = ['Infancia', 'Adolescencia', 'Adultez']
sexos = ['M', 'F']

data = []

for fecha in fechas:
    for dept in departamentos:
        for grupo in grupos_edad:
            for sexo in sexos:
                casos = np.random.randint(20, 300)
                data.append({
                    'Fecha': fecha,
                    'Departamento': dept,
                    'GrupoEdad': grupo,
                    'Sexo': sexo,
                    'Casos': casos
                })

df = pd.DataFrame(data)

# Extraer año-mes como texto tipo '2023-Jan'
# df['Periodo'] = df['Fecha'].dt.strftime('%Y-%b')
df['Periodo'] = df['anio']




# === INICIO APP DASH ===
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Frecuencia de Morbilidad por Departamento y Categoría de Edad", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Selecciona departamento:"),
        dcc.Dropdown(
            options=[{'label': d, 'value': d} for d in df['departamento'].unique()],
            value='Arauca',
            id='departamento-dropdown'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Selecciona categoría de edad:"),
        dcc.Dropdown(
            options=[{'label': g, 'value': g} for g in df['nombre_cat_edad'].unique()],
            value='a. Primera infancia',
            id='grupoedad-dropdown'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='barras-comparativas')
])


@app.callback(
    Output('barras-comparativas', 'figure'),
    Input('departamento-dropdown', 'value'),
    Input('grupoedad-dropdown', 'value')
)
def actualizar_grafico(departamento, nombre_cat_edad):
    df_filtrado = df[(df['Departamento'] == departamento) & (df['GrupoEdad'] == nombre_cat_edad)]

    df_agg = df_filtrado.groupby(['Periodo', 'sexo'])['Enfermedad_Evento'].count().reset_index()
    df_agg = df_agg.sort_values(by='Periodo')

    fig = px.bar(df_agg, 
                 x='Periodo', 
                 y='Enfermedad_Evento', 
                 color='sexo',
                 barmode='group',
                 labels={'Casos': 'Número de Casos', 'Periodo': 'Año'},
                 color_discrete_map={'Masculino': '#2A3180', 'Femenino': '#39A8E0'}
    )
    
    fig.update_layout(
        title=f'Casos de Morbilidad en {departamento} - {nombre_cat_edad}',
        title_x=0.5,
        xaxis_tickangle=-45,
        height=500,
        margin=dict(l=60, r=30, t=60, b=80)
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)


##3




# Display the histogram using Streamlit
#st.success("**GRÁFICO DE DISTRIBUCIÓN**")
#st.plotly_chart(fig, use_container_width=True)

