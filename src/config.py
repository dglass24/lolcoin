from optparse import OptionParser

class Config:
    def __init__(self):
        parser = OptionParser()
        parser.add_option("--host", dest="host",
                          help="host", default='127.0.0.1')
        parser.add_option("-p", "--port", dest="port",
                          help="port the server will listen on", default=5000)
        options, args = parser.parse_args()
        self.options = vars(options) # convert to dict

    def get_option(self, key):
        return self.options[key]
