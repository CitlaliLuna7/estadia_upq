import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(
    page_title="Plataforma de Empleabilidad UPQ",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    data = [
        {"id_empresa": 1, "razon_social": "TechData QRO", "sector": "Tecnología", "parque_industrial": "Parque Industrial Bernardo Quintana", "latitud": 20.5888, "longitud": -100.3899, "id_vacante": 101, "titulo_puesto": "Ingeniero de Machine Learning", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$15,000 MXN", "requisitos": "Python, TensorFlow, Scikit-learn, SQL"},
        {"id_empresa": 2, "razon_social": "DataMetrics", "sector": "Consultoría", "parque_industrial": "El Marqués", "latitud": 20.6120, "longitud": -100.4010, "id_vacante": 102, "titulo_puesto": "Data Engineer Specialist", "area": "Ingeniería de Datos", "modalidad": "Híbrido", "apoyo": "$18,000 MXN", "requisitos": "Python, Spark, PostgreSQL, Docker, AWS"},
        {"id_empresa": 3, "razon_social": "BI Solutions QRO", "sector": "Finanzas", "parque_industrial": "Parque Industrial Innovación", "latitud": 20.5922, "longitud": -100.3750, "id_vacante": 103, "titulo_puesto": "Analista de BI Senior", "area": "Analítica y BI", "modalidad": "Remoto", "apoyo": "$14,000 MXN", "requisitos": "Power BI, SQL Server, Excel Avanzado, Python"},
        {"id_empresa": 4, "razon_social": "AI Vision Labs", "sector": "Investigación", "parque_industrial": "Cerca UPQ / El Marqués", "latitud": 20.5600, "longitud": -100.3200, "id_vacante": 104, "titulo_puesto": "Desarrollador Computer Vision", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$16,500 MXN", "requisitos": "OpenCV, PyTorch, C++, Linux"},
        {"id_empresa": 5, "razon_social": "CloudData Systems", "sector": "Tecnología", "parque_industrial": "Juriquilla Tech Park", "latitud": 20.6500, "longitud": -100.4500, "id_vacante": 105, "titulo_puesto": "Arquitecto de Datos Cloud", "area": "Ingeniería de Datos", "modalidad": "Híbrido", "apoyo": "$20,000 MXN", "requisitos": "Snowflake, Databricks, Python, Airflow"},
        {"id_empresa": 6, "razon_social": "Analytics Hub", "sector": "Manufactura", "parque_industrial": "Parque Industrial Bernardo Quintana", "latitud": 20.5750, "longitud": -100.3600, "id_vacante": 106, "titulo_puesto": "Especialista en Dashboarding", "area": "Analítica y BI", "modalidad": "Presencial", "apoyo": "$13,000 MXN", "requisitos": "Tableau, SQL, Modelado de datos"},
        {"id_empresa": 7, "razon_social": "Deep Learning Corp", "sector": "Inteligencia Artificial", "parque_industrial": "El Marqués", "latitud": 20.6200, "longitud": -100.3900, "id_vacante": 107, "titulo_puesto": "Científico de Datos NLP", "area": "IA / ML", "modalidad": "Remoto", "apoyo": "$19,000 MXN", "requisitos": "Transformers, HuggingFace, Python, MLOps"}
    ]
    return pd.DataFrame(data)

df = cargar_datos()

st.title("Plataforma de Inteligencia Territorial y Vacantes UPQ")
st.markdown("""
Esta plataforma permite el mapeo interactivo y la inteligencia de mercado laboral para egresados de la 
**Universidad Politécnica de Querétaro (UPQ)** en las áreas de **IA / ML, Ingeniería de Datos y Analítica & BI**.
""")
st.divider()

st.sidebar.header("Filtros de Búsqueda")

parques_disponibles = ["Todos"] + sorted(list(df['parque_industrial'].dropna().unique()))
parque_sel = st.sidebar.selectbox("Parque Industrial / Zona:", parques_disponibles)

areas_disponibles = ["Todas"] + sorted(list(df['area'].dropna().unique()))
area_sel = st.sidebar.selectbox("Área de Especialidad:", areas_disponibles)

modalidades_disponibles = ["Todas"] + sorted(list(df['modalidad'].dropna().unique()))
modalidad_sel = st.sidebar.selectbox("Modalidad de Trabajo:", modalidades_disponibles)

df_filtrado = df.copy()

if parque_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['parque_industrial'] == parque_sel]

if area_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado['area'] == area_sel]

if modalidad_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado['modalidad'] == modalidad_sel]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Vacantes Encontradas", len(df_filtrado))
col2.metric("Empresas Mapeadas", df_filtrado['razon_social'].nunique())
col3.metric("Área con Mayor Demanda", df_filtrado['area'].mode()[0] if not df_filtrado.empty else "N/A")
col4.metric("Parques Cubiertos", df_filtrado['parque_industrial'].nunique())

