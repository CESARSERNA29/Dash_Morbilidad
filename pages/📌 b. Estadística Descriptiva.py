# Cargando las Librerías:
    
import streamlit as st
import pandas as pd
# from pandas_profiling import ProfileReport
import streamlit.components.v1 as components

import plotly.express as px
from streamlit_option_menu import option_menu
# from numerize.numerize import numerize
from numerize import numerize

import time
from streamlit_extras.metric_cards import style_metric_cards
# st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go
import plotly.graph_objects as go
# =====================================


# TITULO Y ESTILO DEL ENCABEZADO:
st.set_page_config(page_title="Dashboard ", page_icon="📈", layout="wide")  
st.header("Resumen Estadístico - Enfermedades por Subsectores")
st.markdown("##")
 
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)




# LLAMANDO EL DATAFRAME:
# Importando la tabla agregada con los resmúmenes de las variables:
df_subsectores = pd.read_excel('TablaMorbilidad_Subsectores.xlsx', sheet_name='Hoja1')

# df_subsectores = pd.read_excel(r'C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_Morbilidad_DESPLIEGUE\TablaMorbilidad_Subsectores.xlsx', sheet_name='Hoja1')



# Estructura jerárquica: País > Departamento > Enfermedad


#labels = df_subsectores['labels'].tolist()
#parents = df_subsectores['parents'].tolist()
#conteos = df_subsectores['conteos'].tolist()
#tasas = df_subsectores['tasas'].tolist()



labels = df_subsectores['labels']
parents = df_subsectores['parents']
conteos = df_subsectores['conteos']
tasas = df_subsectores['tasas']



# Etiquetas personalizadas con conteo y tasa
custom_labels = [ f"{l}<br>Casos: {v}<br>Tasa: {t:.1f}/100k" if v != 0 else l 
                 for l, v, t in zip(labels, conteos, tasas)
                 ]


# Sunburst plot
fig = go.Figure(go.Sunburst(
    labels=custom_labels,
    parents=parents,
    values=conteos,
    branchvalues="remainder"  # ahora los padres no necesitan tener suma directa
    ))


# Agregando el Titulo (Elegante)
fig.update_layout( title={
    "text": "Enfermedades más Frecuentes por Departamento",
    "y": 0.95, "x": 0.5, "xanchor": "center", "yanchor": "top", 
    "font": dict(size=34, family="Agency FB", color="black" ) #"darkblue"
    }, margin=dict(t=80, l=10, r=10, b=10))



#fig.show()


