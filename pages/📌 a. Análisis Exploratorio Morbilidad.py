




# Cargando las Librerías:
# ======================

import streamlit as st
import pandas as pd
# from pandas_profiling import ProfileReport
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
# from numerize.numerize import numerize
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
# st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go
# ----------------------------------------------------------



# Descomenta esta línea si usas MySQL:
# from query import *

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
#st.header("MORBILIDAD:  Tratamiento Estadístico, KPI y Tendencias")

st.markdown("""
        <h3 style='text-align: center; color: #333333;'>MORBILIDAD:  Tratamiento Estadístico, KPI y Tendencias </h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="text-align: justify; font-size: 18px; color: #444444;">
        La morbilidad se refiere a la frecuencia o proporción de personas que presentan una enfermedad o condición específica dentro de una población determinada. Desde un enfoque estadístico, el análisis de la morbilidad permite identificar patrones, tendencias y distribuciones geográficas o demográficas de las enfermedades, lo cual es clave para la planificación en salud pública.  
        Mediante indicadores como el número de casos absolutos, la tasa de morbilidad (por cada 10.000 o 100.000 habitantes) o la prevalencia y la incidencia, se pueden evaluar los grupos más afectados, detectar zonas de mayor vulnerabilidad y priorizar recursos. Estas métricas también permiten comparar el comportamiento de enfermedades a lo largo del tiempo o entre regiones, facilitando la toma de decisiones basadas en evidencia.  
        El análisis estadístico de la morbilidad es, por tanto, una herramienta fundamental para monitorear el estado de salud de una población y diseñar intervenciones efectivas.
        </div>
    """, unsafe_allow_html=True)

st.markdown("##")






# Todos los gráficos se personalizan usando CSS , no Streamlit. 
theme_plotly = None 


# Cargar los estilo css:
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Descomenta estas dos líneas si obtienes datos de MySQL:
# result = view_all_data()
# df=pd.DataFrame(result,columns=["Policy","Expiry","Location","State","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])

# cargar archivo Excel | comente esta línea cuando obtenga datos de MySQL:

# df = pd.read_excel("C:/Users/cesar/Downloads/TABLERO_STREAMLIT_DASHBOARD/DASHBOARD_Morbilidad_DESPLIEGUE/Tasas_Morbilidad.xlsx", sheet_name='Hoja1')
df = pd.read_excel('Tasas_Morbilidad_25MB.xlsx', sheet_name='Hoja1')

# Convirtiendo la columna Anio a Categórica:
    # Opción 2: Convertir a categórica (más eficiente)
df['anio'] = df['anio'].astype(str)
    
# ======================================================================



def safe_numerize(value):
    """Convierte un valor a formato numerize de forma segura"""
    try:
        # Manejar valores None o vacíos
        if value is None:
            return "0"
        
        # Convertir a string y limpiar
        str_value = str(value).strip().lower()
        if str_value in ['', 'nan', 'none', 'null']:
            return "0"
        
        # Convertir a número
        num_value = float(value)
        
        # Verificar si es NaN
        if num_value != num_value:  # NaN check sin pandas
            return "0"
        
        # Aplicar numerize
        return numerize(int(num_value))
        
    except (ValueError, TypeError, AttributeError):
        return "0"


# =============================================

# 📍 📎 🗺️ 🎯 🔗 ⚓ 🏠 🏢 🏭 🏬
# 🏷️ 🔖 📋 📝 📄 📊 📈 📉 🗂️ 📁
# 🔧 🔨 ⚙️ 🛠️ ⚡ 🔧 🗝️ 🔑 🎛️ ⚖️
#  ⚠️ ❗ ❓ ✅ ❌ 🟢 🔴 🟡 🟠 🔵
# 👆 👇 👈 👉 ↗️ ↘️ ↙️ ↖️ ⬆️ ⬇️ ⬅️ ➡️
# 💡 🔍 🎲 🎯 🎪 🎨 🎭 🎪 🎊 🎉
# 📊 📈 📉 💹 📋 🗃️ 🗄️ 💾 💿 📀
# 🏥 ⚕️ 💊 🩺 🧬 🦠 💉 🧪 🔬 📱

