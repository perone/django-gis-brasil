# happy fish coding: utf-8

# happy fish-coding: utf-8

import os
import csv
import urllib2
from datetime import datetime

import ckanclient as ck
import dateutil.parser
from pytz import timezone
import progressbar as pbar
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction

from gisbrasil.dataimport import base
from gisbrasil.models import *

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
        coord = GEOSGeometry('POINT (%s %s)' % (lng, lat))
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

class ParserParadas(Parser):
    def parse(self, row):
        item = PortoAlegreParada()
        item.idparada = row['idparada']
        item.codigo = row['codigo']
        item.coordenada = self.latlng_to_wkt(row['latitude'],
            row['longitude'])
        item.terminal = row['terminal']
        return item

class ParserErb(Parser):
    def parse(self, row):
        item = PortoAlegreErb()
        item.dataset_id = row['_id']
        item.empresa_01 = row['EMPRESA_01']
        item.empresa_02 = row['EMPRESA_02']
        item.empresa_03 = row['EMPRESA_03']
        item.empresa_04 = row['EMPRESA_04']
        item.site_01 = row['SITE_01']
        item.site_02 = row['SITE_02']
        item.site_03 = row['SITE_03']
        item.site_04 = row['SITE_04']
        item.nome_da_er = row['NOME_DA_ER']
        item.n13 = row['N13']
        item.bairro = row['BAIRRO']
        item.tipo = row['TIPO']
        item.coordenada = self.latlng_to_wkt(row['LATITUDE'],
            row['LONGITUDE'])
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
        try:
            item.data_hora = self.parse_datetime(row['DATA_HORA'])
        except:
            print 'Registro ignorado, formato de data inválido [%s]' % \
                row['DATA_HORA']
            return None
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

class ParserBikePoa(Parser):
    def parse(self,row):
        item = PortoAlegreEstacaoBikePoa()
        item.dataset_id = row["_id"]
        item.numero = row["numero"]
        item.nome = row["nome"]
        item.coordenada = self.latlng_to_wkt(row["LATITUDE"],
            row["LONGITUDE"])
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
            print '>> Importando dataset %d de %d...' % \
                (index+1, len(self.resource_list))

            url = self.base_url + CkanDatasetImporter.datastore_dump
            request = urllib2.urlopen(url + resource_id)
            request_proxy = RequestProxy(request)

            widgets = ['>>> Progresso: ', pbar.Percentage(), ' ', pbar.Bar(marker="#"),
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

class Bairros(base.Dataset):
    def __init__(self):
        self.shp_filename = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '../../data/rs/portoalegre/bairros_utm22_sad69.shp'))

        self.mapping = {
            'codigo_bairro': 'COD_BAIRRO',
            'oficial': 'OFICIAL',
            'nome_bairro': 'NOM_BAIRRO',
            'poly': 'POLYGON',
        }

    def import_dataset(self):
        lm = LayerMapping(PortoAlegreBairro, self.shp_filename,
            self.mapping, transform=True, encoding='utf-8')
        lm.save(strict=True, verbose=False)

    class Meta:
        title = u'Dados de Bairros de Porto Alegre / RS'
        source = u'UFRGS'
        command = u'--bairros-portoalegre'

class Eixos(base.Dataset):
    def __init__(self):
        self.shp_filename = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '../../data/rs/portoalegre/eixos_ruas_utm22_sad69.shp'))

        self.mapping = {
            'smf_i_i' : 'SMF_I_I',
            'smf_i_f' : 'SMF_I_F',
            'smf_p_i' : 'SMF_P_I',
            'smf_p_f' : 'SMF_P_F',
            'categoria' : 'CATEGORIA',
            'preposicao' : 'PREPOSICAO',
            'nome' : 'NOME',
            'abreviatura' : 'ABREVIAT',
            'cep' : 'CEP',
            'grupo_cep' : 'GRUPO_CEP',
            'geom' : 'MULTILINESTRING',
        }

    def import_dataset(self):
        lm = LayerMapping(PortoAlegreEixo, self.shp_filename,
            self.mapping, transform=True, encoding='utf-8')
        lm.save(strict=True, verbose=False)

    class Meta:
        title = u'Dados de Eixos (ruas, avenidas, etc) de Porto Alegre / RS'
        source = u'UFRGS'
        command = u'--eixos-portoalegre'

class DataPoaDataset(base.Dataset):
    def __init__(self):
        self.base_url = "http://datapoa.com.br"
        self.ckan = ck.CkanClient(base_location=self.base_url + "/api")

    def import_dataset(self):
        importer = CkanDatasetImporter(self.base_url,
            self.parser, self.resource_list)
        importer.import_dataset()

class AcidentesTransito(DataPoaDataset):
    def __init__(self):
        super(AcidentesTransito, self).__init__()
        self.parser = ParserAcidenteTransito()
        self.resource_list = []

    def import_dataset(self):
        entity = self.ckan.package_entity_get("acidentes-de-transito")
        for resource in entity['resources']:
            self.resource_list.append(resource['id'])
        super(AcidentesTransito, self).import_dataset()

    class Meta:
        title = u'Dados de Acidentes de Trânsito de Porto Alegre / RS'
        source = u'DataPoa'
        command = u'--acid-transito-portoalegre'

class EstacoesBikePoa(DataPoaDataset):
    def __init__(self):
        super(EstacoesBikePoa, self).__init__()
        self.resource_list = ['b64586af-cd7c-47c3-9b92-7b99875e1c08']
        self.parser = ParserBikePoa()

    class Meta:
        title = u'Dados de Estações BikePoa de Porto Alegre / RS'
        source = u'DataPoa'
        command = u'--bikepoa-portoalegre'

class PontosTaxi(DataPoaDataset):
    def __init__(self):
        super(PontosTaxi, self).__init__()
        self.resource_list = ['a6bd54de-cff0-4c08-8569-0a54a3f5b1da']
        self.parser = ParserPontoTaxi()

    class Meta:
        title = u'Dados de Pontos de Táxi de Porto Alegre / RS'
        source = u'DataPoa'
        command = u'--taxi-portoalegre'

class ParadasOnibus(DataPoaDataset):
    def __init__(self):
        super(ParadasOnibus, self).__init__()
        self.resource_list = ['8f955225-039e-4dd7-8139-07b635b89e4a']
        self.parser = ParserParadas()

    class Meta:
        title = u'Dados de Paradas de Ônibus de Porto Alegre / RS'
        source = u'DataPoa'
        command = u'--onibus-portoalegre'

class EstacoesRadioBase(DataPoaDataset):
    def __init__(self):
        super(EstacoesRadioBase, self).__init__()
        self.resource_list = ['f1e9a6cb-6ff3-4a51-bece-a42190bef350']
        self.parser = ParserErb()

    class Meta:
        title = u'Dados de Estações Rádio Base de Porto Alegre / RS'
        source = u'DataPoa'
        command = u'--erb-portoalegre'


