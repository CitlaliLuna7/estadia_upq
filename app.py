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
        {"id_empresa": 1, "razon_social": "Proyectos Regalado y Vaca", "sector": "Tecnología", "parque_industrial": "Parque Industrial El Marqués", "latitud": 20.5888, "longitud": -100.3899, "id_vacante": 1, "titulo_puesto": "Practicante de Ciencia de Datos", "area": "IA / ML", "modalidad": "Híbrido", "apoyo": "Alimentos + Beca", "requisitos": "Python, SQL, Analytics"},
        {"id_empresa": 2, "razon_social": "Quintana-Valverde", "sector": "Servicios", "parque_industrial": "None", "latitud": 20.6120, "longitud": -100.4010, "id_vacante": 2, "titulo_puesto": "Analista de Datos Jr", "area": "Business Intelligence", "modalidad": "Presencial", "apoyo": "Beca Económica", "requisitos": "PowerBI, PostgreSQL"},
        {"id_empresa": 3, "razon_social": "Club Jaimes-Fernández", "sector": "Deportes", "parque_industrial": "Parque Industrial El Marqués", "latitud": 20.5922, "longitud": -100.3750, "id_vacante": 3, "titulo_puesto": "Desarrollador Data Pipeline", "area": "Ingeniería de Datos", "modalidad": "Presencial", "apoyo": "Alimentos", "requisitos": "Python, ETL, SQL"},
        {"id_empresa": 4, "razon_social": "ELITEBRAIN", "sector": "Tecnología", "parque_industrial": "Parque Tecnologico / Remoto", "latitud": 20.5600, "longitud": -100.3200, "id_vacante": 4, "titulo_puesto": "Programador de Aplicaciones Web con Inteligencia Artificial", "area": "IA / ML", "modalidad": "Remoto", "apoyo": "$100 a $180 por hora (Medio tiempo)", "requisitos": "Desarrollo web, Python, AI"},
        {"id_empresa": 5, "razon_social": "HOSPITAL MOSCATI", "sector": "Salud", "parque_industrial": "Zona Juriquilla", "latitud": 20.6500, "longitud": -100.4500, "id_vacante": 5, "titulo_puesto": "Lider de Inteligencia Artificial", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$35,000 a $40,000 por mes", "requisitos": "Liderazgo de proyectos, ML, Python"},
        {"id_empresa": 6, "razon_social": "Alesso", "sector": "Industrial", "parque_industrial": "Parque Industrial Benito Juarez", "latitud": 20.5750, "longitud": -100.3600, "id_vacante": 6, "titulo_puesto": "Cientifico de Datos Junior / Ingeniero de Inteligencia Artificial", "area": "Ingeniería de Datos", "modalidad": "Híbrido", "apoyo": "$25,000 a $25,300 por mes", "requisitos": "Python, SQL, TensorFlow"},
        {"id_empresa": 7, "razon_social": "COLEGIO FINLANDES DE QUERETARO", "sector": "Educación", "parque_industrial": "Zona Centro / Milenio", "latitud": 20.5850, "longitud": -100.3700, "id_vacante": 7, "titulo_puesto": "Desarrollador(a) Jr. de Automatizacion con IA", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$16,000 por mes", "requisitos": "Automatización, Python, APIs"},
        {"id_empresa": 8, "razon_social": "Ojiva Consultores", "sector": "Consultoría", "parque_industrial": "Zona Carretas / Centro", "latitud": 20.5900, "longitud": -100.3800, "id_vacante": 8, "titulo_puesto": "Desarrollador de Software Junior", "area": "Analítica y BI", "modalidad": "Híbrido", "apoyo": "$12,000 a $16,000 por mes", "requisitos": "Lógica de programación, SQL"},
        {"id_empresa": 9, "razon_social": "TechCorp Querétaro", "sector": "Tecnología", "parque_industrial": "Parque Industrial Bernardo Quintana", "latitud": 20.5950, "longitud": -100.3950, "id_vacante": 9, "titulo_puesto": "Ingeniero MLOps", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$28,000 por mes", "requisitos": "Docker, Kubernetes, MLflow"},
        {"id_empresa": 10, "razon_social": "DataSmart Solutions", "sector": "Finanzas", "parque_industrial": "Parque Industrial Innovación", "latitud": 20.5800, "longitud": -100.3650, "id_vacante": 10, "titulo_puesto": "Analista de Inteligencia de Negocios", "area": "Analítica y BI", "modalidad": "Remoto", "apoyo": "$20,000 por mes", "requisitos": "Tableau, SQL, Modelado dimensional"},
        {"id_empresa": 11, "razon_social": "Innovación Automotriz", "sector": "Automotriz", "parque_industrial": "Parque Industrial Querétaro", "latitud": 20.7000, "longitud": -100.4400, "id_vacante": 11, "titulo_puesto": "Especialista en Visión Computacional", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$30,000 por mes", "requisitos": "OpenCV, PyTorch, C++"},
        {"id_empresa": 12, "razon_social": "Logística Global QRO", "sector": "Logística", "parque_industrial": "Parque Industrial La Cruz", "latitud": 20.6050, "longitud": -100.3500, "id_vacante": 12, "titulo_puesto": "Data Engineer Sr", "area": "Ingeniería de Datos", "modalidad": "Híbrido", "apoyo": "$32,000 por mes", "requisitos": "Spark, PySpark, AWS Redshift"},
        {"id_empresa": 13, "razon_social": "Kima Analytics", "sector": "Consultoría", "parque_industrial": "Zona Juriquilla", "latitud": 20.6600, "longitud": -100.4600, "id_vacante": 13, "titulo_puesto": "Científico de Datos NLP", "area": "IA / ML", "modalidad": "Remoto", "apoyo": "$27,000 por mes", "requisitos": "Transformers, HuggingFace, NLTK"},
        {"id_empresa": 14, "razon_social": "Biotecnología del Bajío", "sector": "Farmacéutica", "parque_industrial": "Parque Industrial El Marqués", "latitud": 20.5820, "longitud": -100.3720, "id_vacante": 14, "titulo_puesto": "Analista de Bioestadística y Datos", "area": "Ingeniería de Datos", "modalidad": "Presencial", "apoyo": "$18,000 por mes", "requisitos": "R, Python, PostgreSQL"},
        {"id_empresa": 15, "razon_social": "CyberAI Mexico", "sector": "Ciberseguridad", "parque_industrial": "Parque Tecnologico / Remoto", "latitud": 20.5650, "longitud": -100.3250, "id_vacante": 15, "titulo_puesto": "Ingeniero de Ciberseguridad e IA", "area": "IA / ML", "modalidad": "Remoto", "apoyo": "$34,000 por mes", "requisitos": "Python, SIEM, Detección de Anomalías"},
        {"id_empresa": 16, "razon_social": "Grupo Financiero Bajío", "sector": "Banca", "parque_industrial": "Zona Centro / Milenio", "latitud": 20.5890, "longitud": -100.3780, "id_vacante": 16, "titulo_puesto": "Desarrollador BI & Reporting", "area": "Analítica y BI", "modalidad": "Híbrido", "apoyo": "$22,000 por mes", "requisitos": "Power BI, DAX, SQL Server"},
        {"id_empresa": 17, "razon_social": "AeroSpace QRO", "sector": "Aeroespacial", "parque_industrial": "Parque Industrial Aeroespacial", "latitud": 20.6150, "longitud": -100.3300, "id_vacante": 17, "titulo_puesto": "Ingeniero de Datos de Mantenimiento Predictivo", "area": "Ingeniería de Datos", "modalidad": "Presencial", "apoyo": "$26,000 por mes", "requisitos": "IoT Data, Python, Scikit-Learn"},
        {"id_empresa": 18, "razon_social": "Retail Intelligence SA", "sector": "Comercio", "parque_industrial": "Zona Carretas / Centro", "latitud": 20.5910, "longitud": -100.3820, "id_vacante": 18, "titulo_puesto": "Analista de Datos de Clientes", "area": "Analítica y BI", "modalidad": "Presencial", "apoyo": "$15,000 por mes", "requisitos": "SQL, Excel, Segmentación RFM"},
        {"id_empresa": 19, "razon_social": "Deep Learning Mexico", "sector": "Tecnología", "parque_industrial": "Parque Industrial Bernardo Quintana", "latitud": 20.5970, "longitud": -100.3910, "id_vacante": 19, "titulo_puesto": "Desarrollador de Modelos Deep Learning", "area": "IA / ML", "modalidad": "Remoto", "apoyo": "$31,000 por mes", "requisitos": "PyTorch, CUDA, Python"},
        {"id_empresa": 20, "razon_social": "Energías Limpias QRO", "sector": "Energía", "parque_industrial": "Parque Industrial Benito Juarez", "latitud": 20.5780, "longitud": -100.3620, "id_vacante": 20, "titulo_puesto": "Data Scientist de Telemetría", "area": "IA / ML", "modalidad": "Híbrido", "apoyo": "$24,000 por mes", "requisitos": "Time Series, Pandas, Prophet"},
        {"id_empresa": 21, "razon_social": "MacroData Consultores", "sector": "Consultoría", "parque_industrial": "Parque Industrial El Marqués", "latitud": 20.5840, "longitud": -100.3790, "id_vacante": 21, "titulo_puesto": "Consultor ETL / Data Engineer", "area": "Ingeniería de Datos", "modalidad": "Presencial", "apoyo": "$21,000 por mes", "requisitos": "Airflow, Snowflake, Python"},
        {"id_empresa": 22, "razon_social": "SoftQro Labs", "sector": "Software", "parque_industrial": "Zona Juriquilla", "latitud": 20.6550, "longitud": -100.4550, "id_vacante": 22, "titulo_puesto": "Desarrollador FullStack con Integración IA", "area": "IA / ML", "modalidad": "Remoto", "apoyo": "$29,000 por mes", "requisitos": "React, Python, OpenAI API"},
        {"id_empresa": 23, "razon_social": "AgroTech Bajío", "sector": "Agricultura", "parque_industrial": "Parque Industrial El Marqués", "latitud": 20.5810, "longitud": -100.3700, "id_vacante": 23, "titulo_puesto": "Analista de Imágenes Satelitales e IA", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$19,500 por mes", "requisitos": "GIS, Python, CNN"},
        {"id_empresa": 24, "razon_social": "Smart Factory QRO", "sector": "Manufactura", "parque_industrial": "Parque Industrial Querétaro", "latitud": 20.7050, "longitud": -100.4450, "id_vacante": 24, "titulo_puesto": "Ingeniero de Datos Industrial", "area": "Ingeniería de Datos", "modalidad": "Presencial", "apoyo": "$23,000 por mes", "requisitos": "MQTT, OPC-UA, PostgreSQL"},
        {"id_empresa": 25, "razon_social": "Fintech Querétaro", "sector": "Fintech", "parque_industrial": "Zona Carretas / Centro", "latitud": 20.5930, "longitud": -100.3840, "id_vacante": 25, "titulo_puesto": "Científico de Datos de Riesgo Crediticio", "area": "IA / ML", "modalidad": "Híbrido", "apoyo": "$33,000 por mes", "requisitos": "XGBoost, Credit Scoring, Python"},
        {"id_empresa": 26, "razon_social": "Salud Digital MX", "sector": "Salud", "parque_industrial": "Zona Juriquilla", "latitud": 20.6580, "longitud": -100.4580, "id_vacante": 26, "titulo_puesto": "Analista de Inteligencia de Datos Médicos", "area": "Analítica y BI", "modalidad": "Remoto", "apoyo": "$17,500 por mes", "requisitos": "SQL, Power BI, Python"},
        {"id_empresa": 27, "razon_social": "Movilidad Urbana QRO", "sector": "Transporte", "parque_industrial": "Parque Industrial Benito Juarez", "latitud": 20.5730, "longitud": -100.3580, "id_vacante": 27, "titulo_puesto": "Analista de Datos de Tráfico y Rutas", "area": "Analítica y BI", "modalidad": "Presencial", "apoyo": "$16,500 por mes", "requisitos": "Python, Folium, SQL"},
        {"id_empresa": 28, "razon_social": "Cloud Solutions Bajío", "sector": "Servicios Cloud", "parque_industrial": "Parque Tecnologico / Remoto", "latitud": 20.5630, "longitud": -100.3230, "id_vacante": 28, "titulo_puesto": "Arquitecto de Datos AWS/GCP", "area": "Ingeniería de Datos", "modalidad": "Remoto", "apoyo": "$38,000 por mes", "requisitos": "AWS Glue, BigQuery, Terraform"},
        {"id_empresa": 29, "razon_social": "Inmobiliaria Inteligente", "sector": "Inmobiliario", "parque_industrial": "Zona Centro / Milenio", "latitud": 20.5870, "longitud": -100.3730, "id_vacante": 29, "titulo_puesto": "Analista Valuador con Modelos ML", "area": "IA / ML", "modalidad": "Híbrido", "apoyo": "$21,500 por mes", "requisitos": "Scikit-Learn, Regression Models, SQL"},
        {"id_empresa": 30, "razon_social": "Industrias Plásticas del Centro", "sector": "Plásticos", "parque_industrial": "Parque Industrial Innovación", "latitud": 20.5940, "longitud": -100.3770, "id_vacante": 30, "titulo_puesto": "Especialista en Reportes y Métricas BI", "area": "Analítica y BI", "modalidad": "Presencial", "apoyo": "$14,500 por mes", "requisitos": "Excel, Power BI, SQL"},
        {"id_empresa": 31, "razon_social": "Robotics QRO", "sector": "Robótica", "parque_industrial": "Parque Industrial Bernardo Quintana", "latitud": 20.5960, "longitud": -100.3930, "id_vacante": 31, "titulo_puesto": "Ingeniero en Algoritmos de Navegación IA", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$32,000 por mes", "requisitos": "ROS, C++, Python, SLAM"},
        {"id_empresa": 32, "razon_social": "Media & Marketing Analytics", "sector": "Mercadotecnia", "parque_industrial": "Zona Carretas / Centro", "latitud": 20.5920, "longitud": -100.3830, "id_vacante": 32, "titulo_puesto": "Analista de Datos de Campañas Digitales", "area": "Analítica y BI", "modalidad": "Remoto", "apoyo": "$15,500 por mes", "requisitos": "Google Analytics, Python, SQL"},
        {"id_empresa": 1, "razon_social": "Proyectos Regalado y Vaca", "sector": "Tecnología", "parque_industrial": "Parque Industrial El Marqués", "latitud": 20.5888, "longitud": -100.3899, "id_vacante": 33, "titulo_puesto": "Desarrollador Backend de IA", "area": "IA / ML", "modalidad": "Híbrido", "apoyo": "$26,000 por mes", "requisitos": "FastAPI, Python, Docker"},
        {"id_empresa": 4, "razon_social": "ELITEBRAIN", "sector": "Tecnología", "parque_industrial": "Parque Tecnologico / Remoto", "latitud": 20.5600, "longitud": -100.3200, "id_vacante": 34, "titulo_puesto": "Científico de Datos NLP Senior", "area": "IA / ML", "modalidad": "Remoto", "apoyo": "$36,000 por mes", "requisitos": "LLMs, LangChain, Python"},
        {"id_empresa": 5, "razon_social": "HOSPITAL MOSCATI", "sector": "Salud", "parque_industrial": "Zona Juriquilla", "latitud": 20.6500, "longitud": -100.4500, "id_vacante": 35, "titulo_puesto": "Ingeniero de Datos Hospitalarios", "area": "Ingeniería de Datos", "modalidad": "Presencial", "apoyo": "$23,000 por mes", "requisitos": "ETL, SQL Server, Python"},
        {"id_empresa": 6, "razon_social": "Alesso", "sector": "Industrial", "parque_industrial": "Parque Industrial Benito Juarez", "latitud": 20.5750, "longitud": -100.3600, "id_vacante": 36, "titulo_puesto": "Analista BI de Operaciones", "area": "Analítica y BI", "modalidad": "Presencial", "apoyo": "$18,000 por mes", "requisitos": "Power BI, SQL, Excel"},
        {"id_empresa": 9, "razon_social": "TechCorp Querétaro", "sector": "Tecnología", "parque_industrial": "Parque Industrial Bernardo Quintana", "latitud": 20.5950, "longitud": -100.3950, "id_vacante": 37, "titulo_puesto": "Ingeniero de Plataforma de Datos", "area": "Ingeniería de Datos", "modalidad": "Híbrido", "apoyo": "$29,000 por mes", "requisitos": "Kubernetes, Spark, Python"},
        {"id_empresa": 11, "razon_social": "Innovación Automotriz", "sector": "Automotriz", "parque_industrial": "Parque Industrial Querétaro", "latitud": 20.7000, "longitud": -100.4400, "id_vacante": 38, "titulo_puesto": "Analista de Datos de Calidad", "area": "Analítica y BI", "modalidad": "Presencial", "apoyo": "$17,000 por mes", "requisitos": "Minitab, Python, SQL"},
        {"id_empresa": 15, "razon_social": "CyberAI Mexico", "sector": "Ciberseguridad", "parque_industrial": "Parque Tecnologico / Remoto", "latitud": 20.5650, "longitud": -100.3250, "id_vacante": 39, "titulo_puesto": "Investigador de Modelos de Amenazas IA", "area": "IA / ML", "modalidad": "Remoto", "apoyo": "$35,000 por mes", "requisitos": "Python, Threat Modeling, ML"},
        {"id_empresa": 22, "razon_social": "SoftQro Labs", "sector": "Software", "parque_industrial": "Zona Juriquilla", "latitud": 20.6550, "longitud": -100.4550, "id_vacante": 40, "titulo_puesto": "Data Engineer Junior", "area": "Ingeniería de Datos", "modalidad": "Híbrido", "apoyo": "$16,000 por mes", "requisitos": "SQL, Python, Bash"},
        {"id_empresa": 25, "razon_social": "Fintech Querétaro", "sector": "Fintech", "parque_industrial": "Zona Carretas / Centro", "latitud": 20.5930, "longitud": -100.3840, "id_vacante": 41, "titulo_puesto": "Analista BI de Prevención de Fraudes", "area": "Analítica y BI", "modalidad": "Híbrido", "apoyo": "$22,500 por mes", "requisitos": "SQL, Power BI, Python"},
        {"id_empresa": 31, "razon_social": "Robotics QRO", "sector": "Robótica", "parque_industrial": "Parque Industrial Bernardo Quintana", "latitud": 20.5960, "longitud": -100.3930, "id_vacante": 42, "titulo_puesto": "Científico de Datos en Percepción Remota", "area": "IA / ML", "modalidad": "Presencial", "apoyo": "$31,000 por mes", "requisitos": "C++, Python, OpenCV"}
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
            'Analítica y BI': 'green',
            'Business Intelligence': 'green'
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
