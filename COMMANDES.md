# 📋 Commandes Utiles - Bulletin Météo/Mer

## 🚀 Installation

```bash
# 1. Installer les dépendances Python
pip3 install -r requirements.txt

# 2. Configurer les variables d'environnement
cp .env.example .env
nano .env  # ou vim, code, etc.

# 3. Vérifier la configuration
./check_setup.py

# 4. Tester le bulletin
./test_bulletin.sh

# 5. Installer le cron (envoi automatique à 7h30)
./setup_cron.sh
```

## 🧪 Tests

```bash
# Test complet avec vérification des dépendances
./test_bulletin.sh

# Test direct du script Python
python3 weather_bulletin.py

# Vérifier la configuration
./check_setup.py

# Test avec affichage détaillé
python3 -v weather_bulletin.py
```

## ⏰ Gestion du Cron

```bash
# Installer le cron automatiquement
./setup_cron.sh

# Lister les cron jobs actifs
crontab -l

# Éditer manuellement le cron
crontab -e

# Supprimer tous les cron jobs
crontab -r

# Supprimer uniquement le bulletin météo
crontab -l | grep -v "weather_bulletin.py" | crontab -
```

## 📊 Logs

```bash
# Voir les logs en temps réel
tail -f weather_bulletin.log

# Voir les 50 dernières lignes
tail -50 weather_bulletin.log

# Voir les 20 premières lignes
head -20 weather_bulletin.log

# Rechercher les erreurs
grep "❌" weather_bulletin.log

# Rechercher les succès
grep "✅" weather_bulletin.log

# Nettoyer les logs (vider le fichier)
> weather_bulletin.log

# Supprimer le fichier de logs
rm weather_bulletin.log
```

## 🔍 Debugging

```bash
# Vérifier les variables d'environnement
cat .env

# Tester une API spécifique (OpenWeatherMap)
curl "https://api.openweathermap.org/data/2.5/weather?lat=46.1591&lon=-1.1520&appid=VOTRE_CLE&units=metric"

# Obtenir le Chat ID Telegram
curl "https://api.telegram.org/botVOTRE_TOKEN/getUpdates"

# Vérifier Python et les packages
python3 --version
pip3 list | grep requests
pip3 list | grep dotenv

# Tester l'envoi Telegram directement
curl -X POST "https://api.telegram.org/botVOTRE_TOKEN/sendMessage" \
  -d "chat_id=VOTRE_CHAT_ID" \
  -d "text=Test bulletin météo"
```

## 🔑 Obtenir les clés API

```bash
# OpenWeatherMap
open https://openweathermap.org/api

# StormGlass
open https://stormglass.io/

# WorldTides
open https://www.worldtides.info/

# Trouver les coordonnées géographiques
open https://www.latlong.net/
```

## 📦 Gestion des dépendances

```bash
# Installer les dépendances
pip3 install -r requirements.txt

# Installer une dépendance spécifique
pip3 install requests
pip3 install python-dotenv

# Mettre à jour les dépendances
pip3 install --upgrade -r requirements.txt

# Lister les packages installés
pip3 list

# Créer un environnement virtuel (optionnel)
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## 🔄 Mise à jour

```bash
# Mettre à jour depuis Git
git pull

# Réinstaller les dépendances
pip3 install -r requirements.txt

# Reconfigurer le cron
./setup_cron.sh
```

## 🗑️ Désinstallation

```bash
# Supprimer le cron job
crontab -l | grep -v "weather_bulletin.py" | crontab -

# Supprimer les fichiers Python (garder le bot Node.js)
rm weather_bulletin.py
rm requirements.txt
rm setup_cron.sh
rm test_bulletin.sh
rm check_setup.py
rm weather_bulletin.log
rm README_METEO.md
rm QUICK_START_METEO.md
rm ARCHITECTURE_METEO.md
rm API_KEYS_GUIDE.md
rm COMMANDES.md

# Désinstaller les packages Python (si pas utilisés ailleurs)
pip3 uninstall requests python-dotenv
```

## 🛠️ Personnalisation

```bash
# Changer l'heure d'envoi (exemple: 8h00)
crontab -e
# Modifier: 30 7 → 0 8

# Changer la localisation
nano .env
# Modifier: LATITUDE, LONGITUDE, LOCATION_NAME

# Modifier le format du bulletin
nano weather_bulletin.py
# Éditer la fonction format_bulletin()
```

## 📱 Telegram

```bash
# Obtenir les updates du bot
curl "https://api.telegram.org/botVOTRE_TOKEN/getUpdates"

# Envoyer un message de test
curl -X POST "https://api.telegram.org/botVOTRE_TOKEN/sendMessage" \
  -d "chat_id=VOTRE_CHAT_ID" \
  -d "text=🌊 Test bulletin" \
  -d "parse_mode=Markdown"

# Obtenir les infos du bot
curl "https://api.telegram.org/botVOTRE_TOKEN/getMe"

# Lister les commandes du bot
curl "https://api.telegram.org/botVOTRE_TOKEN/getMyCommands"
```

## 🔒 Sécurité

```bash
# Vérifier que .env est ignoré par Git
git status --ignored

# Vérifier le .gitignore
cat .gitignore | grep .env

# Vérifier les permissions des fichiers
ls -la | grep .env

# Changer les permissions du .env (lecture seule)
chmod 600 .env
```

## 📈 Monitoring

```bash
# Vérifier si le cron tourne
ps aux | grep cron

# Voir les logs système du cron (macOS)
log show --predicate 'process == "cron"' --last 1h

# Voir les logs système du cron (Linux)
grep CRON /var/log/syslog

# Tester manuellement à l'heure du cron
# (simuler l'exécution du cron)
cd /Users/francois/bot-snsm && /usr/bin/python3 weather_bulletin.py
```

## 🆘 Dépannage rapide

```bash
# Le bulletin ne s'envoie pas
./check_setup.py                    # Vérifier la config
tail -50 weather_bulletin.log       # Voir les erreurs
python3 weather_bulletin.py         # Tester manuellement

# Erreur "Module not found"
pip3 install -r requirements.txt    # Réinstaller les dépendances

# Erreur "API key invalid"
nano .env                           # Vérifier les clés API
./check_setup.py                    # Valider la config

# Le cron ne s'exécute pas
crontab -l                          # Vérifier qu'il existe
./setup_cron.sh                     # Réinstaller
```

## 📚 Documentation

```bash
# Ouvrir la documentation
open README_METEO.md
open QUICK_START_METEO.md
open ARCHITECTURE_METEO.md
open API_KEYS_GUIDE.md

# Ou avec cat
cat README_METEO.md
cat QUICK_START_METEO.md
```

## 🎯 Raccourcis utiles

```bash
# Alias à ajouter dans ~/.zshrc ou ~/.bashrc
alias bulletin-test="cd /Users/francois/bot-snsm && python3 weather_bulletin.py"
alias bulletin-logs="tail -f /Users/francois/bot-snsm/weather_bulletin.log"
alias bulletin-check="cd /Users/francois/bot-snsm && ./check_setup.py"
alias bulletin-cron="crontab -l | grep weather_bulletin"

# Recharger le shell après modification
source ~/.zshrc  # ou source ~/.bashrc
```
