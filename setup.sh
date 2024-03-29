#!/bin/bash

if [ ! -d "env" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv env
fi

source env/bin/activate

echo "Mise à jour du dépôt git..."
git pull


chmod +x start_up.sh


deactivate

echo "Configuration terminée."
