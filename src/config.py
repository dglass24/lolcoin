from optparse import OptionParser

default_options = {
    'host': '0.0.0.0',
    'port': 5000,
    'dnsseeder_host': '0.0.0.0',
    'dnsseeder_port': 5001,
    'debug_path': 'var/debug.log',
    'blockchain_path': 'var/blockchain',
}

class Config:
    def __init__(self):
        parser = OptionParser()

        parser.add_option("--host", dest="host",
                          help="host", default=default_options.get('host'))

        parser.add_option("--port", dest="port",
                          help="port the server will listen on", default=default_options.get('port'))

        parser.add_option("--dnsseeder_host", dest="dnsseeder_host",
                          help="dnsseeder_host", default=default_options.get('dnsseeder_host'))

        parser.add_option("--dnsseeder_port", dest="dnsseeder_port",
                          help="port the dnsseeder will listen on", default=default_options.get('dnsseeder_port'))

        parser.add_option("--debug_path", dest="debug_path",
                          help="path to debug log", default=default_options.get('debug_path'))

        options, args = parser.parse_args()

        # Override default options with options passed in from command line
        self.options = default_options.copy()
        self.options.update(vars(options))

    def get(self, key):
        return self.options[key]

    def get_host_url(self):
        return 'http://{}:{}'.format(self.get('host'), self.get('port'))

    def get_dnsseeder_url(self):
        return 'http://{}:{}'.format(self.get('dnsseeder_host'), self.get('dnsseeder_port'))

config = Config()