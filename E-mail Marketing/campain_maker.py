import json
import locale
import os
import time

import django
import sys
from datetime import datetime, timedelta



# Ajouter le chemin du dossier Django "AstroNomos" au sys.path
from AstroNomos.assets.main import Horoscope

sys.path.append('/Users/emmanuellandau/PycharmProjects/AstroWeb/AstroNomos')

# Définir la variable d'environnement pour indiquer à Django quel fichier de paramètres utiliser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AstroNomos.AstroNomos.settings')

# Initialiser Django
django.setup()

from newsletter.models import HoroscopeSubscription
from html_maker import HtmlFile
import boto3
from botocore.exceptions import ClientError
from Suscribers import update_record, get_dataset


def update_subscriber_status(email, campaign_name):
    # Charger le fichier JSON existant
    with open('subscribers.json', 'r', encoding='utf-8') as json_file:
        subscribers_data = json.load(json_file)

    # Obtenir la date et l'heure actuelles
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Parcourir les abonnés dans le JSON pour trouver celui qui correspond à l'email donné
    for subscriber in subscribers_data:
        if subscriber['email'] == email:
            # Mettre à jour is_weekly_horoscope_sent à True
            subscriber['is_weekly_horoscope_sent'] = True

            # Ajouter le nouveau log de la campagne
            if 'newsletter_log' not in subscriber or not isinstance(subscriber['newsletter_log'], dict):
                subscriber['newsletter_log'] = {}

            subscriber['newsletter_log'][campaign_name] = current_time

            # Sauvegarder les modifications dans le fichier JSON
            with open('subscribers.json', 'w', encoding='utf-8') as json_file:
                json.dump(subscribers_data, json_file, ensure_ascii=False, indent=4)

            print(f"Abonné {email} mis à jour avec succès dans le fichier JSON.")
            return True

    print(f"Aucun abonné trouvé avec l'email {email}.")
    return False
def push_unsubscribe_link(subscriber_email, email_body_template):
    # Récupérer l'abonné
    subscription = HoroscopeSubscription.objects.filter(email=subscriber_email)
    if subscription.count() > 1:
        # Garder un abonnement et supprimer les autres
        subscription.exclude(pk=subscription.first().pk).delete()
        print(f"{subscription.count() - 1} doublons supprimés.")

    subscription = subscription.first()
    # Générer un jeton de désabonnement unique
    subscription.generate_unsubscribe_token()

    # Construire le lien de désabonnement
    unsubscribe_link = f"http://astro-nomos.com/unsubscribe/{subscription.unsubscribe_token}/"

    # Remplacer la variable {$unsubscribe} par le lien de désabonnement généré
    email_body = email_body_template.replace('{$unsubscribe}', unsubscribe_link)

    return email_body

def get_week_range_str():
    # Obtenir la date actuelle
    today = datetime.now()

    # Calculer le début de la semaine (lundi) et la fin de la semaine (dimanche)
    start_of_week = today - timedelta(days=today.weekday())  # Lundi de la semaine courante
    end_of_week = start_of_week + timedelta(days=6)  # Dimanche de la semaine courante

    # Obtenir le nom des mois pour comparaison
    start_month = start_of_week.strftime("%B")  # Mois en français
    end_month = end_of_week.strftime("%B")      # Mois en français

    # Créer la chaîne de la plage de dates de la semaine
    if start_month == end_month:
        # Les deux dates sont dans le même mois
        date_range_str = f"{start_of_week.day} au {end_of_week.day} {start_month}"
    else:
        # Les deux dates sont dans des mois différents
        date_range_str = f"{start_of_week.day} {start_month} au {end_of_week.day} {end_month}"

    return date_range_str, start_of_week, end_of_week







