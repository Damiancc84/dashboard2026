import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sistema de Control de Recaudación y Auditoría Minera",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Sistema de Control de Recaudación y Auditoría Minera")
st.markdown("### Dashboard Ejecutivo - Período: Julio / Agosto 2026")
st.markdown("---")

# --- DATA HARDCODED FROM SOURCE CSV ---
mda_metrics = {
    "empresa": "MINERA DEL ALTIPLANO S.A.",
    "periodo": "Julio 2026",
    "recaudacion_periodo": 1493421024.8,
    "recaudacion_acumulada": 8542698208.87,
    "periodo_anterior": 452323328.8,
    "var_interanual": 230.17,
    "precio_kg": 26386.41,
    "relacion_facturado_costos": 0.3330
}

liex_metrics = {
    "empresa": "LIEX S.A.",
    "periodo": "Julio 2026",
    "recaudacion_periodo": 357201855.3,
    "recaudacion_acumulada": 6500915172.74,
    "periodo_anterior": 0.0001,
    "var_interanual": 0.0,  # Indeterminado o inf
    "precio_kg": 20850.40,
    "relacion_facturado_costos": 0.7422
}

padron_metrics = {
    "concesionarias_activas": 2,
    "presentaron_ddjj": 1,
    "ddjj_pendientes": 1,
    "sin_pago": 0
}

recaudacion_total = {
    "monto_declarado": 1850622880.1,
    "monto_recaudado_anio": 15043613381.61,
    "deuda_vencida": 0.0,
    "concesionarias_deuda": 0
}

# Historial mensual
meses = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07"]
df_historico = pd.DataFrame({
    "Periodo": meses,
    "Precio MDA (USD)": [11.71, 14.65, 16.36, 17.3, 18.71, 19.21, 17.85],
    "Precio LIEX (USD)": [12.05, 13.76, 14.98, 15.28, 17.71, 15.54, 14.03],
    "Cantidad MDA (Kg)": [2085600, 2919554.65, 3668054.65, 2739968.25, 1613509.3, 1200000, 2742000],
    "Cantidad LIEX (Kg)": [1757740, 1318200, 1790410, 2341360, 2206090, 1350280, 550270],
    "Recaudación MDA (ARS)": [755155979.04, 1189966424.87, 1777291003.41, 1399926234.6, 930151852.74, 705846531.2, 1493421024.8],
    "Recaudación LIEX (ARS)": [1075109103.16, 889443388.47, 873750537.41, 1227023899.01, 1248175886.49, 830210502.9, 357201855.3],
    "Total Recaudación (ARS)": [1830265082.2, 2079409813.34, 2651041540.82, 2626950133.61, 2178327739.23, 1536057034.1, 1850622880.1]
})


# --- SIDEBAR FILTERS ---
st.sidebar.header("Filtros Globales")
empresa_seleccionada = st.sidebar.selectbox("Seleccionar Empresa Vista Detallada:", ["Todas", "Minera del Altiplano", "LIEX S.A."])

# --- ROW 1: RESUMEN DE CONTROL GENERAL ---
st.subheader("📌 III. RESUMEN DE RECAUDACIÓN TOTAL Y PADRÓN")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Monto Declarado Período (Julio)", f"$ {recaudacion_total['monto_declarado']:,.2f}")
with c2:
    st.metric("Efectivamente Recaudado Año", f"$ {recaudacion_total['monto_recaudado_anio']:,.2f}")
with c3:
    st.metric("Concesionarias Activas (Agosto)", f"{padron_metrics['concesionarias_activas']}")
with c4:
    st.metric("DDJJ Pendientes", f"{padron_metrics['ddjj_pendientes']}", delta="- Sin Deuda Vencida")

# --- ROW 2: DETALLE POR EMPRESA ---
st.subheader("🏢 I. MÉTRICAS FINANCIERAS POR CONCESIONARIA")

col_mda, col_liex = st.columns(2)

if empresa_seleccionada in ["Todas", "Minera del Altiplano"]:
    with col_mda:
        st.markdown(f"#### {mda_metrics['empresa']}")
        st.write(f"**Recaudación Período:** $ {mda_metrics['recaudacion_periodo']:,.2f}")
        st.write(f"**Acumulada del Año:** $ {mda_metrics['recaudacion_acumulada']:,.2f}")
        st.write(f"**Variación Interanual:** {mda_metrics['var_interanual']}%")
        st.write(f"**Precio x Kg (Carbonato Litio):** $ {mda_metrics['precio_kg']:,.2f}")
        st.progress(mda_metrics['relacion_facturado_costos'], text=f"Relación Facturado/Costos: {mda_metrics['relacion_facturado_costos']:.2%}")

if empresa_seleccionada in ["Todas", "LIEX S.A."]:
    with col_liex:
        st.markdown(f"#### {liex_metrics['empresa']}")
        st.write(f"**Recaudación Período:** $ {liex_metrics['recaudacion_periodo']:,.2f}")
        st.write(f"**Acumulada del Año:** $ {liex_metrics['recaudacion_acumulada']:,.2f}")
        st.write(f"**Variación Interanual:** N/A")
        st.write(f"**Precio x Kg (Carbonato Litio):** $ {liex_metrics['precio_kg']:,.2f}")
        st.progress(liex_metrics['relacion_facturado_costos'], text=f"Relación Facturado/Costos: {liex_metrics['relacion_facturado_costos']:.2%}")

st.markdown("---")

# --- ROW 3: GRAFICOS EVOLUTIVOS ---
st.subheader("📈 IV. GRÁFICAS EVOLUTIVAS HISTÓRICAS (2026)")

tab1, tab2, tab3 = st.tabs(["💰 Evolución de Recaudación", "⚖️ Comparativa de Precios USD", "📦 Volúmenes de Producción (Kg)"])

with tab1:
    fig_rec = px.bar(
        df_historico, 
        x="Periodo", 
        y=["Recaudación MDA (ARS)", "Recaudación LIEX (ARS)"],
        title="Recaudación Mensual por Empresa (ARS)",
        barmode="stack",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    fig_rec.add_trace(go.Scatter(x=df_historico["Periodo"], y=df_historico["Total Recaudación (ARS)"], name="Total General", mode="lines+markers", line=dict(color="black", width=2)))
    st.plotly_chart(fig_rec, use_container_width=True)

with tab2:
    fig_precios = px.line(
        df_historico, 
        x="Periodo", 
        y=["Precio MDA (USD)", "Precio LIEX (USD)"],
        markers=True,
        title="Evolución de Precio Declarado por Kg (USD)",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(fig_precios, use_container_width=True)

with tab3:
    fig_cant = px.bar(
        df_historico, 
        x="Periodo", 
        y=["Cantidad MDA (Kg)", "Cantidad LIEX (Kg)"],
        title="Cantidad de Litio Declarada (Kg) por Mes",
        barmode="group"
    )
    st.plotly_chart(fig_cant, use_container_width=True)

# --- ROW 4: DATA TABLE ---
st.subheader("📋 Datos Históricos Detallados")
st.dataframe(df_historico.style.format({
    "Precio MDA (USD)": "{:,.2f}",
    "Precio LIEX (USD)": "{:,.2f}",
    "Cantidad MDA (Kg)": "{:,.0f}",
    "Cantidad LIEX (Kg)": "{:,.0f}",
    "Recaudación MDA (ARS)": "$ {:,.2f}",
    "Recaudación LIEX (ARS)": "$ {:,.2f}",
    "Total Recaudación (ARS)": "$ {:,.2f}"
}), use_container_width=True)
