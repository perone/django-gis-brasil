# happy fish-coding: utf-8

import os
import csv
import urllib2
import json
from datetime import datetime


import progressbar as pbar
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from django.db import transaction

from pytz import timezone
from django.utils import timezone as django_tz
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
OPENDATAPOA_REST_SEARCH_BASE_URL = "http://datapoa.com.br/api/action/datastore_search"
OPENDATAPOA_BASE_URL = "http://www.opendatapoa.com.br/storage/f/"
OPENDATAPOA_TRANSITO_ACIDENTE = {
    2012: "2013-11-08T12%3A32%3A00.175Z/acidentes-2012.csv",
    2011: "2013-11-08T12%3A31%3A12.053Z/acidentes-2011.csv",
    2010: "2013-11-08T12%3A22%3A45.238Z/acidentes-2010.csv",
    2009: "2013-11-06T16%3A52%3A35.356Z/acidentes-2009.csv",
    2008: "2013-11-06T16%3A47%3A41.635Z/acidentes-2008.csv",
    2007: "2013-11-06T16%3A38%3A56.849Z/acidentes-2007.csv",
    2006: "2013-11-06T16%3A33%3A16.142Z/acidentes-2006.csv",
    2005: "2013-11-06T14%3A25%3A20.052Z/acidentes-2005.csv",
    2004: "2013-11-06T17%3A40%3A46.014Z/acidentes-2004.csv",
    2003: "2013-11-06T17%3A38%3A06.476Z/acidentes-2003.csv",
    2002: "2013-11-06T17%3A34%3A58.965Z/acidentes-2002.csv",
    2001: "2013-11-06T17%3A30%3A42.711Z/acidentes-2001.csv",
    2000: "2013-11-06T17%3A26%3A29.293Z/acidentes-2000.csv",
}

OPENDATAPOA_BIKEPOA_FILTER = "?resource_id=b64586af-cd7c-47c3-9b92-7b99875e1c08"
OPENDATAPOA_BIKEPOA_QUERY = OPENDATAPOA_REST_SEARCH_BASE_URL + OPENDATAPOA_BIKEPOA_FILTER


municipios_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'data/brasil/55mu2500gsd.shp'))

portoalegrebairro_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'data/rs/portoalegre/bairros_utm22_sad69.shp'))

def latlng_to_wkt(lat, lng):
    lat_s = lat.replace(",", ".")
    lng_s = lng.replace(",", ".")
    coord = GEOSGeometry('POINT (%s %s)' % (lng_s, lat_s))
    return coord

def parse_datetime(dttime):
    brasil_tzone = timezone("America/Sao_Paulo")
    if len(dttime)==8:
        parsed_dt = datetime.strptime(dttime, '%Y%m%d')
    else:
        parsed_dt = datetime.strptime(dttime, '%Y%m%d %H:%M')
    parsed_dt = parsed_dt.replace(tzinfo=brasil_tzone)
    return parsed_dt

class RequestProxy(object):
    def __init__(self, request):
        self.request = request
        self.it = iter(self.request)
        self.pos = 0
        content_length = request.info().getheader('Content-Length')
        self.total_size = float(content_length.strip())

    def progress(self):
        return float(self.pos*100.0/self.total_size)

    def next(self):
        next_data = self.it.next()
        self.pos += len(next_data)
        return next_data

    def __iter__(self):
       return self

def load_municipios_brasil(verbose=True):
    print
    print ">> Importando dados de Municipios do Brasil..."
    lm = LayerMapping(Municipio, municipios_shp, municipios_mapping,
                    transform=True, encoding='latin-1')
    lm.save(strict=True, verbose=verbose)

def load_portoalegre_bairros(verbose=True):
    print
    print ">> Importando dados de bairros de Porto Alegre / RS..."
    lm = LayerMapping(PortoAlegreBairro, portoalegrebairro_shp, portoalegrebairro_mapping,
                    transform=True, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)

def load_opendatapoa_estacoes_bikepoa():
    raw_data = urllib2.urlopen(OPENDATAPOA_BIKEPOA_QUERY)
    print
    print ">> Importando dados das Estações do BikePoa de Porto Alegre / RS..."
    json_data = json.load(raw_data)
    
    for row in json_data['result']:
        estacao = PortoAlegreEstacaoBikePoa()
        estacao.dataset_id = row["_id"]
        estacao.numero = row["numero"]
        estacao.nome = row["nome"]
        estacao.coordenada = latlng_to_wkt(row["LATITUDE"], row["LONGITUDE"])
        estacao.save()
    print
    print ">> Dados do BikePoa de Porto Alegre / RS importados!"
        


def load_opendatapoa_acid_transito_year(year):
    url_storage = OPENDATAPOA_TRANSITO_ACIDENTE[year]
    print
    print ">> Importando dados de Acidentes de Transito de %d de Porto Alegre / RS..." % year
    request = urllib2.urlopen(OPENDATAPOA_BASE_URL + url_storage)
    request_proxy = RequestProxy(request)
    widgets = ['Importando: ', pbar.Percentage(), ' ', pbar.Bar(marker="#"),
               ' ', pbar.ETA()]
    progress = pbar.ProgressBar(widgets=widgets, maxval=100).start()
    input_csv = csv.DictReader(request_proxy, delimiter=";")
    
    with transaction.commit_on_success():
        for row in input_csv:
            val =  request_proxy.progress()
            progress.update(val)
           
            item = PortoAlegreAcidenteTransito()
            item.dataset_id = row['ID']
            item.logradouro1 = row['LOG1']
            item.logradouro2 = row['LOG2']
            item.predial = row['PREDIAL1']
            item.local = row['LOCAL']
            item.tipo_acidente = row['TIPO_ACID']
            item.local_via = row['LOCAL_VIA']
            
            try:
                item.data_hora = parse_datetime(row['DATA_HORA'])
            except:
                print "\nWarning: Registro ignorado, formato de data invalido: '%s'\n" % row['DATA_HORA']
                continue

            item.dia_semana = row['DIA_SEM']
            item.feridos = row['FERIDOS']
            item.mortes = row['MORTES']
            item.mortes_post = row['MORTE_POST']
            item.fatais = row['FATAIS']
            item.auto = row['AUTO']
            item.taxi = row['TAXI']
            item.lotacao = row['LOTACAO']
            item.onibus_urb = row['ONIBUS_URB']
            item.onibus_int = row['ONIBUS_INT']
            item.caminhao = row['CAMINHAO']
            item.moto = row['MOTO']
            item.carroca = row['CARROCA']
            item.bicicleta = row['BICICLETA']
            item.outro = row['OUTRO']
            item.tempo = row['TEMPO']
            item.noite_dia = row['NOITE_DIA']
            item.fonte = row['FONTE']
            item.boletim = row['BOLETIM']
            item.regiao = row["REGIAO"]
            item.dia = row["DIA"]
            item.mes = row["MES"]
            item.ano = row["ANO"]
            item.fx_hora = row["FX_HORA"]
            item.cont_acid = row["CONT_ACID"]
            item.cont_vit = row["CONT_VIT"]
            item.ups = row["UPS"]
            item.coordenada = latlng_to_wkt(row["LATITUDE"], row["LONGITUDE"])
            item.save()
        
    progress.finish()
    request.close()

def load_opendatapoa_acid_transito():
    for year in OPENDATAPOA_TRANSITO_ACIDENTE.keys():
        load_opendatapoa_acid_transito_year(year)

