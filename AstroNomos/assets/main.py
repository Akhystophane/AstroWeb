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
        print(f"Astrological Chart for {self.day}/{self.month}/{self.year} at {self.hour}:{self.minute}")
        print(f"Location: Latitude {self.latitude}, Longitude {self.longitude}")

        if chart_type == "birth":
            print("House Cusps:")
            for i, cusp in enumerate(self.houses_cusps):
                print(f"House {i + 1} Cusp: {cusp}°")
            print(f"Ascendant: {self.ascendant}°")
            print(f"Midheaven (MC): {self.mc}°")
            print("Planets Positions at Birth:")
            for name, position in self.planets_positions.items():
                print(f"{name}: {position[0]}° in {self.get_zodiac_sign(position[0])}")

        elif chart_type == "transit":
            print("Transiting Planets Positions:")
            if positions:
                for name, position in positions.items():
                    print(f"{name} Transit: {position[0]}° in {self.get_zodiac_sign(position[0])}")
            else:
                print("No transit data provided.")

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


# Example usage:
# chart = AstrologicalChart(year=2024, month=8, day=4, hour=15, minute=30, latitude=48.8566, longitude=2.3522)
# chart.display_chart()

# Outputs:
# Sun: ~ 12° Leo (approx. 132.738° - 120° Leo boundary)
# Ascendant: ~ 19° Scorpio (approx. 252.121° - 240° Scorpio boundary)
