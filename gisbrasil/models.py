# happy fish-coding: utf-8

from django.contrib.gis.db import models

class Municipio(models.Model):
    geocode = models.IntegerField()
    uf = models.CharField(max_length=254)
    sigla = models.CharField(max_length=254)
    nome_municipio = models.CharField('Nome do Município', max_length=254)
    regiao = models.CharField('Região', max_length=254)
    mesorregiao = models.CharField('Mesorregião', max_length=254)
    nome_mesorregiao = models.CharField('Nome da Mesorregião', max_length=254)
    microregiao = models.CharField('Microrregião', max_length=254)
    nome_microrregiao = models.CharField('Nome da Microrregião', max_length=254)

    multipoly = models.MultiPolygonField()
    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Municipio'
        verbose_name_plural = u'Municipios'

    def __unicode__(self):
        return self.nome_municipio

class PortoAlegreBairro(models.Model):
    codigo_bairro = models.IntegerField('Código do Bairro')
    oficial = models.CharField(max_length=1)
    nome_bairro = models.CharField('Nome do Bairro', max_length=50)

    poly = models.PolygonField()
    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Bairro'
        verbose_name_plural = u'Porto Alegre - Bairro'

    def __unicode__(self):
        return self.nome_bairro

class PortoAlegreAcidenteTransito(models.Model):
    dataset_id = models.IntegerField()
    logradouro1 = models.CharField(max_length=300)
    logradouro2 = models.CharField(max_length=300)
    predial = models.CharField(max_length=20)
    local = models.CharField(max_length=100)
    tipo_acidente = models.CharField(max_length=100)
    local_via = models.CharField(max_length=300)
    data_hora = models.DateTimeField()
    dia_semana = models.CharField(max_length=50)
    feridos = models.IntegerField()
    mortes = models.IntegerField()
    mortes_post = models.IntegerField()
    fatais = models.IntegerField()
    auto = models.IntegerField()
    taxi = models.IntegerField()
    lotacao = models.IntegerField()
    onibus_urb = models.IntegerField()
    onibus_int = models.IntegerField()
    caminhao = models.IntegerField()
    moto = models.IntegerField()
    carroca = models.IntegerField()
    bicicleta = models.IntegerField()
    outro = models.IntegerField()
    tempo = models.CharField(max_length=300)
    noite_dia = models.CharField(max_length=50)
    fonte = models.CharField(max_length=100)
    boletim = models.CharField(max_length=30)
    regiao = models.CharField(max_length=100)
    dia = models.IntegerField()
    mes = models.IntegerField()
    ano = models.IntegerField()
    fx_hora = models.IntegerField()
    cont_acid = models.IntegerField()
    cont_vit = models.IntegerField()
    ups = models.IntegerField()
    coordenada = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Acidente de Trânsito'
        verbose_name_plural = u'Porto Alegre - Acidentes de Trânsito'

    def __unicode__(self):
        return self.logradouro1

class PortoAlegreEstacaoBikePoa(models.Model):
    dataset_id = models.IntegerField()
    numero = models.IntegerField()
    nome = models.CharField(max_length=100)
    coordenada = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Estação BikePoa'
        verbose_name_plural = u'Porto Alegre - Estações BikePoa'

    def __unicode__(self):
        return u'ID: %s, Nome da estação: %s' % (self.dataset_id, self.nome)

class PortoAlegreTaxi(models.Model):
    idtaxi = models.IntegerField()
    endereco = models.CharField(max_length=300)
    telefone = models.CharField(max_length=20)
    coordenada = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Ponto de Táxi'
        verbose_name_plural = u'Porto Alegre - Pontos de Táxi'

    def __unicode__(self):
        return self.endereco

class PortoAlegreParada(models.Model):
    TERMINAL_CHOICES = (
        ('S', 'Sim'),
        ('N', 'Não'),
    )

    idparada = models.IntegerField()
    codigo = models.IntegerField()
    coordenada = models.PointField()
    terminal = models.CharField(max_length=2, choices=TERMINAL_CHOICES)

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Parada de Ônibus'
        verbose_name_plural = u'Porto Alegre - Paradas de Ônibus'

    def __unicode__(self):
        return self.codigo


