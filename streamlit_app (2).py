
import streamlit as st
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import statistics

st.set_page_config(layout="wide")
st.title("🌱 Simulador de Crecimiento de Plantas con Análisis Estadístico")
st.markdown("Este simulador modela el crecimiento de frijoles en San Pedro de la Paz considerando el **tiempo de remojo antes de la germinación** y condiciones climáticas realistas.")

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

# Simulación completa
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
                'Tiempo de Remojo (h)': remojo,
                'Planta': f'Planta-{planta}',
                'Día': dia,
                'Altura (cm)': round(altura, 2)
            })

df = pd.DataFrame(datos)

# Mostrar gráfico de crecimiento promedio con desviación estándar ±0.5 cm
st.subheader("📊 Crecimiento Promedio por Día (con ±0.5 cm)")
fig, ax = plt.subplots(figsize=(10, 5))
for remojo in sorted(remojos):
    subset = df[df['Tiempo de Remojo (h)'] == remojo]
    promedio = subset.groupby('Día')['Altura (cm)'].mean()
    ax.plot(promedio.index, promedio.values, label=f"{remojo}h")
    ax.fill_between(promedio.index, promedio.values - 0.5, promedio.values + 0.5, alpha=0.2)
ax.set_xlabel("Día")
ax.set_ylabel("Altura (cm)")
ax.set_title("Altura Promedio con Variabilidad Estimada (±0.5 cm)")
ax.legend(title="Remojo")
st.pyplot(fig)

# Estadísticas finales por condición
st.subheader("📈 Estadísticas Finales por Tiempo de Remojo")
resultados = []
for remojo in sorted(remojos):
    final = df[(df['Día'] == dias) & (df['Tiempo de Remojo (h)'] == remojo)]
    alturas = final['Altura (cm)'].tolist()
    media = round(statistics.mean(alturas), 2)
    mediana = round(statistics.median(alturas), 2)
    try:
        moda = round(statistics.mode(alturas), 2)
    except:
        moda = "—"
    desv = round(statistics.stdev(alturas), 2) if len(alturas) > 1 else 0
    resultados.append({
        'Remojo (h)': remojo,
        'Media (cm)': f"{media} ± 0.5",
        'Mediana (cm)': mediana,
        'Moda (cm)': moda,
        'Desviación estándar': desv
    })

st.table(pd.DataFrame(resultados))

# Mostrar tabla completa (opcional)
if st.checkbox("📋 Mostrar tabla completa de simulación"):
    st.dataframe(df)

# Exportar datos
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("💾 Descargar datos como CSV", csv, "simulacion_plantas.csv", "text/csv")

# Nota
st.markdown("**Notas:** Las medidas incluyen una variabilidad estimada de ± 0.5 cm por día. El simulador no reemplaza datos reales pero permite visualizar tendencias probables según factores ambientales y el remojo previo a la germinación.")
