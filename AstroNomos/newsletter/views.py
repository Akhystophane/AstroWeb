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


import requests
from django.http import JsonResponse

def tiktok_callback(request):
    """
    Vue qui reçoit la redirection OAuth de TikTok :
    https://www.astro-nomos.com/callback?code=...&state=...
    """
    # 1. Récupérer le paramètre 'code' dans l'URL
    code = request.GET.get("code")
    state = request.GET.get("state")

    if not code:
        return HttpResponse("No 'code' found in the query parameters.", status=400)

    # 2. Échanger le code contre un access token TikTok
    #    - On fait un POST sur https://open.tiktokapis.com/v2/oauth/token/
    #    - Les paramètres attendus : client_key, client_secret, code, redirect_uri, grant_type=authorization_code

    client_key = "TON_CLIENT_KEY"       # stocke en variable d'env en prod !
    client_secret = "TON_CLIENT_SECRET" # stocke en variable d'env en prod !
    redirect_uri = "https://www.astro-nomos.com/callback"  # la même que déclarée dans la console TikTok

    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    data = {
        "client_key": client_key,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code != 200:
        return HttpResponse(f"Error fetching token: {response.status_code} {response.text}", status=400)

    token_data = response.json()
    # Exemple de réponse attendue :
    # {
    #   "data": {
    #       "access_token": "...",
    #       "expires_in": 7200,
    #       "refresh_token": "...",
    #       "scope": "...",
    #       ...
    #   }
    # }

    # 3. Stocker ou manipuler le token
    #    - Soit en base de données (modèle Django), soit en session,
    #      soit rediriger l'utilisateur vers une page "compte lié", etc.
    access_token = token_data.get("access_token")
    if not access_token:
        # Parfois la clé peut être dans token_data["data"]["access_token"]
        access_token = token_data.get("data", {}).get("access_token")

    if not access_token:
        return HttpResponse("No access token in response.", status=400)
    print(access_token)

    # 4. (Optionnel) Enregistrer le token en base, ou le stocker en session
    #    Par exemple, si tu as un modèle "UserToken":
    # from .models import UserToken
    # UserToken.objects.create(token=access_token, ...)

    # 5. Rediriger ou retourner un message
    return JsonResponse({
        "status": "success",
        "access_token": access_token,
        "raw_response": token_data
    })