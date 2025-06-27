
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
df_GrupoEnfer = pd.read_excel('Tabla_Grafico_Cascada.xlsx', sheet_name='Hoja1')

# Cambiar round por parte entera
df_GrupoEnfer["TotCasos"] = df_GrupoEnfer["TotCasos"].astype(int)
df_GrupoEnfer["Tot_pob10"] = df_GrupoEnfer["Tot_pob10"].astype(int)

# =====================================
# FILTRO POR DEPARTAMENTO:
# Asumiendo que existe una columna 'departamento' en el DataFrame
# Si la columna tiene otro nombre, cambia 'departamento' por el nombre correcto

# Verificar si existe la columna departamento
if 'departamento' in df_GrupoEnfer.columns:
    departamentos_disponibles = ['Todos los Dptos'] + sorted(df_GrupoEnfer['departamento'].unique().tolist())
    
    # Crear el selectbox para filtrar por departamento
    departamento_seleccionado = st.selectbox(
        "Selecciona el Departamento:",
        options=departamentos_disponibles,
        index=0
    )
    
    # Filtrar los datos según la selección
    if departamento_seleccionado == 'Todos los Dptos':
        # Agregar datos por grupo para todos los departamentos
        df_filtrado = df_GrupoEnfer.groupby('grupo').agg({
            'TotCasos': 'sum',
            'Tot_pob10': 'sum'
        }).reset_index()
        titulo_grafico = "Todos los Departamentos"
    else:
        # Filtrar por departamento específico
        df_filtrado = df_GrupoEnfer[df_GrupoEnfer['departamento'] == departamento_seleccionado].copy()
        titulo_grafico = departamento_seleccionado
else:
    st.error("La columna 'departamento' no existe en el DataFrame. Por favor verifica el nombre correcto de la columna.")
    st.write("Columnas disponibles:", df_GrupoEnfer.columns.tolist())
    # Usar todos los datos si no existe la columna departamento
    df_filtrado = df_GrupoEnfer.copy()
    titulo_grafico = "Datos Generales"

# =====================================
# PREPARAR DATOS PARA EL GRÁFICO:
    
GrupoEnf = df_filtrado['grupo'].tolist()
y_list = df_filtrado['TotCasos'].tolist()
x_list = GrupoEnf
Total = 'Total'
x_list = GrupoEnf + ['Total']  # Esta línea agrega el valor de la variable total al final de la lista x_list.
total = int(sum(y_list))  # Cambiar round por int
y_list.append(total)  # Esta línea agrega el valor de la variable total al final de la lista y_list.

# Función para formato con punto de miles
def formato_miles(valor):
    return f"{valor:,.0f}".replace(",", ".")

# Preparar texto con formato miles y color HTML
text_list = []
for index, item in enumerate(y_list):
    texto = formato_miles(item)
    if index != 0 and index != len(y_list) - 1:
        texto = f'+{texto}'
    text_list.append(texto)


# Aplicar formato de color a las etiquetas
for index, item in enumerate(text_list):
    if item.startswith('+') and index != 0 and index != len(text_list) - 1:
        text_list[index] = f'<span style="color:#2ca02c">{item}</span>'
    elif item.startswith('-') and index != 0 and index != len(text_list) - 1:
        text_list[index] = f'<span style="color:#d62728">{item}</span>'
    if index == 0 or index == len(text_list) - 1:
        text_list[index] = f'<b>{item}</b>'



# Crear líneas de cuadrícula
dict_list = []
max_value = max(y_list) if y_list else 1200
step = max(200, int(max_value / 6))  # Ajustar el paso según el valor máximo
for i in range(0, int(max_value * 1.2), step):
    dict_list.append(dict(
            type="line",
            line=dict(
                 color="#666666",
                 dash="dot"
            ),
            x0=-0.5,
            y0=i,
            x1=len(x_list),
            y1=i,
            line_width=1,
            layer="below"))

# =====================================
# CREAR EL GRÁFICO WATERFALL:

# Método alternativo: Crear el gráfico con absolute para el total
# Modificar la lista de medidas para que el Total sea absolute
y_list_modified = y_list.copy()
measures = ["absolute"] + ["relative"] * (len(y_list) - 2) + ["absolute"]

# Para el total, usar el valor real en lugar del acumulado
y_list_modified[-1] = sum(y_list[:-1])  # El total real sin duplicar

fig = go.Figure(go.Waterfall(
    name = "prevalencia", orientation = "v",
    measure = measures,
    x = x_list,
    y = y_list_modified,
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

# Actualizar el layout del gráfico
fig.update_layout(
    title = {
        'text': f'<b>Waterfall Chart - {titulo_grafico}</b><br><span style="color:#666666">Prevalencia de Enfermedades Mentales de 2013 a 2014</span>',
        'x': 0.5,
        'xanchor': 'center'
    },
    showlegend = False,
    height=650,
    font={
        'family':'Open Sans, light',
        'color':'black',
        'size':14
    },
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_title="Casos",
    shapes=dict_list
)


# Fuente de las etiquetas:
fig.update_xaxes(tickangle=-45, tickfont=dict(family='Open Sans, light', color='black', size=14))
fig.update_yaxes(tickangle=0, tickfont=dict(family='Open Sans, light', color='black', size=14))

# =====================================
# MOSTRAR EL GRÁFICO:
st.plotly_chart(fig, use_container_width=True)

# =====================================
# INFORMACIÓN ADICIONAL (OPCIONAL):
if 'departamento' in df_GrupoEnfer.columns:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total de Casos",
            value=f"{total:,}".replace(",", ".")
        )
    
    with col2:
        if departamento_seleccionado != 'Todos los Dptos':
            st.metric(
                label="Departamento Seleccionado",
                value=departamento_seleccionado
            )
        else:
            st.metric(
                label="Departamentos Incluidos",
                value=len(df_GrupoEnfer['departamento'].unique())
            )
    
    with col3:
        st.metric(
            label="Grupos de Enfermedades",
            value=len(GrupoEnf)
        )