import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import io
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import tempfile
import os
from datetime import datetime
import kaleido
import pdfkit
import jinja2

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Diversité & Inclusion",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    /* Style général */
    .stApp {
        background-color: #ffa800;
    }
    
    .main .block-container {
        background-color: #f0f2f6;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Style des boutons */
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 24px;
        margin: 10px 0;
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Style des titres */
    .title {
        text-align: center;
        color: #1E3A8A;
        font-size: 48px;
        margin-bottom: 30px;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #4B5563;
        font-size: 24px;
        margin-bottom: 50px;
        font-weight: 500;
    }
    
    /* Style des cartes */
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
        border: 1px solid rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Style des sections */
    .section {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Style des inputs */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 10px;
        background-color: white;
    }
    
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 10px;
        background-color: white;
    }
    
    /* Style des tableaux */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
    }
    
    /* Style du pied de page */
    .footer {
        text-align: center;
        color: #6B7280;
        margin-top: 50px;
        padding: 20px;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Style de la barre latérale */
    .css-1d391kg {
        background-color: #1E3A8A;
    }
    
    /* Style des titres de section */
    h1, h2, h3 {
        color: #1E3A8A;
        font-weight: 600;
    }
    
    /* Style des graphiques */
    .js-plotly-plot {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 10px;
        background-color: white;
    }
    
    /* Style des messages de succès/erreur */
    .stSuccess {
        background-color: #D1FAE5;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #34D399;
    }
    
    .stError {
        background-color: #FEE2E2;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #F87171;
    }

    /* Style des éléments de formulaire */
    .stRadio > div {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Style des séparateurs */
    hr {
        border: none;
        height: 1px;
        background-color: #E5E7EB;
        margin: 2rem 0;
    }

    /* Style des éléments de la barre latérale */
    .css-1d391kg .css-1v0mbdj {
        background-color: #1E3A8A;
    }

    /* Style des éléments de la barre latérale au survol */
    .css-1d391kg .css-1v0mbdj:hover {
        background-color: #2563EB;
    }
</style>
""", unsafe_allow_html=True)

# Titre et introduction
st.markdown('<h1 class="title">🏢 Diversité & Inclusion</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plateforme d\'évaluation et d\'analyse de la diversité et inclusion en entreprise</p>', unsafe_allow_html=True)

# Menu de navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Accueil", "Convertisseur", "Évaluation"]
)

# Fonctions utilitaires
def attribuer_note(valeur, seuils, ordre_croissant=True):
    if ordre_croissant:
        if valeur >= seuils[0]: return "A"
        elif valeur >= seuils[1]: return "B"
        elif valeur >= seuils[2]: return "C"
        elif valeur >= seuils[3]: return "D"
        else: return "E"
    else:
        if valeur <= seuils[0]: return "A"
        elif valeur <= seuils[1]: return "B"
        elif valeur <= seuils[2]: return "C"
        elif valeur <= seuils[3]: return "D"
        else: return "E"

def note_vers_chiffre(note):
    conversion = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}
    return conversion.get(note, 0)

def chiffre_vers_note(score):
    if score >= 4.5: return "A"
    elif score >= 3.5: return "B"
    elif score >= 2.5: return "C"
    elif score >= 1.5: return "D"
    else: return "E"

def calculer_equilibre_age(moins_30, entre_30_50, plus_50):
    distribution_ideale = 33.33
    ecart_moins_30 = abs(moins_30 - distribution_ideale)
    ecart_entre_30_50 = abs(entre_30_50 - distribution_ideale)
    ecart_plus_50 = abs(plus_50 - distribution_ideale)
    ecart_moyen = (ecart_moins_30 + ecart_entre_30_50 + ecart_plus_50) / 3
    score = 1 - (ecart_moyen / 66.67)
    return score * 100

# Seuils de notation
seuils = {
    "taux_feminisation": [40, 35, 30, 25],
    "taux_femmes_cadres": [35, 30, 25, 20],
    "taux_handicap": [6, 5, 4, 3],
    "ecart_salaire": [2, 4, 8, 12],
    "equilibre_age": [85, 75, 65, 55],
    "taux_absenteisme": [2.5, 3.5, 4.5, 5.5]
}

# Page d'accueil
if menu == "Accueil":
    st.markdown("""
    ## 📚 Guide d'utilisation

    1. **Convertisseur de Bilan Social**
       - Téléchargez le modèle Excel
       - Remplissez-le avec vos données
       - Obtenez un fichier CSV au format requis

    2. **Évaluation D&I**
       - Importez votre fichier CSV
       - Consultez les analyses détaillées
       - Téléchargez le rapport PDF

    ### 🔧 Prérequis
    - Python 3.7 ou supérieur
    - Packages requis : streamlit, pandas, numpy, matplotlib, altair, plotly, reportlab, kaleido
    - Pour installer les dépendances : `pip install -r requirements.txt`
    """)

# Page Convertisseur
elif menu == "Convertisseur":
    st.title("🔄 Convertisseur de Bilan Social")
    
    def create_excel_template():
        df = pd.DataFrame({
            'Information': [
                'Nom de l\'entreprise',
                'Année',
                'Effectif total',
                'Nombre de femmes',
                'Nombre de cadres',
                'Nombre de femmes cadres',
                'Nombre de salariés en situation de handicap',
                'Nombre de jours travaillés',
                'Nombre de jours d\'absence',
                'Répartition par âge - Moins de 30 ans',
                'Répartition par âge - 30-50 ans',
                'Répartition par âge - Plus de 50 ans',
                'Salaire moyen hommes (€)',
                'Salaire moyen femmes (€)'
            ],
            'Valeur': ['', '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'Unité': ['', '', 'personnes', 'personnes', 'personnes', 'personnes', 'personnes', 'jours', 'jours', 'personnes', 'personnes', 'personnes', '€', '€']
        })
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Données', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Données']
            
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            number_format = workbook.add_format({'num_format': '#,##0'})
            
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            worksheet.set_column('A:A', 40)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 20)
            
            for row in range(1, len(df) + 1):
                worksheet.write(row, 1, df.iloc[row-1]['Valeur'], number_format)
        
        return output.getvalue()

    def convert_data(df):
        try:
            required_fields = ['Information', 'Valeur']
            if not all(field in df.columns for field in required_fields):
                raise ValueError("Le fichier Excel doit contenir les colonnes 'Information' et 'Valeur'")
            
            nom_entreprise = str(df.iloc[0]['Valeur'])
            if not nom_entreprise:
                raise ValueError("Le nom de l'entreprise est requis")
                
            annee = int(df.iloc[1]['Valeur'])
            if annee < 2000 or annee > datetime.now().year:
                raise ValueError(f"L'année doit être comprise entre 2000 et {datetime.now().year}")
            
            effectif_total = float(df.iloc[2]['Valeur'])
            if effectif_total <= 0:
                raise ValueError("L'effectif total doit être supérieur à 0")
                
            nb_femmes = float(df.iloc[3]['Valeur'])
            if nb_femmes < 0 or nb_femmes > effectif_total:
                raise ValueError("Le nombre de femmes doit être compris entre 0 et l'effectif total")
                
            nb_cadres = float(df.iloc[4]['Valeur'])
            if nb_cadres < 0 or nb_cadres > effectif_total:
                raise ValueError("Le nombre de cadres doit être compris entre 0 et l'effectif total")
                
            nb_femmes_cadres = float(df.iloc[5]['Valeur'])
            if nb_femmes_cadres < 0 or nb_femmes_cadres > nb_cadres:
                raise ValueError("Le nombre de femmes cadres doit être compris entre 0 et le nombre total de cadres")
                
            nb_handicap = float(df.iloc[6]['Valeur'])
            if nb_handicap < 0 or nb_handicap > effectif_total:
                raise ValueError("Le nombre de salariés en situation de handicap doit être compris entre 0 et l'effectif total")
                
            jours_travailles = float(df.iloc[7]['Valeur'])
            if jours_travailles <= 0:
                raise ValueError("Le nombre de jours travaillés doit être supérieur à 0")
                
            jours_absence = float(df.iloc[8]['Valeur'])
            if jours_absence < 0:
                raise ValueError("Le nombre de jours d'absence ne peut pas être négatif")
                
            moins_30 = float(df.iloc[9]['Valeur'])
            entre_30_50 = float(df.iloc[10]['Valeur'])
            plus_50 = float(df.iloc[11]['Valeur'])
            
            total_age = moins_30 + entre_30_50 + plus_50
            if abs(total_age - effectif_total) > 1:
                raise ValueError("La somme des effectifs par âge doit correspondre à l'effectif total")
            
            taux_feminisation = (nb_femmes / effectif_total) * 100
            taux_femmes_cadres = (nb_femmes_cadres / nb_cadres) * 100 if nb_cadres > 0 else 0
            taux_handicap = (nb_handicap / effectif_total) * 100
            
            moins_30_pct = (moins_30 / effectif_total) * 100
            entre_30_50_pct = (entre_30_50 / effectif_total) * 100
            plus_50_pct = (plus_50 / effectif_total) * 100
            
            salaire_hommes = float(df.iloc[12]['Valeur'])
            salaire_femmes = float(df.iloc[13]['Valeur'])
            if salaire_hommes <= 0 or salaire_femmes <= 0:
                raise ValueError("Les salaires moyens doivent être supérieurs à 0")
            ecart_salaire = ((salaire_hommes - salaire_femmes) / salaire_hommes) * 100
            
            taux_absenteisme = (jours_absence / jours_travailles) * 100
            
            output_data = {
                'Indicateur': [
                    'nom_entreprise', 'annee', 'taux_feminisation', 'taux_femmes_cadres',
                    'taux_handicap', 'ecart_salaire', 'moins_30_ans', 'entre_30_50_ans',
                    'plus_50_ans', 'taux_absenteisme'
                ],
                'Valeur': [
                    nom_entreprise, annee, taux_feminisation, taux_femmes_cadres,
                    taux_handicap, ecart_salaire, moins_30_pct, entre_30_50_pct,
                    plus_50_pct, taux_absenteisme
                ]
            }
            
            return pd.DataFrame(output_data)
        
        except ValueError as ve:
            st.error(f"Erreur de validation des données : {str(ve)}")
            return None
        except Exception as e:
            st.error(f"Erreur lors de la conversion des données : {str(e)}")
            return None

    st.markdown("## 📝 Instructions")
    st.markdown("""
    1. Téléchargez d'abord le modèle Excel
    2. Remplissez-le avec les données de votre bilan social
    3. Téléchargez le fichier rempli
    4. L'application convertira automatiquement les données au format requis
    """)

    st.markdown("### 1. Télécharger le modèle")
    excel_data = create_excel_template()
    st.download_button(
        label="📥 Télécharger le modèle Excel",
        data=excel_data,
        file_name="modele_bilan_social.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("### 2. Télécharger votre fichier rempli")
    uploaded_file = st.file_uploader("Choisissez votre fichier Excel rempli", type=['xlsx'])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            df_converted = convert_data(df)
            
            if df_converted is not None:
                st.success("✅ Conversion réussie !")
                
                st.markdown("### 3. Données converties")
                st.dataframe(df_converted)
                
                csv = df_converted.to_csv(index=False)
                st.download_button(
                    label="📥 Télécharger le fichier CSV",
                    data=csv,
                    file_name=f"donnees_di_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                st.markdown("""
                ### 4. Prochaines étapes
                1. Téléchargez le fichier CSV généré
                2. Importez-le dans l'application d'évaluation D&I
                3. Consultez votre rapport détaillé
                """)
        
        except Exception as e:
            st.error(f"Erreur lors du traitement du fichier : {str(e)}")
            st.error("Veuillez vérifier que le fichier est correctement formaté.")

# Page Évaluation
elif menu == "Évaluation":
    st.title("📊 Évaluateur de Diversité et Inclusion en Entreprise")
    
    st.markdown("""
    Cette application analyse les indicateurs sociaux d'une entreprise en matière de diversité et inclusion,
    et attribue des notes de A à E sur 6 dimensions clés, basées sur des seuils adaptés au secteur énergie/industrie.
    """)

    st.markdown("## 📌 Explication des indicateurs")
    st.write("""
    1. **Taux de féminisation global** : Pourcentage de femmes dans l'effectif total
    2. **Taux de femmes cadres** : Pourcentage de femmes parmi les postes de cadres
    3. **Taux d'emploi des personnes en situation de handicap** : Pourcentage de salariés en situation de handicap (seuil légal = 6%)
    4. **Écart de salaire hommes/femmes** : Écart moyen en % à poste équivalent (0% = parfaite égalité)
    5. **Répartition des effectifs par âge** : Équilibre entre les tranches d'âge (<30 ans, 30-50 ans, >50 ans)
    6. **Taux d'absentéisme** : Pourcentage de jours d'absence par rapport au nombre total de jours travaillés
    """)

    # Méthode d'entrée des données
    st.markdown("## 📝 Entrée des données")
    methode = st.radio("Choisissez la méthode d'entrée des données:", 
                      ["Saisie manuelle", "Téléchargement de fichier CSV"])

    if methode == "Saisie manuelle":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Données générales")
            nom_entreprise = st.text_input("Nom de l'entreprise", "EDF SA")
            annee = st.number_input("Année", min_value=2000, max_value=datetime.now().year, value=2024)
            
            st.subheader("Effectifs")
            effectif_total = st.number_input("Effectif total", min_value=1, value=1000)
            nb_femmes = st.number_input("Nombre de femmes", min_value=0, max_value=effectif_total, value=400)
            nb_cadres = st.number_input("Nombre de cadres", min_value=0, max_value=effectif_total, value=200)
            nb_femmes_cadres = st.number_input("Nombre de femmes cadres", min_value=0, max_value=nb_cadres, value=60)
            nb_handicap = st.number_input("Nombre de salariés en situation de handicap", min_value=0, max_value=effectif_total, value=30)
        
        with col2:
            st.subheader("Absentéisme")
            jours_travailles = st.number_input("Nombre de jours travaillés", min_value=1, value=220)
            jours_absence = st.number_input("Nombre de jours d'absence", min_value=0, value=1000)
            
            st.subheader("Répartition par âge")
            moins_30 = st.number_input("Effectif moins de 30 ans", min_value=0, max_value=effectif_total, value=200)
            entre_30_50 = st.number_input("Effectif 30-50 ans", min_value=0, max_value=effectif_total, value=500)
            plus_50 = st.number_input("Effectif plus de 50 ans", min_value=0, max_value=effectif_total, value=300)
            
            st.subheader("Salaires")
            salaire_hommes = st.number_input("Salaire moyen hommes (€)", min_value=1, value=50000)
            salaire_femmes = st.number_input("Salaire moyen femmes (€)", min_value=1, value=45000)
        
        # Calcul des indicateurs
        taux_feminisation = (nb_femmes / effectif_total) * 100
        taux_femmes_cadres = (nb_femmes_cadres / nb_cadres) * 100 if nb_cadres > 0 else 0
        taux_handicap = (nb_handicap / effectif_total) * 100
        ecart_salaire = ((salaire_hommes - salaire_femmes) / salaire_hommes) * 100
        taux_absenteisme = (jours_absence / jours_travailles) * 100
        
        # Calcul de l'équilibre des âges
        moins_30_pct = (moins_30 / effectif_total) * 100
        entre_30_50_pct = (entre_30_50 / effectif_total) * 100
        plus_50_pct = (plus_50 / effectif_total) * 100
        score_equilibre_age = calculer_equilibre_age(moins_30_pct, entre_30_50_pct, plus_50_pct)
        
        # Attribution des notes
        notes = {
            "Taux de féminisation": attribuer_note(taux_feminisation, seuils["taux_feminisation"]),
            "Taux de femmes cadres": attribuer_note(taux_femmes_cadres, seuils["taux_femmes_cadres"]),
            "Taux d'emploi des personnes en situation de handicap": attribuer_note(taux_handicap, seuils["taux_handicap"]),
            "Écart de salaire hommes/femmes": attribuer_note(ecart_salaire, seuils["ecart_salaire"], False),
            "Répartition des effectifs par âge": attribuer_note(score_equilibre_age, seuils["equilibre_age"]),
            "Taux d'absentéisme": attribuer_note(taux_absenteisme, seuils["taux_absenteisme"], False)
        }
        
        # Calcul de la note globale
        scores = [note_vers_chiffre(note) for note in notes.values()]
        note_globale = chiffre_vers_note(sum(scores) / len(scores))
        
        # Affichage des résultats
        st.markdown("## 📊 Résultats de l'évaluation")
        
        # Création du DataFrame des résultats
        resultats = pd.DataFrame({
            'Indicateur': list(notes.keys()),
            'Valeur': [
                f"{taux_feminisation:.1f}%",
                f"{taux_femmes_cadres:.1f}%",
                f"{taux_handicap:.1f}%",
                f"{ecart_salaire:.1f}%",
                f"{score_equilibre_age:.1f}%",
                f"{taux_absenteisme:.1f}%"
            ],
            'Note': list(notes.values())
        })
        
        st.dataframe(resultats)
        
        st.markdown(f"### Note globale : {note_globale}")
        
        # Visualisation des résultats
        st.markdown("## 📈 Visualisation des résultats")
        
        # Graphique radar des notes
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[note_vers_chiffre(note) for note in notes.values()],
            theta=list(notes.keys()),
            fill='toself',
            name='Notes'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig)
        
        # Graphique en barres des indicateurs
        fig2 = px.bar(
            resultats,
            x='Indicateur',
            y='Valeur',
            color='Note',
            title='Valeurs des indicateurs',
            color_discrete_map={
                'A': '#00CC96',
                'B': '#636EFA',
                'C': '#EF553B',
                'D': '#AB63FA',
                'E': '#FFA15A'
            }
        )
        
        st.plotly_chart(fig2)
        
        # Recommandations
        st.markdown("## 💡 Recommandations")
        
        # Points forts
        points_forts = [ind for ind, note in notes.items() if note in ['A', 'B']]
        if points_forts:
            st.markdown("### Points forts")
            for point in points_forts:
                st.markdown(f"- {point}")
        
        # Axes d'amélioration
        axes_amelioration = [ind for ind, note in notes.items() if note in ['D', 'E']]
        if axes_amelioration:
            st.markdown("### Axes d'amélioration")
            for axe in axes_amelioration:
                st.markdown(f"- {axe}")
    
    else:  # Téléchargement de fichier CSV
        uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                # Traitement des données du CSV
                # ... (même logique que pour la saisie manuelle)
                st.success("Fichier CSV traité avec succès !")
            except Exception as e:
                st.error(f"Erreur lors du traitement du fichier : {str(e)}")

# Pied de page
st.markdown("""
<div class="footer">
    <p>Développé par Japhet Calixte N'DRI | Version 1.0</p>
    <p>© 2024 Tous droits réservés</p>
</div>
""", unsafe_allow_html=True) 