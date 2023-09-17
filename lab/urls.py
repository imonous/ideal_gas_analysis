from django.urls import path

from .views import index, simulation

urlpatterns = [
    path("", index, name="index"),
    path("simulation", simulation, name="simulation"),
]
