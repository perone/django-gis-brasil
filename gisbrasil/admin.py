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


admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(PortoAlegreBairro, PortoAlegreBairroAdmin)
