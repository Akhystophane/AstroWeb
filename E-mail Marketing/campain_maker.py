import os
from html_maker import HtmlFile
import mailerlite as MailerLite
from Suscribers import char_exists



api_key = os.getenv('MAILERLITE_API_KEY')
client = MailerLite.Client({
  'api_key': api_key
})


astro_signs = []
signs = [
    # ["aries", "Bélier", "♈"],
    # ["taurus", "Taureau", "♉"],
    # ["gemini", "Gémeaux", "♊"],
    # ["cancer", "Cancer", "♋"],
    # ["leo", "Lion", "♌"],
    # ["virgo", "Vierge", "♍"],
    # ["libra", "Balance", "♎"],
    # ["scorpio", "Scorpion", "♏"],
    # ["capricorn", "Capricorne", "♑"],
    # ["aquarius", "Verseau", "♒"],
    # ["pisces", "Poisson", "♓"],
    ["sagittarius", "Sagittaire", "♐"],
]
data = client.subscribers.list()
for sign in signs:
    if char_exists(sign[0],data, 'sign', fields=True):
        astro_signs.append([sign[1], sign[2]])

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



for html in htmls:

    params = {
        "name": html.campaign_name,
        "type": "regular",
        "emails": [{
            "subject": f"{html.sign} les astres on quelque chose d'important à te dire cette semaine... 👀",
            "from_name": "AstroNomos",
            "from": "newsletter@astro-nomos.com",
            "content": html.content()
        }]
    }

    response = client.campaigns.create(params)
    print(response)