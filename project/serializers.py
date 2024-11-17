from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'fam', 'name', 'otc', 'phone',
        )


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = (
            'latitude', 'longitude', 'height'
        )


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = (
            'winter', 'summer', 'autumn', 'spring',
        )


class PerevalSerializer(serializers.ModelSerializer):
    user

