from .models import *
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


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
            'latitude', 'longitude', 'height',
        )


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = (
            'winter', 'summer', 'autumn', 'spring',
        )


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.CharField()

    class Meta:
        model = Images
        fields = (
            'data', 'title',
        )


class PerevalSerializer(WritableNestedModelSerializer):
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
        # read_only_fields = ['status']

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get("user")

            if data_user is not None:
                validating_user_field = [
                    instance_user.fam != data_user.get('fam'),
                    instance_user.name != data_user.get('name'),
                    instance_user.otc != data_user.get('otc'),
                    instance_user.phone != data_user.get('phone'),
                    instance_user.email != data_user.get('email'),
                ]

                if any(validating_user_field):
                    raise serializers.ValidationError({"Error": "Запрещено изменять данные пользователя"})
            else:
                raise serializers.ValidationError({"Error": "Данные пользователя отсутствуют"})

        return data
