# 🏗️ Architecture - Bulletin Météo/Mer

## 📁 Structure du projet

```
bot-snsm/
├── 🤖 Bot Telegram Node.js (existant)
│   ├── bot.js                    # Bot principal (départ/retour en mer)
│   ├── package.json
│   └── node_modules/
│
├── 🌊 Bulletin Météo/Mer Python (nouveau)
│   ├── weather_bulletin.py       # Script principal
│   ├── requirements.txt          # Dépendances Python
│   ├── setup_cron.sh            # Installation automatique du cron
│   ├── test_bulletin.sh         # Script de test
│   └── weather_bulletin.log     # Logs (généré automatiquement)
│
├── 📚 Documentation
│   ├── README.md                # Documentation bot principal
│   ├── README_METEO.md          # Documentation complète météo
│   ├── QUICK_START_METEO.md     # Guide de démarrage rapide
│   └── ARCHITECTURE_METEO.md    # Ce fichier
│
└── ⚙️ Configuration
    ├── .env                      # Variables d'environnement (secret)
    ├── .env.example             # Template de configuration
    └── .gitignore               # Fichiers à ignorer
```

## 🔄 Flux de données

```
┌─────────────────────────────────────────────────────────┐
│                    CRON JOB (7h30)                      │
│              Déclenche automatiquement                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              weather_bulletin.py                        │
│                                                         │
│  1. Charge les variables d'environnement (.env)        │
│  2. Appelle les 3 APIs en parallèle                    │
│  3. Formate le bulletin                                │
│  4. Envoie sur Telegram                                │
└─────────────────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│OpenWeatherMap│ │StormGlass│ │ WorldTides   │
│              │ │          │ │              │
│ • Vent       │ │ • Eau    │ │ • Marées     │
│ • Temp       │ │ • Houle  │ │ • Hauteurs   │
└──────────────┘ └──────────┘ └──────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Bulletin formaté     │
        │   (Markdown)           │
        └────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Telegram Bot API     │
        │   Envoi du message     │
        └────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Chat/Groupe Telegram  │
        │  📱 Bulletin reçu      │
        └────────────────────────┘
```

## 🔌 APIs utilisées

### 1. OpenWeatherMap
- **Endpoint** : `api.openweathermap.org/data/2.5/weather`
- **Données** : Météo actuelle
- **Limite gratuite** : 1000 appels/jour
- **Fréquence** : 1x/jour → OK ✅

### 2. StormGlass
- **Endpoint** : `api.stormglass.io/v2/weather/point`
- **Données** : Conditions maritimes
- **Limite gratuite** : 50 appels/jour
- **Fréquence** : 1x/jour → OK ✅

### 3. WorldTides
- **Endpoint** : `www.worldtides.info/api/v3`
- **Données** : Marées et hauteurs
- **Limite gratuite** : 1000 appels/mois
- **Fréquence** : 30x/mois → OK ✅

## ⏰ Planification (Cron)

```bash
# Format cron : minute heure jour mois jour_semaine commande
30 7 * * * cd /path/to/bot-snsm && python3 weather_bulletin.py >> weather_bulletin.log 2>&1
```

- `30 7` → 7h30
- `* * *` → Tous les jours, tous les mois, tous les jours de la semaine
- `>> weather_bulletin.log` → Logs en append
- `2>&1` → Erreurs aussi dans le log

## 🔐 Sécurité

### Variables sensibles (dans .env)
```env
TELEGRAM_BOT_TOKEN=secret_token
TELEGRAM_CHAT_ID=123456789
OPENWEATHER_API_KEY=secret_key
STORMGLASS_API_KEY=secret_key
WORLDTIDES_API_KEY=secret_key
```

### Protection
- ✅ `.env` dans `.gitignore`
- ✅ `.env.example` pour template
- ✅ Pas de secrets hardcodés
- ✅ Tokens chargés via `python-dotenv`

## 🚀 Déploiement

### Option 1 : Serveur local (Mac/Linux)
```bash
# Installation
pip3 install -r requirements.txt
./setup_cron.sh

# Le cron s'exécute automatiquement
```

### Option 2 : Serveur distant (VPS)
```bash
# Sur le serveur
git clone <repo>
cd bot-snsm
pip3 install -r requirements.txt
cp .env.example .env
nano .env  # Configurer les clés
./setup_cron.sh
```

### Option 3 : Docker (futur)
```dockerfile
# Possibilité d'ajouter un Dockerfile
# avec cron intégré
```

## 📊 Monitoring

### Logs
```bash
# Voir les logs en temps réel
tail -f weather_bulletin.log

# Dernières 50 lignes
tail -50 weather_bulletin.log

# Rechercher des erreurs
grep "❌" weather_bulletin.log
```

### Vérification cron
```bash
# Lister les crons actifs
crontab -l

# Logs système cron (macOS)
log show --predicate 'process == "cron"' --last 1h

# Logs système cron (Linux)
grep CRON /var/log/syslog
```

## 🔄 Évolutions possibles

### Court terme
- [ ] Alertes si vent > X nœuds
- [ ] Prévisions sur 3 jours
- [ ] Graphiques météo

### Moyen terme
- [ ] Base de données historique
- [ ] Statistiques mensuelles
- [ ] API webhook au lieu de cron

### Long terme
- [ ] Interface web de configuration
- [ ] Multi-localisation
- [ ] ML pour prédictions personnalisées

## 🐛 Troubleshooting

### Le bulletin n'arrive pas
1. Vérifier le cron : `crontab -l`
2. Vérifier les logs : `tail weather_bulletin.log`
3. Tester manuellement : `python3 weather_bulletin.py`

### Erreurs API
- Vérifier les clés dans `.env`
- Vérifier les quotas API
- Vérifier la connexion internet

### Erreurs Telegram
- Vérifier le `TELEGRAM_CHAT_ID`
- Vérifier le `TELEGRAM_BOT_TOKEN`
- Le bot doit être admin du groupe (si groupe)

## 📞 Support

Pour toute question :
1. Consulter `README_METEO.md`
2. Vérifier les logs
3. Tester avec `test_bulletin.sh`
