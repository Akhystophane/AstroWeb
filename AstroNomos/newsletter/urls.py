from django.urls import path
from . import views

urlpatterns = [
    path('', views.horoscope, name='horoscope'),
    path('test', views.index, name='index'),
    path('subscribe/', views.subscribe, name='subscribe'),

]