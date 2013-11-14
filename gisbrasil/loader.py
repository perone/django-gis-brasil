# happy fish-coding: utf-8

import os
import csv
import urllib2
import json
from datetime import datetime

import ckanclient as ck
import dateutil.parser

import progressbar as pbar
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from django.db import transaction

from pytz import timezone
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

class RequestProxy(object):
    def __init__(self, request):
        self.request = request
        self.it = iter(self.request)
        self.pos = 0
        content_length = request.info().getheader('Content-Length')
        self.total_size = int(content_length.strip())

    def __len__(self):
        return self.total_size

    def progress(self):
        return self.pos

    def next(self):
        next_data = self.it.next()
        self.pos += len(next_data)
        return next_data

    def __iter__(self):
       return self

class Parser(object):
    def latlng_to_wkt(self, lat, lng):
        lat_s = lat.replace(",", ".")
        lng_s = lng.replace(",", ".")
        coord = GEOSGeometry('POINT (%s %s)' % (lng_s, lat_s))
        return coord

    def parse_datetime(self, dttime):
        brasil_tzone = timezone("America/Sao_Paulo")
        parsed_dt = dateutil.parser.parse(dttime)
        parsed_dt = parsed_dt.replace(tzinfo=brasil_tzone)
        return parsed_dt

class ParserPontoTaxi(Parser):
    def parse(self, row):
        item = PortoAlegreTaxi()
        item.idtaxi = row['idtaxi']
        item.endereco = row['endereco']
        item.telefone = row['telefone']
        item.coordenada = self.latlng_to_wkt(row['latitude'],
            row['longitude'])
        return item

class ParserAcidenteTransito(Parser):
    def parse(self, row):
        item = PortoAlegreAcidenteTransito()
        item.dataset_id = row['ID']
        item.logradouro1 = row['LOG1']
        item.logradouro2 = row['LOG2']
        item.predial = row['PREDIAL1']
        item.local = row['LOCAL']
        item.tipo_acidente = row['TIPO_ACID']
        item.local_via = row['LOCAL_VIA']
        item.data_hora = self.parse_datetime(row['DATA_HORA'])
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
        item.coordenada = \
            self.latlng_to_wkt(row["LATITUDE"], row["LONGITUDE"])
        return item

class CkanDatasetImporter(object):
    datastore_dump = "/datastore/dump/"

    def __init__(self, base_url, parser, resource_list=None):
        self.base_url = base_url
        if resource_list is None:
            self.resource_list = []
        else:
            self.resource_list = resource_list
        self.parser = parser

    def import_dataset(self):
        for index, resource_id in enumerate(self.resource_list):
            print '>>> Importando dataset %d de %d...' % \
                (index+1, len(self.resource_list))

            url = self.base_url + CkanDatasetImporter.datastore_dump
            request = urllib2.urlopen(url + resource_id)
            request_proxy = RequestProxy(request)

            widgets = ['>>>> Progresso: ', pbar.Percentage(), ' ', pbar.Bar(marker="#"),
                ' ', pbar.ETA(), ' Velocidade: ', pbar.FileTransferSpeed()]
            progress = pbar.ProgressBar(widgets=widgets, maxval=len(request_proxy))
            progress.start()
            
            input_csv = csv.DictReader(request_proxy, delimiter=",")
    
            with transaction.commit_on_success():
                for row in input_csv:
                    item = self.parser.parse(row)
                    val = request_proxy.progress()
                    progress.update(val)
                    if item:
                        item.save()
                    else:
                        continue

            progress.finish()
            request.close()


OPENDATAPOA_REST_SEARCH_BASE_URL = "http://datapoa.com.br/api/action/datastore_search"
OPENDATAPOA_BIKEPOA_FILTER = "?resource_id=b64586af-cd7c-47c3-9b92-7b99875e1c08"
OPENDATAPOA_BIKEPOA_QUERY = OPENDATAPOA_REST_SEARCH_BASE_URL + OPENDATAPOA_BIKEPOA_FILTER

municipios_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'data/brasil/55mu2500gsd.shp'))

portoalegrebairro_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'data/rs/portoalegre/bairros_utm22_sad69.shp'))

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
    
    for row in json_data['result']['records']:
        estacao = PortoAlegreEstacaoBikePoa()
        estacao.dataset_id = row["_id"]
        estacao.numero = row["numero"]
        estacao.nome = row["nome"]
        estacao.coordenada = GEOSGeometry('POINT (%s %s)' % (row["LATITUDE"], row["LONGITUDE"]))
        estacao.save()
    print
    print ">> Dados do BikePoa de Porto Alegre / RS importados!"
        
def load_opendatapoa_acid_transito():
    ckan = ck.CkanClient(base_location="http://datapoa.com.br/api")
    entity = ckan.package_entity_get("acidentes-de-transito")
    resource_list = []
    for resource in entity['resources']:
        resource_list.append(resource['id'])

    print
    print ">> Importando dados de Acidentes de Transito de Porto Alegre / RS..."

    importer = CkanDatasetImporter("http://datapoa.com.br",
        ParserAcidenteTransito(), resource_list)
    importer.import_dataset()

def load_opendatapoa_ponto_taxi():
    resource_list = ['a6bd54de-cff0-4c08-8569-0a54a3f5b1da']
    print
    print ">> Importando dados de Pontos de Táxi de Porto Alegre / RS..."

    importer = CkanDatasetImporter("http://datapoa.com.br",
        ParserPontoTaxi(), resource_list)
    importer.import_dataset()
