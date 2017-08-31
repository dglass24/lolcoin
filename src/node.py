class Node:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Node url:%s>" % (self.url)