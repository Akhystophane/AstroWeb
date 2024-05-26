from django.urls import path
from . import views

urlpatterns = [
    path('', views.horoscope, name='horoscope'),
    path('success/', views.success, name='success'),
    path('subscribe/', views.subscribe, name='subscribe'),

]