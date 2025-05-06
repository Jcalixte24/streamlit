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
            'Effectif handicapés',
            'Effectif non-handicapés',
            'Moyenne salaire femmes',
            'Moyenne salaire hommes',
            'Effectif < 30 ans',
            'Effectif 30-50 ans',
            'Effectif > 50 ans',
            'Jours d\'absence'
        ],
        'Valeur': [''] * 11,
        'Description': [
            'Nombre total d\'employés',
            'Nombre d\'employées femmes',
            'Nombre d\'employés hommes',
            'Nombre d\'employés en situation de handicap',
            'Nombre d\'employés non-handicapés',
            'Salaire moyen des femmes (en euros)',
            'Salaire moyen des hommes (en euros)',
            'Nombre d\'employés de moins de 30 ans',
            'Nombre d\'employés entre 30 et 50 ans',
            'Nombre d\'employés de plus de 50 ans',
            'Nombre total de jours d\'absence'
        ]
    }
    return pd.DataFrame(template_data)

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
            # Conversion en CSV
            csv = df.to_csv(index=False)
            
            # Bouton de téléchargement
            st.download_button(
                label="📥 Télécharger le fichier CSV",
                data=csv,
                file_name="bilan_social.csv",
                mime="text/csv"
            )
            
            # Affichage des données
            st.markdown("### 📊 Aperçu des données")
            st.dataframe(df)
            
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la conversion : {str(e)}")

# Pied de page
st.markdown("""
<div class="footer">
    <p>Développé par Japhet Calixte N'DRI | Version 1.0</p>
    <p>© 2024 Tous droits réservés</p>
</div>
""", unsafe_allow_html=True) 