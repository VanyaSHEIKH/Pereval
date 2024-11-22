from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields='__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = (
            'winter', 'summer', 'autumn', 'spring',
        )


class ImagesSerializer(serializers.ModelSerializer):
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
                raise serializers.ValidationError({"Ошибка": "Запрещено изменять данные пользователя"})
        return data
