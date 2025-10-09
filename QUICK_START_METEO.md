# 🚀 Démarrage Rapide - Bulletin Météo/Mer

## ⚡ Installation en 5 minutes

### 1️⃣ Installer les dépendances Python

```bash
pip3 install -r requirements.txt
```

### 2️⃣ Obtenir les clés API (gratuites)

1. **OpenWeatherMap** : https://openweathermap.org/api
   - Créer un compte → API Keys → Copier la clé

2. **StormGlass** : https://stormglass.io/
   - S'inscrire → Dashboard → API Key

3. **WorldTides** : https://www.worldtides.info/
   - S'inscrire → Account → API Key

### 3️⃣ Obtenir votre Chat ID Telegram

```bash
# Envoyez un message à votre bot, puis :
curl "https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates" | grep chat
```

Ou visitez : `https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates`

### 4️⃣ Configurer le fichier .env

Ajoutez ces lignes à votre `.env` :

```env
# Chat ID Telegram
TELEGRAM_CHAT_ID=123456789

# Clés API
OPENWEATHER_API_KEY=abc123...
STORMGLASS_API_KEY=def456...
WORLDTIDES_API_KEY=ghi789...

# Localisation (exemple : La Rochelle)
LATITUDE=46.1591
LONGITUDE=-1.1520
LOCATION_NAME=La Rochelle
```

💡 **Trouvez vos coordonnées** : https://www.latlong.net/

### 5️⃣ Tester

```bash
./test_bulletin.sh
```

### 6️⃣ Installer le cron (envoi automatique à 7h30)

```bash
./setup_cron.sh
```

## ✅ C'est tout !

Le bulletin sera envoyé automatiquement chaque matin à **7h30**.

---

## 📋 Commandes utiles

```bash
# Tester manuellement
python3 weather_bulletin.py

# Voir les logs
tail -f weather_bulletin.log

# Vérifier le cron
crontab -l

# Désinstaller le cron
crontab -e  # puis supprimer la ligne weather_bulletin.py
```

## 🔧 Changer l'heure d'envoi

```bash
crontab -e
```

Modifiez la ligne :
- `30 7` → 7h30
- `0 8` → 8h00
- `15 6` → 6h15

## 📖 Documentation complète

Voir `README_METEO.md` pour plus de détails.
