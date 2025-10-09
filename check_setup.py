#!/usr/bin/env python3
"""
Script de vérification de la configuration du bulletin météo/mer
Vérifie que toutes les dépendances et clés API sont correctement configurées
"""

import os
import sys
from pathlib import Path

# Couleurs pour l'affichage
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def print_status(message, status):
    """Affiche un message avec un statut coloré"""
    if status == "OK":
        print(f"{GREEN}✅ {message}{NC}")
    elif status == "ERROR":
        print(f"{RED}❌ {message}{NC}")
    elif status == "WARNING":
        print(f"{YELLOW}⚠️  {message}{NC}")
    else:
        print(f"{BLUE}ℹ️  {message}{NC}")

def check_python_version():
    """Vérifie la version de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print_status(f"Python {version.major}.{version.minor}.{version.micro}", "OK")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor} (requis: 3.7+)", "ERROR")
        return False

def check_dependencies():
    """Vérifie que les dépendances Python sont installées"""
    required = ['requests', 'dotenv']
    missing = []
    
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print_status(f"Package '{package}' installé", "OK")
        except ImportError:
            print_status(f"Package '{package}' manquant", "ERROR")
            missing.append(package)
    
    return len(missing) == 0

def check_env_file():
    """Vérifie l'existence du fichier .env"""
    if Path('.env').exists():
        print_status("Fichier .env trouvé", "OK")
        return True
    else:
        print_status("Fichier .env manquant", "ERROR")
        print(f"  {YELLOW}→ Copiez .env.example vers .env et configurez-le{NC}")
        return False

def check_env_variables():
    """Vérifie les variables d'environnement"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        'TELEGRAM_BOT_TOKEN': 'Token du bot Telegram',
        'TELEGRAM_CHAT_ID': 'ID du chat Telegram',
        'OPENWEATHER_API_KEY': 'Clé API OpenWeatherMap',
        'STORMGLASS_API_KEY': 'Clé API StormGlass',
        'WORLDTIDES_API_KEY': 'Clé API WorldTides',
        'LATITUDE': 'Latitude',
        'LONGITUDE': 'Longitude',
        'LOCATION_NAME': 'Nom du lieu'
    }
    
    all_ok = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value not in ['votre_token_telegram_ici', 'votre_chat_id_ici', 
                                     'votre_cle_openweathermap_ici', 'votre_cle_stormglass_ici',
                                     'votre_cle_worldtides_ici']:
            print_status(f"{description} ({var})", "OK")
        else:
            print_status(f"{description} ({var}) non configuré", "ERROR")
            all_ok = False
    
    return all_ok

def check_script_permissions():
    """Vérifie les permissions des scripts"""
    scripts = ['weather_bulletin.py', 'setup_cron.sh', 'test_bulletin.sh']
    all_ok = True
    
    for script in scripts:
        if Path(script).exists():
            if os.access(script, os.X_OK):
                print_status(f"Script '{script}' exécutable", "OK")
            else:
                print_status(f"Script '{script}' non exécutable", "WARNING")
                print(f"  {YELLOW}→ Exécutez: chmod +x {script}{NC}")
                all_ok = False
        else:
            print_status(f"Script '{script}' manquant", "ERROR")
            all_ok = False
    
    return all_ok

def check_api_connectivity():
    """Vérifie la connectivité aux APIs (test basique)"""
    try:
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test OpenWeatherMap
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if api_key and api_key != 'votre_cle_openweathermap_ici':
            try:
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather",
                    params={'lat': 0, 'lon': 0, 'appid': api_key},
                    timeout=5
                )
                if response.status_code == 200:
                    print_status("Connexion OpenWeatherMap", "OK")
                elif response.status_code == 401:
                    print_status("Clé OpenWeatherMap invalide", "ERROR")
                else:
                    print_status(f"OpenWeatherMap erreur {response.status_code}", "WARNING")
            except Exception as e:
                print_status(f"Erreur OpenWeatherMap: {str(e)[:50]}", "WARNING")
        else:
            print_status("OpenWeatherMap non testé (clé manquante)", "WARNING")
        
        return True
    except ImportError:
        print_status("Module 'requests' manquant pour tester les APIs", "WARNING")
        return False

def main():
    """Fonction principale"""
    print(f"\n{BLUE}{'='*60}{NC}")
    print(f"{BLUE}🔍 Vérification de la configuration - Bulletin Météo/Mer{NC}")
    print(f"{BLUE}{'='*60}{NC}\n")
    
    checks = []
    
    # 1. Version Python
    print(f"{BLUE}📌 Version Python{NC}")
    checks.append(check_python_version())
    print()
    
    # 2. Dépendances
    print(f"{BLUE}📦 Dépendances Python{NC}")
    checks.append(check_dependencies())
    print()
    
    # 3. Fichier .env
    print(f"{BLUE}⚙️  Fichier de configuration{NC}")
    env_exists = check_env_file()
    checks.append(env_exists)
    print()
    
    # 4. Variables d'environnement
    if env_exists:
        print(f"{BLUE}🔑 Variables d'environnement{NC}")
        checks.append(check_env_variables())
        print()
    
    # 5. Permissions des scripts
    print(f"{BLUE}🔐 Permissions des scripts{NC}")
    checks.append(check_script_permissions())
    print()
    
    # 6. Connectivité API
    print(f"{BLUE}🌐 Connectivité APIs{NC}")
    check_api_connectivity()
    print()
    
    # Résumé
    print(f"{BLUE}{'='*60}{NC}")
    if all(checks):
        print(f"{GREEN}✅ Configuration complète ! Vous pouvez lancer le bulletin.{NC}")
        print(f"\n{BLUE}🚀 Prochaines étapes :{NC}")
        print(f"  1. Tester : {YELLOW}./test_bulletin.sh{NC}")
        print(f"  2. Installer le cron : {YELLOW}./setup_cron.sh{NC}")
    else:
        print(f"{RED}❌ Configuration incomplète. Corrigez les erreurs ci-dessus.{NC}")
        print(f"\n{BLUE}📚 Ressources :{NC}")
        print(f"  • Guide rapide : {YELLOW}QUICK_START_METEO.md{NC}")
        print(f"  • Guide des clés API : {YELLOW}API_KEYS_GUIDE.md{NC}")
        print(f"  • Documentation : {YELLOW}README_METEO.md{NC}")
    print(f"{BLUE}{'='*60}{NC}\n")
    
    sys.exit(0 if all(checks) else 1)

if __name__ == "__main__":
    main()
