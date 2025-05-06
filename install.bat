@echo off
echo Installation des dépendances pour l'application Diversité & Inclusion...

:: Création d'un environnement virtuel
python -m venv venv
call venv\Scripts\activate

:: Installation des packages Python
pip install streamlit==1.32.0
pip install pandas==2.2.1
pip install numpy==1.26.4
pip install plotly==5.19.0
pip install pdfkit==1.0.0
pip install Jinja2==3.1.3
pip install python-dotenv==1.0.1
pip install openpyxl==3.1.2
pip install matplotlib==3.8.3
pip install altair==5.2.0
pip install reportlab==4.1.0
pip install kaleido==0.2.1

:: Installation de wkhtmltopdf (nécessaire pour pdfkit)
echo Téléchargement de wkhtmltopdf...
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.msvc2015-win64.exe' -OutFile 'wkhtmltox-installer.exe'}"
echo Installation de wkhtmltopdf...
wkhtmltox-installer.exe /S

:: Nettoyage
del wkhtmltox-installer.exe

echo Installation terminée !
echo Pour lancer l'application, exécutez : streamlit run main.py
pause 