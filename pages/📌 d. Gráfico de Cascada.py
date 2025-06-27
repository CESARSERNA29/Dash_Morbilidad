
# Cargando las Librerías:
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
import plotly.graph_objects as go

# =====================================
# TITULO Y ESTILO DEL ENCABEZADO:
st.set_page_config(page_title="Dashboard ", page_icon="📈", layout="wide")  
st.header("Resumen del Total de Casos por cada Grupo de Eventos")
st.markdown("##")

# Cargar La base:  Tabla_Grafico_Cascada
try:
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Archivo style.css no encontrado. Continuando sin estilos personalizados.")

# LLAMANDO EL DATAFRAME:

# Importando la tabla agregada con los resúmenes de las variables:
df_GrupoEnfer = pd.read_excel(r'C:/Users/cesar/Downloads/TABLERO_STREAMLIT_DASHBOARD/DASHBOARD_Morbilidad_DESPLIEGUE/Tabla_Grafico_Cascada.xlsx', sheet_name='Hoja1')
#df_GrupoEnfer = pd.read_excel('Tabla_Grafico_Cascada.xlsx', sheet_name='Hoja1')

# Cambiar round por parte entera
df_GrupoEnfer["TotCasos"] = df_GrupoEnfer["TotCasos"].astype(int)
df_GrupoEnfer["Tot_pob10"] = df_GrupoEnfer["Tot_pob10"].astype(int)
    
GrupoEnf = df_GrupoEnfer['grupo'].tolist()
y_list = df_GrupoEnfer['TotCasos'].tolist()
x_list = GrupoEnf
Total = 'Total'
x_list = GrupoEnf + ['Total']  # Esta línea agrega el valor de la variable total al final de la lista x_list.
total = int(sum(y_list))  # Cambiar round por int
y_list.append(total)  # Esta línea agrega el valor de la variable total al final de la lista y_list.

text_list = []
for index, item in enumerate(y_list):
    if item > 0 and index != 0 and index != len(y_list) - 1:
        text_list.append(f'+{str(y_list[index])}')
    else:
        text_list.append(str(y_list[index]))
for index, item in enumerate(text_list):
    if item[0] == '+' and index != 0 and index != len(text_list) - 1:
        text_list[index] = '<span style="color:#2ca02c">' + text_list[index] + '</span>'
    elif item[0] == '-' and index != 0 and index != len(text_list) - 1:
        text_list[index] = '<span style="color:#d62728">' + text_list[index] + '</span>'
    if index == 0 or index == len(text_list) - 1:
        text_list[index] = '<b>' + text_list[index] + '</b>'

dict_list = []
for i in range(0, 1200, 200):
    dict_list.append(dict(
            type="line",
            line=dict(
                 color="#666666",
                 dash="dot"
            ),
            x0=-0.5,
            y0=i,
            x1=6,
            y1=i,
            line_width=1,
            layer="below"))

fig = go.Figure(go.Waterfall(
    name = "e-commerce", orientation = "v",
    measure = ["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
    x = x_list,
    y = y_list,
    text = text_list,
    textposition = "outside",
    connector = {"line":{"color":'rgba(0,0,0,0)'}},
    increasing = {"marker":{"color":"#2ca02c"}},
    decreasing = {"marker":{"color":"#d62728"}},
    totals={'marker':{"color":"#9467bd"}},
    textfont={"family":"Open Sans, light",
              "color":"black"
             }
))

fig.update_layout(
    title =
        {'text':'<b>Waterfall Chart</b><br><span style="color:#666666">Prevalencia de Enfermedades Mentales de 2013 a 2014</span>'},
    showlegend = False,
    height=650,
    font={
        'family':'Open Sans, light',
        'color':'black',
        'size':14     # Tamaño de las cifras
    },
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_title="Casos",
    shapes=dict_list
)

# Fuente de las etiquetas:
fig.update_xaxes(tickangle=-45, tickfont=dict(family='Open Sans, light', color='black', size=14))
fig.update_yaxes(tickangle=0, tickfont=dict(family='Open Sans, light', color='black', size=14))

# CAMBIO PRINCIPAL: Usar st.plotly_chart() en lugar de fig.show()
st.plotly_chart(fig, use_container_width=True)