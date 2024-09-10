from django.contrib import admin
from .models import Customer, HoroscopeSubscription

# Enregistrement du modèle Customer dans l'admin
admin.site.register(Customer)
# Enregistrement du modèle dans l'admin
@admin.register(HoroscopeSubscription)
class HoroscopeSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'zodiac_sign', 'subscribed')  # Champs à afficher dans la liste admin
    search_fields = ('email', 'first_name')  # Champs sur lesquels vous pouvez effectuer des recherches
    list_filter = ('subscribed', 'zodiac_sign')