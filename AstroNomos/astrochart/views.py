from datetime import datetime

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import React
from .serializer import ReactSerializer, TransitSerializer
from rest_framework.response import Response
from rest_framework import status

from assets.main import AstrologicalChart

from assets.Interpretation import get_birth_chart, get_transit_chart


class ReactItemView(generics.ListCreateAPIView):
    queryset = React.objects.all()
    serializer_class = ReactSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(birth_location__icontains=name)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        chart = AstrologicalChart(
            year=instance.birth_date.year,
            month=instance.birth_date.month,
            day=instance.birth_date.day,
            hour=instance.birth_time.hour,
            minute=instance.birth_time.minute,
            latitude=48.3,  # Supposons une fonction pour cela
            longitude=2.4  # Supposons une fonction pour cela

        )

        # Générer des informations supplémentaires ici (ex: une carte de naissance)
        birth_chart_data = chart.display_chartV2()
        birth_card = get_birth_chart(birth_chart_data)

        headers = self.get_success_headers(serializer.data)
        print(birth_card)

        # Retourner la réponse avec les données générées
        return Response({
            'message': 'Formulaire soumis avec succès',
            'birth_chart': birth_card
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class TransitChartView(generics.CreateAPIView):
    serializer_class = TransitSerializer

    def create(self, request, *args, **kwargs):
        print("Requête reçue avec les données:", request.data)  # Journal de débogage

        # Validation des données d'entrée
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        print("Données validées:", validated_data)  # Journal de débogage

        print('soucis', validated_data['birth_date'], validated_data['birth_time'])

        # Extraction des données validées
        birth_date = validated_data['birth_date']
        birth_time = validated_data['birth_time']
        transit_start_date = validated_data['transit_start_date']
        transit_end_date = validated_data['transit_end_date']

        print("birth_date:", birth_date, type(birth_date))  # Vérifier que birth_date est de type datetime.date
        print("birth_time:", birth_time, type(birth_time))
        birth_chart = AstrologicalChart(
            year=birth_date.year,
            month=birth_date.month,
            day=birth_date.day,
            hour=birth_time.hour,
            minute=birth_time.minute,
            latitude=10,
            longitude=10
        )

        # Calcul des transits
        transits = birth_chart.calculate_transits_for_period(
            start_date=transit_start_date,
            end_date=transit_end_date
        )

        # Comparaison des transits avec la carte natale
        transit_results = []
        for date, transit_positions in transits.items():
            comparison = {}
            for planet, transit_position in transit_positions.items():
                natal_position = birth_chart.planets_positions.get(planet, [0])[0]
                aspect = birth_chart.calculate_aspect(transit_position, natal_position)
                comparison[planet] = {
                    'transit_position': transit_position,
                    'natal_position': natal_position,
                    'aspect': aspect
                }
            transit_results.append({
                'date': date.strftime('%Y-%m-%d'),
                'comparisons': comparison
            })

        transit_chart = get_transit_chart(transit_results)
        print("Traitement réussi")  # Journal de débogage

        return Response({
            'message': 'Cartes de transit générées avec succès',
            'transit_results': transit_chart
        }, status=status.HTTP_201_CREATED)

