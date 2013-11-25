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

class PortoAlegreEixo(models.Model):
    nome = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=30)
    cep = models.IntegerField('CEP')
    grupo_cep = models.IntegerField('Grupo CEP')
    preposicao = models.CharField(max_length=10)
    categoria = models.CharField(max_length=20)
    smf_i_i = models.IntegerField('Nro Impar Inicial')
    smf_i_f = models.IntegerField('Nro Impar Final')
    smf_p_i = models.IntegerField('Nro Par Inicial')
    smf_p_f = models.IntegerField('Nro Par Final')

    geom = models.MultiLineStringField()
    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Eixo'
        verbose_name_plural = u'Porto Alegre - Eixos'

    def __unicode__(self):
        return self.nome

class PortoAlegreAcidenteTransito(models.Model):
    dataset_id = models.IntegerField()
    logradouro1 = models.CharField('Logradouro 1', max_length=300)
    logradouro2 = models.CharField('Logradouro 2', max_length=300)
    predial = models.CharField(max_length=20)
    local = models.CharField(max_length=100)
    tipo_acidente = models.CharField('Tipo de Acidente', max_length=100)
    local_via = models.CharField(max_length=300)
    data_hora = models.DateTimeField()
    dia_semana = models.CharField('Dia da Semana', max_length=50)
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
    noite_dia = models.CharField('Noite ou Dia', max_length=50)
    fonte = models.CharField(max_length=100)
    boletim = models.CharField(max_length=30)
    regiao = models.CharField(max_length=100)
    dia = models.IntegerField()
    mes = models.IntegerField()
    ano = models.IntegerField()
    fx_hora = models.IntegerField('Faixa de Horário')
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
    dataset_id = models.IntegerField('Dataset ID')
    numero = models.IntegerField()
    nome = models.CharField(max_length=100)
    coordenada = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Estação BikePoa'
        verbose_name_plural = u'Porto Alegre - Estações BikePoa'

    def __unicode__(self):
        return u'ID: %s, Nome da estação: %s' % (self.dataset_id, self.nome)

class PortoAlegreEspacoCultural(models.Model):
    _id = models.IntegerField('Dataset ID')
    endereco = models.CharField(max_length=200)
    complemento = models.CharField(max_length=100, null=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=200)
    telefone = models.CharField(max_length=100, null=True)
    bairro = models.CharField(max_length=100, null=True)
    regiao_op = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=200, null=True)
    tipo = models.CharField(max_length=100, null=True)
    categoria = models.CharField(max_length=100, null=True)
    coordenada = models.PointField()
    endereco_formatado = models.CharField(max_length=400)

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Espaço Cultural'
        verbose_name_plural = u'Porto Alegre - Espaços Culturais'

    def __unicode__(self):
        return '%s - %s' % (self.name, self.endereco_formatado)

class PortoAlegreTaxi(models.Model):
    idtaxi = models.IntegerField(u'ID do Táxi')
    endereco = models.CharField(max_length=300)
    telefone = models.CharField(max_length=20)
    coordenada = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Ponto de Táxi'
        verbose_name_plural = u'Porto Alegre - Pontos de Táxi'

    def __unicode__(self):
        return self.endereco

class PortoAlegreErb(models.Model):
    TIPO_CHOICES = (
        ('T', 'T'),
        ('P', 'P'),
    )
    dataset_id = models.IntegerField(u'ID da ERB')
    empresa_01 = models.CharField(max_length=50)
    empresa_02 = models.CharField(max_length=50)
    empresa_03 = models.CharField(max_length=50)
    empresa_04 = models.CharField(max_length=50)
    site_01 = models.CharField(max_length=50)
    site_02 = models.CharField(max_length=50)
    site_03 = models.CharField(max_length=50)
    site_04 = models.CharField(max_length=50)
    nome_da_er = models.CharField(max_length=50)
    n13 = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    coordenada = models.PointField()

    class Meta:
        verbose_name = u'Porto Alegre - Estação Rádio Base'
        verbose_name_plural = u'Porto Alegre - Estações Rádio Base'

    def __unicode__(self):
        return self.nome_da_er

class PortoAlegreLixeiras(models.Model):
    CATEGORIA_CHOICES = (
        ('AV', 'Avenida'),
        ('LG', 'Largo'),
        ('PCA', 'Praça'),
        ('R', 'Rua'),
    )
    _id = models.IntegerField('Dataset ID')
    cod_lograd = models.IntegerField(u'Código do Logradouro')
    categoria = models.CharField(max_length=5, choices=CATEGORIA_CHOICES)
    preposicao = models.CharField(max_length=10, null=True)
    nome = models.CharField(max_length=100, null=True)
    lote = models.IntegerField('Lote')
    secao = models.CharField(max_length=50)
    referencia = models.CharField(max_length=100, null=True)
    data_insta = models.CharField(max_length=100)
    observacao = models.CharField(max_length=500, null=True)
    coordenada = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Lixeira'
        verbose_name_plural = u'Porto Alegre - Lixeiras'

    def __unicode__(self):
        return '%s , %s' % (self.nome, self.lote)


class PortoAlegreConteinerLixo(models.Model):
    YN_CHOICES = (
        ('x', 'Sim'),
        ('', 'Não'),
    )

    AV_STATUS_CHOICES = (
        ('M', 'M'),
        ('U', 'U'),
    )

    AV_SIDE_CHOICES = (
        ('L', 'L'),
        ('R', 'R'),
    )

    _id = models.IntegerField('Dataset ID')
    nro = models.IntegerField(u'Número', null=True)
    cap = models.IntegerField('Cap', null=True)
    cdl = models.IntegerField('CDL', null=True)
    cat = models.CharField(max_length=10, null=True)
    prep = models.CharField(max_length=50, null=True)
    logradouro = models.CharField(max_length=100)
    lote = models.IntegerField('Lote', null=True)
    referencia = models.CharField(max_length=200)
    passeio = models.CharField(max_length=2, choices=YN_CHOICES)
    area_azul = models.CharField(max_length=2, choices=YN_CHOICES)
    observacao = models.CharField(max_length=200)
    av_status = models.CharField(max_length=2, choices=AV_STATUS_CHOICES)
    av_score = models.IntegerField('Av Score', null=True)
    av_side = models.CharField(max_length=2, choices=AV_SIDE_CHOICES)
    coordenada = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Contêiner de Lixo'
        verbose_name_plural = u'Porto Alegre - Contêineres de Lixo'

    def __unicode__(self):
        return '%s' % self.nro


class PortoAlegreParada(models.Model):
    TERMINAL_CHOICES = (
        ('S', 'Sim'),
        ('N', 'Não'),
    )

    idparada = models.IntegerField('ID da Parada')
    codigo = models.IntegerField(u'Código')
    coordenada = models.PointField()
    terminal = models.CharField(max_length=2, choices=TERMINAL_CHOICES)

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'Porto Alegre - Parada de Ônibus'
        verbose_name_plural = u'Porto Alegre - Paradas de Ônibus'

    def __unicode__(self):
        return self.codigo


