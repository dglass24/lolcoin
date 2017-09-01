from optparse import OptionParser

default_options = {
    'dnsseeder_url': 'http://127.0.0.1:3343'
}

class Config:
    def __init__(self):
        parser = OptionParser()
        parser.add_option("--host", dest="host",
                          help="host", default='127.0.0.1')
        parser.add_option("-p", "--port", dest="port",
                          help="port the server will listen on", default=5000)
        options, args = parser.parse_args()

        # Override default options with options passed in from command line
        self.options = default_options.copy()
        self.options.update(vars(options))

    def get(self, key):
        return self.options[key]

    def get_host_url(self):
        return 'http://{}:{}'.format(self.get('host'), self.get('port'))
