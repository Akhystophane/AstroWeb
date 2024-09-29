# from datetime import datetime
#
# from rest_framework import generics
# from rest_framework.exceptions import ValidationError
# from rest_framework.views import APIView
#
# from .models import React
# from .serializer import ReactSerializer, TransitSerializer
# from rest_framework.response import Response
# from rest_framework import status
#
# from assets.main import AstrologicalChart
#
# from assets.Interpretation import get_birth_chart, get_transit_chart
#
#
# class ReactItemView(generics.ListCreateAPIView):
#     queryset = React.objects.all()
#     serializer_class = ReactSerializer
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         firebase_uid = self.request.query_params.get('firebase_uid')
#         birth_location = self.request.query_params.get('birth_location')
#         birth_date = self.request.query_params.get('birth_date')
#
#         if firebase_uid:
#             queryset = queryset.filter(firebase_uid=firebase_uid)
#         if birth_location:
#             queryset = queryset.filter(birth_location__icontains=birth_location)
#         if birth_date:
#             queryset = queryset.filter(birth_date=birth_date)
#
#         return queryset
#
#     def create(self, request, *args, **kwargs):
#         print("Données de la requête :", request.data)  # Log des données reçues
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)  # Si cela échoue, il imprimera l'erreur exacte
#         instance = self.perform_create(serializer)
#
#         chart = AstrologicalChart(
#             year=instance.birth_date.year,
#             month=instance.birth_date.month,
#             day=instance.birth_date.day,
#             hour=instance.birth_time.hour,
#             minute=instance.birth_time.minute,
#             latitude=48.3,  # Supposons une fonction pour cela
#             longitude=2.4  # Supposons une fonction pour cela
#         )
#
#         birth_chart_data = chart.display_chartV2()
#         birth_card = get_birth_chart(birth_chart_data)
#
#         headers = self.get_success_headers(serializer.data)
#
#         return Response({
#             'message': 'Formulaire soumis avec succès',
#             'birth_chart': birth_card
#         }, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         return serializer.save()
#
#     def put(self, request, *args, **kwargs):
#         firebase_uid = request.query_params.get('firebase_uid')
#         if not firebase_uid:
#             return Response({"detail": "firebase_uid is required for update."}, status=status.HTTP_400_BAD_REQUEST)
#
#         instance = React.objects.filter(firebase_uid=firebase_uid).first()
#         if not instance:
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         if getattr(instance, '_prefetched_objects_cache', None):
#             instance._prefetched_objects_cache = {}
#
#         return Response(serializer.data)
#
#     def perform_update(self, serializer):
#         serializer.save()
#
#
# class TransitChartView(generics.CreateAPIView):
#     serializer_class = TransitSerializer
#
#     def create(self, request, *args, **kwargs):
#         print("Requête reçue avec les données:", request.data)  # Journal de débogage
#
#         # Validation des données d'entrée
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         validated_data = serializer.validated_data
#
#         print("Données validées:", validated_data)  # Journal de débogage
#
#         print('soucis', validated_data['birth_date'], validated_data['birth_time'])
#
#         # Extraction des données validées
#         birth_date = validated_data['birth_date']
#         birth_time = validated_data['birth_time']
#         transit_start_date = validated_data['transit_start_date']
#         transit_end_date = validated_data['transit_end_date']
#
#         print("birth_date:", birth_date, type(birth_date))  # Vérifier que birth_date est de type datetime.date
#         print("birth_time:", birth_time, type(birth_time))
#         birth_chart = AstrologicalChart(
#             year=birth_date.year,
#             month=birth_date.month,
#             day=birth_date.day,
#             hour=birth_time.hour,
#             minute=birth_time.minute,
#             latitude=10,
#             longitude=10
#         )
#
#         # Calcul des transits
#         transits = birth_chart.calculate_transits_for_period(
#             start_date=transit_start_date,
#             end_date=transit_end_date
#         )
#
#         # Comparaison des transits avec la carte natale
#         transit_results = []
#         for date, transit_positions in transits.items():
#             comparison = {}
#             for planet, transit_position in transit_positions.items():
#                 natal_position = birth_chart.planets_positions.get(planet, [0])[0]
#                 aspect = birth_chart.calculate_aspect(transit_position, natal_position)
#                 comparison[planet] = {
#                     'transit_position': transit_position,
#                     'natal_position': natal_position,
#                     'aspect': aspect
#                 }
#             transit_results.append({
#                 'date': date.strftime('%Y-%m-%d'),
#                 'comparisons': comparison
#             })
#
#         transit_chart = get_transit_chart(transit_results)
#         print("Traitement réussi")  # Journal de débogage
#
#         return Response({
#             'message': 'Cartes de transit générées avec succès',
#             'transit_results': transit_chart
#         }, status=status.HTTP_201_CREATED)
#
# from rest_framework import generics
# from .models import React
# from .serializer import ReactSerializer
#
# class ReactDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = React.objects.all()
#     serializer_class = ReactSerializer
#     lookup_field = 'firebase_uid'          # Use 'firebase_uid' as the lookup field
#     lookup_url_kwarg = 'firebase_uid'      # Match the URL parameter name
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)  # Permet de prendre en charge les mises à jour partielles
#         instance = self.get_object()  # Récupérer l'objet à mettre à jour
#
#         # Sérialiser les données de la requête
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#
#         # Effectuer la mise à jour
#         self.perform_update(serializer)
#
#         # Calculer la carte astrologique si les données de naissance sont mises à jour
#         chart = AstrologicalChart(
#             year=serializer.validated_data['birth_date'].year,
#             month=serializer.validated_data['birth_date'].month,
#             day=serializer.validated_data['birth_date'].day,
#             hour=serializer.validated_data['birth_time'].hour,
#             minute=serializer.validated_data['birth_time'].minute,
#             latitude=48.3,  # Latitude exemple
#             longitude=2.4  # Longitude exemple
#         )
#
#         # Générer des informations supplémentaires ici (ex: une carte de naissance)
#         birth_chart_data = chart.display_chartV2()
#         birth_card = get_birth_chart(birth_chart_data)
#
#         return Response({
#             'message': 'Données mises à jour avec succès',
#             'birth_chart': birth_card,
#             'data': serializer.data
#         }, status=status.HTTP_200_OK)
#
#     def perform_update(self, serializer):
#         serializer.save()
#
#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def perform_destroy(self, instance):
#         instance.delete()
"----------------------------------------------------------------------------------------------------------------------"
"----------------------------------------------------------------------------------------------------------------------"
"----------------------------------------------------------------------------------------------------------------------"
"----------------------------------------------------------------------------------------------------------------------"
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle



