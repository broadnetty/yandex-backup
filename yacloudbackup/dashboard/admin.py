from django.contrib import admin

# Register your models here.
from .models import CachedResources

admin.site.register(CachedResources)