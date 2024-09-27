from django.contrib import admin
from .models import React, UserProfile, TransitChart  # Importer votre modèle
# Enregistrez le modèle UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('firebase_uid', 'name', 'is_active', 'is_admin')  # Colonnes à afficher dans l'admin
    search_fields = ('firebase_uid', 'name')  # Champs à utiliser pour la recherche

# Enregistrez le modèle React
@admin.register(React)
class ReactAdmin(admin.ModelAdmin):
    list_display = ('firebase_uid', 'name', 'birth_date', 'birth_time', 'birth_location')  # Colonnes à afficher dans l'admin
    search_fields = ('firebase_uid', 'name')  # Champs à utiliser pour la recherche

@admin.register(TransitChart)
class TransitChartAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'transit_start_date', 'transit_end_date')
    search_fields = ('user__firebase_uid', 'name')
