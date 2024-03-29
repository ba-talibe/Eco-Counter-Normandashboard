@echo off


if not exist env (
    echo Création de l'environnement virtuel...
    python -m venv env
)


call env\Scripts\activate.bat


echo Mise à jour du dépôt git...
git pull


echo Rendre le script start_up.sh exécutable...
icacls start_up.sh /grant:r "%username%":(RX)


deactivate

echo Configuration terminée.
