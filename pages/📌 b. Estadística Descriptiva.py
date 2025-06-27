


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
st.header("Resumen Estadístico - Enfermedades por Subsectores")
st.markdown("##")
 
# Cargar CSS si existe el archivo
try:
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Archivo style.css no encontrado. Continuando sin estilos personalizados.")

# LLAMANDO EL DATAFRAME:
try:
    # Importando la tabla agregada con los resúmenes de las variables:
    df_subsectores = pd.read_excel('TablaMorbilidad_Subsectores.xlsx', sheet_name='Hoja1')
    
    # Estructura jerárquica: País > Departamento > Enfermedad
    labels = df_subsectores['labels'].tolist()
    parents = df_subsectores['parents'].tolist()
    conteos = df_subsectores['conteos'].tolist()
    tasas = df_subsectores['tasas'].tolist()
    
    # Etiquetas personalizadas con conteo y tasa
    custom_labels = [f"{l}<br>Casos: {v}<br>Tasa: {t:.1f}/100k" if v != 0 else l 
                     for l, v, t in zip(labels, conteos, tasas)]
    
    # Sunburst plot
    fig = go.Figure(go.Sunburst(
        labels=custom_labels,
        parents=parents,
        values=conteos,
        branchvalues="remainder"  # ahora los padres no necesitan tener suma directa
    ))
    
    # Agregando el Titulo (Elegante)
    fig.update_layout(
        title={
            "text": "Enfermedades más Frecuentes por Departamento",
            "y": 0.95, 
            "x": 0.5, 
            "xanchor": "center", 
            "yanchor": "top", 
            "font": dict(size=34, family="Agency FB", color="black")
        }, 
        margin=dict(t=80, l=10, r=10, b=10)
    )
    
    # ¡AQUÍ ESTÁ LA LÍNEA QUE FALTABA!
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
except FileNotFoundError:
    st.error("Archivo 'TablaMorbilidad_Subsectores.xlsx' no encontrado. Verifica que el archivo esté en el directorio correcto.")
except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    
    # Mostrar datos de ejemplo para verificar que el código funciona
    st.info("Mostrando gráfico de ejemplo:")
    
    # Datos de ejemplo
    sample_data = {
        'labels': ['Colombia', 'Bogotá', 'Antioquia', 'Valle', 'Diabetes', 'Hipertensión', 'Asma'],
        'parents': ['', 'Colombia', 'Colombia', 'Colombia', 'Bogotá', 'Antioquia', 'Valle'],
        'conteos': [0, 0, 0, 0, 1500, 2000, 800],
        'tasas': [0, 0, 0, 0, 15.5, 25.2, 12.8]
    }
    
    labels_sample = sample_data['labels']
    parents_sample = sample_data['parents']
    conteos_sample = sample_data['conteos']
    tasas_sample = sample_data['tasas']
    
    custom_labels_sample = [f"{l}<br>Casos: {v}<br>Tasa: {t:.1f}/100k" if v != 0 else l 
                           for l, v, t in zip(labels_sample, conteos_sample, tasas_sample)]
    
    fig_sample = go.Figure(go.Sunburst(
        labels=custom_labels_sample,
        parents=parents_sample,
        values=conteos_sample,
        branchvalues="remainder"
    ))
    
    fig_sample.update_layout(
        title={
            "text": "Ejemplo - Enfermedades más Frecuentes por Departamento",
            "y": 0.95, 
            "x": 0.5, 
            "xanchor": "center", 
            "yanchor": "top", 
            "font": dict(size=24, family="Arial", color="black")
        }, 
        margin=dict(t=80, l=10, r=10, b=10)
    )
    
    st.plotly_chart(fig_sample, use_container_width=True)


















