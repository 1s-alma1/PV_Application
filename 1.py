import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# ---------------------
# CONFIGURATION STREAMLIT
# ---------------------
st.set_page_config(
    page_title="Simulateur Solaire",
    page_icon="☀️",
    layout="centered"
)

# ---------------------
# STYLING : fond en ligne
# ---------------------
def add_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1584270354949-8d72dbde4703");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}
        .block-container {{
            background: rgba(0,0,0,0.65);
            padding: 2rem;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_background()

# ---------------------
# DONNÉES DE BASE
# ---------------------
surface_panneau_m2 = 1.8
irradiation_marseille = 1824  # kWh/m²/an
conso_annuelle = 8261  # kWh/an

# Types de panneaux
panneaux = {
    "Monocristallin": {"rendement": 20.0, "prix_watt": 1.2},
    "Polycristallin": {"rendement": 17.5, "prix_watt": 1.0},
    "Amorphe": {"rendement": 10.0, "prix_watt": 0.8},
    "Hétérojonction": {"rendement": 21.5, "prix_watt": 1.5},
    "Bifacial": {"rendement": 19.5, "prix_watt": 1.4}
}

# ---------------------
# INTERFACE
# ---------------------
st.title("☀️ Simulateur d’installation photovoltaïque")
st.subheader("Choisissez votre configuration solaire")

type_choisi = st.selectbox("Type de panneau :", list(panneaux.keys()))
nb_panneaux = st.slider("Nombre de panneaux :", 0, 25, 10)

# ---------------------
# CALCULS
# ---------------------
rendement = panneaux[type_choisi]['rendement']
prix_watt = panneaux[type_choisi]['prix_watt']

surface_totale = nb_panneaux * surface_panneau_m2
puissance_kWp = (rendement / 100) * surface_totale
production = puissance_kWp * irradiation_marseille

# Répartition
auto_conso = min(production, conso_annuelle) * 0.9
besoin_reseau = conso_annuelle - auto_conso
surplus = max(0, production - auto_conso)

# Coût
cout_total = puissance_kWp * 1000 * prix_watt

# ---------------------
# MÉTÉO ALÉATOIRE
# ---------------------
meteo = random.choice(["☀️ Ensoleillé", "🌤️ Nuageux", "🌧️ Pluvieux", "⛅ Variable", "🌩️ Orageux"])

# ---------------------
# AFFICHAGE DES RÉSULTATS
# ---------------------
st.markdown(f"### 🌦️ Météo actuelle : **{meteo}**")
st.markdown(f"#### 🌍 Surface totale installée : **{surface_totale:.2f} m²**")
st.markdown(f"#### ⚡ Puissance installée : **{puissance_kWp:.2f} kWc**")
st.markdown(f"#### 🔋 Production annuelle estimée : **{production:.0f} kWh/an**")
st.markdown(f"#### 💡 Autoconsommation estimée : **{auto_conso:.0f} kWh/an**")
st.markdown(f"#### 🔌 Besoin du réseau : **{besoin_reseau:.0f} kWh/an**")
st.markdown(f"#### 💰 Coût estimé de l’installation : **{cout_total:,.0f} €**")

# ---------------------
# GRAPHIQUE : PRODUCTION VS CONSOMMATION
# ---------------------
fig, ax = plt.subplots()
ax.bar(["Consommation"], [conso_annuelle], color="red", label="Besoin")
ax.bar(["Production"], [production], color="green", label="Production")
ax.set_ylabel("Énergie (kWh/an)")
ax.set_title("Comparaison : Production vs Consommation")
ax.legend()
st.pyplot(fig)

# ---------------------
# LÉGENDE CRÉATEUR
# ---------------------
st.markdown("---")
st.markdown("📘 *Salma Attaibe – Université de Lorraine*", unsafe_allow_html=True)
