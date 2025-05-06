# Application Diversité & Inclusion

Cette application permet d'évaluer et d'analyser la diversité et l'inclusion dans une entreprise.

## Prérequis

- Python 3.9 ou supérieur
- Git (pour cloner le dépôt)
- wkhtmltopdf (pour la génération de PDF)

## Installation automatique (Windows)

1. Double-cliquez sur le fichier `install.bat`
2. Attendez que l'installation se termine
3. Lancez l'application avec la commande : `streamlit run main.py`

## Installation manuelle

1. Créez un environnement virtuel :
```bash
python -m venv venv
```

2. Activez l'environnement virtuel :
- Windows :
```bash
venv\Scripts\activate
```
- Linux/Mac :
```bash
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Installez wkhtmltopdf :
- Windows : Téléchargez et installez depuis https://wkhtmltopdf.org/downloads.html
- Linux :
```bash
sudo apt-get install wkhtmltopdf
```
- Mac :
```bash
brew install wkhtmltopdf
```

## Lancement de l'application

1. Activez l'environnement virtuel si ce n'est pas déjà fait
2. Exécutez la commande :
```bash
streamlit run main.py
```

## Structure du projet

- `main.py` : Page d'accueil de l'application
- `pages/1_Convertisseur.py` : Outil de conversion des données
- `pages/2_Evaluation.py` : Module d'évaluation D&I
- `.streamlit/config.toml` : Configuration de l'application
- `requirements.txt` : Liste des dépendances Python

## Dépendances principales

- streamlit==1.32.0
- pandas==2.2.1
- numpy==1.26.4
- plotly==5.19.0
- pdfkit==1.0.0
- Jinja2==3.1.3
- python-dotenv==1.0.1
- openpyxl==3.1.2
- matplotlib==3.8.3
- altair==5.2.0
- reportlab==4.1.0
- kaleido==0.2.1

## Développé par

Japhet Calixte N'DRI
Version 1.0 