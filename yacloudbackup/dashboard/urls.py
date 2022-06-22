from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('resources', views.resources, name='resources'),
    path('sessions', views.sessions, name='sessions'),
    path('policies', views.policies, name='policies')
]