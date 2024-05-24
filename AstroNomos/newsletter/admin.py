from django.contrib import admin
from .models import Customer

# Enregistrement du modèle Customer dans l'admin
admin.site.register(Customer)
