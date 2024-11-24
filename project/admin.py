from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Level)
admin.site.register(Coordinates)
admin.site.register(Images)
admin.site.register(Pereval)