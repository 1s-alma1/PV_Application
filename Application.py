import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============ CONFIG PAGE ============
st.set_page_config(
    page_title="Simulateur Solaire",
    page_icon="☀️",
    layout="centered"
)

# ======== BACKGROUND STYLING ========
def add_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1584270354949-8d72dbde4703");
            background-size: cover;
            background-position: top left;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #ffffff;
        }}
        .css-1d391kg {{
            background: rgba(0,0,0,0.6) !important;
            border-radius: 10px;
            padding: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_background()

# ========== PANNEAU TYPES ==========
panneaux = {
    "Monocristallin": {"rendement": 20.0, "cout_watt": 1.2},
    "Polycristallin": {"rendement": 17.5, "cout_watt": 1.0},
    "Amorphe": {"rendement": 10.0, "cout_watt": 0.8},
    "Hétérojonction": {"rendement": 21.5, "cout_watt": 1.5},
    "Bifacial": {"rendement": 19.5, "cout_watt": 1.4},
}

# ========== ENTRÉES UTILISATEUR ==========
st.title("☀️ Simulateur d'installation solaire résidentielle")
st.markdown("### Choisis ton panneau solaire et dimensionne ton projet")

type_panneau = st.selectbox("Type de panneau :", list(panneaux.keys()))
nb_panneaux = st.slider("Nombre de panneaux :", 5, 30, 12)
surface_par_panneau = 1.8  # m²

# ========== CONSTANTES ==========
irradiation = 1824  # kWh/m²/an (Marseille)
conso_annuelle = 8261  # kWh/an
puissance_unitaire = 400  # W

# ========== CALCULS ==========
donnees = panneaux[type_panneau]
rendement = donnees["rendement"]
cout_watt = donnees["cout_watt"]

surface_totale = nb_panneaux * surface_par_panneau
puissance_installée_kwp = (rendement / 100) * surface_totale
production = puissance_installée_kwp * irradiation  # kWh/an
autoconso = min(conso_annuelle, production) * 0.9
injection = max(0, production - autoconso)
reprise = max(0, conso_annuelle - autoconso)

eco_auto = autoconso * 0.25
revenu_inj = injection * 0.10
eco_totale = eco_auto + revenu_inj

investissement = puissance_installée_kwp * 1000 * cout_watt
roi = round((eco_totale * 20 - investissement) / investissement * 100, 2)

# ========== AFFICHAGE ==========
st.subheader("🔎 Résultats de simulation")
st.markdown(f"**Surface occupée :** {surface_totale:.2f} m²")
st.markdown(f"**Puissance installée :** {puissance_installée_kwp:.2f} kWc")
st.markdown(f"**Production annuelle estimée :** {production:.0f} kWh/an")
st.markdown(f"**Économie estimée :** {eco_totale:.0f} €/an")
st.markdown(f"**Coût d’installation :** {investissement:,.0f} €")
st.markdown(f"**Retour sur investissement (ROI sur 20 ans) :** {roi} %")

# ========== GRAPHIQUE ==========
fig, ax = plt.subplots()
labels = ['Autoconsommée', 'Injectée', 'Reprise réseau']
values = [autoconso, injection, reprise]
colors = ['green', 'orange', 'red']

ax.bar(labels, values, color=colors)
ax.set_title("Comparaison production vs consommation")
ax.set_ylabel("kWh/an")
st.pyplot(fig)

# ========== MÉTÉO ALÉATOIRE (bonus animation) ==========
import random
meteo = random.choice(['☀️ Ensoleillé', '🌤️ Partiellement nuageux', '⛅ Nuages légers', '🌧️ Pluie', '🌩️ Orage'])
st.markdown(f"### 🌦️ Météo actuelle simulée : {meteo}")
