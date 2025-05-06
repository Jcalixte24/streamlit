@echo off
echo Installation des dependances...
pip install -r requirements.txt

echo.
echo Lancement de l'application...
streamlit run main.py

pause 