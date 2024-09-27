import json
import psycopg2
def get_dataset():
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
    # for subscriber in subscribers:
    #     if not char_exists(subscriber[1], data, 'email'):
    #         response = client.subscribers.update(subscriber[1], fields={'first_name': subscriber[2], 'sign': subscriber[3]})
    #         print(subscriber[1])
    return subscribers, cursor

import dns.resolver

def check_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.NXDOMAIN:
        return False


# Charger le fichier JSON existant ou en créer un nouveau s'il n'existe pas
def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []  # Retourne une liste vide si le fichier n'existe pas
def create_record():
    # Récupérer les noms des colonnes de la table
    subscribers, cursor = get_dataset()
    column_names = [desc[0] for desc in cursor.description]

    # Créer une liste de dictionnaires avec les résultats et ajouter les nouvelles clés
    subscribers_with_keys = []
    for subscriber in subscribers:
        subscriber_dict = dict(zip(column_names, subscriber))
        subscriber_dict['is_weekly_horoscope_sent'] = False  # Ajouter la clé avec valeur False
        subscriber_dict['newsletter_log'] = {}  # Ajouter la clé avec un dictionnaire vide
        subscribers_with_keys.append(subscriber_dict)

    # Fermer le curseur et la connexion
    cursor.close()
    conn.close()

    # Enregistrer le résultat dans un fichier JSON
    with open('subscribers.json', 'w', encoding='utf-8') as json_file:
        json.dump(subscribers_with_keys, json_file, ensure_ascii=False, indent=4)

    print("Fichier JSON créé avec succès : subscribers.json")


# Fonction pour mettre à jour le fichier JSON en fonction des données de la base de données
def update_record(reset=False):
    subscribers, cursor = get_dataset()
    # Charger le fichier JSON existant
    json_data = load_json_file('subscribers.json')

    # Récupérer les emails existants dans le fichier JSON
    json_emails = {subscriber['email']: subscriber for subscriber in json_data}

    # Récupérer les noms des colonnes de la table
    column_names = [desc[0] for desc in cursor.description]

    # Mise à jour des abonnés
    for subscriber in subscribers:
        # Convertir chaque tuple en dictionnaire
        subscriber_dict = dict(zip(column_names, subscriber))
        email = subscriber_dict['email']

        # Vérifier si l'utilisateur est déjà dans le fichier JSON
        if email in json_emails:
            if reset:
                subscriber_dict['is_weekly_horoscope_sent'] = False
            # Mettre à jour l'utilisateur existant
            json_emails[email].update(subscriber_dict)
        else:
            # Ajouter un nouvel utilisateur
            subscriber_dict['is_weekly_horoscope_sent'] = False
            subscriber_dict['newsletter_log'] = {}
            json_emails[email] = subscriber_dict

    # Créer un ensemble d'emails à partir des abonnés de la base de données convertis en dictionnaires
    db_emails = {dict(zip(column_names, subscriber))['email'] for subscriber in subscribers}

    # Supprimer les utilisateurs du fichier JSON qui ne sont pas dans la base de données
    json_data = [user for email, user in json_emails.items() if email in db_emails]

    # Enregistrer les modifications dans le fichier JSON
    with open('subscribers.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    print("Fichier JSON mis à jour avec succès.")



# create_record(subscribers)
# update_record(reset=True)

