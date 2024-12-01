"""
URL configuration for Pereval project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from project import viewsets
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# drf_spectacular
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView
# )


router = routers.DefaultRouter()
router.register(r'SubmitData', viewsets.PerevalViewset, basename='pereval')

schema_view = get_schema_view(
       openapi.Info(
           title="Your API",
           default_version='v1',
           description="Test description",
           terms_of_service="https://www.google.com/policies/terms/",
           contact=openapi.Contact(email="contact@yourapi.local"),
           license=openapi.License(name="BSD License"),
       ),
       public=True,
   )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    re_path(
        r'^swagger.(?P<format>json|yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),


    # drf_spectacular

    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    # path(
    #     'api/schema/swagger-ui/',
    #     SpectacularSwaggerView.as_view(url_name='schema'),
    #     name='swagger-ui'
    # ),
    # path(
    #     'api/schema/redoc/',
    #     SpectacularRedocView.as_view(url_name='schema'),
    #     name='redoc'
    # ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
