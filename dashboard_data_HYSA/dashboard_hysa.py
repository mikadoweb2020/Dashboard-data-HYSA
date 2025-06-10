
import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des fichiers
@st.cache_data
def load_data():
    monthly = pd.read_csv("monthly_data.csv")
    users = pd.read_csv("user_data.csv")
    buildings = pd.read_csv("building_data.csv")
    delays = pd.read_csv("delays_data.csv")
    non_completed = pd.read_csv("non_completed_data.csv")
    return monthly, users, buildings, delays, non_completed

monthly_data, user_data, building_data, delays_data, non_completed_data = load_data()

st.set_page_config(layout="wide")
st.title("Tableau de bord KPI - HYSA")

# KPIs globaux
col1, col2 = st.columns(2)
with col1:
    st.metric("% global complétion", f"{monthly_data['Taux de complétion (%)'].mean():.2f}%")
with col2:
    moyenne_retard = delays_data['Retard (jours)'].mean()
    st.metric("Retard moyen (jours)", f"{moyenne_retard:.2f} j")

# Visualisation par mois
st.subheader("Taux de complétion par mois")
fig1 = px.bar(monthly_data, x="Mois_Année", y="Taux de complétion (%)", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

# Visualisation par utilisateur
st.subheader("Taux de complétion par utilisateur")
fig2 = px.bar(user_data, x="Nom utilisateur", y="Taux de complétion (%)", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)

# Visualisation par bâtiment
st.subheader("Taux de complétion par bâtiment")
fig3 = px.bar(building_data, x="Bâtiment", y="Taux de complétion (%)", text_auto=True)
st.plotly_chart(fig3, use_container_width=True)

# Analyse des retards
st.subheader("Distribution des retards")
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    utilisateur_sel = st.selectbox("Filtrer par utilisateur", ["Tous"] + delays_data["Nom utilisateur"].dropna().unique().tolist())
with col_filter2:
    batiment_sel = st.selectbox("Filtrer par bâtiment", ["Tous"] + delays_data["Bâtiment"].dropna().unique().tolist())

filtres = delays_data.copy()
if utilisateur_sel != "Tous":
    filtres = filtres[filtres["Nom utilisateur"] == utilisateur_sel]
if batiment_sel != "Tous":
    filtres = filtres[filtres["Bâtiment"] == batiment_sel]

fig4 = px.histogram(filtres, x="Retard (jours)", nbins=20, title="Histogramme des retards")
st.plotly_chart(fig4, use_container_width=True)

# BT non complétés
st.subheader("Liste des bons de travail non complétés")
st.dataframe(non_completed_data, use_container_width=True)
