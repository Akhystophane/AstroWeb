from rest_framework import serializers
from .models import React, TransitChart

from rest_framework import serializers
from .models import React
from .models import UserProfile


class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['firebase_uid', 'birth_date', 'birth_time', 'birth_location', 'name']
        read_only_fields = ['firebase_uid']


class BirthChartSerializer(serializers.Serializer):
    birth_date = serializers.DateField(required=True)
    birth_time = serializers.TimeField(required=True)
    birth_location = serializers.CharField(max_length=255, required=True)


class TransitChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitChart
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        return TransitChart.objects.create(user=user, **validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['firebase_uid', 'name']
        read_only_fields = ['firebase_uid']