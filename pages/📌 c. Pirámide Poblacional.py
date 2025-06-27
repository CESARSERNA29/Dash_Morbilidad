import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# =====================================
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Pirámide Poblacional", page_icon="👥", layout="wide")
st.header("Pirámide Poblacional por Departamento y Año")
st.markdown("##")

# Definición de la paleta de colores
P_Colores = {
    "Azul_cl": "#39A8E0",
    "Gris": "#9D9D9C",
    "Verde": "#009640",
    "Naranja": "#F28F1C",
    "Azul_os": "#2A3180",
    "Rojo": "#E5352B",
    "Morado": "#662681"
}

# =====================================
# FUNCIONES

def lectura_frec_dataframe(df0):
    """
    Procesa un DataFrame que ya está cargado en memoria
    """
    orden_rangos_edad = ['0 - 4','5 - 9','10 - 14','15 - 19','20 - 24','25 - 29' ,'30 - 34', '35 - 39',
                        '40 - 44', '45 - 49','50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74' ,'75 - 79', '80 - 84', '85 - 89']
    
    # Convert 'rango_edad' column to a categorical type with the specified order
    df0['rango_edad'] = pd.Categorical(df0['rango_edad'], categories=orden_rangos_edad, ordered=True)
    
    # Sort the DataFrame by the ordered 'rango_edad'
    df0 = df0.sort_values('rango_edad')
    
    # Se reestructura la base para disponer valores de H y M en columnas
    df = df0.pivot_table(index=['anio','region', 'departamento', 'rango_edad'],
                        columns='sexo', values='pob', observed=False).reset_index()
    df = df.rename_axis(None, axis=1)
    df['Total'] = df['Femenino'] + df['Masculino']
    df.rename(columns={'Femenino':'Mujeres','Masculino':'Hombres'}, inplace=True)
    
    return df

def graficar_piramide(df, dpto, año):
    """
    Genera una pirámide poblacional usando matplotlib
    """
    df_filtered = df.copy()

    if dpto != "Todos":
        df_filtered = df_filtered[df_filtered["departamento"] == dpto]

    if año != "Todos":
        df_filtered = df_filtered[df_filtered["anio"] == año]

    # Agrupar datos
    df_plot = df_filtered.groupby("rango_edad", observed=False)[["Hombres", "Mujeres"]].sum().reset_index()

    # Calculate percentages
    df_plot['Total_age_group'] = df_plot['Hombres'] + df_plot['Mujeres']
    total = df_plot['Total_age_group'].sum()
    df_plot['Hombres_pct'] = (df_plot['Hombres'] / total) * 100
    df_plot['Mujeres_pct'] = (df_plot['Mujeres'] / total) * 100

    # Calcular límites
    Lim_h = df_plot['Hombres_pct'].max()
    Lim_m = df_plot['Mujeres_pct'].max()
    Lim = max(Lim_h, Lim_m)
    Lim = np.floor(Lim) + 3

    # Recalcular columnas necesarias para la pirámide
    df_plot["Female_Left"] = 0
    df_plot["Female_Width"] = df_plot["Mujeres_pct"]
    df_plot["Male_Left"] = -df_plot["Hombres_pct"]
    df_plot["Male_Width"] = df_plot["Hombres_pct"]

    # Colores
    Col_M = P_Colores.get('Rojo')
    Col_H = P_Colores.get('Azul_os')
    
    # Create the figure
    plt.style.use("fivethirtyeight")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Crear las barras
    ax.barh(df_plot["rango_edad"], df_plot["Female_Width"], color=Col_M, label="Mujeres")
    ax.barh(df_plot["rango_edad"], df_plot["Male_Width"], left=df_plot["Male_Left"], color=Col_H, label="Hombres")

    # Agregar etiquetas de porcentaje
    for idx in range(len(df_plot)):
        ax.text(df_plot["Male_Left"].iloc[idx] - 0.1, idx, f"{df_plot['Hombres_pct'].iloc[idx]:.1f}%", 
                ha="right", va="center", fontsize=10, color=Col_H, fontweight="bold")
        ax.text(df_plot["Female_Width"].iloc[idx] + 0.1, idx, f"{df_plot['Mujeres_pct'].iloc[idx]:.1f}%", 
                ha="left", va="center", fontsize=10, color=Col_M, fontweight="bold")

    # Configuración del gráfico
    Lim_int = int(Lim)
    ax.set_xlim(-Lim, Lim)
    ax.set_xticks([])  # Omitir las etiquetas del eje x
    ax.set_ylabel("Rango de Edad", fontsize=14)

    # Título dinámico
    title = f"Pirámide Poblacional - {dpto}"
    if año != "Todos":
        title += f" ({año})"
    ax.set_title(title, fontsize=16, fontweight="bold", pad=20)

    ax.grid(False)
    ax.legend(loc='upper right', fontsize=12)
    
    plt.tight_layout()
    return fig

# =====================================
# CARGA DE DATOS

try:
    # Lectura de la base desde la carpeta
    df0 = pd.read_csv('Poblacion_prm.csv', sep=';')
    
    # Procesar datos
    orden_rangos_edad = ['0 - 4','5 - 9','10 - 14','15 - 19','20 - 24','25 - 29' ,'30 - 34', '35 - 39',
                        '40 - 44', '45 - 49','50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74' ,'75 - 79', '80 - 84', '85 - 89']
    
    df0['rango_edad'] = pd.Categorical(df0['rango_edad'], categories=orden_rangos_edad, ordered=True)
    df0 = df0.sort_values('rango_edad')
    
    # Usar la función para procesar los datos
    df = lectura_frec_dataframe(df0)
    
    # =====================================
    # CONTROLES DE STREAMLIT
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Dropdown de departamentos
        departamento = sorted(df["departamento"].unique().tolist())
        departamento.insert(0, "Todos")
        dpto_seleccionado = st.selectbox("Seleccione Departamento:", departamento)
    
    with col2:
        # Dropdown de año
        año = sorted(df["anio"].unique().tolist())
        año.insert(0, "Todos")
        año_seleccionado = st.selectbox("Seleccione Año:", año)
    
    # =====================================
    # GENERAR Y MOSTRAR GRÁFICO
    
    if st.button("Generar Pirámide") or True:  # Se actualiza automáticamente
        with st.spinner("Generando pirámide poblacional..."):
            fig = graficar_piramide(df, dpto_seleccionado, año_seleccionado)
            st.pyplot(fig)
    
    # =====================================