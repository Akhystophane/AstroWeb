from django.shortcuts import render
from django.http import HttpResponse
from .forms import CustomerForm
def index(request):
    form = CustomerForm()

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'newsletter/index.html', context)

def subscribe(request):
    return HttpResponse("Page d'abonnement à la newsletter.")
