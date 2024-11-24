from frontend.services import decode_binary_string_to_image_file
from .models import *
from rest_framework import serializers
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = (
            'winter', 'summer', 'autumn', 'spring',
        )


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.ImageField()

    class Meta:
        model = Images
        fields = ('data', 'title',
                  )


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordinatesSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)
    add_data = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Pereval
        fields = ('id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_data',
                  'user', 'coords', 'level', 'images', 'status',
                  )
        read_only_fields = ['status']

    def create(self, validated_data):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user = User.objects.create(**user)
        coords = Coordinates.objects.create(**coords)
        level = Level.objects.create(**level)

        pereval = Pereval.objects.create(user=user, coords=coords, level=level, **validated_data)

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            img = decode_binary_string_to_image_file(pereval.id, title, data)
            img_path = f'{settings.SITE_URL}/{img.name}'
            Images.objects.create(data=img_path,pereval=pereval, title=title)

        return pereval

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get("user")
            validating_user_field = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_field):
                raise serializers.ValidationError({"Error": "Запрещено изменять данные пользователя"})
        return data
