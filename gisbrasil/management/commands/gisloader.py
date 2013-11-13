# happy fish-coding: utf-8

from django.core.management.base import BaseCommand, CommandError
import gisbrasil

class Command(BaseCommand):
    help = 'Load the GIS data from shapefiles to the database.'

    def handle(self, *args, **options):
        verbosity = int(options['verbosity']) > 1 
                
        print 'django-gisbrasil v.%s' % gisbrasil.__version__
        print 'Authors: %s' % gisbrasil.__author__

        self.stdout.write('')

        self.stdout.write('Loading Brazilian cities data into Database (this may take a while)...', ending='')
        self.stdout.flush()
        gisbrasil.loader.load_municipios_brasil(verbosity)
        self.stdout.write(' done !')

        self.stdout.write('Loading Porto Alegre data...', ending='')
        self.stdout.flush()
        gisbrasil.loader.load_portoalegre_bairros(verbosity)
        self.stdout.write(' done !')

        self.stdout.write('Loading Porto Alegre car stats...', ending='')
        self.stdout.flush()
        gisbrasil.loader.load_portoalegre_acidente_transito(verbosity)
        self.stdout.write(' done !')

        self.stdout.write('')

