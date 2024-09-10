import os

from AstroNomos.newsletter.models import HoroscopeSubscription
from html_maker import HtmlFile
import mailerlite as MailerLite
from Suscribers import char_exists
import boto3
from botocore.exceptions import ClientError

# Remplacez par vos informations
SENDER = "newsletter@astro-nomos.com"
RECIPIENT = "emnl.busi@outlook.fr"
AWS_REGION = "us-east-1"
client = boto3.client('ses', region_name=AWS_REGION)


def push_unsubscribe_link(subscriber_email, email_body_template):
    # Récupérer l'abonné
    subscription = HoroscopeSubscription.objects.get(email=subscriber_email)

    # Générer un jeton de désabonnement unique
    subscription.generate_unsubscribe_token()

    # Construire le lien de désabonnement
    unsubscribe_link = f"http://astro-nomos.com/unsubscribe/{subscription.unsubscribe_token}/"

    # Remplacer la variable {$unsubscribe} par le lien de désabonnement généré
    email_body = email_body_template.replace('{$unsubscribe}', unsubscribe_link)

    return email_body


suscribers = [(9, 'yeroniang585@gmail.com', 'Yero', 'capricorn')]

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
data = ["emnl.busi@outlook.fr"]
astro_signs = [["cancer", "Cancer", "♋"]]
print(astro_signs)

htmls = []
for astro_sign in astro_signs:

    variables = {
    "sign": astro_sign[0],
    "sign_emoji": astro_sign[1],
    "love_img_url": "https://storage.mlcdn.com/account_image/954202/H2KjQhp6NnVK2ygP4GbcDxVURtZ17Y2agivQoFzq.png",
    "money_img_url": "https://storage.mlcdn.com/account_image/954202/LYbN58bxFxnmjrFRXkhFmuMS4pbr7bWtK4ukW5Dz.png",
    "health_img_url": "https://storage.mlcdn.com/account_image/954202/QWgMrXZJdFNuLEBAbWIqrUPc7oUa2GxXp692S5pf.png",
    }

    html = HtmlFile("weekly_newsletter.html", variables)
    content = html.content()
    htmls.append(html)



for suscriber in suscribers:

    # Objet et corps de l'email
    SUBJECT = f"{suscriber[2]} les astres on quelque chose d'important à te dire cette semaine... 👀"
    BODY_TEXT = "Bonjour,\nCeci est un email envoyé via Amazon SES."
    BODY_HTML = None
    for html in htmls:
        if html.sign == suscriber[3]:
            BODY_HTML = push_unsubscribe_link(suscriber[1], html.content())
    if not BODY_HTML:
        print(f"{ suscriber[3]} n'est pas dans {astro_signs}")
        break
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
        print("Email envoyé! Message ID:"),
        print(response['MessageId'])
    except ClientError as e:
        print(e.response['Error']['Message'])
