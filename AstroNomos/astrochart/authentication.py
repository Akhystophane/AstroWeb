import logging

from rest_framework import authentication, exceptions
import firebase_admin
from firebase_admin import auth as firebase_auth

# Initialisez l'application Firebase Admin si ce n'est pas déjà fait
from .models import React, UserProfile

logger = logging.getLogger(__name__)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if not firebase_admin._apps:
            try:
                cred = firebase_admin.credentials.Certificate(
                    '/Users/emmanuellandau/Downloads/astronomos-ef1e7-firebase-adminsdk-h33a2-784eef27f6.json')
                firebase_admin.initialize_app(cred)
            except Exception as e:
                logger.error(f"Erreur lors de l'initialisation de Firebase Admin SDK: {e}")
                raise exceptions.AuthenticationFailed('Failed to initialize Firebase Admin SDK')
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header:
            return None

        id_token = auth_header.split(' ').pop()
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid Firebase token')

        uid = decoded_token.get('uid')
        user, created = UserProfile.objects.get_or_create(firebase_uid=uid, defaults={'name': 'Default Name'})

        # Vous pouvez créer un objet utilisateur personnalisé ou utiliser le modèle React
        user.uid = uid  # Assurez-vous que l'objet utilisateur a un attribut 'uid'

        return (user, None)
