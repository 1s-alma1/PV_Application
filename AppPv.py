import streamlit as st
import matplotlib.pyplot as plt

# -------- CONFIGURATION --------
st.set_page_config(page_title="Projet PV - Salma", page_icon="☀️", layout="centered")

# -------- TITRE & METEO --------
st.title("🔆 Simulation photovoltaïque – Projet Salma Attaibe")

meteo = st.selectbox("🌦️ Choisissez la météo actuelle :", ["☀️ Ensoleillé", "🌤️ Nuageux", "🌧️ Pluvieux"])
st.markdown(f"### Météo sélectionnée : {meteo}")

# -------- DONNÉES TECHNIQUES PANNEAUX --------
panneaux = {
    "Monocristallin": {"rendement": 20.0, "prix_watt": 1.2},
    "Polycristallin": {"rendement": 17.5, "prix_watt": 1.0},
    "Amorphe": {"rendement": 10.0, "prix_watt": 0.8},
    "Hétérojonction": {"rendement": 21.5, "prix_watt": 1.5},
    "Bifacial": {"rendement": 19.5, "prix_watt": 1.4}
}

type_choisi = st.selectbox("🔋 Type de panneau :", list(panneaux.keys()))
nb_panneaux = st.slider("🔢 Nombre de panneaux (max 20) :", 0, 20, 10)

# -------- CONSTANTES PROJET --------
surface_panneau = 1.8  # m²
irradiation = 1824  # kWh/m²/an à Marseille
conso_annuelle = 8261  # kWh/an

# -------- CALCULS --------
infos = panneaux[type_choisi]
rendement = infos['rendement']
prix_watt = infos['prix_watt']

surface_totale = nb_panneaux * surface_panneau
puissance_kWp = (rendement / 100) * surface_totale
production = puissance_kWp * irradiation

autoconso = min(production, conso_annuelle) * 0.9
besoin_reseau = conso_annuelle - autoconso
injection = max(0, production - autoconso)
cout_total = puissance_kWp * 1000 * prix_watt

# -------- AFFICHAGE RÉSULTATS --------
st.subheader("🔎 Résultats du projet")
st.markdown(f"**Surface occupée :** {surface_totale:.2f} m²")
st.markdown(f"**Puissance installée :** {puissance_kWp:.2f} kWc")
st.markdown(f"**Production estimée :** {production:.0f} kWh/an")
st.markdown(f"**Autoconsommation estimée :** {autoconso:.0f} kWh/an")
st.markdown(f"**Besoin du réseau :** {besoin_reseau:.0f} kWh/an")
st.markdown(f"**Surplus injecté :** {injection:.0f} kWh/an")
st.markdown(f"**Coût estimé :** {cout_total:,.0f} €")

# -------- GRAPHIQUE 1 : Production vs Consommation --------
fig1, ax1 = plt.subplots()
ax1.bar(["Production"], [production], color="green", label="Production PV")
ax1.bar(["Consommation"], [conso_annuelle], color="red", label="Consommation maison")
ax1.set_title("⚡ Production vs Besoin")
ax1.set_ylabel("kWh/an")
ax1.legend()
st.pyplot(fig1)

# -------- GRAPHIQUE 2 : Répartition énergie --------
fig2, ax2 = plt.subplots()
labels = ["Autoconsommée", "Injectée au réseau", "Reprise du réseau"]
vals = [autoconso, injection, besoin_reseau]
colors = ["limegreen", "orange", "gray"]
ax2.bar(labels, vals, color=colors)
ax2.set_title("🔄 Répartition de l’énergie solaire")
ax2.set_ylabel("kWh/an")
st.pyplot(fig2)

# -------- SIGNATURE --------
st.markdown("---")
st.caption("👩‍🎓 Salma Attaibe – Université de Lorraine")
