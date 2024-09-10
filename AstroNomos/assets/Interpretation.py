import ast

from openai import OpenAI

def get_birth_chart(astro_data):
    # Function to add an image URL to each card
    def add_image_url(chart, url):
        for key in chart:
            chart[key]['imageUrl'] = url

        return chart

    prompt = f"""Réalise moi une carte astrale synthétique sur la base des éléments suivants.
     Ta réponse contient uniquement un dictionnaire python de 4 clés au format Clé (par exemple,
      "ascendant_card") qui identifie la carte.
    Valeurs sous forme de dictionnaire contenant les champs suivants :
    title : Le titre de la carte, comme "Ascendant en Sagittaire".
    subtitle : Un sous-titre qui décrit brièvement l'aspect, par exemple "L'ascendant en Sagittaire dépeint un individu
     plein de vie, toujours en quête d'aventure et de sens."
    description : Un texte plus long qui explique en détail l'aspect astrologique. Ce texte peut inclure plusieurs phrases.
     données astrologiques :{astro_data}"""
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
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

    prompt = f"""Réalise moi une carte de transit presonnalisée  sur la base des éléments suivants.
     Ta réponse contient uniquement un dictionnaire python de 4 clés au format Clé (par exemple,
      "love") qui identifie la carte.
    Valeurs sous forme de dictionnaire contenant les champs suivants :
    title : Le titre de la carte, comme "Les Défis de l'Ambition".
    subtitle : Un sous-titre qui décrit brièvement le contenu, par exemple " : Soleil et Jupiter en Confrontation..."
    description : Un texte plus long qui explique en détail la situation. Ce texte peut inclure plusieurs phrases.
     données astrologiques :{astro_data}"""
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
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