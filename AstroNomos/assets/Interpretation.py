import ast

from openai import OpenAI

def get_birth_chart(astro_data):
    # Function to add an image URL to each card
    def add_image_url(chart, url):
        for key in chart:
            chart[key]['imageUrl'] = url

        return chart
    if not astro_data:
        return None

    prompt = f"""Réalise moi une carte astrale sur la base des éléments suivants.
     Ta réponse contient uniquement un dictionnaire python de 4 clés au format Clé (par exemple,
      "ascendant_card") qui identifie la carte.
      Tu dois tutoyer, etre chaleureux et utiliser des émojis échappe bien ton dict.
    pour chaque clé tu as un dict de 4 couples suivants : :
    title : Le titre de la carte.
    subtitle : Un sous-titre qui décrit brièvement l'aspect avec intrigue"
    description : Un texte plus long qui explique en détail l'aspect astrologique. Ce texte doit inclure plusieurs phrases.
     données astrologiques :{astro_data}"""
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es un astrologue dévoué."},
            {"role": "user", "content": prompt}
        ]
    )

    script_text = str(completion.choices[0].message.content)
    start = script_text.find("{")
    end = script_text.rfind("}") + 1

    card = ast.literal_eval(script_text[start:end])
    # Adding the placeholder image URL to each card
    card = add_image_url(card, "https://via.placeholder.com/300x200")
    return card

def get_transit_chart(astro_data):
    # Function to add an image URL to each card
    def add_image_url(chart, url):
        for key in chart:
            chart[key]['imageUrl'] = url

        return chart

    if not astro_data:
        return None

    prompt = f"""Réalise moi une carte de transit personnalisée  sur la base des éléments suivants.
     Ta réponse contient uniquement un dictionnaire python de 4 clés au format Clé (par exemple,
      "love") qui identifie la carte. Tutoies, utilise des émojis et échappe bien ton dict.
    pour chaque clé tu as un dict de 4 couples suivants :
    title : Le titre aguicheur de la carte.
    subtitle : Un sous-titre qui décrit brièvement le contenu en teasant.
    description : Un texte plus long qui explique en détail la situation. Ce texte peut inclure plusieurs phrases.
     données astrologiques :{astro_data}"""
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es un astrologue storyteller dévoué."},
            {"role": "user", "content": prompt}
        ]
    )

    script_text = str(completion.choices[0].message.content)
    start = script_text.find("{")
    end = script_text.rfind("}") + 1

    card = ast.literal_eval(script_text[start:end])
    # Adding the placeholder image URL to each card
    card = add_image_url(card, "https://via.placeholder.com/300x200")
    return card

# card = get_transit_chart("""
# Julian Day: 2460527.0625
# Sidereal Time: 10.407103809949778
# House Cusps:
# House 1 Cusp: 229.58134369492524°
# House 2 Cusp: 259.90997807901795°
# House 3 Cusp: 297.88458913040824°
# House 4 Cusp: 336.72055562867115°
# House 5 Cusp: 7.905317110873057°
# House 6 Cusp: 31.282340783671316°
# House 7 Cusp: 49.58134369492524°
# House 8 Cusp: 79.90997807901795°
# House 9 Cusp: 117.88458913040824°
# House 10 Cusp: 156.72055562867115°
# House 11 Cusp: 187.90531711087309°
# House 12 Cusp: 211.28234078367132°
# Ascendant: 229.58134369492524°
# Midheaven (MC): 156.72055562867115°
# Sun: 132.65821339242572°
# Moon: 133.74787170864025°
# Mercury: 154.0867161348841°
# Venus: 149.34076865806313°
# Mars: 70.01977335377694°
# Jupiter: 75.02662672783227°
# Saturn: 348.4130341314856°
# Uranus: 56.928876813801416°
# Neptune: 359.6463869365295°
# Pluto: 300.58111244249625°
# Astrological Chart for 4/8/2024 at 15:30
# Location: Latitude 48.8566, Longitude 2.3522
# Julian Day: 2460527.0625
# Sidereal Time: 10.407103809949778
# House Cusps:
# House 1 Cusp: 229.58134369492524°
# House 2 Cusp: 259.90997807901795°
# House 3 Cusp: 297.88458913040824°
# House 4 Cusp: 336.72055562867115°
# House 5 Cusp: 7.905317110873057°
# House 6 Cusp: 31.282340783671316°
# House 7 Cusp: 49.58134369492524°
# House 8 Cusp: 79.90997807901795°
# House 9 Cusp: 117.88458913040824°
# House 10 Cusp: 156.72055562867115°
# House 11 Cusp: 187.90531711087309°
# House 12 Cusp: 211.28234078367132°
# Ascendant: 229.58134369492524°
# Midheaven (MC): 156.72055562867115°
# Planets Positions:
# Sun: 132.65821339242572° in Leo
# Moon: 133.74787170864025° in Leo
# Mercury: 154.0867161348841° in Virgo
# Venus: 149.34076865806313° in Leo
# Mars: 70.01977335377694° in Gemini
# Jupiter: 75.02662672783227° in Gemini
# Saturn: 348.4130341314856° in Pisces
# Uranus: 56.928876813801416° in Taurus
# Neptune: 359.6463869365295° in Pisces
# Pluto: 300.58111244249625° in Aquarius""")
# print(card)