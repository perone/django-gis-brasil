# happy fish-coding: utf-8

from django.core.management.base import BaseCommand, CommandError
import gisbrasil

from gisbrasil.dataimport import base
from gisbrasil.dataimport import brasil
from gisbrasil.dataimport import rs

class Command(BaseCommand):
    help = u'Carrega os conjuntos de dados disponíveis para o banco de dados.'

    def __init__(self, *args, **kwargs):
        self.datasets = [
            brasil.MunicipiosBrasil(),
            rs.portoalegre.Bairros(),
            rs.portoalegre.AcidentesTransito(),
            rs.portoalegre.EstacoesBikePoa(),
            rs.portoalegre.PontosTaxi(),
            rs.portoalegre.ParadasOnibus(),
            rs.portoalegre.Eixos(),
            rs.portoalegre.EstacoesRadioBase(),
        ]
        for dataset in self.datasets:
            dataset.register(self)
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        print 'django-gisbrasil v.%s' % gisbrasil.__version__
        print 'Autores: %s' % gisbrasil.__author__
        print
 
        execution_flags = []        
        for dataset in self.datasets:
            execution_flags.append(dataset.check_trigger(options))

        if not any(execution_flags):
            for dataset in self.datasets:
                dataset.run_import()
                print

