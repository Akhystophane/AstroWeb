from rest_framework import serializers
from .models import React

class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['firebase_uid', 'id', 'birth_date', 'birth_time', 'birth_location']

class TransitSerializer(serializers.ModelSerializer):
    # Champs personnalisés, non liés au modèle
    transit_start_date = serializers.DateField()  # Définir des champs de type DateField pour les dates de transit
    transit_end_date = serializers.DateField()
    birth_time = serializers.TimeField()

    class Meta:
        model = React
        fields = ['firebase_uid', 'id', 'birth_date', 'birth_time', 'birth_location',
                  'transit_start_date', 'transit_end_date']