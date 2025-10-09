#!/usr/bin/env python3
"""
Bot SNSM - Bulletin Météo/Mer Automatique
Envoie chaque matin un bulletin complet avec :
- Vent et température (OpenWeatherMap)
- Température de l'eau et houle (StormGlass)
- Horaires de marées (WorldTides)
"""

import os
import sys
import requests
import locale
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configurer la locale en français
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR')
    except:
        pass  # Si la locale française n'est pas disponible, on continue en anglais

# Charger les variables d'environnement
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_METEO_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_METEO_CHAT_ID')  # ID du groupe/canal où envoyer le bulletin

# Clés API météo/mer
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY')
WORLDTIDES_API_KEY = os.getenv('WORLDTIDES_API_KEY')

# Coordonnées géographiques (à ajuster selon votre localisation)
LATITUDE = float(os.getenv('LATITUDE', '46.1591'))  # Exemple : La Rochelle
LONGITUDE = float(os.getenv('LONGITUDE', '-1.1520'))
LOCATION_NAME = os.getenv('LOCATION_NAME', 'La Rochelle')


def get_weather_data():
    """Récupère les données météo depuis OpenWeatherMap"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': LATITUDE,
            'lon': LONGITUDE,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',
            'lang': 'fr'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'description': data['weather'][0]['description'].capitalize(),
            'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s -> km/h
            'wind_speed_knots': round(data['wind']['speed'] * 1.944, 1),  # m/s -> nœuds
            'wind_direction': data['wind'].get('deg', 0),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure']
        }
    except Exception as e:
        print(f"❌ Erreur OpenWeatherMap: {e}")
        return None


def get_wind_direction_text(degrees):
    """Convertit les degrés en direction cardinale"""
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSO', 'SO', 'OSO', 'O', 'ONO', 'NO', 'NNO']
    index = round(degrees / 22.5) % 16
    return directions[index]


def get_sea_conditions():
    """Récupère les conditions maritimes depuis StormGlass"""
    try:
        url = "https://api.stormglass.io/v2/weather/point"
        
        # Timestamp actuel
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=24)
        
        params = {
            'lat': LATITUDE,
            'lng': LONGITUDE,
            'params': 'waterTemperature,waveHeight,wavePeriod,waveDirection',
            'start': start.timestamp(),
            'end': end.timestamp()
        }
        
        headers = {
            'Authorization': STORMGLASS_API_KEY
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Prendre les données de la première heure disponible
        if data.get('hours') and len(data['hours']) > 0:
            hour_data = data['hours'][0]
            
            return {
                'water_temp': round(hour_data.get('waterTemperature', {}).get('sg', 0), 1),
                'wave_height': round(hour_data.get('waveHeight', {}).get('sg', 0), 2),
                'wave_period': round(hour_data.get('wavePeriod', {}).get('sg', 0), 1),
                'wave_direction': round(hour_data.get('waveDirection', {}).get('sg', 0), 0)
            }
        return None
    except Exception as e:
        print(f"❌ Erreur StormGlass: {e}")
        return None


def get_tide_data():
    """Récupère les horaires de marées depuis WorldTides"""
    try:
        url = "https://www.worldtides.info/api/v3"
        
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        params = {
            'extremes': '',
            'lat': LATITUDE,
            'lon': LONGITUDE,
            'key': WORLDTIDES_API_KEY,
            'start': int(today.timestamp()),
            'length': 86400  # 24 heures en secondes
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        tides = []
        max_height = 0  # Pour détecter les grandes marées
        
        if 'extremes' in data:
            for extreme in data['extremes']:
                tide_time = datetime.fromtimestamp(extreme['dt'])
                tide_type = 'Haute mer' if extreme['type'] == 'High' else 'Basse mer'
                tide_height = round(extreme['height'], 2)
                
                if extreme['type'] == 'High' and tide_height > max_height:
                    max_height = tide_height
                
                tides.append({
                    'time': tide_time.strftime('%H:%M'),
                    'type': tide_type,
                    'height': tide_height
                })
        
        return {'tides': tides, 'max_height': max_height}
    except Exception as e:
        print(f"❌ Erreur WorldTides: {e}")
        return None


def format_bulletin(weather, sea, tide_data):
    """Formate le bulletin météo/mer en message Telegram"""
    now = datetime.now()
    date_str = now.strftime('%A %d %B %Y').capitalize()
    
    message = f"🌊 *BULLETIN MÉTÉO SNSM* 🌊\n"
    message += f"📅 {date_str}\n"
    message += f"📍 {LOCATION_NAME}\n\n"
    
    # Météo
    if weather:
        message += "🌤 *MÉTÉO*\n"
        message += f"• Température : {weather['temperature']}°C (ressenti {weather['feels_like']}°C)\n"
        message += f"• Conditions : {weather['description']}\n"
        message += f"• Vent : {weather['wind_speed_knots']} nœuds ({weather['wind_speed']} km/h) - {get_wind_direction_text(weather['wind_direction'])}\n"
        message += f"• Humidité : {weather['humidity']}%\n"
        message += f"• Pression : {weather['pressure']} hPa\n\n"
    else:
        message += "⚠️ Données météo indisponibles\n\n"
    
    # Conditions maritimes
    if sea:
        message += "🌊 *CONDITIONS MARITIMES*\n"
        message += f"• Température eau : {sea['water_temp']}°C\n"
        message += f"• Hauteur houle : {sea['wave_height']} m\n"
        message += f"• Période houle : {sea['wave_period']} s\n"
        message += f"• Direction houle : {get_wind_direction_text(sea['wave_direction'])}\n\n"
    else:
        message += "⚠️ Données maritimes indisponibles\n\n"
    
    # Marées
    if tide_data:
        tides = tide_data.get('tides', [])
        max_height = tide_data.get('max_height', 0)
        
        message += "🌙 *MARÉES DU JOUR*\n"
        
        # Alerte grande marée basée sur la hauteur
        if max_height >= 7.0:
            message += "⚠️ *VIGILANCE : GRANDE MARÉE* ⚠️\n"
        elif max_height >= 6.5:
            message += "⚡ Marée importante\n"
        
        if tides and len(tides) > 0:
            for tide in tides:
                emoji = "⬆️" if tide['type'] == 'Haute mer' else "⬇️"
                message += f"{emoji} {tide['time']} - {tide['type']} ({tide['height']}m)\n"
            message += "\n"
        else:
            message += "⚠️ Données de marées indisponibles\n\n"
    else:
        message += "⚠️ Données de marées indisponibles\n\n"
    
    message += f"_Généré automatiquement à {now.strftime('%H:%M')}_"
    
    return message


def send_telegram_message(message):
    """Envoie le message sur Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        print("✅ Bulletin envoyé avec succès sur Telegram")
        return True
    except Exception as e:
        print(f"❌ Erreur envoi Telegram: {e}")
        return False


def main():
    """Fonction principale"""
    print(f"🚀 Démarrage du bulletin météo/mer - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Vérifier les variables d'environnement essentielles
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ ERREUR: TELEGRAM_METEO_BOT_TOKEN ou TELEGRAM_METEO_CHAT_ID manquant dans .env")
        sys.exit(1)
    
    if not all([OPENWEATHER_API_KEY, STORMGLASS_API_KEY, WORLDTIDES_API_KEY]):
        print("⚠️ ATTENTION: Certaines clés API sont manquantes")
    
    # Récupérer les données
    print("📡 Récupération des données météo...")
    weather = get_weather_data()
    
    print("🌊 Récupération des conditions maritimes...")
    sea = get_sea_conditions()
    
    print("🌙 Récupération des marées...")
    tide_data = get_tide_data()
    
    # Formater et envoyer le bulletin
    bulletin = format_bulletin(weather, sea, tide_data)
    print("\n" + "="*50)
    print(bulletin)
    print("="*50 + "\n")
    
    # Envoyer sur Telegram
    if send_telegram_message(bulletin):
        print("✅ Mission accomplie !")
    else:
        print("❌ Échec de l'envoi")
        sys.exit(1)


if __name__ == "__main__":
    main()
