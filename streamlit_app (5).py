
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics
import random

st.set_page_config(layout="wide")
st.title("📊 Balkendiagramm zur Pflanzenhöhe nach Einweichzeit")

st.markdown("Dieses Diagramm zeigt die durchschnittliche Endhöhe von *Phaseolus vulgaris* (Gemeine Bohne) nach verschiedenen Einweichzeiten vor der Keimung.")

# Einstellungen
tage = 15
pflanzen = 50
einweichzeiten = [0, 6, 12, 24, 36, 48]

# Klimaparameter
klima = {
    'temp_min': 9,
    'temp_max': 15,
    'feuchtigkeit': 79,
    'regen': 190,
    'regentage': 5,
    'regenwahrscheinlichkeit': 0.24
}

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

# Wachstumsfunktion
def wachstum(temp, feucht, regen, faktor):
    if temp < 10:
        w = 0.03
    elif temp < 15:
        w = 0.05
    else:
        w = 0.07
    if feucht > 80:
        w *= 1.1
    elif feucht < 60:
        w *= 0.9
    if regen > 5:
        w *= 1.2
    return w * faktor

# Daten generieren
ergebnisse = []
for t in einweichzeiten:
    faktor = einweich_faktor(t)
    endhoehen = []
    for p in range(pflanzen):
        hoehe = 0
        for tag in range(tage):
            temp = random.uniform(klima['temp_min'], klima['temp_max'])
            feucht = random.uniform(klima['feuchtigkeit'] - 5, klima['feuchtigkeit'] + 5)
            regen = random.uniform(0, klima['regen'] / klima['regentage']) if random.random() < klima['regenwahrscheinlichkeit'] else 0
            hoehe += wachstum(temp, feucht, regen, faktor)
        endhoehen.append(round(hoehe, 2))
    mittel = round(np.mean(endhoehen), 2)
    std = round(np.std(endhoehen), 2)
    ergebnisse.append({'Einweichzeit (h)': t, 'Ø Endhöhe (cm)': mittel, 'Standardabweichung': std})

df = pd.DataFrame(ergebnisse)

# Diagramm
st.subheader("Abbildung 1: Durchschnittliche Endhöhe (± 0,5 cm) nach Einweichzeit")
fig, ax = plt.subplots()
farben = plt.cm.viridis(np.linspace(0.2, 0.8, len(df)))
ax.bar(df['Einweichzeit (h)'], df['Ø Endhöhe (cm)'], yerr=0.5, capsize=5, color=farben)
ax.set_xlabel("Einweichzeit (h)")
ax.set_ylabel("Körpergröße in cm (± 0,5 cm)")
ax.set_title("Einfluss der Einweichzeit auf die Pflanzenhöhe (Phaseolus vulgaris)")
ax.set_ylim([0, max(df['Ø Endhöhe (cm)']) + 2])
st.pyplot(fig)

# Daten anzeigen
if st.checkbox("📋 Tabelle anzeigen"):
    st.dataframe(df)
