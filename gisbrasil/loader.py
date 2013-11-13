# happy fish-coding: utf-8

import os
import csv
import urllib2
from django.contrib.gis.utils import LayerMapping
from models import *

municipios_mapping = {
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

portoalegrebairro_mapping = {
    'codigo_bairro': 'COD_BAIRRO',
    'oficial': 'OFICIAL',
    'nome_bairro': 'NOM_BAIRRO',
    'poly': 'POLYGON',
}

OPENDATAPOA_BASE_URL = "http://www.opendatapoa.com.br"
OPENDATAPOA_TRANSITO_ACIDENTE = "/storage/f/2013-11-08T12%3A32%3A00.175Z/acidentes-2012.csv"

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

class RequestProxy(object):
    def __init__(self, request):
        self.request = request
        self.it = iter(self.request)
        self.pos = 0
        content_length = request.info().getheader('Content-Length')
        self.total_size = int(content_length.strip())

    def progress(self):
        return self.pos*100/self.total_size

    def next(self):
        next_data = self.it.next()
        self.pos += len(next_data)
        return next_data

    def __iter__(self):
       return self

def load_portoalegre_acidente_transito(verbose=True):
    request = urllib2.urlopen(OPENDATAPOA_BASE_URL + OPENDATAPOA_TRANSITO_ACIDENTE)
    request_proxy = RequestProxy(request)

    input_csv = csv.DictReader(request_proxy, delimiter=";")
    for row in input_csv:
        if int(request_proxy.progress())%10==0:
            print "Perc: %0.2f" % request_proxy.progress()

    request.close()

