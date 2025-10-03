# 🚤 Bot SNSM Telegram

Bot Telegram pour gérer les départs et retours en mer de l'équipe SNSM.

## 📋 Fonctionnalités

- `/depart` - Signaler un départ en mer avec choix du lieu
- `/retour` - Signaler un retour à la station (RAS)
- `/status` - Voir qui est en mer actuellement
- `/aide` - Afficher l'aide

## 🚀 Installation

### Prérequis

- Node.js (version 14 ou supérieure)
- Un bot Telegram (créé via [@BotFather](https://t.me/botfather))

### Étapes

1. **Cloner le repository**
   ```bash
   git clone <url-du-repo>
   cd bot-snsm
   ```

2. **Installer les dépendances**
   ```bash
   npm install
   ```

3. **Configurer le token Telegram**
   
   Créez un fichier `.env` à la racine du projet :
   ```bash
   cp .env.example .env
   ```
   
   Éditez `.env` et ajoutez votre token Telegram :
   ```
   TELEGRAM_BOT_TOKEN=votre_token_ici
   ```

4. **Lancer le bot**
   ```bash
   node bot.js
   ```

## 🌐 Déploiement

### Option 1 : VPS avec PM2 (recommandé)

```bash
# Installer PM2
npm install -g pm2

# Lancer le bot en arrière-plan
pm2 start bot.js --name bot-snsm

# Configurer le démarrage automatique
pm2 startup
pm2 save
```

### Option 2 : Render.com (gratuit, recommandé)

1. **Créer un compte sur [Render.com](https://render.com)**

2. **Pousser votre code sur GitHub** (voir instructions ci-dessous)

3. **Créer un nouveau Web Service sur Render** :
   - Connectez votre repository GitHub
   - Build Command: `npm install`
   - Start Command: `npm start`
   - Type: **Web Service**
   - Plan: Free

4. **Configurer les variables d'environnement** :
   - Dans Render Dashboard → Environment
   - Ajouter : `TELEGRAM_BOT_TOKEN` = votre token

5. **Déployer** : Render déploiera automatiquement à chaque push

**Note** : Le bot inclut un serveur HTTP sur le port configuré par Render pour satisfaire les exigences de health check. Le bot Telegram fonctionne en mode polling en parallèle.

### Option 3 : Autres services cloud

- **Railway.app** : Déploiement automatique depuis GitHub
- **Fly.io** : Hébergement gratuit pour petits projets

### Option 3 : Hébergement mutualisé (webhook requis)

Pour utiliser sur un hébergement mutualisé comme O2Switch, il faut convertir le bot en mode webhook (polling non supporté).

## 📝 Lieux configurés

- Plage de Saint Cieux
- Plage de l'Islet

Pour modifier les lieux, éditez la ligne 34 de `bot.js`.

## 🔒 Sécurité

⚠️ **Ne jamais commiter le fichier `.env` sur GitHub !**

Le fichier `.gitignore` est configuré pour l'exclure automatiquement.

## 🔗 Pousser sur GitHub

```bash
# Créer un nouveau repository sur GitHub (via l'interface web)
# Puis exécuter :

git remote add origin https://github.com/VOTRE_USERNAME/bot-snsm.git
git branch -M main
git push -u origin main
```

## 📄 Licence

ISC
