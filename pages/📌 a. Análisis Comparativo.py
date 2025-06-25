import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

#config page layout to wide
st.set_page_config(page_title="Home",page_icon="",layout="wide")

st.success("**TABLA DE DISTRIBUCIÓN DE FRECUENCIAS**")

#load css
theme_plotly = None 

# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#load dataframe


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
    # Dropdown para departamento
    departamento_selected = st.selectbox(
        "Selecciona departamento:",
        options=df['departamento'].unique(),
        index=0
    )

with col2:
    # Dropdown para categoría de edad
    categoria_edad_selected = st.selectbox(
        "Selecciona categoría de edad:",
        options=df['nombre_cat_edad'].unique(),
        index=0
    )

# Función para actualizar gráfico
def crear_grafico(departamento, nombre_cat_edad):
    # Filtrar datos
    df_filtrado = df[
        (df['departamento'] == departamento) & 
        (df['nombre_cat_edad'] == nombre_cat_edad)
    ]
    
    if df_filtrado.empty:
        st.warning(f"No hay datos para {departamento} - {nombre_cat_edad}")
        return None
    
    # Agrupar datos
    # Nota: Asumiendo que tienes columnas 'sexo' y alguna columna para contar casos
    # Ajusta los nombres de columnas según tu dataset real
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
        
        # Crear gráfico
        fig = px.bar(
            df_agg, 
            x='Periodo', 
            y=y_column, 
            color='sexo',
            barmode='group',
            labels={y_column: 'Número de Casos', 'Periodo': 'Año'},
            color_discrete_map={'Masculino': '#2A3180', 'Femenino': '#39A8E0'},
            title=f'Casos de Morbilidad en {departamento} - {nombre_cat_edad}'
        )
        
        fig.update_layout(
            title_x=0.5,
            xaxis_tickangle=-45,
            height=500,
            margin=dict(l=60, r=30, t=60, b=80)
        )
        
        return fig
    else:
        # Si no hay columna sexo, hacer gráfico simple
        df_agg = df_filtrado.groupby('Periodo').size().reset_index(name='Casos')
        
        fig = px.bar(
            df_agg,
            x='Periodo',
            y='Casos',
            title=f'Casos de Morbilidad en {departamento} - {nombre_cat_edad}',
            color_discrete_sequence=['#2A3180']
        )
        
        fig.update_layout(
            title_x=0.5,
            xaxis_tickangle=-45,
            height=500
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

