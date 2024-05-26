from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomerForm
from .forms import HoroscopeForm

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
