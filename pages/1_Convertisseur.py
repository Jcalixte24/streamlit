import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io

# Configuration de la page
st.set_page_config(
    page_title="Convertisseur de Bilan Social",
    page_icon="📊",
    layout="wide"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .title {
        text-align: center;
        color: #1E3A8A;
        font-size: 36px;
        margin-bottom: 20px;
    }
    .subtitle {
        text-align: center;
        color: #4B5563;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .footer {
        text-align: center;
        color: #6B7280;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# Titre et introduction
st.markdown('<h1 class="title">📊 Convertisseur de Bilan Social</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transformez vos données de bilan social au format requis pour l\'évaluation</p>', unsafe_allow_html=True)

def create_excel_template():
    """Crée un modèle Excel avec les colonnes requises"""
    template_data = {
        'Indicateur': [
            'Effectif total',
            'Effectif femmes',
            'Effectif hommes',
            'Effectif femmes cadres',
            'Effectif hommes cadres',
            'Effectif handicapés',
            'Effectif non-handicapés',
            'Moyenne salaire femmes',
            'Moyenne salaire hommes',
            'Effectif < 30 ans',
            'Effectif 30-50 ans',
            'Effectif > 50 ans',
            'Jours d\'absence',
            'Nom entreprise',
            'Année'
        ],
        'Valeur': [''] * 15,
        'Description': [
            'Nombre total d\'employés',
            'Nombre d\'employées femmes',
            'Nombre d\'employés hommes',
            'Nombre d\'employées femmes cadres',
            'Nombre d\'employés hommes cadres',
            'Nombre d\'employés en situation de handicap',
            'Nombre d\'employés non-handicapés',
            'Salaire moyen des femmes (en euros)',
            'Salaire moyen des hommes (en euros)',
            'Nombre d\'employés de moins de 30 ans',
            'Nombre d\'employés entre 30 et 50 ans',
            'Nombre d\'employés de plus de 50 ans',
            'Nombre total de jours d\'absence',
            'Nom de l\'entreprise',
            'Année du bilan social'
        ]
    }
    return pd.DataFrame(template_data)

def calculate_indicators(df):
    """Calcule les indicateurs à partir des données brutes"""
    # Création d'un dictionnaire pour stocker les valeurs
    indicators = {}
    
    try:
        # Vérification que toutes les colonnes requises sont présentes
        required_indicators = [
            'Effectif total', 'Effectif femmes', 'Effectif hommes',
            'Effectif femmes cadres', 'Effectif hommes cadres',
            'Effectif handicapés', 'Moyenne salaire femmes', 'Moyenne salaire hommes',
            'Effectif < 30 ans', 'Effectif 30-50 ans', 'Effectif > 50 ans',
            'Jours d\'absence', 'Nom entreprise', 'Année'
        ]
        
        # Vérification des indicateurs présents
        missing_indicators = []
        for indicator in required_indicators:
            if indicator not in df['Indicateur'].values:
                missing_indicators.append(indicator)
        
        if missing_indicators:
            raise ValueError(f"Indicateurs manquants dans le fichier : {', '.join(missing_indicators)}")
        
        # Récupération des valeurs de base avec vérification
        def get_value(indicator_name):
            value = df[df['Indicateur'] == indicator_name]['Valeur'].values
            if len(value) == 0:
                raise ValueError(f"Valeur manquante pour l'indicateur : {indicator_name}")
            try:
                return float(value[0])
            except (ValueError, TypeError):
                raise ValueError(f"Valeur invalide pour l'indicateur {indicator_name} : {value[0]}")
        
        # Récupération des valeurs textuelles
        def get_text_value(indicator_name):
            value = df[df['Indicateur'] == indicator_name]['Valeur'].values
            if len(value) == 0:
                raise ValueError(f"Valeur manquante pour l'indicateur : {indicator_name}")
            return str(value[0])
        
        # Récupération des valeurs numériques
        total = get_value('Effectif total')
        femmes = get_value('Effectif femmes')
        hommes = get_value('Effectif hommes')
        femmes_cadres = get_value('Effectif femmes cadres')
        hommes_cadres = get_value('Effectif hommes cadres')
        total_cadres = femmes_cadres + hommes_cadres
        handicapes = get_value('Effectif handicapés')
        salaire_femmes = get_value('Moyenne salaire femmes')
        salaire_hommes = get_value('Moyenne salaire hommes')
        moins_30 = get_value('Effectif < 30 ans')
        entre_30_50 = get_value('Effectif 30-50 ans')
        plus_50 = get_value('Effectif > 50 ans')
        absences = get_value('Jours d\'absence')
        
        # Récupération des valeurs textuelles
        nom_entreprise = get_text_value('Nom entreprise')
        annee = get_text_value('Année')
        
        # Vérification de la cohérence des données
        if total != (femmes + hommes):
            st.warning("Attention : La somme des effectifs femmes et hommes ne correspond pas à l'effectif total")
        
        if total != (moins_30 + entre_30_50 + plus_50):
            st.warning("Attention : La somme des effectifs par tranche d'âge ne correspond pas à l'effectif total")
        
        if femmes_cadres > femmes:
            st.warning("Attention : Le nombre de femmes cadres est supérieur au nombre total de femmes")
        
        if hommes_cadres > hommes:
            st.warning("Attention : Le nombre d'hommes cadres est supérieur au nombre total d'hommes")
        
        # Calcul des indicateurs
        indicators['nom_entreprise'] = nom_entreprise
        indicators['annee'] = annee
        indicators['taux_feminisation'] = round((femmes / total) * 100, 1)
        indicators['taux_femmes_cadres'] = round((femmes_cadres / total_cadres) * 100, 1) if total_cadres > 0 else 0
        indicators['taux_handicap'] = round((handicapes / total) * 100, 1)
        indicators['ecart_salaire'] = round(((salaire_hommes - salaire_femmes) / salaire_hommes) * 100, 1)
        indicators['moins_30_ans'] = round((moins_30 / total) * 100, 1)
        indicators['entre_30_50_ans'] = round((entre_30_50 / total) * 100, 1)
        indicators['plus_50_ans'] = round((plus_50 / total) * 100, 1)
        indicators['taux_absenteisme'] = round((absences / (total * 220)) * 100, 1)  # 220 jours ouvrables par an
        
        return indicators
        
    except Exception as e:
        st.error(f"Erreur lors du calcul des indicateurs : {str(e)}")
        return None

# Création et téléchargement du modèle Excel
st.markdown("### 📥 Télécharger le modèle")
st.markdown("""
1. Téléchargez le modèle Excel ci-dessous
2. Remplissez-le avec vos données
3. Revenez sur cette page pour convertir votre fichier
""")

template_df = create_excel_template()
excel_buffer = io.BytesIO()
template_df.to_excel(excel_buffer, index=False)
excel_data = excel_buffer.getvalue()

st.download_button(
    label="📥 Télécharger le modèle Excel",
    data=excel_data,
    file_name="modele_bilan_social.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Upload du fichier
st.markdown("### 📤 Convertir votre fichier")
st.markdown("""
1. Sélectionnez votre fichier Excel rempli
2. Cliquez sur 'Convertir'
3. Téléchargez le fichier CSV généré
""")

uploaded_file = st.file_uploader("Choisissez votre fichier Excel", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(uploaded_file)
        
        # Vérification des colonnes requises
        required_columns = ['Indicateur', 'Valeur']
        if not all(col in df.columns for col in required_columns):
            st.error("Le fichier doit contenir les colonnes 'Indicateur' et 'Valeur'")
        else:
            # Calcul des indicateurs
            indicators = calculate_indicators(df)
            
            if indicators is not None:
                # Création du DataFrame final
                final_df = pd.DataFrame(list(indicators.items()), columns=['Indicateur', 'Valeur'])
                
                # Conversion en CSV
                csv = final_df.to_csv(index=False)
                
                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger le fichier CSV",
                    data=csv,
                    file_name="bilan_social.csv",
                    mime="text/csv"
                )
                
                # Affichage des données
                st.markdown("### 📊 Aperçu des données")
                st.dataframe(final_df)
            
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la conversion : {str(e)}")

# Pied de page
st.markdown("""
<div class="footer">
    <p>Développé par Japhet Calixte N'DRI | Version 1.0</p>
    <p>© 2024 Tous droits réservés</p>
</div>
""", unsafe_allow_html=True) 
