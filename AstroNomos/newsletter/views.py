from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CustomerForm
from .forms import HoroscopeForm
from .models import HoroscopeSubscription


def index(request):
    form = CustomerForm()

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'horoscope.html', context)

def horoscope(request):
    if request.method == 'POST':
        form = HoroscopeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HoroscopeForm()

    return render(request, 'newsletter/index.html', {'form': form})

def success(request):
    return render(request, 'newsletter/success.html')
def subscribe(request):
    return HttpResponse("Page d'abonnement à la newsletter.")


def unsubscribe(request, token):
    # Rechercher l'abonné à l'aide du jeton de désabonnement
    subscription = get_object_or_404(HoroscopeSubscription, unsubscribe_token=token)

    # Marquer l'abonné comme désabonné
    subscription.subscribed = False
    subscription.save()

    # Renvoyer une réponse de confirmation
    return HttpResponse("Vous avez été désabonné avec succès.")