# 🦷 DentalTreatmentDashboard

Dashboard interactif en Python pour l’analyse de traitements dentaires robotisés.

Ce projet a été réalisé dans le cadre d’un exercice de sélection, avec pour objectif de générer automatiquement un rapport visuel à partir de données issues d’un fichier CSV.

## 🎯 Objectif

Le but de cet exercice est de développer un script Python permettant de générer un dashboard visuel à partir d’un fichier CSV détaillant des traitements dentaires robotisés.

L'objectif est de créer un outil interactif qui facilite la lecture des données, met en lumière des relations intéressantes entre les variables et permet d'évaluer la qualité des traitements robotisés et la satisfaction des patients et des dentistes.

## 📁 Données exploitées

Le fichier CSV comporte les colonnes suivantes :

- **TreatmentID** : identifiant du traitement
- **NumberOfTeeth** : nombre de dents traitées
- **SetupDuration(sec)** : durée d'installation/configuration (en secondes)
- **TreatmentDuration(sec)** : durée du traitement (en secondes)
- **Interruptions** : nombre de pauses/interruptions
- **Errors** : nombre d’erreurs détectées
- **PatientRating** : note de satisfaction du patient (1 à 5)
- **DoctorRating** : note du praticien (1 à 5)

## 🛠️ Technologies utilisées

- Python 3.x
- Pandas
- Streamlit
- Plotly Express
- Seaborn
- Matplotlib

## 📊 Fonctionnalités du Dashboard

### 🔍 Barre latérale (sidebar)

#### Filtres interactifs :
- Note du patient (PatientRating)
- Nombre de dents traitées (NumberOfTeeth)

#### Options de visualisation :
- Afficher le jeu de données brut (option non affichée par défaut)
- Afficher les statistiques descriptives (option non affichée par défaut)

#### Visualisations par défaut :
- Histogramme de la durée du traitement
- Matrice de corrélation entre les variables
- Durée de traitement vs Nombre de dents traitées
- Durée de préparation vs Durée de traitement
- Interruptions vs Satisfaction patient
- Comparaison des notes patient / dentiste
- KPIs (indicateurs clés)
- Radar Chart (comparaison des indicateurs par traitement)
- Camembert de satisfaction des patients

## 🧠 Interface principale

### Aperçu des traitements filtrés

Liste dynamique en fonction des filtres sélectionnés.

#### Indicateurs clés (KPI) :
- Moyenne du nombre de dents traitées
- Moyenne des notes patient et dentiste
- Taux moyen d’interruptions

#### Visualisations interactives :
- 📌 Distribution de la durée de traitement
- 🔗 Corrélation entre les variables (heatmap)
- 📈 Durée de traitement vs Nombre de dents
- ⚠️ Interruptions/Erreurs vs Satisfaction patient
- 🧑‍⚕️ Boxplot PatientRating vs DoctorRating
- ⏱️ Durée de préparation vs Durée de traitement
- 🕸️ Radar - comparaison des indicateurs par traitement
- 🥧 Camembert des taux de satisfaction des patients

**Tous les graphiques sont dynamiques** :
➡️ Infos au survol, zoom, sélection à la souris...

## 🧪 Utilisation

### ▶️ Lancement local

1. Clone le projet :

```terminal
git clone https://github.com/chra03/DentalTreatmentDashboard.git
cd DentalTreatmentDashboard
```

2.Installe les dépendances :
```terminal
pip install -r requirements.txt
```

3.Lance l'application avec Streamlit :
```terminal
streamlit run dashboard1.py
```
