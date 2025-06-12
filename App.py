import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIG STREAMLIT ---
st.set_page_config(
    page_title="Simulateur Solaire Projet Salma",
    page_icon="☀️",
    layout="centered"
)

# --- MÉTÉO & FOND ---
backgrounds = {
    "☀️ Ensoleillé": "https://images.unsplash.com/photo-1509395176047-4a66953fd231",
    "🌤️ Nuageux": "https://images.unsplash.com/photo-1618221597737-8fef07c6a3d8",
    "🌧️ Pluvieux": "https://images.unsplash.com/photo-1607746882042-944635dfe10e"
}
meteo = st.selectbox("🌦️ Météo actuelle :", list(backgrounds.keys()))
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{backgrounds[meteo]}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- DONNÉES PANNEAUX ---
panneaux = {
    "Monocristallin": {"rendement": 20.0, "prix_watt": 1.2},
    "Polycristallin": {"rendement": 17.5, "prix_watt": 1.0},
    "Amorphe": {"rendement": 10.0, "prix_watt": 0.8},
    "Hétérojonction": {"rendement": 21.5, "prix_watt": 1.5},
    "Bifacial": {"rendement": 19.5, "prix_watt": 1.4}
}

# --- PARAMÈTRES FIXES DU PROJET ---
conso_annuelle = 8261  # kWh/an
surface_panneau = 1.8  # m²
irradiation = 1824     # kWh/m²/an à Marseille

# --- INTERFACE UTILISATEUR ---
st.title("🔆 Simulation PV - Projet Salma")
type_choisi = st.selectbox("🔋 Type de panneau :", list(panneaux.keys()))
nb_panneaux = st.slider("🔢 Nombre de panneaux (400 Wc) :", 0, 20, 10)

# --- CALCULS ADAPTÉS AU PROJET ---
rendement = panneaux[type_choisi]["rendement"]
prix_watt = panneaux[type_choisi]["prix_watt"]

surface_totale = nb_panneaux * surface_panneau
puissance_kWp = (rendement / 100) * surface_totale
production = puissance_kWp * irradiation

autoconso = min(production, conso_annuelle) * 0.9
besoin_reseau = conso_annuelle - autoconso
surplus = max(0, production - autoconso)

cout_total = puissance_kWp * 1000 * prix_watt

# --- AFFICHAGE DES DONNÉES ---
st.subheader("🔎 Résultats de simulation")
st.markdown(f"**Surface installée :** {surface_totale:.2f} m²")
st.markdown(f"**Puissance installée :** {puissance_kWp:.2f} kWc")
st.markdown(f"**Production estimée :** {production:.0f} kWh/an")
st.markdown(f"**Autoconsommée :** {autoconso:.0f} kWh/an")
st.markdown(f"**Réseau requis :** {besoin_reseau:.0f} kWh/an")
st.markdown(f"**Surplus injecté :** {surplus:.0f} kWh/an")
st.markdown(f"**Coût estimé :** {cout_total:,.0f} €")

# --- GRAPHIQUE 1 : Production vs Besoin ---
fig1, ax1 = plt.subplots()
ax1.bar(["Production"], [production], color="green", label="Production")
ax1.bar(["Consommation"], [conso_annuelle], color="red", label="Consommation")
ax1.set_title("⚡ Production vs Besoin Réel")
ax1.set_ylabel("kWh/an")
ax1.legend()
st.pyplot(fig1)

# --- GRAPHIQUE 2 : Répartition interne ---
fig2, ax2 = plt.subplots()
labels = ["Autoconsommée", "Injectée", "Reprise Réseau"]
vals = [autoconso, surplus, besoin_reseau]
colors = ["limegreen", "orange", "gray"]
ax2.bar(labels, vals, color=colors)
ax2.set_title("🔄 Répartition de l’énergie solaire")
ax2.set_ylabel("kWh/an")
st.pyplot(fig2)

# --- SIGNATURE ---
st.markdown("---")
st.markdown("📘 _Salma Attaibe – Université de Lorraine_")
