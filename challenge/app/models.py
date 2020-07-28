from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import pre_delete
from django.dispatch import receiver

def validate_image(image):
    try:
        file_size = image.file.size
    except Exception:
        file_size = image.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f'O tamanho máximo é {limit_mb} MB')

# Create your models here.


class Cliente(models.Model):
    foto = models.ImageField(
        null=True, blank=True, verbose_name='Foto',
        validators=[validate_image])
    nome = models.CharField(
        max_length=30, verbose_name='Nome')
    sobrenome = models.CharField(
        max_length=30, verbose_name='Sobrenome')
    cpf = models.CharField(
        max_length=30, verbose_name='CPF', unique=True,
        validators=[
            RegexValidator('^\d{3}\.\d{3}\.\d{3}\-\d{2}$', 
                message="Formato esperado: '999.999.999-99'")])
    rg = models.CharField(
        max_length=30, verbose_name='RG', unique=True,
        validators=[
            RegexValidator(
                '^(\d\.?-?)+$')])
    telefone = models.CharField(
        max_length=30, verbose_name='Telefone',
        validators=[
            RegexValidator(
                '\(\d{2}\) \d{5}-\d{4}',
                message="Formato esperado: '(99) 99999-9999'")])
    email = models.EmailField(verbose_name='Email', unique=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'.upper()

    class Meta:
        verbose_name = 'Cliente'


class Endereco(models.Model):
    cliente = models.ForeignKey(
        'Cliente', verbose_name='Cliente',
        on_delete=models.CASCADE,
        related_name='enderecos')
    TIPO_CHOICES = [
        ('Principal', 'Principal'),
        ('Secundário', 'Secundário'),
    ]
    tipo = models.CharField(
        max_length=10, choices=TIPO_CHOICES,
        default='Principal', verbose_name='Tipo')
    ESTADO_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]
    logradouro = models.CharField(
        verbose_name='Logradouro', max_length=30)
    bairro = models.CharField(
        verbose_name='Bairro', max_length=30)
    cidade = models.CharField(
        verbose_name='Cidade', max_length=30)
    estado = models.CharField(
        verbose_name='Estado',
        max_length=2, choices=ESTADO_CHOICES,
        default='SP')
    numero = models.PositiveIntegerField(
        verbose_name='Número')

    def __str__(self):
        return (
            f'{self.logradouro}, {self.bairro}.'
            f' {self.cidade}-{self.estado}'
            f' ({self.tipo} de {self.cliente})'
        ).upper()

    class Meta:
        verbose_name = 'Endereço'
        unique_together = [[
            'logradouro',
            'bairro', 'cidade',
            'estado', 'numero'
        ], ]


@receiver(pre_delete, sender=Cliente)
def archive_cliente(sender, instance, **kwargs):
    ClienteArquivo(
        original_pk=instance.pk,
        foto=instance.foto, nome=instance.nome,
        sobrenome=instance.sobrenome,
        cpf=instance.cpf, rg=instance.rg,
        telefone=instance.telefone, email=instance.email
    ).save()


@receiver(pre_delete, sender=Endereco)
def archive_endereco(sender, instance, **kwargs):
    EnderecoArquivo(
        cliente_original=instance.cliente.pk,
        original_pk=instance.pk, tipo=instance.tipo,
        logradouro=instance.logradouro,
        bairro=instance.bairro, cidade=instance.cidade,
        estado=instance.estado, numero=instance.numero,
    ).save()

"""
Archives
"""


class ClienteArquivo(models.Model):
    deleted_on = models.DateTimeField(auto_now_add=True)
    original_pk = models.IntegerField()
    foto = models.ImageField()
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    cpf = models.CharField(max_length=30)
    rg = models.CharField(max_length=30)
    telefone = models.CharField(max_length=30)
    email = models.EmailField()


class EnderecoArquivo(models.Model):
    cliente_original = models.IntegerField()
    original_pk = models.IntegerField()
    tipo = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    numero = models.PositiveIntegerField()
