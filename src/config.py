import os
from optparse import OptionParser

print os.environ['HOME']

default_options = {
    'miner_host': '0.0.0.0',
    'miner_port': 5001,
    'seed_host': os.environ['SEEDHOST'] or '0.0.0.0',
    'seed_port': os.environ['SEEDPORT'] or 5000,
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