# =============================================



with st.expander("👉 Mostrar Filtros", expanded=False):
    Departamento = st.multiselect(
        "Selecciona Departamento",
        options=df["departamento"].unique(),
        default=df["departamento"].unique(),
    )

    Municipio = st.multiselect(
        "Selecciona Municipio",
        options=df["municipio"].unique(),
        default=df["municipio"].unique(),
    )

    Grupo = st.multiselect(
        "Selecciona el Grupo de Enfermedad",
        options=df["grupo"].unique(),
        default=df["grupo"].unique(),
    )








df_selection=df.query(
    "departamento==@Departamento & municipio==@Municipio & grupo ==@Grupo"
)



# Esta función realiza análisis descriptivos básicos como media, moda, suma, etc.
def Home():
    with st.expander("Ver el Conjunto de Datos en Excel"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=["anio", "sexo", "nombre_cat_edad", "departamento", "municipio", "componente", "capitulo", "grupo", "Enfermedad_Evento", "pob10", "tasa_morb", "Tot_Eventos"])
        st.dataframe(df_selection[showData],use_container_width=True)
    # calcular los análisis:
    total_investment = float(pd.Series(df_selection['Tot_Eventos']).sum())
    investment_mode1 = float(pd.Series(df_selection['departamento']).nunique())
    investment_mode2 = float(pd.Series(df_selection['municipio']).nunique())
    investment_median= float(pd.Series(df_selection['Enfermedad_Evento']).nunique()) 


    total1,total2,total3,total4,total5=st.columns(5,gap='small')
    with total1:
        st.info('Tot. Eventos',icon="🎯")
        st.metric(label="Tot. Casos", value=f"{total_investment:,.0f}".replace(",", "."))
    with total2:
        st.info('Tot. Dptos.',icon="🎯")
        st.metric(label="Tot. Dptos.",value=f"{investment_mode1:,.0f}")

    with total3:
        st.info('Tot. Municip.',icon="🎯")
        st.metric(label="Tot. Municip.",value=f"{investment_mode2:,.0f}")

    with total4:
        st.info('Tot. Grupo',icon="🎯")
        st.metric(label="Tot. Grupo",value=f"{investment_median:,.0f}")
        

    #variable distribution Histogram
    with st.expander("Distribución de Frecuencias - Variables Cuantitativas"):
     df.hist(figsize=(16,8),color='#898784', zorder=2, rwidth=0.9,legend = ['tasa_morb']);
     st.pyplot()