st.divider()

tab1, tab2, tab3 = st.tabs(["Mapa de Empleabilidad", "Indicadores de Mercado", "Lista de Vacantes"])

with tab1:
    st.subheader("Ubicación Geográfica de Entidades Empleadoras")
    
    df_mapa = df_filtrado.dropna(subset=['latitud', 'longitud'])
    
    if df_mapa.empty:
        st.warning("No hay vacantes con coordenadas válidas para mostrar en el mapa con los filtros seleccionados.")
    else:
        lat_centro = df_mapa['latitud'].mean()
        lon_centro = df_mapa['longitud'].mean()
        
        mapa = folium.Map(location=[lat_centro, lon_centro], zoom_start=11, tiles="OpenStreetMap")
        
        colores_area = {
            'IA / ML': 'purple',
            'Ingeniería de Datos': 'blue',
            'Analítica y BI': 'green'
        }
        
        for _, row in df_mapa.iterrows():
            color = colores_area.get(row['area'], 'gray')
            
            popup_html = f"""
            <div style='font-family: Arial, sans-serif; width: 220px;'>
                <h4 style='margin-bottom:5px; color:#0056b3;'>{row['razon_social']}</h4>
                <b>Puesto:</b> {row['titulo_puesto']}<br>
                <b>Área:</b> {row['area']}<br>
                <b>Modalidad:</b> {row['modalidad']}<br>
                <b>Sueldo/Apoyo:</b> {row['apoyo']}<br>
                <b>Zona:</b> {row['parque_industrial']}
            </div>
            """
            
            folium.Marker(
                location=[row['latitud'], row['longitud']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{row['razon_social']} - {row['titulo_puesto']}",
                icon=folium.Icon(color=color)
            ).add_to(mapa)
            
        st_folium(mapa, width="100%", height=500)

with tab2:
    st.subheader("Análisis Estadístico de la Demanda Laboral")
    
    if not df_filtrado.empty:
        g_col1, g_col2 = st.columns(2)
        
        with g_col1:
            df_area_chart = df_filtrado.dropna(subset=['area'])
            if not df_area_chart.empty:
                fig_area = px.pie(
                    df_area_chart, 
                    names='area', 
                    title='Distribución por Especialidad Técnica',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig_area, use_container_width=True)
            
        with g_col2:
            df_parques = df_filtrado['parque_industrial'].dropna().value_counts().reset_index()
            df_parques.columns = ['Parque Industrial', 'Vacantes']
            
            if not df_parques.empty:
                fig_parque = px.bar(
                    df_parques, 
                    x='Vacantes', 
                    y='Parque Industrial', 
                    orientation='h',
                    title='Concentración de Vacantes por Parque Industrial',
                    color='Vacantes',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_parque, use_container_width=True)
            
        df_mod_chart = df_filtrado.dropna(subset=['modalidad'])
        if not df_mod_chart.empty:
            fig_mod = px.histogram(
                df_mod_chart, 
                x='modalidad', 
                color='area', 
                barmode='group',
                title='Distribución de Modalidad según la Especialidad',
                labels={'modalidad': 'Modalidad', 'count': 'Número de Vacantes'}
            )
            st.plotly_chart(fig_mod, use_container_width=True)

with tab3:
    st.subheader("Explorador Detallado de Requisitos y Contrata")
    
    busqueda = st.text_input("Buscar palabra clave (ej. Python, SQL, AWS, Docker):", "")
    
    df_tabla = df_filtrado.copy()
    if busqueda:
        df_tabla = df_tabla[
            df_tabla['titulo_puesto'].astype(str).str.contains(busqueda, case=False, na=False) |
            df_tabla['requisitos'].astype(str).str.contains(busqueda, case=False, na=False) |
            df_tabla['razon_social'].astype(str).str.contains(busqueda, case=False, na=False)
        ]
        
    columnas_mostrar = ['razon_social', 'titulo_puesto', 'area', 'modalidad', 'apoyo', 'parque_industrial', 'requisitos']
    st.dataframe(df_tabla[columnas_mostrar], use_container_width=True, hide_index=True)
    
    csv_bytes = df_tabla[columnas_mostrar].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Exportar Consulta a CSV",
        data=csv_bytes,
        file_name="reporte_vacantes_upq.csv",
        mime="text/csv"
    )
