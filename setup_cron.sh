#!/bin/bash
# Script d'installation du cron job pour le bulletin météo/mer SNSM

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌊 Installation du cron job - Bulletin Météo/Mer SNSM${NC}\n"

# Récupérer le chemin absolu du répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/weather_bulletin.py"

# Vérifier que Python 3 est installé
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    exit 1
fi

# Vérifier que le script Python existe
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}❌ Le script weather_bulletin.py n'existe pas${NC}"
    exit 1
fi

# Rendre le script Python exécutable
chmod +x "$PYTHON_SCRIPT"

# Créer la ligne cron (tous les jours à 7h30)
CRON_LINE="30 7 * * * cd $SCRIPT_DIR && /usr/bin/python3 $PYTHON_SCRIPT >> $SCRIPT_DIR/weather_bulletin.log 2>&1"

# Vérifier si le cron existe déjà
if crontab -l 2>/dev/null | grep -q "weather_bulletin.py"; then
    echo -e "${BLUE}ℹ️  Un cron job existe déjà pour ce script${NC}"
    echo -e "${BLUE}Voulez-vous le remplacer ? (o/n)${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Oo]$ ]]; then
        echo -e "${RED}❌ Installation annulée${NC}"
        exit 0
    fi
    # Supprimer l'ancien cron
    crontab -l 2>/dev/null | grep -v "weather_bulletin.py" | crontab -
fi

# Ajouter le nouveau cron job
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

echo -e "${GREEN}✅ Cron job installé avec succès !${NC}\n"
echo -e "${BLUE}📅 Le bulletin sera envoyé tous les jours à 7h30${NC}"
echo -e "${BLUE}📝 Les logs seront dans : $SCRIPT_DIR/weather_bulletin.log${NC}\n"

# Afficher les cron jobs actuels
echo -e "${BLUE}📋 Cron jobs actuels :${NC}"
crontab -l

echo -e "\n${GREEN}🎉 Installation terminée !${NC}"
echo -e "${BLUE}💡 Pour tester manuellement : python3 $PYTHON_SCRIPT${NC}"
