import logging
import os
import json
from rest_framework import authentication, exceptions
import firebase_admin
from firebase_admin import auth as firebase_auth

# Initialisez l'application Firebase Admin si ce n'est pas déjà fait
from .models import React, UserProfile

logger = logging.getLogger(__name__)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Vérifiez si Firebase Admin SDK est déjà initialisé
        if not firebase_admin._apps:
            try:
                # Récupérez les informations d'authentification Firebase à partir des variables d'environnement
                firebase_credentials = os.getenv('FIREBASE_ADMIN_CREDENTIALS')
                if not firebase_credentials:
                    raise ValueError("Firebase credentials are not set in the environment")

                # Charger et convertir la chaîne JSON en dictionnaire Python
                cred = firebase_admin.credentials.Certificate(json.loads(firebase_credentials))
                firebase_admin.initialize_app(cred)
            except Exception as e:
                logger.error(f"Erreur lors de l'initialisation de Firebase Admin SDK: {e}")
                raise exceptions.AuthenticationFailed('Failed to initialize Firebase Admin SDK')

        # Extraire l'en-tête d'authentification (Authorization: Bearer <token>)
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None  # Aucune authentification fournie, donc ne pas bloquer la requête

        # Récupérer le token JWT (Firebase ID token)
        id_token = auth_header.split(' ').pop()
        try:
            # Vérifiez et décodez le token Firebase
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du token Firebase: {e}")
            raise exceptions.AuthenticationFailed('Invalid Firebase token')

        # Récupérez l'UID de l'utilisateur à partir du token décodé
        uid = decoded_token.get('uid')
        if not uid:
            raise exceptions.AuthenticationFailed('No UID found in token')

        # Créer ou récupérer un utilisateur associé à cet UID
        user, created = UserProfile.objects.get_or_create(firebase_uid=uid, defaults={'name': 'Default Name'})

        # Vous pouvez créer un objet utilisateur personnalisé ou utiliser le modèle React si nécessaire
        user.uid = uid  # Assurez-vous que l'objet utilisateur a un attribut 'uid'

        # Retournez l'utilisateur authentifié
        return (user, None)
