# 🔑 Guide d'obtention des clés API

## 1. OpenWeatherMap (Météo)

### 📝 Inscription
1. Aller sur https://openweathermap.org/api
2. Cliquer sur **"Sign Up"** (en haut à droite)
3. Remplir le formulaire :
   - Email
   - Mot de passe
   - Accepter les conditions

### 🔑 Obtenir la clé
1. Se connecter
2. Aller dans **"API keys"** (menu)
3. Copier la clé par défaut ou créer une nouvelle
4. ⚠️ **Attendre 10 minutes** (activation de la clé)

### 💰 Plan gratuit
- ✅ 1000 appels/jour
- ✅ Données actuelles
- ✅ Suffisant pour 1 appel/jour

### 📋 Ajouter au .env
```env
OPENWEATHER_API_KEY=votre_cle_ici
```

---

## 2. StormGlass (Conditions maritimes)

### 📝 Inscription
1. Aller sur https://stormglass.io/
2. Cliquer sur **"Get Started"**
3. Créer un compte (email + mot de passe)
4. Confirmer l'email

### 🔑 Obtenir la clé
1. Se connecter au Dashboard
2. Aller dans **"API"** ou **"Settings"**
3. Copier l'**API Key**

### 💰 Plan gratuit
- ✅ 50 appels/jour
- ✅ Données maritimes complètes
- ✅ Suffisant pour 1 appel/jour

### 📋 Ajouter au .env
```env
STORMGLASS_API_KEY=votre_cle_ici
```

---

## 3. WorldTides (Marées)

### 📝 Inscription
1. Aller sur https://www.worldtides.info/
2. Cliquer sur **"Developer"** puis **"Sign Up"**
3. Créer un compte gratuit

### 🔑 Obtenir la clé
1. Se connecter
2. Aller dans **"Account"** ou **"API Keys"**
3. Copier la clé API

### 💰 Plan gratuit
- ✅ 1000 appels/mois
- ✅ Données de marées mondiales
- ✅ Suffisant pour 30 appels/mois

### 📋 Ajouter au .env
```env
WORLDTIDES_API_KEY=votre_cle_ici
```

---

## 4. Chat ID Telegram

### 🔍 Méthode 1 : Via API
1. Envoyer un message à votre bot
2. Ouvrir dans un navigateur :
   ```
   https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates
   ```
3. Chercher `"chat":{"id":123456789}`
4. Copier le nombre (votre Chat ID)

### 🔍 Méthode 2 : Via curl
```bash
curl "https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates" | grep -o '"chat":{"id":[0-9]*' | grep -o '[0-9]*$'
```

### 🔍 Méthode 3 : Bot @userinfobot
1. Chercher **@userinfobot** sur Telegram
2. Démarrer une conversation
3. Il vous donnera votre ID

### 📋 Ajouter au .env
```env
TELEGRAM_CHAT_ID=123456789
```

---

## 📍 Coordonnées géographiques

### 🌍 Trouver vos coordonnées

**Option 1 : LatLong.net**
1. Aller sur https://www.latlong.net/
2. Chercher votre ville
3. Copier Latitude et Longitude

**Option 2 : Google Maps**
1. Clic droit sur votre localisation
2. Cliquer sur les coordonnées pour les copier
3. Format : `46.1591, -1.1520`

**Option 3 : OpenStreetMap**
1. Aller sur https://www.openstreetmap.org/
2. Chercher votre lieu
3. Clic droit → "Afficher l'adresse"

### 📋 Ajouter au .env
```env
LATITUDE=46.1591
LONGITUDE=-1.1520
LOCATION_NAME=La Rochelle
```

---

## ✅ Vérification finale

Votre fichier `.env` doit contenir :

```env
# Bot Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=123456789

# APIs Météo/Mer
OPENWEATHER_API_KEY=abc123def456...
STORMGLASS_API_KEY=xyz789uvw012...
WORLDTIDES_API_KEY=mno345pqr678...

# Localisation
LATITUDE=46.1591
LONGITUDE=-1.1520
LOCATION_NAME=La Rochelle
```

## 🧪 Tester la configuration

```bash
# Tester le bulletin
python3 weather_bulletin.py

# Ou utiliser le script de test
./test_bulletin.sh
```

## 🔒 Sécurité

- ⚠️ **Ne jamais partager vos clés API**
- ⚠️ **Ne jamais commiter le fichier `.env`**
- ✅ Le `.env` est déjà dans `.gitignore`
- ✅ Utilisez `.env.example` comme template

## 📊 Limites des plans gratuits

| API | Limite | Notre usage | Status |
|-----|--------|-------------|--------|
| OpenWeatherMap | 1000/jour | 1/jour | ✅ OK |
| StormGlass | 50/jour | 1/jour | ✅ OK |
| WorldTides | 1000/mois | 30/mois | ✅ OK |

## 🆘 Problèmes courants

### Clé OpenWeatherMap invalide
- Attendre 10 minutes après création
- Vérifier que la clé est bien copiée
- Pas d'espaces avant/après

### StormGlass 401 Unauthorized
- Vérifier le format : `Authorization: <votre_cle>`
- Pas de préfixe "Bearer"

### WorldTides pas de données
- Vérifier les coordonnées (océan proche)
- Certaines zones n'ont pas de données de marées

### Chat ID ne fonctionne pas
- Pour un groupe : ajouter le bot comme admin
- Pour un canal : utiliser `@channel_name`
- Vérifier que le bot a reçu au moins 1 message
