# VERSION: 0.1
# AUTHORS: KR@justfoolingaround (https://github.com/justfoolingaround)

import requests

from urllib.parse import quote

ENGINE_NAME = "SolidTorrents API (qBittorrent)"

def sanitize_stdout_data(txt: str, *, sanitation_txts='|'):
    """
    Sanitation of strings like '|' which might cause issues in the stdout stream read.    
    """
    return ''.join(t if t.isascii() and not t in sanitation_txts else quote(t) for t in txt)

def query_string(dict_obj: dict):
    """
    Formatting the query parameters for the final url.
    """
    return '?' + "&".join("%s=%s" % (k, v) for k, v in dict_obj.items())

def to_stdout(content: dict, *, ignore_error=True):
    """
    Formatting the content and sending that data to the stdout.
    """
    return print('{magnet}|{category} - {name}|{size}|{seeders}|{leechers}|{engine}|{url}'.format(
                    magnet=sanitize_stdout_data(content.get('magnet', '')),
                    category=sanitize_stdout_data(content.get('category', '')),
                    name=sanitize_stdout_data(content.get('title', '')),
                    size=content.get('size', 0),
                    seeders=content.get('swarm', {}).get('seeders', 0),
                    leechers=content.get('swarm', {}).get('leechers', 0),
                    engine=ENGINE_NAME,
                    url="https://www.solidtorrents.net/view/%s" % content.get('_id', '')
        ))
        
class qBittorrentExtension:
    """
    A base class for qBittorrent extensions.
    """
    url = None
    name = None
    supported_categories = {}
    
    def search(self, what, cat):
        raise NotImplementedError()

class solidtorrents(qBittorrentExtension):
    """
    A SolidTorrentsAPI Extension for qBittorrent.
    
    SolidTorrents is a DHT crawler with a very promising API.
    """
    
    url = "https://www.solidtorrents.net"
    name = "SolidTorrents"
    supported_categories = {
            'all': ['all'],
            'movies': ['video'],
            'tv': ['video'],
            'music': ['audio'],
            'games': ['program', 'android'],
            'anime': ['video'],
            'software': ['program', 'android', 'archive', 'discimage', 'sourcecode', 'database'],
            'pictures': ['image'],
            'books': ['document', 'ebook', 'database'],
        }
    
    ENDPOINT = "https://www.solidtorrents.net/api/v1/"
    DEFAULT_PARAMS = {'sort': 'seeders', 'fuv': 'yes'} # Default parameters for searching; modify this if required.
    
    def __init__(self):
        """
        Initializing the session that is going to be used in this extension.
        """
        self.session = requests.Session()
    
    def generate_results(self, query, cat):
        """
        A generator that will provide you search results continously until exhaustion so that the search results look juicier.
        """
        current, total = 0, 1
        
        if query == '--no-query':
            query = ''
        
        while current < total:
            data = self.session.get("%s/search%s" % (self.ENDPOINT, query_string(self.DEFAULT_PARAMS | {'category': cat, 'q': query, 'skip': current}))).json()
            total = data.get('hits', {}).get('value', 0)
            current += 20
            yield from data.get('results', [])
        
    def search(self, what, cat='all'):
        """
        The main search function.
        """
        for content in self.generate_results(what, '+'.join(self.supported_categories.get(cat, 'all'))):
            to_stdout(content)
        

if __name__ == '__main__':
    """
    Debug mode; run from cli with a search query for checking/testing/debugging.
    """
    import sys
    solidtorrents().search(' '.join(sys.argv[1:]))