from django.urls import path
from . import views

urlpatterns = [
    path('', views.horoscope, name='horoscope'),
    path('success/', views.success, name='success'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<str:token>/', views.unsubscribe, name='unsubscribe'),
    path("callback/", views.tiktok_callback, name="tiktok_callback"),

]