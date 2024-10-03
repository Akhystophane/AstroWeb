"""
URL configuration for AstroNomos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from newsletter import views as newsletter_views

from astrochart.views import ReactItemView, TransitChartView, BirthChartView, UserReactDataView, FrontendAppView
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('newsletter/', include('newsletter.urls')),
    path('newsletter/', newsletter_views.horoscope, name='newsletter'),
    path('react', ReactItemView.as_view(), name='react-items'),
    # path('react/<str:firebase_uid>', ReactDetailView.as_view(), name='react-detail-update'),
    path('user/data/<str:firebase_uid>/', ReactItemView.as_view(), name='user-data'),  # Inclure firebase_uid
    path('', FrontendAppView.as_view(), name='frontend'),

    path('charts/birth/', BirthChartView.as_view(), name='birth-chart'),
    path('charts/transit/', TransitChartView.as_view(), name='transit-chart'),
    # path('user/data/', ReactItemView.as_view(), name='user-data'),
    path('user-react-data/', UserReactDataView.as_view(), name='user-react-data'),
    path('__/auth/iframe', TemplateView.as_view(template_name="__/auth/iframe.html")),
    path('__/auth/handler', TemplateView.as_view(template_name="__/auth/handler.html")),  # Réutiliser le même template

]