from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from .serializers import *
from .models import *


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordinatesViewset(viewsets.ModelViewSet):
    queryset = Coordinates.objects.all()
    serializer_class = CoordinatesSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ["user__email"]

    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "created_status": "success",
                "message": "OK",
                'id': serializer.data['id'],
            })

        return Response({
            "error_status": "error",
            "message": serializer.errors,
            "id": None,
        })

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == "new":
            serializer = PerevalSerializer(pereval, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "state": "1",
                    "message": "Запись изменена",
                })

            else:
                return Response({
                    "state": "0",
                    "message": serializer.errors,
                })

        return Response({
            "state": "0",
            "message": f"Отклонено. Причина {pereval.get_status_display()} ",
        })