def create_weekly_horoscopes():
    htmls = []
    date_range_str, start_date, end_date = get_week_range_str()

    for astro_sign in astro_signs:
        # # Exemple sans les paramètres optionnels
        horoscope_without_birth_info = Horoscope(start_date, end_date, astro_sign[0])
        astro_data = horoscope_without_birth_info.display_horoscope_data()

        variables = {
        "sign": astro_sign[1],
        "sign_emoji": astro_sign[2],
        "date_range_str" : date_range_str,
        "astro_data" : astro_data,
        "love_img_url": "https://storage.mlcdn.com/account_image/954202/H2KjQhp6NnVK2ygP4GbcDxVURtZ17Y2agivQoFzq.png",
        "money_img_url": "https://storage.mlcdn.com/account_image/954202/LYbN58bxFxnmjrFRXkhFmuMS4pbr7bWtK4ukW5Dz.png",
        "health_img_url": "https://storage.mlcdn.com/account_image/954202/QWgMrXZJdFNuLEBAbWIqrUPc7oUa2GxXp692S5pf.png",
        }
        print(variables)
        html = HtmlFile("weekly_newsletter.html", variables)
        content = html.content()
        htmls.append({'sign': astro_sign[0], 'html_content': content, 'campaign_name': html.campaign_name})  # Sauvegarder le signe et le contenu HTML


    # Sauvegarder le contenu HTML dans un fichier JSON
    with open('weekly_horoscopes.json', 'w', encoding='utf-8') as json_file:
        json.dump(htmls, json_file, ensure_ascii=False, indent=4)

    print("Contenu HTML sauvegardé dans weekly_horoscopes.json.")

def load_weekly_horoscopes():
    try:
        with open('weekly_horoscopes.json', 'r', encoding='utf-8') as json_file:
            htmls = json.load(json_file)
        return htmls
    except FileNotFoundError:
        print("Fichier JSON introuvable.")
        return []

def send_horoscopes():
    htmls = load_weekly_horoscopes()
    with open('subscribers.json', 'r', encoding='utf-8') as json_file:
        subscribers = json.load(json_file)



    for subscriber in subscribers:
        if subscriber["is_weekly_horoscope_sent"]:
            print(f"on a deja envoyé a {subscriber['first_name']}")
        else:
            RECIPIENT = subscriber["email"]
            # Objet et corps de l'email
            SUBJECT = f"{subscriber['first_name']} les astres on quelque chose d'important à te dire cette semaine... 👀"
            BODY_TEXT = "Bonjour,\nCeci est un email envoyé via Amazon SES."
            BODY_HTML = None
            campagne_name = None
            for html in htmls:
                if html['sign'] == subscriber["zodiac_sign"]:
                    BODY_HTML = push_unsubscribe_link(subscriber["email"], html['html_content'])
                    campagne_name = html['campaign_name']
            if not BODY_HTML:
                print(f"{ subscriber['zodiac_sign']} n'est pas dans {astro_signs}")

            # Format de l'email
            CHARSET = "UTF-8"

            # send the email
            try:
                response = client.send_email(
                    Destination={
                        'ToAddresses': [
                            RECIPIENT,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': BODY_HTML,
                            },
                            'Text': {
                                'Charset': CHARSET,
                                'Data': BODY_TEXT,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': SUBJECT,
                        },
                    },
                    Source=SENDER,
                )
                # Affichez l'ID du message si l'envoi est réussi
                print(RECIPIENT, subscriber["zodiac_sign"] )
                print("Email envoyé! Message ID:"),
                print(response['MessageId'])
                print(update_subscriber_status(subscriber["email"], campagne_name))
                # time.sleep(0.5)
            except ClientError as e:
                print(e.response['Error']['Message'])

# Remplacez par vos informations
SENDER = "newsletter@astro-nomos.com"
AWS_REGION = "us-east-1"
client = boto3.client('ses', region_name=AWS_REGION)

update_record(reset=True)

# suscribers = [(9, 'emnl.busi@outlook.fr', 'Emmanuel', 'gemini')]
# suscribers, _ = get_dataset()

signs = [
    ["aries", "Bélier", "♈"],
    ["taurus", "Taureau", "♉"],
    ["gemini", "Gémeaux", "♊"],
    ["cancer", "Cancer", "♋"],
    ["leo", "Lion", "♌"],
    ["virgo", "Vierge", "♍"],
    ["libra", "Balance", "♎"],
    ["scorpio", "Scorpion", "♏"],
    ["capricorn", "Capricorne", "♑"],
    ["aquarius", "Verseau", "♒"],
    ["pisces", "Poisson", "♓"],
    ["sagittarius", "Sagittaire", "♐"],
]

astro_signs = signs
print(astro_signs)
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# create_weekly_horoscopes()
send_horoscopes()

# print(subscribers)