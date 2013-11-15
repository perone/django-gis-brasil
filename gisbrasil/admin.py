from django.contrib.gis import admin
from models import *

class MunicipioAdmin(admin.GeoModelAdmin):
    list_filter = ['sigla', 'regiao', 'nome_mesorregiao',
        'nome_microrregiao']

    list_display = ['nome_municipio', 'sigla', 'regiao',
        'nome_mesorregiao', 'nome_microrregiao']

    search_fields = ['nome_municipio']

class PortoAlegreBairroAdmin(admin.GeoModelAdmin):
    list_filter = ['oficial']

    list_display = ['codigo_bairro', 'nome_bairro', 'oficial']

    search_fields = ['nome_bairro']

class PortoAlegreAcidenteTransitoAdmin(admin.GeoModelAdmin):
    list_display = ['dataset_id', 'data_hora', 'logradouro1',
        'logradouro2', 'local', 'tipo_acidente', 'noite_dia', 'tempo']
    list_filter = ['tipo_acidente', 'noite_dia', 'fonte', 'local',
        'data_hora', 'tempo']
    search_fields = ['logradouro1', 'logradouro2', 'dataset_id']

class PortoAlegreTaxiAdmin(admin.GeoModelAdmin):
    list_display = ['idtaxi', 'endereco', 'telefone']
    search_fields = ['idtaxi', 'endereco', 'telefone']

class PortoAlegreEstacaoBikePoaAdmin(admin.GeoModelAdmin):
    list_display = ['dataset_id', 'numero', 'nome']
    search_fields = ['dataset_id', 'numero', 'nome']

class PortoAlegreParadaAdmin(admin.GeoModelAdmin):
    list_display = ['idparada', 'codigo', 'terminal']
    search_fields = ['idparada', 'codigo']

admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(PortoAlegreBairro, PortoAlegreBairroAdmin)
admin.site.register(PortoAlegreAcidenteTransito, PortoAlegreAcidenteTransitoAdmin)
admin.site.register(PortoAlegreTaxi, PortoAlegreTaxiAdmin)
admin.site.register(PortoAlegreEstacaoBikePoa, PortoAlegreEstacaoBikePoaAdmin)
admin.site.register(PortoAlegreParada, PortoAlegreParadaAdmin)

