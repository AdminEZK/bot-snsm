#!/bin/bash
# Script de test pour le bulletin météo/mer

echo "🧪 Test du bulletin météo/mer SNSM"
echo "=================================="
echo ""

# Vérifier que Python 3 est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérifier que le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Le fichier .env n'existe pas"
    echo "📝 Copiez .env.example vers .env et remplissez les clés API"
    exit 1
fi

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances Python..."
pip3 install -r requirements.txt --quiet

echo ""
echo "🚀 Exécution du bulletin..."
echo "=================================="
echo ""

# Exécuter le script
python3 weather_bulletin.py

echo ""
echo "=================================="
echo "✅ Test terminé"
