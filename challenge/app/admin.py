from django.contrib import admin

from app.models import Cliente, Endereco
from app.forms import EnderecoForm
# Register your models here.


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    form = EnderecoForm


admin.site.register(Cliente)


"""
Archives
"""

'''
from app.models import ClienteArquivo, EnderecoArquivo

admin.site.register(ClienteArquivo)
admin.site.register(EnderecoArquivo)
'''
