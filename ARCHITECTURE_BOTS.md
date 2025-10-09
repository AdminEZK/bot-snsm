# 🏗️ Architecture des Bots SNSM

Ce document explique l'architecture du système avec **deux bots Telegram séparés**.

---

## 📊 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────┐
│                    PROJET BOT-SNSM                      │
└─────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐      ┌──────▼──────────┐
        │   BOT ÉQUIPE   │      │   BOT MÉTÉO     │
        │    (bot.js)    │      │(weather_bulletin│
        │                │      │     .py)        │
        └────────────────┘      └─────────────────┘
```

---

## 🚤 Bot 1 : Suivi d'Équipe

### Fichier principal
- **`bot.js`** (Node.js)

### Token utilisé
- `TELEGRAM_BOT_TOKEN` (dans `.env`)

### Fonctionnalités
- ✅ Commande `/depart` - Signaler un départ en mer
- ✅ Commande `/retour` - Signaler un retour
- ✅ Commande `/status` - Voir qui est en mer
- ✅ Commande `/aide` - Afficher l'aide

### Mode de fonctionnement
- **Toujours actif** (polling continu)
- **Interactif** (répond aux commandes utilisateurs)
- **Hébergé sur Render** (serveur distant)

### Dépendances
```json
{
  "node-telegram-bot-api": "^0.66.0",
  "dotenv": "^16.4.7",
  "express": "^4.21.1"
}
```

---

## 🌤 Bot 2 : Bulletin Météo

### Fichier principal
- **`weather_bulletin.py`** (Python)

### Tokens utilisés
- `TELEGRAM_METEO_BOT_TOKEN` (dans `.env`)
- `TELEGRAM_METEO_CHAT_ID` (dans `.env`)

### Fonctionnalités
- 🌤 Données météo (OpenWeatherMap)
- 🌊 Conditions maritimes (StormGlass)
- 🌙 Marées (WorldTides)

### Mode de fonctionnement
- **Exécution programmée** (cron à 7h30)
- **Automatique** (pas d'interaction)
- **Local** (sur votre machine/serveur)

### Dépendances
```txt
requests==2.31.0
python-dotenv==1.0.0
```

---

## 🔑 Configuration des tokens

### Fichier `.env`

```env
# Bot 1 - Suivi d'équipe
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...

# Bot 2 - Bulletin météo
TELEGRAM_METEO_BOT_TOKEN=789012:GHI-JKL...
TELEGRAM_METEO_CHAT_ID=-1001234567890

# APIs météo/mer
OPENWEATHER_API_KEY=...
STORMGLASS_API_KEY=...
WORLDTIDES_API_KEY=...

# Localisation
LATITUDE=46.1591
LONGITUDE=-1.1520
LOCATION_NAME=La Rochelle
```

---

## 🔄 Flux de données

### Bot Équipe (bot.js)
```
Utilisateur → Telegram → Bot JS → Réponse immédiate
                           ↓
                    Mise à jour status
```

### Bot Météo (weather_bulletin.py)
```
Cron (7h30) → Script Python → APIs externes → Formatage → Telegram
                                ↓
                        OpenWeatherMap
                        StormGlass
                        WorldTides
```

---

## 🚀 Déploiement

### Bot Équipe
- **Hébergement** : Render.com
- **Disponibilité** : 24/7
- **Démarrage** : Automatique via Render

### Bot Météo
- **Hébergement** : Local (ou serveur personnel)
- **Disponibilité** : Exécution quotidienne
- **Démarrage** : Cron job

---

## 📁 Structure des fichiers

```
bot-snsm/
├── bot.js                          # Bot suivi d'équipe
├── weather_bulletin.py             # Bot bulletin météo
├── package.json                    # Dépendances Node.js
├── requirements.txt                # Dépendances Python
├── .env                            # Configuration (2 tokens)
├── .env.example                    # Template de config
├── GUIDE_CREATION_BOT_METEO.md     # Guide création bot météo
└── README_METEO.md                 # Doc bulletin météo
```

---

## ⚠️ Points importants

### Pourquoi deux bots séparés ?

1. **Éviter les conflits** : Un seul token ne peut pas être utilisé par deux processus simultanément
2. **Séparation des responsabilités** : Chaque bot a une fonction distincte
3. **Flexibilité** : Possibilité d'arrêter/modifier un bot sans affecter l'autre
4. **Sécurité** : Tokens séparés = meilleure isolation

### Limitations

- **Telegram** : Un token = un bot = un processus actif
- **APIs gratuites** : Limites de requêtes (StormGlass: 50/jour, WorldTides: 1000/mois)

---

## 🔧 Maintenance

### Mettre à jour le bot équipe
```bash
# Sur Render, push sur GitHub
git push origin main
# Render redéploie automatiquement
```

### Mettre à jour le bot météo
```bash
# Modifier weather_bulletin.py
git add weather_bulletin.py
git commit -m "Update weather bot"
git push

# Le cron utilisera la nouvelle version
```

---

## 🆘 Dépannage

### Les deux bots ne fonctionnent pas
→ Vérifiez que vous avez **deux tokens différents**

### Conflit de tokens
→ Assurez-vous que `bot.js` utilise `TELEGRAM_BOT_TOKEN` et `weather_bulletin.py` utilise `TELEGRAM_METEO_BOT_TOKEN`

### Le bulletin n'est pas envoyé
→ Vérifiez le cron : `crontab -l`
→ Vérifiez les logs : `tail -f weather_bulletin.log`

---

**Architecture mise à jour le 09/10/2025**
