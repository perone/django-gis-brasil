# happy fish coding: utf-8

import os

from django.contrib.gis.utils import LayerMapping

from gisbrasil.dataimport import base
from gisbrasil.models import *

class MunicipiosBrasil(base.DatasetABC):
    def __init__(self):
        self.shp_filename = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
            '../data/brasil/55mu2500gsd.shp'))

        self.mapping = {
            'geocode': 'GEOCODIG_M',
            'uf': 'UF',
            'sigla': 'Sigla',
            'nome_municipio': 'Nome_Munic',
            'regiao': 'Regiao',
            'mesorregiao': 'Mesoregia',
            'nome_mesorregiao': 'Nome_Meso',
            'microregiao': 'Microrregi',
            'nome_microrregiao': 'Nome_Micro',
            'multipoly' : 'MULTIPOLYGON',
        }

    def import_dataset(self):
        lm = LayerMapping(Municipio, self.shp_filename, self.mapping,
            transform=True, encoding='latin-1')
        lm.save(strict=True, verbose=False)

    class Meta:
        title = u'Dados de Municípios do Brasil'
        source = u'IBGE'
        command = u'--municipios-brasil'
