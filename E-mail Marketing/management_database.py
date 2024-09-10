import csv
import psycopg2

# Lire les emails valides à partir du fichier CSV
valid_emails = set()

# Remplacez le chemin par le chemin réel de votre fichier CSV
csv_file_path = '/Users/emmanuellandau/Downloads/newsletter_horoscopesubscription.valids.csv'

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        email = row[0].strip()  # Supprime les espaces blancs autour des emails
        valid_emails.add(email)

# Informations de connexion à la base de données
conn_info = {
    'dbname': 'd7sbfac7jcpjh2',
    'user': 'ucqhnftdmflm74',
    'password': 'p7969dce61f8091b0a9fb823dbeef78344e1ad53100c233c5507967e451567099',
    'host': 'cat670aihdrkt1.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

# Établir la connexion
conn = psycopg2.connect(**conn_info)
cursor = conn.cursor()

# Convertir l'ensemble des emails valides en une liste de chaînes formatées pour SQL
valid_emails_list = tuple(valid_emails)  # Convertir en tuple pour la requête SQL

# Requête SQL pour supprimer les abonnés dont l'email n'est pas dans la liste des emails valides
delete_query = """
DELETE FROM newsletter_horoscopesubscription
WHERE email NOT IN %s;
"""

# Exécuter la requête de suppression
cursor.execute(delete_query, (valid_emails_list,))
conn.commit()

# Fermer le curseur et la connexion
cursor.close()
conn.close()

print("Les abonnés non valides ont été supprimés de la base de données.")
