from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
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
                "status": status.HTTP_201_CREATED,
                "message": "OK",
                'id': serializer.data['id'],
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": serializer.errors,
            "id": None,
        }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == "new":
            serializer = PerevalSerializer(pereval, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "state": "1",
                    "message": "Запись изменена",
                }, status=status.HTTP_200_OK)

            return Response({
                "state": "0",
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "state": "0",
                "message": f"Отклонено. Причина: {pereval.get_status_display()}",
            }, status=status.HTTP_403_FORBIDDEN)