#graphs
def graphs():
    investment_by_business_type=(
        df_selection.groupby(by=["anio"]).count()[["tasa_morb"]].sort_values(by="tasa_morb")
    )
    
    # Convertir el índice en una columna
    investment_by_business_type = investment_by_business_type.reset_index()
    
    # CORRECCIÓN: Usar 'tasa_morb' como y, no 'index'
    fig_investment = px.bar(
        investment_by_business_type,
        x="anio", 
        y="tasa_morb",  # ← Esta es la columna correcta
        title="Análisis de Morbilidad por Año", 
        color_discrete_sequence=["#0083B8"] * len(investment_by_business_type),
        template="plotly_white"
    )
    
    fig_investment.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Mostrar la cuadrícula del eje y y establecer su color  
     paper_bgcolor='rgba(0, 0, 0, 0)',  # Establecer el color del fondo  en transparente
     xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Mostrar la cuadrícula del eje x y establecer su color
     )
    
    # gráfico de regresión lineal simple de inversión por nombre_cat_edad
    investment_state = df_selection.groupby(by=["nombre_cat_edad"]).count()[["tasa_morb"]]
    
    investment_state_reset = investment_state.reset_index()    
    
    fig_state = px.line(investment_state_reset, 
                   x="nombre_cat_edad",  # Categorías de edad en el eje X
                   y="tasa_morb",        # Conteo/tasa en el eje Y
                   orientation="v", 
                   title="<b> TASA DE MORBILIDAD POR CATEGORÍA DE EDADES </b>",
                   color_discrete_sequence=["#0083b8"]*len(investment_state_reset), 
                   template="plotly_white",
                   
    )
    
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"), 
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False))
        )
    
    left,right,center=st.columns(3)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
    
    with center:
      #pie chart
      fig = px.pie(df_selection, values='tasa_morb', names='departamento', title="<b> TASA  MORBILIDAD POR DEPARTAMENTO </b>")
      fig.update_layout(legend_title="Dptos.", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


# función para mostrar las ganancias actuales frente al objetivo esperado
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=3000000000
    current=df_selection["Investment"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader("Objetivo cumplido !")
    else:
     st.write("tienes ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
     for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1,text=" Objetivo Porcentual")

#menu bar
def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Menú Principal",
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    Home()
    graphs()
 if selected=="Progress":
    #st.subheader(f"Page: {selected}")
    Progressbar()
    graphs()


sideBar()
#st.sidebar.image("data/Logo_UNILLANOS.png",caption="")      # LOGO
st.sidebar.image("Logo_UNILLANOS.png",caption="")            # LOGO



st.subheader('Seleccione Atributos para Observar Tendencias de Distrib. Por Cuartiles',)
#feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
feature_y = st.selectbox('Seleccionar función para (Y) Datos cuantitativos', df_selection.select_dtypes("number").columns)
fig2 = go.Figure(
    data=[go.Box(x=df['grupo'], y=df[feature_y])],
    layout=go.Layout(
        title=go.layout.Title(text="Distribución Numérica, por Grupo de Enfermedades"),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        font=dict(color='#cecdcd'),  # Set text color to black
    )
)
# Display the Plotly figure using Streamlit
st.plotly_chart(fig2,use_container_width=True)



#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

















st.markdown("##")
st.markdown("##")

st.markdown("##")







import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Morbilidad",
    page_icon="📊",
    layout="wide"
)

# Cargar dataframe
@st.cache_data
def load_data():
    df = pd.read_excel('Tasas_Morbilidad.xlsx', sheet_name='Hoja1')
    # Convertir año a categórica
    df['anio'] = df['anio'].astype(str)
    # Crear columna Periodo
    df['Periodo'] = df['anio']
    return df

df = load_data()

# Sidebar con logo
st.sidebar.image("data/logo1.png")

# Título principal
st.title("📊 Análisis Comparativo de Morbilidad")

# === SECCIÓN 1: TABLA DE FRECUENCIAS ===
st.header("📈 Tabla de Frecuencias por Categoría de Edad")

# Calcular frecuencias
frequency = df.nombre_cat_edad.value_counts().sort_index()
percentage_frequency = frequency / len(df.nombre_cat_edad) * 100
cumulative_frequency = frequency.cumsum()
relative_frequency = frequency / len(df.nombre_cat_edad)
cumulative_relative_frequency = relative_frequency.cumsum()

# Crear tabla resumen
summary_table = pd.DataFrame({
    'Freq.': frequency,
    '% Freq.': percentage_frequency,
    'Freq. Acum.': cumulative_frequency,
    'Freq. Relat.': relative_frequency,
    'Freq. Relat. Acum.': cumulative_relative_frequency
})

# Selector de columnas para mostrar
showData = st.multiselect(
    "### FILTRO - Selecciona las columnas a mostrar:",
    summary_table.columns.tolist(),
    default=summary_table.columns.tolist()
)

if showData:
    st.dataframe(summary_table[showData], use_container_width=True)
else:
    st.warning("Selecciona al menos una columna para mostrar")

# === SECCIÓN 2: GRÁFICO INTERACTIVO ===
st.header("📊 Frecuencia de Morbilidad por Departamento y Categoría de Edad")

# Crear columnas para los filtros
col1, col2 = st.columns(2)

with col1:
    # Dropdown para departamento (agregando opción "Todos")
    departamentos_options = ['Todos'] + list(df['departamento'].unique())
    departamento_selected = st.selectbox(
        "Selecciona departamento:",
        options=departamentos_options,
        index=0
    )

with col2:
    # Dropdown para categoría de edad (agregando opción "Todas")
    categorias_options = ['Todas'] + list(df['nombre_cat_edad'].unique())
    categoria_edad_selected = st.selectbox(
        "Selecciona categoría de edad:",
        options=categorias_options,
        index=0
    )

# Función para actualizar gráfico
def crear_grafico(departamento, nombre_cat_edad):
    # Filtrar datos según las selecciones
    df_filtrado = df.copy()
    
    # Aplicar filtro de departamento
    if departamento != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['departamento'] == departamento]
    
    # Aplicar filtro de categoría de edad
    if nombre_cat_edad != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['nombre_cat_edad'] == nombre_cat_edad]
    
    if df_filtrado.empty:
        st.warning(f"No hay datos para {departamento} - {nombre_cat_edad}")
        return None
    
    # Determinar título del gráfico
    if departamento == 'Todos' and nombre_cat_edad == 'Todas':
        titulo = 'Casos de Morbilidad - Todos los Departamentos y Categorías de Edad'
    elif departamento == 'Todos':
        titulo = f'Casos de Morbilidad - Todos los Departamentos - {nombre_cat_edad}'
    elif nombre_cat_edad == 'Todas':
        titulo = f'Casos de Morbilidad en {departamento} - Todas las Categorías de Edad'
    else:
        titulo = f'Casos de Morbilidad en {departamento} - {nombre_cat_edad}'
    
    # Agrupar datos
    if 'sexo' in df_filtrado.columns:
        # Si tienes columna de casos específica, úsala; si no, cuenta las filas
        if 'Enfermedad_Evento' in df_filtrado.columns:
            df_agg = df_filtrado.groupby(['Periodo', 'sexo'])['Enfermedad_Evento'].count().reset_index()
            y_column = 'Enfermedad_Evento'
        else:
            # Contar filas por grupo
            df_agg = df_filtrado.groupby(['Periodo', 'sexo']).size().reset_index(name='Casos')
            y_column = 'Casos'
        
        df_agg = df_agg.sort_values(by='Periodo')
        
        # Crear gráfico con sexo
        fig = px.bar(
            df_agg, 
            x='Periodo', 
            y=y_column, 
            color='sexo',
            barmode='group',
            labels={y_column: 'Número de Casos', 'Periodo': 'Año'},
            color_discrete_map={'Masculino': '#2A3180', 'Femenino': '#39A8E0'},
            title=titulo
        )
        
    else:
        # Si no hay columna sexo, hacer gráfico simple
        if 'Enfermedad_Evento' in df_filtrado.columns:
            df_agg = df_filtrado.groupby('Periodo')['Enfermedad_Evento'].count().reset_index()
            y_column = 'Enfermedad_Evento'
        else:
            df_agg = df_filtrado.groupby('Periodo').size().reset_index(name='Casos')
            y_column = 'Casos'
        
        fig = px.bar(
            df_agg,
            x='Periodo',
            y=y_column,
            title=titulo,
            color_discrete_sequence=['#2A3180'],
            labels={y_column: 'Número de Casos', 'Periodo': 'Año'}
        )
    
    fig.update_layout(
        title_x=0.5,
        xaxis_tickangle=-45,
        height=500,
        margin=dict(l=60, r=30, t=60, b=80)
    )
    
    return fig

# Crear y mostrar gráfico
fig = crear_grafico(departamento_selected, categoria_edad_selected)

if fig:
    st.plotly_chart(fig, use_container_width=True)

# === SECCIÓN 3: INFORMACIÓN ADICIONAL ===
st.header("ℹ️ Información del Dataset")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Registros", f"{len(df):,}")

with col2:
    st.metric("Departamentos", f"{df['departamento'].nunique()}")

with col3:
    st.metric("Categorías de Edad", f"{df['nombre_cat_edad'].nunique()}")

# Mostrar vista previa del dataset
with st.expander("🔎 Ver Vista Previa del Dataset"):
    st.dataframe(df.head(), use_container_width=True)

# Información sobre las columnas
with st.expander("📋 Información de Columnas"):
    st.write("**Columnas disponibles en el dataset:**")
    for i, col in enumerate(df.columns, 1):
        st.write(f"{i}. **{col}** - Tipo: {df[col].dtype}")

##3




# Display the histogram using Streamlit
#st.success("**GRÁFICO DE DISTRIBUCIÓN**")
#st.plotly_chart(fig, use_container_width=True)

