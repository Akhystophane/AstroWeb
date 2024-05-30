import os
import mailerlite as MailerLite
import psycopg2

api_key = os.getenv('MAILERLITE_API_KEY')
client = MailerLite.Client({
  'api_key': api_key
})

# Informations de connexion
conn_info = {
    'dbname': 'd7sbfac7jcpjh2',
    'user': 'ucqhnftdmflm74',
    'password': 'p7969dce61f8091b0a9fb823dbeef78344e1ad53100c233c5507967e451567099',
    'host': 'cat670aihdrkt1.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
    'port': '5432'  # par défaut, c'est généralement 5432
}


# Établir la connexion
conn = psycopg2.connect(**conn_info)
cursor = conn.cursor()

# Exécuter une requête SQL
cursor.execute("SELECT * FROM newsletter_horoscopesubscription")

# Récupérer les résultats
subscribers = cursor.fetchall()
# Fermer le curseur et la connexion
cursor.close()
conn.close()


data = client.subscribers.list()


def char_exists(email, data, char, fields=False):
    if fields:
        for record in data['data']:
            if record['fields'][char] == email:
                return True
    else:
        for record in data['data']:
            if record[char] == email:
                return True
    return False

for subscriber in subscribers:
    if not char_exists(subscriber[1], data, 'email'):
        response = client.subscribers.update(subscriber[1], fields={'first_name': subscriber[2], 'sign': subscriber[3]})
        print(response)

