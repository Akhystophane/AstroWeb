from django.forms import ModelForm
from .models import Customer, HoroscopeSubscription
from django import forms



class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'

class HoroscopeForm(forms.ModelForm):
    zodiac_sign = forms.ChoiceField(
        choices=[('', 'Ton signe astrologique...')] + HoroscopeSubscription.ZODIAC_SIGN_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = HoroscopeSubscription
        fields = ['email', 'first_name', 'zodiac_sign']  # Les champs à inclure dans le formulaire
