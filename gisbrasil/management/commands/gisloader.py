# happy fish-coding: utf-8

from django.core.management.base import BaseCommand, CommandError
import gisbrasil

class Command(BaseCommand):
    help = 'Load the GIS data from shapefiles to the database.'

    def handle(self, *args, **options):
        verbosity = int(options['verbosity']) > 1 
                
        print 'django-gisbrasil v.%s' % gisbrasil.__version__
        print 'Authors: %s' % gisbrasil.__author__
        print

        #gisbrasil.loader.load_municipios_brasil(verbosity)
        #gisbrasil.loader.load_portoalegre_bairros(verbosity)
        #gisbrasil.loader.load_opendatapoa_acid_transito()
        #gisbrasil.loader.load_opendatapoa_estacoes_bikepoa()
        gisbrasil.loader.load_opendatapoa_ponto_taxi()
        

