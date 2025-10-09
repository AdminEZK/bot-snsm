# 🌊 Bulletin Météo/Mer Automatique - Bot SNSM

Système automatisé d'envoi quotidien d'un bulletin météo et conditions maritimes sur Telegram.

## 📋 Fonctionnalités

Le bulletin quotidien inclut :

- **🌤 Météo** (OpenWeatherMap)
  - Température et ressenti
  - Conditions météo
  - Vent (vitesse en nœuds et km/h, direction)
  - Humidité et pression

- **🌊 Conditions maritimes** (StormGlass)
  - Température de l'eau
  - Hauteur de houle
  - Période de houle
  - Direction de houle

- **🌙 Marées** (WorldTides)
  - Horaires des hautes et basses mers
  - Hauteurs des marées

## 🚀 Installation

### 1. Prérequis

- Python 3.7+
- Un bot Telegram (token déjà configuré)
- Clés API pour :
  - [OpenWeatherMap](https://openweathermap.org/api) (gratuit)
  - [StormGlass](https://stormglass.io/) (gratuit jusqu'à 50 requêtes/jour)
  - [WorldTides](https://www.worldtides.info/) (gratuit jusqu'à 1000 requêtes/mois)

### 2. Installation des dépendances Python

```bash
pip3 install -r requirements.txt
```

### 3. Configuration

1. **Obtenir votre Chat ID Telegram** :
   - Envoyez un message à votre bot
   - Visitez : `https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates`
   - Récupérez le `chat.id` dans la réponse

2. **Configurer les variables d'environnement** :

Ajoutez ces lignes à votre fichier `.env` :

```env
# Chat ID pour recevoir le bulletin
TELEGRAM_CHAT_ID=votre_chat_id_ici

# Clés API Météo/Mer
OPENWEATHER_API_KEY=votre_cle_openweathermap_ici
STORMGLASS_API_KEY=votre_cle_stormglass_ici
WORLDTIDES_API_KEY=votre_cle_worldtides_ici

# Coordonnées géographiques (ajustez selon votre localisation)
LATITUDE=46.1591
LONGITUDE=-1.1520
LOCATION_NAME=La Rochelle
```

3. **Ajuster les coordonnées** :
   - Trouvez vos coordonnées sur [LatLong.net](https://www.latlong.net/)
   - Mettez à jour `LATITUDE`, `LONGITUDE` et `LOCATION_NAME`

## 🧪 Test

Testez le bulletin manuellement :

```bash
# Méthode 1 : Script de test
chmod +x test_bulletin.sh
./test_bulletin.sh

# Méthode 2 : Direct
python3 weather_bulletin.py
```

## ⏰ Planification automatique (Cron)

### Installation automatique

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

Le bulletin sera envoyé **tous les jours à 7h30**.

### Installation manuelle

1. Ouvrir l'éditeur cron :
```bash
crontab -e
```

2. Ajouter cette ligne (remplacez `/chemin/vers` par votre chemin réel) :
```cron
30 7 * * * cd /chemin/vers/bot-snsm && /usr/bin/python3 weather_bulletin.py >> weather_bulletin.log 2>&1
```

3. Sauvegarder et quitter

### Vérifier le cron

```bash
# Lister les cron jobs
crontab -l

# Voir les logs
tail -f weather_bulletin.log
```

## 📊 Exemple de bulletin

```
🌊 BULLETIN MÉTÉO/MER SNSM 🌊
📅 Mercredi 08 octobre 2025
📍 La Rochelle

🌤 MÉTÉO
• Température : 18.5°C (ressenti 17.2°C)
• Conditions : Ciel dégagé
• Vent : 12.5 nœuds (23.1 km/h) - NO
• Humidité : 72%
• Pression : 1015 hPa

🌊 CONDITIONS MARITIMES
• Température eau : 16.8°C
• Hauteur houle : 0.85 m
• Période houle : 5.2 s
• Direction houle : O

🌙 MARÉES DU JOUR
⬇️ 06:23 - Basse mer (1.45m)
⬆️ 12:47 - Haute mer (5.82m)
⬇️ 18:56 - Basse mer (1.38m)

_Généré automatiquement à 07:30_
```

## 🔧 Personnalisation

### Changer l'heure d'envoi

Modifiez la ligne cron :
- `30 7` = 7h30
- `0 8` = 8h00
- `15 6` = 6h15

### Ajouter plusieurs destinataires

Pour envoyer à plusieurs chats/groupes, modifiez `weather_bulletin.py` :

```python
TELEGRAM_CHAT_IDS = [
    'chat_id_1',
    'chat_id_2',
    'chat_id_3'
]

# Dans send_telegram_message()
for chat_id in TELEGRAM_CHAT_IDS:
    # ... envoyer le message
```

## 🐛 Dépannage

### Le bulletin n'est pas envoyé

1. Vérifier les logs :
```bash
tail -f weather_bulletin.log
```

2. Tester manuellement :
```bash
python3 weather_bulletin.py
```

3. Vérifier le cron :
```bash
crontab -l
```

### Erreurs API

- **OpenWeatherMap** : Vérifiez que votre clé est activée (peut prendre 10 min)
- **StormGlass** : Limite de 50 requêtes/jour en gratuit
- **WorldTides** : Limite de 1000 requêtes/mois en gratuit

### Chat ID incorrect

Récupérez votre Chat ID :
```bash
curl "https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates"
```

## 📝 Logs

Les logs sont automatiquement enregistrés dans `weather_bulletin.log` :

```bash
# Voir les derniers logs
tail -20 weather_bulletin.log

# Suivre en temps réel
tail -f weather_bulletin.log

# Nettoyer les vieux logs
> weather_bulletin.log
```

## 🔐 Sécurité

- ⚠️ **Ne jamais commiter le fichier `.env`** (contient les clés API)
- Les clés API sont déjà dans `.gitignore`
- Gardez vos tokens confidentiels

## 📚 Ressources

- [OpenWeatherMap API](https://openweathermap.org/api)
- [StormGlass API](https://docs.stormglass.io/)
- [WorldTides API](https://www.worldtides.info/apidocs)
- [Cron Guide](https://crontab.guru/)

## 🆘 Support

En cas de problème :
1. Vérifiez les logs
2. Testez manuellement le script
3. Vérifiez vos clés API
4. Vérifiez votre Chat ID Telegram
