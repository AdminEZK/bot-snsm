# 🌊 Bienvenue - Bulletin Météo/Mer SNSM

## 🎉 Installation terminée !

Votre système de bulletin météo/mer automatique est prêt.

---

## 🚀 Démarrage en 3 étapes

### 1️⃣ Installer les dépendances Python
```bash
pip3 install -r requirements.txt
```

### 2️⃣ Configurer les clés API
```bash
# Copier le template
cp .env.example .env

# Éditer avec vos clés
nano .env
```

📖 **Besoin d'aide pour les clés ?** → [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)

🤖 **Créer le bot météo séparé** → [GUIDE_CREATION_BOT_METEO.md](GUIDE_CREATION_BOT_METEO.md)

### 3️⃣ Tester et automatiser
```bash
# Vérifier la configuration
./check_setup.py

# Tester le bulletin
./test_bulletin.sh

# Installer le cron (envoi automatique à 7h30)
./setup_cron.sh
```

---

## 📚 Documentation disponible

| Fichier | Description |
|---------|-------------|
| **[GUIDE_CREATION_BOT_METEO.md](GUIDE_CREATION_BOT_METEO.md)** | 🤖 **Créer le bot météo séparé** |
| **[INDEX_METEO.md](INDEX_METEO.md)** | 📑 Index de navigation |
| **[QUICK_START_METEO.md](QUICK_START_METEO.md)** | ⚡ Démarrage rapide (5 min) |
| **[README_METEO.md](README_METEO.md)** | 📖 Documentation complète |
| **[API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)** | 🔑 Guide des clés API |
| **[ARCHITECTURE_METEO.md](ARCHITECTURE_METEO.md)** | 🏗️ Architecture technique |
| **[COMMANDES.md](COMMANDES.md)** | 💻 Toutes les commandes |
| **[RESUME_INSTALLATION.md](RESUME_INSTALLATION.md)** | 📦 Résumé de l'installation |
| **[FILES_CREATED.md](FILES_CREATED.md)** | 📋 Liste des fichiers créés |

---

## 🎯 Prochaine étape

👉 **Ouvrir** : [QUICK_START_METEO.md](QUICK_START_METEO.md)

Ou lire l'index complet :
```bash
cat INDEX_METEO.md
```

---

## ✨ Ce que fait le système

Chaque matin à **7h30**, le bot envoie automatiquement sur Telegram :

🌤 **Météo** (OpenWeatherMap)
- Température, vent, conditions

🌊 **Conditions maritimes** (StormGlass)  
- Température eau, houle

🌙 **Marées** (WorldTides)
- Horaires et hauteurs

---

## 🆘 Besoin d'aide ?

```bash
# Vérifier la configuration
./check_setup.py

# Voir toutes les commandes
cat COMMANDES.md

# Consulter la doc complète
cat README_METEO.md
```

---

**Bon vent ! ⛵**
