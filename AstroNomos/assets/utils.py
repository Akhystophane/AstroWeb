# utils.py
import ast
from datetime import datetime

from openai import OpenAI

from .main import AstrologicalChart
from .Interpretation import get_birth_chart, get_transit_chart


def generate_birth_chart(birth_date, birth_time, birth_location):
    # Convertir les dates et heures en objets datetime si nécessaire
    # Obtenir la latitude et la longitude à partir du lieu de naissance
    latitude, longitude = get_coordinates_from_location(birth_location)
    logger = logging.getLogger(__name__)
    logger.debug("nogger.")
    logger.debug(f"Prompt: {latitude}, Response: {longitude}")
    # Créer l'objet AstrologicalChart
    chart = AstrologicalChart(
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
        hour=birth_time.hour,
        minute=birth_time.minute,
        latitude=latitude,
        longitude=longitude
    )

    # Générer la carte de naissance
    birth_chart_data = chart.display_chartV2()
    print("generate_birth_chart", birth_chart_data)
    birth_chart = get_birth_chart(birth_chart_data)

    return birth_chart, latitude, longitude
import logging

def get_coordinates_from_location(location):
    prompt = f"""Tu dois me trouver les coordonées de ce lieu :{location}, ta réponse est uniquement un tuple de 2 nbr (latitude,
longitude), si le lieu fourni est vraiment introuvable ta réponse est simplement : None"""
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es un géographe informaticien."},
            {"role": "user", "content": prompt}
        ]
    )

    script_text = str(completion.choices[0].message.content)

    if "None" in script_text:
        return (48.8566, 2.3522)
    else:
        start = script_text.find("(")
        end = script_text.rfind(")") + 1

    coordinates = ast.literal_eval(script_text[start:end])
    return coordinates  # Exemple pour Paris


def generate_transit_chart(birth_date, birth_time, birth_location, transit_start_date, transit_end_date):
    # Obtenir la latitude et la longitude à partir du lieu de naissance
    latitude, longitude = get_coordinates_from_location(birth_location)

    # Créer l'objet AstrologicalChart pour la date de naissance
    birth_chart = AstrologicalChart(
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
        hour=birth_time.hour,
        minute=birth_time.minute,
        latitude=latitude,
        longitude=longitude
    )

    # Calculer les transits pour la période spécifiée
    transits = birth_chart.calculate_transits_for_period(
        start_date=transit_start_date,
        end_date=transit_end_date
    )

    # Comparer les transits avec la carte natale
    transit_results = []
    for date, transit_positions in transits.items():
        comparison = {}
        for planet, transit_position in transit_positions.items():
            natal_position = birth_chart.planets_positions.get(planet, [0])[0]
            aspect = birth_chart.calculate_aspect(transit_position, natal_position)
            comparison[planet] = {
                'transit_position': transit_position,
                'natal_position': natal_position,
                'aspect': aspect
            }
        transit_results.append({
            'date': date.strftime('%Y-%m-%d'),
            'comparisons': comparison
        })

    # Interpréter les résultats des transits
    transit_chart = get_transit_chart(transit_results)

    return transit_chart

# birth_date = datetime(1995, 7, 15)  # 15 juillet 1995
# birth_time = datetime.strptime('14:30', '%H:%M')  # 14h30
# birth_location = 'Paris'  # Lieu de naissance fictif
#
# # Appel de la fonction pour tester avec ces fausses données
# birth_chart = generate_birth_chart(birth_date, birth_time, birth_location)
#
# print(birth_chart)