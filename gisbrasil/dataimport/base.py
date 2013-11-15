# happy fish-coding: utf-8
from optparse import make_option

class DatasetABC(object):
    def register(self, cmd):
        opt = make_option(self.Meta.command,
            action='store_true',
            dest=self.Meta.command[2:],
            default=False,
            help=self.Meta.title)
        cmd.option_list = cmd.option_list + (opt,)

    def run_import(self):
    	print '> Carregando dataset: %s' % self.Meta.title
    	self.import_dataset()
    	print '> Dataset carregado com sucesso !'

    def check_trigger(self, options):
    	if self.Meta.command[2:] in options:
    		if options[self.Meta.command[2:]]:
    			self.run_import()
    			return True
    	return False