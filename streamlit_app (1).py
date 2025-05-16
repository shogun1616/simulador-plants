
import streamlit as st
import pandas as pd
import random

st.title("🌱 Simulador de Crecimiento de Plantas")
st.markdown("Simula el crecimiento de frijoles en San Pedro de la Paz según condiciones climáticas promedio de mayo y el tiempo de remojo antes de la germinación.")

# Controles interactivos
dias = st.slider("Días de simulación", 1, 30, 15)
plantas = st.slider("Número de plantas", 1, 100, 50)
temp_min = st.slider("Temperatura mínima (°C)", 5, 20, 9)
temp_max = st.slider("Temperatura máxima (°C)", 10, 30, 15)
humedad_prom = st.slider("Humedad promedio (%)", 40, 100, 79)
precipitacion = st.slider("Precipitación mensual (mm)", 0, 300, 190)
dias_lluvia = st.slider("Días de lluvia al mes", 1, 30, 5)
prob_lluvia = st.slider("Probabilidad diaria de lluvia", 0.0, 1.0, 0.24)
tiempo_remojo = st.slider("⏳ Tiempo de remojo antes de germinar (horas)", 0, 48, 12)

# Función que ajusta crecimiento según el tiempo de remojo
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

# Simulación de crecimiento
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
f_rem = factor_remojo(tiempo_remojo)
for planta in range(1, plantas + 1):
    altura = 0
    for dia in range(1, dias + 1):
        temp_dia = random.uniform(temp_min, temp_max)
        humedad_dia = random.uniform(humedad_prom - 5, humedad_prom + 5)
        lluvia_dia = random.uniform(0, precipitacion / dias_lluvia) if random.random() < prob_lluvia else 0
        crecimiento = crecimiento_diario(temp_dia, humedad_dia, lluvia_dia, f_rem)
        altura += crecimiento
        datos.append({
            'Planta': f'Planta-{planta}',
            'Día': dia,
            'Altura (cm)': round(altura, 2)
        })

# Convertir a DataFrame
df = pd.DataFrame(datos)

# Mostrar resultados
st.subheader("📈 Crecimiento promedio por día")
promedios = df.groupby('Día')['Altura (cm)'].mean()
st.line_chart(promedios)

# Mostrar tabla si el usuario quiere
if st.checkbox("Mostrar tabla completa de datos"):
    st.dataframe(df)

# Explicación
st.markdown("**Nota:** El tiempo de remojo afecta el crecimiento diario. Un remojo óptimo (12–24 h) maximiza el crecimiento inicial. Remojos muy cortos o muy largos pueden disminuir el ritmo de germinación.")
