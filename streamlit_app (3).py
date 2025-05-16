
import streamlit as st
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import statistics

st.set_page_config(layout="wide")
st.title("🌱 Simulador de Crecimiento de Plantas con Análisis Estadístico Avanzado")
st.markdown("Simula el crecimiento de frijoles considerando **tiempos de remojo previos a la germinación** y factores climáticos típicos de San Pedro de la Paz. El análisis incluye gráficas detalladas y estadísticas clave.")

# Parámetros de simulación
dias = st.slider("Días de simulación", 5, 30, 15)
plantas = st.slider("Número de plantas por condición", 5, 100, 50)
remojos = st.multiselect("Tiempos de remojo a comparar (en horas)", [0, 6, 12, 18, 24, 30, 36, 48], [0, 12, 24, 36])
temp_min = st.slider("Temperatura mínima (°C)", 5, 20, 9)
temp_max = st.slider("Temperatura máxima (°C)", 10, 30, 15)
humedad_prom = st.slider("Humedad promedio (%)", 40, 100, 79)
precipitacion = st.slider("Precipitación mensual (mm)", 0, 300, 190)
dias_lluvia = st.slider("Días de lluvia al mes", 1, 30, 5)
prob_lluvia = st.slider("Probabilidad diaria de lluvia", 0.0, 1.0, 0.24)

# Función para modificar crecimiento según tiempo de remojo
def factor_remojo(t):
    if t < 6:
        return 0.6
    elif t < 12:
        return 0.8
    elif t <= 24:
        return 1.0
    elif t <= 36:
        return 0.9
    else:
        return 0.7

# Función de crecimiento diario
def crecimiento_diario(temp, humedad, lluvia, factor_rem):
    if temp < 10:
        crecimiento = 0.03
    elif temp < 15:
        crecimiento = 0.05
    else:
        crecimiento = 0.07
    if humedad > 80:
        crecimiento *= 1.1
    elif humedad < 60:
        crecimiento *= 0.9
    if lluvia > 5:
        crecimiento *= 1.2
    crecimiento *= factor_rem
    return round(crecimiento, 3)

# Simulación
datos = []

for remojo in remojos:
    f_rem = factor_remojo(remojo)
    for planta in range(1, plantas + 1):
        altura = 0
        for dia in range(1, dias + 1):
            temp_dia = random.uniform(temp_min, temp_max)
            humedad_dia = random.uniform(humedad_prom - 5, humedad_prom + 5)
            lluvia_dia = random.uniform(0, precipitacion / dias_lluvia) if random.random() < prob_lluvia else 0
            crecimiento = crecimiento_diario(temp_dia, humedad_dia, lluvia_dia, f_rem)
            altura += crecimiento
            datos.append({
                'Remojo (h)': remojo,
                'Planta': f'Planta-{planta}',
                'Día': dia,
                'Altura (cm)': round(altura, 2)
            })

df = pd.DataFrame(datos)

# Sección: Gráfico de media con ±0.5 cm
st.subheader("📊 Media diaria por condición (con ±0.5 cm)")
fig1, ax1 = plt.subplots(figsize=(10, 4))
for remojo in sorted(remojos):
    grupo = df[df['Remojo (h)'] == remojo].groupby('Día')['Altura (cm)'].mean()
    ax1.plot(grupo.index, grupo.values, label=f"{remojo}h")
    ax1.fill_between(grupo.index, grupo.values - 0.5, grupo.values + 0.5, alpha=0.2)
ax1.set_xlabel("Día")
ax1.set_ylabel("Altura (cm)")
ax1.legend()
st.pyplot(fig1)

# Sección: Mediana
st.subheader("📈 Mediana diaria por condición")
fig2, ax2 = plt.subplots(figsize=(10, 4))
for remojo in sorted(remojos):
    grupo = df[df['Remojo (h)'] == remojo].groupby('Día')['Altura (cm)'].median()
    ax2.plot(grupo.index, grupo.values, label=f"{remojo}h")
ax2.set_xlabel("Día")
ax2.set_ylabel("Altura (cm)")
ax2.legend()
st.pyplot(fig2)

# Sección: Moda
st.subheader("📉 Moda diaria por condición (cuando existe)")
fig3, ax3 = plt.subplots(figsize=(10, 4))
for remojo in sorted(remojos):
    alturas_modas = []
    for d in range(1, dias + 1):
        valores = df[(df['Día'] == d) & (df['Remojo (h)'] == remojo)]['Altura (cm)'].tolist()
        try:
            alturas_modas.append(statistics.mode(valores))
        except:
            alturas_modas.append(np.nan)
    ax3.plot(range(1, dias + 1), alturas_modas, label=f"{remojo}h")
ax3.set_xlabel("Día")
ax3.set_ylabel("Moda Altura (cm)")
ax3.legend()
st.pyplot(fig3)

# Sección: Desviación estándar
st.subheader("📊 Desviación estándar por día")
fig4, ax4 = plt.subplots(figsize=(10, 4))
for remojo in sorted(remojos):
    grupo = df[df['Remojo (h)'] == remojo].groupby('Día')['Altura (cm)'].std()
    ax4.plot(grupo.index, grupo.values, label=f"{remojo}h")
ax4.set_xlabel("Día")
ax4.set_ylabel("Desviación estándar")
ax4.legend()
st.pyplot(fig4)

# Histograma final
st.subheader("📌 Histogramas finales por condición")
cols = st.columns(len(remojos))
for i, remojo in enumerate(sorted(remojos)):
    with cols[i]:
        st.markdown(f"**Remojo {remojo}h**")
        alturas = df[(df['Día'] == dias) & (df['Remojo (h)'] == remojo)]['Altura (cm)']
        fig, ax = plt.subplots()
        ax.hist(alturas, bins=10, color='skyblue', edgecolor='black')
        ax.set_title("Distribución final")
        st.pyplot(fig)

# Diagrama de dispersión
st.subheader("📎 Diagrama de dispersión final")
fig5, ax5 = plt.subplots()
for remojo in sorted(remojos):
    sub = df[(df['Día'] == dias) & (df['Remojo (h)'] == remojo)]
    ax5.scatter([remojo]*len(sub), sub['Altura (cm)'], label=f"{remojo}h", alpha=0.6)
ax5.set_xlabel("Tiempo de remojo (h)")
ax5.set_ylabel("Altura final (cm)")
ax5.set_title("Altura final por condición")
ax5.legend()
st.pyplot(fig5)

# Mostrar tabla de datos
if st.checkbox("📋 Mostrar datos simulados"):
    st.dataframe(df)

# Descargar CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("💾 Descargar CSV", csv, "simulacion_planta.csv", "text/csv")

st.markdown("**Notas:** Las gráficas muestran una estimación con una variación diaria de ± 0.5 cm.")
