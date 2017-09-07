import os
from optparse import OptionParser

def get_env(var, default):
    if var in os.environ:
        return os.environ[var]
    else:
        return default

default_options = {
    'miner_host': get_env('MINERHOST', '0.0.0.0'),
    'miner_port': get_env('MINERPORT', 5000),
    'seed_host': get_env('SEEDHOST', '0.0.0.0'),
    'seed_port': get_env('SEEDPORT', 5000),
    'debug_path': 'var/debug.log',
    'blockchain_path': 'var/blockchain',
}

class Config:
    def __init__(self):
        parser = OptionParser()

        parser.add_option("--miner_host", dest="miner_host",
                          help="miner_host", default=default_options.get('miner_host'))

        parser.add_option("--miner_post", dest="miner_post",
                          help="port the server will listen on", default=default_options.get('miner_post'))

        parser.add_option("--seed_host", dest="seed_host",
                          help="seed_host", default=default_options.get('seed_host'))

        parser.add_option("--seed_port", dest="seed_port",
                          help="port the seeder will listen on", default=default_options.get('seed_port'))

        parser.add_option("--debug_path", dest="debug_path",
                          help="path to debug log", default=default_options.get('debug_path'))

        options, args = parser.parse_args()

        # Override default options with options passed in from command line
        self.options = default_options.copy()
        self.options.update(vars(options))

    def get(self, key):
        return self.options[key]

    def get_host_url(self):
        return 'http://{}:{}'.format(self.get('miner_host'), self.get('miner_port'))

    def get_dnsseeder_url(self):
        return 'http://{}:{}'.format(self.get('seed_host'), self.get('seed_port'))

config = Config()