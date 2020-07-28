from rest_framework import serializers

from app.models import Cliente, Endereco


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        exclude = []


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        exclude = []
        extra_kwargs = {
            'tipo': {
                'required': True
            },
            'cliente': {
                    'required': False,
                    'write_only': True,
                }
        }

    def save(self, *args, **kwargs):
        cliente = kwargs.get('cliente')
        tipo = self.validated_data.get('tipo')
        if tipo and cliente:
            qs = Endereco.objects.filter(
                cliente=cliente,
                tipo='Principal')
            if tipo == 'Principal':
                if qs:
                    raise serializers.ValidationError({
                        'tipo': 'Já existe um endereço principal.'})
            elif not qs:
                raise serializers.ValidationError(
                    {'tipo': 'Defina o endereço como principal'})
        return super().save(*args, **kwargs)
