"""challenge.api URL Configuration."""
from django.urls import path, include

from rest_framework import routers

from api.views import (
    error404, EnderecoDetailView,
    EnderecoListView, ClienteListView,
    ClienteDetailView)

urlpatterns = [
    path('cliente/', ClienteListView.as_view()),
    path('cliente/<int:pk>/', ClienteDetailView.as_view()),
    path(
        'cliente/<int:cliente_pk>/endereco/',
        EnderecoListView.as_view()),
    path(
        'cliente/<int:cliente_pk>/endereco/<int:endereco_pk>/',
        EnderecoDetailView.as_view()),
]

handler404 = error404
