# 🌤 Guide : Créer un Bot Telegram pour le Bulletin Météo

Ce guide vous explique comment créer un **second bot Telegram** dédié au bulletin météo, séparé du bot de suivi d'équipe.

---

## 🎯 Pourquoi deux bots ?

- **Bot 1 (bot.js)** : Suivi d'équipe en temps réel (départ/retour)
- **Bot 2 (weather_bulletin.py)** : Bulletin météo automatique quotidien

Avoir deux bots séparés évite les conflits et permet une meilleure organisation.

---

## 📝 Étapes de création

### 1️⃣ Créer le nouveau bot avec BotFather

1. **Ouvrir Telegram** et chercher `@BotFather`

2. **Démarrer une conversation** avec BotFather

3. **Créer le bot** :
   ```
   /newbot
   ```

4. **Choisir un nom** (exemple) :
   ```
    Bulletin Météo
   ```

5. **Choisir un username** (doit finir par "bot", exemple) :
   ```
   snsm_meteo_bot
   ```

6. **Copier le token** fourni par BotFather
   ```
   Format: 8433756544:AAH6hYu5d6i0ci84WXCa3M1S6TS_aKUqT-w
   ```

---

### 2️⃣ Obtenir le Chat ID

#### Option A : Via le bot existant (si vous avez déjà un groupe)

1. **Ajouter le nouveau bot** au groupe/canal où vous voulez recevoir le bulletin

2. **Envoyer un message** dans le groupe (n'importe quoi)

3. **Visiter cette URL** dans votre navigateur (remplacez `VOTRE_TOKEN`) :
   ```
   https://api.telegram.org/botVOTRE_TOKEN/getUpdates
   ```

4. **Chercher le `chat.id`** dans la réponse JSON
   ```json
   {
     "chat": {
       "id": 6892309735,  ← Votre Chat ID
       "title": "Groupe SNSM"
     }
   }
   ```

#### Option B : Créer une conversation privée

1. **Chercher votre nouveau bot** dans Telegram (par son username)

2. **Démarrer une conversation** avec `/start`

3. **Visiter l'URL** ci-dessus pour récupérer votre Chat ID personnel

---

### 3️⃣ Configurer le fichier .env

1. **Ouvrir votre fichier `.env`**

2. **Ajouter les nouvelles variables** :
   ```env
   # Bot Telegram - Bulletin Météo (weather_bulletin.py)
   TELEGRAM_METEO_BOT_TOKEN=8433756544:AAH6hYu5d6i0ci84WXCa3M1S6TS_aKUqT-w
   TELEGRAM_METEO_CHAT_ID=-6892309735
   ```

3. **Vérifier que vous avez aussi** :
   ```env
   # Bot Telegram - Suivi d'équipe (bot.js)
   TELEGRAM_BOT_TOKEN=votre_token_bot_equipe
   
   # Clés API Météo/Mer
   OPENWEATHER_API_KEY=...
   STORMGLASS_API_KEY=...
   WORLDTIDES_API_KEY=...
   
   # Coordonnées
   LATITUDE=46.1591
   LONGITUDE=-1.1520
   LOCATION_NAME=La Rochelle
   ```

---

### 4️⃣ Tester le bulletin météo

```bash
# Tester manuellement
python3 weather_bulletin.py
```

Vous devriez recevoir le bulletin sur Telegram ! 🎉

---

## ✅ Vérifications

### Le bot fonctionne si :
- ✅ Vous recevez un message du nouveau bot
- ✅ Le message contient les données météo, maritimes et marées
- ✅ Aucune erreur dans le terminal

### En cas de problème :

#### ❌ "TELEGRAM_METEO_BOT_TOKEN manquant"
→ Vérifiez que le token est bien dans `.env`

#### ❌ "Unauthorized" ou "Forbidden"
→ Vérifiez que le token est correct et que le bot a accès au chat

#### ❌ "Chat not found"
→ Vérifiez le Chat ID et que le bot est bien ajouté au groupe

#### ❌ Pas de données météo/mer
→ Vérifiez vos clés API (OpenWeatherMap, StormGlass, WorldTides)

---

## 🔐 Sécurité

⚠️ **Important** :
- Ne partagez **jamais** vos tokens
- Le fichier `.env` est dans `.gitignore` (ne sera pas commité)
- Gardez vos clés API confidentielles

---

## 📚 Prochaines étapes

Une fois le bot météo configuré :

1. **Automatiser l'envoi** avec cron (voir `setup_cron.sh`)
2. **Personnaliser** les horaires d'envoi
3. **Ajouter** d'autres destinataires si besoin

Consultez `README_METEO.md` pour plus de détails.

---

## 🆘 Besoin d'aide ?

- Vérifiez que Python 3 est installé : `python3 --version`
- Vérifiez les dépendances : `pip3 install -r requirements.txt`
- Consultez les logs : `tail -f weather_bulletin.log`

**Bon vent ! ⛵**
