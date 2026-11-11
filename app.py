import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import io
from fpdf import FPDF

# Configuracion basica de la pagina
st.set_page_config(
    page_title="ColdSense IoT - Monitoreo de Cadena de Frio",
    layout="wide"
)

# Generamos datos ficticios de 24 horas para simular las lecturas de los sensores
@st.cache_data
def generar_datos_historicos():
    np.random.seed(42)
    fechas = [datetime.now() - timedelta(minutes=10 * i) for i in range(144)]
    fechas.reverse()

    # Temperatura normal alrededor de 4 C con un pico simulado para probar la alerta
    temp_camara1 = np.random.normal(loc=4.0, scale=1.2, size=144)
    temp_camara1[50:55] += 5.5

    humedad_camara1 = np.random.normal(loc=60.0, scale=3.0, size=144)
    puerta_estado = [1 if t > 7.0 else 0 for t in temp_camara1]

    return pd.DataFrame({
        "Timestamp": fechas,
        "Nodo_ID": "Nodo-CamaraFria-01",
        "Temperatura_C": np.round(temp_camara1, 2),
        "Humedad_Pct": np.round(humedad_camara1, 2),
        "Puerta_Abierta": puerta_estado
    })

df_iot = generar_datos_historicos()

# Menu lateral con controles de rol y limites de temperatura
st.sidebar.title("ColdSense IoT")
st.sidebar.caption("Sistema de Monitoreo Ambiental y Alertas")

rol = st.sidebar.selectbox(
    "Seleccionar Rol de Usuario",
    ["Administrador", "Supervisor / Calidad", "Tecnico de Mantenimiento"]
)

st.sidebar.divider()
st.sidebar.subheader("Configuracion de Umbrales")
temp_min = st.sidebar.slider("Temperatura Minima Permitida (C)", -5.0, 5.0, 2.0)
temp_max = st.sidebar.slider("Temperatura Maxima Permitida (C)", 0.0, 15.0, 8.0)

# Encabezado principal
st.title("Panel de Monitoreo en Tiempo Real")
st.markdown(f"**Usuario en sesion:** `{rol}` | **Ubicacion:** Almacen Central de Medicamentos")

# Tomamos la ultima lectura recibida para mostrar el estado actual
ultima_lectura = df_iot.iloc[-1]
temp_actual = ultima_lectura["Temperatura_C"]
hum_actual = ultima_lectura["Humedad_Pct"]
puerta_actual = "ABIERTA" if ultima_lectura["Puerta_Abierta"] == 1 else "CERRADA"

# Validamos si la temperatura actual sobrepasa los umbrales elegidos
if temp_actual > temp_max or temp_actual < temp_min:
    estado_sistema = "CRITICO"
else:
    estado_sistema = "NORMAL"

# Tarjetas numericas superiores (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperatura Actual", f"{temp_actual} C", delta=f"{round(temp_actual - 4.0, 2)} C vs Media")
col2.metric("Humedad Relativa", f"{hum_actual} %")
col3.metric("Estado de Puerta", puerta_actual)
col4.metric("Estado del Sistema", estado_sistema)

st.divider()

# Grafica interactiva del historial con las lineas de limite
st.subheader("Monitoreo Historico de Temperatura y Humedad")

fig = px.line(
    df_iot, 
    x="Timestamp", 
    y="Temperatura_C", 
    title="Comportamiento Termico en Camara de Refrigeracion (C)",
    labels={"Temperatura_C": "Temperatura (C)", "Timestamp": "Fecha y Hora"}
)

fig.add_hline(y=temp_max, line_dash="dash", line_color="red", annotation_text="Limite Maximo")
fig.add_hline(y=temp_min, line_dash="dash", line_color="blue", annotation_text="Limite Minimo")

st.plotly_chart(fig, use_container_width=True)

# Tabla que muestra solo los momentos en los que se rompieron los umbrales
st.subheader("Registro de Eventos y Desviaciones")
alertas_df = df_iot[(df_iot["Temperatura_C"] > temp_max) | (df_iot["Temperatura_C"] < temp_min)]

if not alertas_df.empty:
    st.error(f"Se han detectado {len(alertas_df)} registros fuera de los rangos seguros.")
    st.table(alertas_df)
else:
    st.success("No se han registrado desviaciones de temperatura.")

st.divider()

# Propuesta conceptual del modulo de mantenimiento predictivo con IA
st.subheader("Analisis Predictivo (Mantenimiento Basado en IA)")
with st.expander("Ver Analisis Predictivo del Compresor"):
    st.write("Deteccion de degradacion analizando el tiempo que le toma enfriar la camara tras abrir la puerta.")
    desgaste_estimado = 18.5
    st.progress(desgaste_estimado / 100)
    st.caption(f"Desgaste estimado del compresor: **{desgaste_estimado}%** (Operacion Eficiente)")
    st.info("Prediccion: Se estima requerir mantenimiento preventivo dentro de 45 dias.")

st.divider()

# Modulo para generar y descargar reportes en Excel y PDF
st.subheader("Exportacion de Reportes para Auditoria")
col_exp1, col_exp2 = st.columns(2)

# Crear archivo Excel en memoria
buffer_excel = io.BytesIO()
with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
    df_iot.to_excel(writer, index=False, sheet_name="Datos_ColdSense")

col_exp1.download_button(
    label="Descargar Reporte en Excel",
    data=buffer_excel.getvalue(),
    file_name="Reporte_ColdSense_IoT.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Crear reporte PDF usando FPDF
def generar_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "Reporte de Cumplimiento Cadena de Frio - ColdSense IoT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(190, 8, f"Fecha de emision: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(190, 8, f"Total de lecturas registradas: {len(df)}", ln=True)
    pdf.cell(190, 8, f"Alertas registradas: {len(alertas_df)}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

col_exp2.download_button(
    label="Descargar Reporte en PDF",
    data=generar_pdf(df_iot),
    file_name="Reporte_ColdSense_IoT.pdf",
    mime="application/pdf"
)
