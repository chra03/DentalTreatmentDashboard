import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Rapport de Traitement Dentaire", layout="wide")

st.title("🦷 Rapport interactif sur les traitements dentaires robotisés")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("DataScienceTreatmentData.csv", sep=";")
    return df

df = load_data()

# Sidebar - Filtres utilisateur
st.sidebar.header("🎛️ Filtres interactifs")

note_min = st.sidebar.slider("Note minimale du patient", 1, 5, 3)
nb_dents = st.sidebar.slider(
    "Nombre de dents traitées",
    int(df['NumberOfTeeth'].min()),
    int(df['NumberOfTeeth'].max()),
    (4, 10)
)

# Application des filtres
df_filtered = df[
    (df["PatientRating"] >= note_min) &
    (df["NumberOfTeeth"].between(nb_dents[0], nb_dents[1]))
]


# Sélecteurs de visualisations
st.sidebar.subheader("📌 Sélection des graphiques à afficher")
show_data = st.sidebar.checkbox("Afficher le tableau des données", False)
show_stats = st.sidebar.checkbox("Afficher les stats descriptives", False)
show_hist = st.sidebar.checkbox("Histogramme durée traitement", True)
show_corr = st.sidebar.checkbox("Matrice de corrélation", True)
show_scatter_1 = st.sidebar.checkbox("Durée vs dents traitées", True)
show_scatter_2 = st.sidebar.checkbox("Durée de préparation vs Durée de traitement", True)
show_satisfaction = st.sidebar.checkbox("Interruptions vs satisfaction", True)
show_notes = st.sidebar.checkbox("Comparaison notes patient / dentiste", True)
show_kpi = st.sidebar.checkbox("KPI - Métriques clés", True)
show_radar = st.sidebar.checkbox("Toile d'araignée (Radar Chart)", True)
show_pie = st.sidebar.checkbox("Camembert des notes patient", True)

# Titre principal
st.markdown(f"###  {df_filtered.shape[0]} traitements affichés après filtrage")

# Affichage conditionnel
if show_data:
    st.subheader("📄 Aperçu des données")
    st.dataframe(df_filtered)

if show_stats:
    st.subheader("📊 Statistiques descriptives")
    st.write(df_filtered.describe())

if show_kpi:
    st.subheader("📊 Métriques Clés (KPI)")
    st.metric("Total traitements", df_filtered.shape[0])
    st.metric("Taux interruption moyen", f"{df_filtered['Interruptions'].mean():.2f}")
    st.metric("Note patient moyenne", f"{df_filtered['PatientRating'].mean():.2f}")
    st.metric("Note dentiste moyenne", f"{df_filtered['DoctorRating'].mean():.2f}")

if show_hist:
    st.subheader("⏱️ Durées des traitements")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_filtered["TreatmentDuration(sec)"], bins=10, kde=True, ax=ax)
    ax.set_title("Distribution de la durée des traitements")
    st.pyplot(fig)

if show_corr:
    st.subheader("🔍 Corrélation entre les variables")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df_filtered.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    
    # Rotation des labels X (en bas) et Y (à gauche)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    
    st.pyplot(fig)


if show_scatter_1:
    st.subheader("🦷 Durée vs Nombre de dents")
    # Filtrer les données pour enlever les lignes avec un PatientRating égal à 6
    df_filtered_no_6 = df_filtered[df_filtered["PatientRating"] != 6]
    
    # Créer le graphique avec les données filtrées
    fig = px.scatter(df_filtered_no_6, x="NumberOfTeeth", y="TreatmentDuration(sec)", color="PatientRating",
                     hover_data=["DoctorRating", "Interruptions"], title="Durée vs Dents")
    st.plotly_chart(fig)


if show_satisfaction:
    st.subheader("🚫 Interruptions/erreurs vs Satisfaction")
    fig = px.scatter(df_filtered, x="Interruptions", y="Errors", color="DoctorRating", size="PatientRating",
                     hover_data=["TreatmentID"], title="Satisfaction et erreurs")
    st.plotly_chart(fig)

if show_scatter_2:
    st.subheader("⏱️ Durée de préparation vs Durée de traitement")
    fig = px.scatter(df_filtered, x="SetupDuration(sec)", y="TreatmentDuration(sec)",
                     title="Relation entre la durée de préparation et la durée de traitement",
                     labels={"SetupDuration(sec)": "Durée de préparation (sec)",
                             "TreatmentDuration(sec)": "Durée du traitement (sec)"})
    st.plotly_chart(fig)    



# Radar chart : comparaison des indicateurs par traitement
st.subheader("🕸️ Radar - Comparaison des indicateurs par traitement")

# Choix d’un traitement
selected_id = st.selectbox("Choisissez un ID de traitement", df_filtered["TreatmentID"].unique())
selected_row = df_filtered[df_filtered["TreatmentID"] == selected_id].iloc[0]

# Variables à afficher
indicators = ["PatientRating", "DoctorRating", "Errors", "Interruptions", "NumberOfTeeth"]

# Récupération des valeurs brutes
values = [selected_row[ind] for ind in indicators]
values += values[:1]  # fermer la boucle

# Étiquettes correspondantes
theta = indicators + [indicators[0]]

# Création du radar avec échelle de 0 à 10
import plotly.graph_objects as go

fig = go.Figure(
    data=go.Scatterpolar(
        r=values,
        theta=theta,
        fill='toself',
        name=f"Traitement {selected_id}",
        marker_color='royalblue'
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 10],
            tickvals=list(range(0, 11, 2)),  # ticks de 0 à 10 tous les 2
            tickfont=dict(size=12)
        )
    ),
    showlegend=False,
    title=f"Radar des indicateurs pour le traitement {selected_id}"
)

st.plotly_chart(fig)



if show_pie:
    st.subheader("🥧 Répartition des notes des patients")

    # Pour le pie chart
    rating_counts = df_filtered["PatientRating"].value_counts().sort_index()

    # On supprime la valeur 6 si elle existe
    rating_counts = rating_counts[rating_counts.index != 6]

    total = rating_counts.sum()

    # Création du graphique avec Plotly
    fig = px.pie(
        names=rating_counts.index,
        values=rating_counts,
        labels={rating: f"Note {rating}" for rating in rating_counts.index},
        title="Distribution des notes des patients",
        hole=0.3,  # Optionnel, pour un camembert "doughnut"
        color=rating_counts.index,  # Couleurs distinctes pour chaque note
        color_discrete_sequence=sns.color_palette("pastel").as_hex(),  # Palette pastel
        hover_data=[rating_counts.index, rating_counts]  # Afficher le nombre et pourcentage au survol
    )

    # Mettre à jour les labels pour afficher les pourcentages
    fig.update_traces(
        hovertemplate='%{label}: %{percent:.2%}<br>Nombre: %{value}<br>Pourcentage: %{percent:.2%}'
    )

    st.plotly_chart(fig)

if show_notes:
    st.subheader("🧾 Note patient vs dentiste")
    fig = px.box(df_filtered.melt(value_vars=["PatientRating", "DoctorRating"]),
                 x="variable", y="value", title="Comparaison des notes patient / dentiste")
    st.plotly_chart(fig)