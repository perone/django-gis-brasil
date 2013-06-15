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
