from django.forms import ModelForm

from app.models import Endereco


class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        exclude = []

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        tipo = cleaned_data.get('tipo')
        if tipo and cliente:
            qs = Endereco.objects.filter(
                cliente=cliente,
                tipo='Principal')
            if tipo == 'Principal':
                if qs:
                    self.add_error(
                        'tipo', 'Já existe um endereço principal'
                    )
            elif not qs:
                self.add_error(
                    'tipo', 'É preciso selecionar o endereço como principal'
                )