# views.py

from rest_framework import generics, permissions
from .models import UserProfile, TransitChart
from .serializer import UserProfileSerializer, BirthChartSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        firebase_uid = self.request.user.uid  # Obtenez le UID depuis le token Firebase
        return UserProfile.objects.get(firebase_uid=firebase_uid)

from rest_framework import generics, permissions
from .models import React
from .serializer import ReactSerializer

class ReactItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = React.objects.all()
    serializer_class = ReactSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'firebase_uid'

    def get_queryset(self):
        # Filtrer les données pour n'afficher que celles de l'utilisateur authentifié
        firebase_uid = self.request.user.uid  # Obtenez le UID depuis le token Firebase
        return React.objects.filter(firebase_uid=firebase_uid)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from assets.utils import generate_birth_chart  # Fonction utilitaire à créer

class BirthChartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        # Utiliser le serializer pour valider les données
        serializer = BirthChartSerializer(data=request.data)
        if serializer.is_valid():
            birth_date = serializer.validated_data['birth_date']
            birth_time = serializer.validated_data['birth_time']
            birth_location = serializer.validated_data['birth_location']
            name = serializer.validated_data.get('name', '')  # Obtenir le nom si fourni

            # Générer la carte de naissance
            birth_chart = generate_birth_chart(birth_date, birth_time, birth_location)

            # Enregistrer les données dans le modèle React
            firebase_uid = request.user.firebase_uid  # Assurez-vous que ceci est correct
            react_instance = React.objects.create(
                firebase_uid=firebase_uid,
                birth_date=birth_date,
                birth_time=birth_time,
                birth_location=birth_location,
                name=name
            )

            return Response({
                'message': 'Carte de naissance générée avec succès',
                'birth_chart': birth_chart,
                'chart_id': react_instance.id  # Optionnel : retourner l'ID de l'enregistrement
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from assets.utils import generate_transit_chart
from .serializer import TransitChartSerializer

class TransitChartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        serializer = TransitChartSerializer(data=request.data)
        if serializer.is_valid():
            # Récupérer les données validées
            birth_date = serializer.validated_data['birth_date']
            birth_time = serializer.validated_data['birth_time']
            birth_location = serializer.validated_data['birth_location']
            transit_start_date = serializer.validated_data['transit_start_date']
            transit_end_date = serializer.validated_data['transit_end_date']
            name = serializer.validated_data.get('name', '')

            # Générer la carte de transit
            transit_chart_data = generate_transit_chart(
                birth_date,
                birth_time,
                birth_location,
                transit_start_date,
                transit_end_date
            )

            # Enregistrer les données dans le modèle TransitChart
            transit_chart_instance = TransitChart.objects.create(
                user=request.user,  # Utiliser l'utilisateur authentifié
                birth_date=birth_date,
                birth_time=birth_time,
                birth_location=birth_location,
                transit_start_date=transit_start_date,
                transit_end_date=transit_end_date,
                name=name
            )

            return Response({
                'message': 'Cartes de transit générées avec succès',
                'transit_chart': transit_chart_data,
                'chart_id': transit_chart_instance.id
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserReactDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        react_data = React.objects.filter(user=request.user)
        serializer = ReactSerializer(react_data, many=True)
        return Response(serializer.data)

from django.views.generic import TemplateView

class FrontendAppView(TemplateView):
    template_name = 'index.html'