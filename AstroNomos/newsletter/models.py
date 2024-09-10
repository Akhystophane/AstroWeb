import uuid

from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    e_mail = models.EmailField(max_length=200, default='')

    def __str__(self):
        return self.first_name


class HoroscopeSubscription(models.Model):
    ZODIAC_SIGN_CHOICES = [
        ('aries', '♈ Bélier'),
        ('taurus', '♉ Taureau'),
        ('gemini', '♊ Gémeaux'),
        ('cancer', '♋ Cancer'),
        ('leo', '♌ Lion'),
        ('virgo', '♍ Vierge'),
        ('libra', '♎ Balance'),
        ('scorpio', '♏ Scorpion'),
        ('sagittarius', '♐ Sagittaire'),
        ('capricorn', '♑ Capricorne'),
        ('aquarius', '♒ Verseau'),
        ('pisces', '♓ Poissons'),
    ]

    zodiac_sign = models.CharField(
        max_length=20,
        choices=ZODIAC_SIGN_CHOICES,
        # default='aries'  # optionnellement, vous pouvez ajouter un choix par défaut
    )
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=100)
    subscribed = models.BooleanField(default=True)  # Nouveau champ pour gérer l'abonnement
    unsubscribe_token = models.CharField(max_length=64, unique=True, null=True, blank=True)  # Jeton de désabonnement

    def __str__(self):
        return f"{self.first_name} ({self.zodiac_sign})"

    def generate_unsubscribe_token(self):
        # Génère un jeton unique pour le désabonnement
        self.unsubscribe_token = str(uuid.uuid4())
        self.save()

