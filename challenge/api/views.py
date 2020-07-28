from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import status

from api.serializers import (
    ClienteSerializer, EnderecoSerializer)
from app.models import Cliente, Endereco

# Create your views here.

class JsonDetailView(generics.RetrieveUpdateDestroyAPIView):
    def put(self, request, *args, **kwargs):
        try:
            return super().put(request, *args, **kwargs)
        except ParseError as e:
            return Response(
                {'ValidationError': str(e)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def patch(self, request, *args, **kwargs):
        try:
            return super().patch(request, *args, **kwargs)
        except ParseError as e:
            return Response(
                {'ValidationError': str(e)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class JsonListView(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ParseError as e:
            return Response(
                {'ValidationError': str(e)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ClienteDetailView(JsonDetailView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ClienteListView(JsonListView):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()


class EnderecoListView(JsonListView):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

    def get_queryset(self):
        cliente_pk = self.kwargs['cliente_pk']
        cliente = get_object_or_404(
            Cliente.objects.all(), pk=cliente_pk)
        qs = cliente.enderecos.all()
        return qs

    def perform_create(self, serializer):
        cliente_pk = self.kwargs['cliente_pk']
        cliente = get_object_or_404(
            Cliente.objects.all(), pk=cliente_pk)
        serializer.save(cliente=cliente)


class EnderecoDetailView(JsonDetailView):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

    def get_object(self):
        cliente_pk = self.kwargs['cliente_pk']
        endereco_pk = self.kwargs['endereco_pk']
        cliente = get_object_or_404(
                Cliente.objects.all(), pk=cliente_pk)
        obj = get_object_or_404(
                cliente.enderecos.all(), pk=endereco_pk)
        return obj

def error404(request, exception=None):
    raise NotFound(
        detail='Rota não encontrada',
        code=404)
