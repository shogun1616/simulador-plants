# Volver a intentar guardar el código combinado como archivo descargable

codigo_combinado = '''
import streamlit as st
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import statistics

st.set_page_config(layout="wide")
st.title("🌱 Simulierte Untersuchung: Einfluss der Einweichzeit auf das Wachstum von Phaseolus vulgaris")

st.markdown(\"\"\"
Dieses Tool simuliert das Pflanzenwachstum unter kontrollierten Umweltbedingungen und analysiert den Einfluss der **Einweichzeit** auf die Endhöhe der Pflanzen.
\"\"\")

# Parameter
tage = st.slider("📅 Simulationsdauer (Tage)", 5, 30, 15)
pflanzen = st.slider("🌱 Pflanzen pro Gruppe", 5, 100, 50)
einweichzeiten = st.multiselect("⏳ Einweichzeiten (in Stunden)", [0, 6, 12, 18, 24, 30, 36, 48], default=[0, 12, 24, 36])
temp_min = st.slider("🌡️ Minimale Temperatur (°C)", 5, 20, 9)
temp_max = st.slider("🌡️ Maximale Temperatur (°C)", 10, 30, 15)
feuchtigkeit = st.slider("💧 Durchschnittliche Luftfeuchtigkeit (%)", 40, 100, 79)
niederschlag = st.slider("🌧️ Monatlicher Niederschlag (mm)", 0, 300, 190)
regentage = st.slider("🌦️ Regentage pro Monat", 1, 30, 5)
regenwahrscheinlichkeit = st.slider("☁️ Regenwahrscheinlichkeit (pro Tag)", 0.0, 1.0, 0.24)

# Einweichfaktor
def einweich_faktor(t):
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

# Wachstum pro Tag
def wachstum_pro_tag(temp, hum, rain, faktor):
    if temp < 10:
        w = 0.03
    elif temp < 15:
        w = 0.05
    else:
        w = 0.07
    if hum > 80:
        w *= 1.1
    elif hum < 60:
        w *= 0.9
    if rain > 5:
        w *= 1.2
    return w * faktor

# Simulation
daten = []
statistik = []

for zeit in einweichzeiten:
    f = einweich_faktor(zeit)
    endhoehen = []
    for p in range(pflanzen):
        hoehe = 0
        for tag in range(tage):
            temp = random.uniform(temp_min, temp_max)
            hum = random.uniform(feuchtigkeit - 5, feuchtigkeit + 5)
            rain = random.uniform(0, niederschlag / regentage) if random.random() < regenwahrscheinlichkeit else 0
            hoehe += wachstum_pro_tag(temp, hum, rain, f)
            daten.append({
                "Einweichzeit (h)": zeit,
                "Pflanze": f"Pflanze-{p+1}",
                "Tag": tag + 1,
                "Höhe (cm)": round(hoehe, 2)
            })
        endhoehen.append(hoehe)
    statistik.append({
        "Einweichzeit (h)": zeit,
        "Ø Endhöhe (cm)": round(np.mean(endhoehen), 2),
        "Median": round(np.median(endhoehen), 2),
        "Modus": round(statistics.mode(endhoehen), 2) if len(set(endhoehen)) > 1 else "—",
        "Standardabweichung": round(np.std(endhoehen), 2)
    })

df = pd.DataFrame(daten)
df_stats = pd.DataFrame(statistik)

# Hauptdiagramme
st.subheader("📈 Wachstumskurven pro Gruppe")
fig1, ax1 = plt.subplots()
for zeit in einweichzeiten:
    gruppe = df[df["Einweichzeit (h)"] == zeit]
    mittel = gruppe.groupby("Tag")["Höhe (cm)"].mean()
    ax1.plot(mittel.index, mittel.values, label=f"{zeit} h")
ax1.set_xlabel("Tag")
ax1.set_ylabel("Höhe (cm)")
ax1.set_title("Tägliche Durchschnittshöhe (± 0.5 cm)")
ax1.legend()
st.pyplot(fig1)

# BU-konformes Balkendiagramm
st.subheader("📊 Abbildung 1: Durchschnittliche Endhöhe (± 0,5 cm)")
fig2, ax2 = plt.subplots()
farben = plt.cm.viridis(np.linspace(0.2, 0.8, len(df_stats)))
ax2.bar(df_stats["Einweichzeit (h)"], df_stats["Ø Endhöhe (cm)"], yerr=0.5, capsize=5, color=farben)
ax2.set_xlabel("Einweichzeit (h)")
ax2.set_ylabel("Körpergröße in cm (± 0,5 cm)")
ax2.set_title("Einfluss der Einweichzeit auf die Pflanzenhöhe (Phaseolus vulgaris)")
st.pyplot(fig2)

# Statistik-Tabelle
st.subheader("📋 Statistische Übersicht")
st.dataframe(df_stats)

# Rohdaten optional
if st.checkbox("📁 Gesamte Simulationsdaten anzeigen"):
    st.dataframe(df)

# CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("💾 CSV herunterladen", csv, "pflanzensimulation.csv", "text/csv")
'''

# Guardar archivo como streamlit_app.py
file_path = "/mnt/data/streamlit_app.py"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(codigo_combinado)

file_path
