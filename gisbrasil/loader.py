# happy fish-coding: utf-8

import os
from django.contrib.gis.utils import LayerMapping
from models import *

municipios_mapping = {
    'geocode': 'GEOCODIG_M',
    'uf': 'UF',
    'sigla': 'Sigla',
    'nome_municipio': 'Nome_Munic',
    'regiao': u'Regi\xe3o',
    'mesorregiao': u'Mesorregi\xe3',
    'nome_mesorregiao': 'Nome_Meso',
    'microregiao': 'Microrregi',
    'nome_microrregiao': 'Nome_Micro',
    'multipoly' : 'MULTIPOLYGON',
}

portoalegrebairro_mapping = {
    'codigo_bairro': 'COD_BAIRRO',
    'oficial': 'OFICIAL',
    'nome_bairro': 'NOM_BAIRRO',
    'poly': 'POLYGON',
}

municipios_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'data/brasil/55mu2500gsd.shp'))

portoalegrebairro_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'data/rs/portoalegre/bairros_utm22_sad69.shp'))

def load_municipios_brasil(verbose=True):
    lm = LayerMapping(Municipio, municipios_shp, municipios_mapping,
                    transform=True, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)

def load_portoalegre_bairros(verbose=True):
    lm = LayerMapping(PortoAlegreBairro, portoalegrebairro_shp, portoalegrebairro_mapping,
                    transform=True, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)
