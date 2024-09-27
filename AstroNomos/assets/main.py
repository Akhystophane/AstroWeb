import swisseph as swe
import datetime


class AstrologicalChart:
    def __init__(self, year, month, day, hour, minute, latitude, longitude):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.latitude = latitude
        self.longitude = longitude
        self.julian_day = None
        self.sidereal_time = None
        self.houses_cusps = None
        self.ascendant = None
        self.mc = None
        self.planets_positions = {}

        self.calculate_julian_day()
        self.calculate_sidereal_time()
        self.calculate_houses()
        self.calculate_planets_positions()

    def calculate_julian_day(self):
        birth_time = datetime.datetime(self.year, self.month, self.day, self.hour, self.minute)
        # Correct for DST if necessary
        birth_time = birth_time - datetime.timedelta(hours=2)  # Paris in August is UTC+2
        self.julian_day = swe.julday(birth_time.year, birth_time.month, birth_time.day,
                                     birth_time.hour + birth_time.minute / 60.0)
        print(f"Julian Day: {self.julian_day}")

    def calculate_sidereal_time(self):
        self.sidereal_time = swe.sidtime(self.julian_day)
        print(f"Sidereal Time: {self.sidereal_time}")

    def calculate_houses(self):
        house_system = b'P'  # 'P' for Placidus
        self.houses_cusps, ascmc = swe.houses(self.julian_day, self.latitude, self.longitude, house_system)
        self.ascendant = ascmc[0]
        self.mc = ascmc[1]

        print("House Cusps:")
        for i, cusp in enumerate(self.houses_cusps):
            print(f"House {i + 1} Cusp: {cusp}°")

        print(f"Ascendant: {self.ascendant}°")
        print(f"Midheaven (MC): {self.mc}°")

    def calculate_planets_positions(self):
        planet_names = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
        planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS,
                      swe.NEPTUNE, swe.PLUTO]

        for name, planet_id in zip(planet_names, planet_ids):
            planet_position = swe.calc_ut(self.julian_day, planet_id)[0]
            self.planets_positions[name] = planet_position
            print(f"{name}: {planet_position[0]}°")

    def calculate_transits(self, start_date, end_date, step_days=1):
        """Calculate the planetary transits between a given start date and end date."""
        transits = {}
        current_date = start_date

        while current_date <= end_date:
            julian_day = swe.julday(current_date.year, current_date.month, current_date.day,
                                    current_date.hour + current_date.minute / 60.0)

            positions = {}
            planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS,
                          swe.NEPTUNE, swe.PLUTO]
            planet_names = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
                            "Pluto"]

            for name, planet_id in zip(planet_names, planet_ids):
                planet_position = swe.calc_ut(julian_day, planet_id)[0]
                positions[name] = planet_position[0]  # Position en degré

            transits[current_date] = positions
            current_date += datetime.timedelta(days=step_days)

        return transits

    def display_chart(self):
        print(f"Astrological Chart for {self.day}/{self.month}/{self.year} at {self.hour}:{self.minute}")
        print(f"Location: Latitude {self.latitude}, Longitude {self.longitude}")
        print(f"Julian Day: {self.julian_day}")
        print(f"Sidereal Time: {self.sidereal_time}")
        print("House Cusps:")
        for i, cusp in enumerate(self.houses_cusps):
            print(f"House {i + 1} Cusp: {cusp}°")
        print(f"Ascendant: {self.ascendant}°")
        print(f"Midheaven (MC): {self.mc}°")
        print("Planets Positions:")
        for name, position in self.planets_positions.items():
            print(f"{name}: {position[0]}° in {self.get_zodiac_sign(position[0])}")

    def display_chartV2(self, chart_type="birth", positions=None):
        chart_data = {}
        chart_data["location"] = {"latitude": self.latitude, "longitude": self.longitude}
        chart_data["birth_date"] = {"day": self.day, "month": self.month, "year": self.year}
        chart_data["birth_time"] = {"hour": self.hour, "minute": self.minute}

        if chart_type == "birth":
            chart_data["houses"] = {f"House {i + 1}": cusp for i, cusp in enumerate(self.houses_cusps)}
            chart_data["ascendant"] = self.ascendant
            chart_data["midheaven"] = self.mc
            chart_data["planets_positions"] = {name: position[0] for name, position in self.planets_positions.items()}

        elif chart_type == "transit" and positions:
            chart_data["transiting_planets"] = {name: position for name, position in positions.items()}

        return chart_data

    def calculate_transits_for_period(self, start_date, end_date, step_days=1):
        """Calculate planetary transits for a specific person over a given period."""
        transits = {}
        current_date = start_date

        while current_date <= end_date:
            # Calcul du jour julien (Julian Day) sans utiliser l'heure et la minute
            julian_day = swe.julday(current_date.year, current_date.month, current_date.day)

            positions = {}
            planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS,
                          swe.NEPTUNE, swe.PLUTO]
            planet_names = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
                            "Pluto"]

            for name, planet_id in zip(planet_names, planet_ids):
                planet_position = swe.calc_ut(julian_day, planet_id)[0]
                positions[name] = planet_position[0]  # Position en degré

            transits[current_date] = positions
            current_date += datetime.timedelta(days=step_days)

        return transits

    def compare_transits_with_natal_chart(self, transits):
        """Compare transit positions with the natal chart of the person."""
        print("Comparison of Transits with Natal Chart:")
        for date, transit_positions in transits.items():
            print(f"Transits for {date.strftime('%Y-%m-%d')}:")
            for planet, transit_position in transit_positions.items():
                natal_position = self.planets_positions.get(planet, [0])[0]  # Position de naissance de la planète
                print(f"{planet}: Transit at {transit_position:.2f}°, Natal at {natal_position:.2f}°")
                # Calculer l'aspect ici, par exemple la conjonction si l'écart est < 5°
                aspect = self.calculate_aspect(transit_position, natal_position)
                if aspect:
                    print(f"  Aspect: {aspect}")
            print()

    @staticmethod
    def calculate_aspect(transit_position, natal_position):
        """Calculate if there's an aspect between transit and natal positions."""
        diff = abs(transit_position - natal_position) % 360
        if diff < 5 or diff > 355:
            return "Conjunction"
        elif 85 <= diff <= 95 or 265 <= diff <= 275:
            return "Square"
        elif 175 <= diff <= 185:
            return "Opposition"
        elif 115 <= diff <= 125 or 235 <= diff <= 245:
            return "Trine"
        # Ajouter d'autres aspects si nécessaire
        return None

    @staticmethod
    def get_zodiac_sign(degree):
        zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        index = int(degree // 30)
        return zodiac_signs[index]


import datetime
import swisseph as swe


class Horoscope:
    def __init__(self, start_date, end_date, zodiac_sign, birth_time=None, latitude=None, longitude=None):
        self.start_date = start_date
        self.end_date = end_date
        self.zodiac_sign = zodiac_sign
        self.birth_time = birth_time  # Tuple (hour, minute) ou None
        self.latitude = latitude
        self.longitude = longitude
        self.transits = {}
        self.ascendant = None
        self.houses_cusps = None
        self.aspects = []

        # Calculer les éléments astrologiques pour la période donnée
        self.generate_horoscope()

    def generate_horoscope(self):
        """Calculate planetary positions, houses, and aspects for each day in the given date range."""
        current_date = self.start_date

        while current_date <= self.end_date:
            # Calcul du jour julien (Julian Day) avec ou sans heure et minute
            if self.birth_time:
                julian_day = swe.julday(current_date.year, current_date.month, current_date.day,
                                        self.birth_time[0] + self.birth_time[1] / 60.0)
            else:
                julian_day = swe.julday(current_date.year, current_date.month, current_date.day)

            # Calculer les positions des planètes pour le jour courant
            positions = self.calculate_planetary_positions(julian_day)

            # Calculer les maisons astrologiques et l'ascendant seulement si les informations de naissance sont fournies
            if self.birth_time and self.latitude is not None and self.longitude is not None:
                self.calculate_houses_and_ascendant(julian_day)
            else:
                self.ascendant = None
                self.houses_cusps = None

            # Calculer les aspects planétaires
            aspects = self.calculate_planetary_aspects(positions)

            # Stocker les données pour la date actuelle
            self.transits[current_date.strftime('%Y-%m-%d')] = {
                "positions": positions,
                "ascendant": self.ascendant,
                "houses": self.houses_cusps,
                "aspects": aspects
            }

            # Avancer d'un jour
            current_date += datetime.timedelta(days=1)

    def calculate_planetary_positions(self, julian_day):
        """Calculate the positions of planets for a given Julian day."""
        positions = {}
        planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS,
                      swe.NEPTUNE, swe.PLUTO]
        planet_names = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

        for name, planet_id in zip(planet_names, planet_ids):
            planet_position = swe.calc_ut(julian_day, planet_id)[0]
            positions[name] = planet_position[0]  # Position en degrés

        return positions

    def calculate_houses_and_ascendant(self, julian_day):
        """Calculate the ascendant and houses for the birth time and location."""
        house_system = b'P'  # 'P' for Placidus
        self.houses_cusps, ascmc = swe.houses(julian_day, self.latitude, self.longitude, house_system)
        self.ascendant = ascmc[0]  # Ascendant

    def calculate_planetary_aspects(self, positions):
        """Calculate aspects (angles) between planets."""
        aspects = []
        planet_names = list(positions.keys())
        planet_positions = list(positions.values())

        for i in range(len(planet_names)):
            for j in range(i + 1, len(planet_names)):
                angle = abs(planet_positions[i] - planet_positions[j]) % 360
                aspect = self.get_aspect(angle)
                if aspect:
                    aspects.append({
                        "planet1": planet_names[i],
                        "planet2": planet_names[j],
                        "angle": angle,
                        "aspect": aspect
                    })
        return aspects

    @staticmethod
    def get_aspect(angle):
        """Determine the aspect based on the angle between two planets."""
        if abs(angle) < 5 or abs(angle - 360) < 5:
            return "Conjunction"
        elif abs(angle - 90) < 5 or abs(angle - 270) < 5:
            return "Square"
        elif abs(angle - 180) < 5:
            return "Opposition"
        elif abs(angle - 120) < 5 or abs(angle - 240) < 5:
            return "Trine"
        elif abs(angle - 60) < 5 or abs(angle - 300) < 5:
            return "Sextile"
        return None

    def display_horoscope_data(self):
        """Collect and return the calculated horoscope data including ascendant, houses, and aspects as a single string."""
        result = ""  # Utiliser une chaîne de caractères pour accumuler le résultat
        transits_items = list(self.transits.items())  # Convertir les transits en liste pour un traitement facile
        num_transits = len(transits_items)

        # Si le nombre de transits est inférieur ou égal à 6, on les affiche tous
        if num_transits <= 6:
            selected_transits = transits_items
        else:
            # Sélectionner le premier et le dernier transit
            selected_transits = [transits_items[0], transits_items[-1]]

            # Calculer comment distribuer les autres transits de manière homogène
            step = (num_transits - 1) // 5  # Diviser les transits restants de manière égale entre le premier et le dernier
            for i in range(1, 5):  # Sélectionner 4 transits supplémentaires de manière homogène
                selected_transits.insert(i, transits_items[i * step])

        # Parcourir les transits sélectionnés et les ajouter au résultat
        for date, data in selected_transits:
            entry = f"Date: {date}\n"

            if data['ascendant'] is not None:
                entry += f"Ascendant: {data['ascendant']:.2f}°\n"

            if data['houses'] is not None:
                entry += "Houses:\n"
                for i, cusp in enumerate(data['houses']):
                    entry += f"  House {i + 1}: {cusp:.2f}°\n"

            if data['aspects']:
                entry += "Aspects:\n"
                for aspect in data['aspects']:
                    entry += f"  {aspect['planet1']} {aspect['aspect']} {aspect['planet2']} at {aspect['angle']:.2f}°\n"

            entry += "\n"  # Ajouter une ligne vide entre chaque entrée de date

            # Ajouter l'entrée au résultat
            result += entry

        # Retourner la chaîne de caractères des résultats
        return result.strip()  # Supprimer tout espace blanc supplémentaire à la fin

# # Exemple avec les paramètres optionnels fournis
# birth_time = (14, 30)  # Exemple : 14:30 (2:30 PM)
# latitude = 48.8566  # Latitude de Paris
# longitude = 2.3522  # Longitude de Paris
# horoscope_with_birth_info = Horoscope(start_date, end_date, zodiac_sign, birth_time, latitude, longitude)
# horoscope_with_birth_info.display_horoscope_data()
#

# Example usage:
# chart = AstrologicalChart(year=2024, month=8, day=4, hour=15, minute=30, latitude=48.8566, longitude=2.3522)
# chart.display_chart()

# Outputs:
# Sun: ~ 12° Leo (approx. 132.738° - 120° Leo boundary)
# Ascendant: ~ 19° Scorpio (approx. 252.121° - 240° Scorpio boundary)

