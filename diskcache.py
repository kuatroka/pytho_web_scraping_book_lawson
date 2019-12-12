import os
import re
import json
import zlib
from urllib.parse import urlsplit
from datetime import datetime, timedelta

class DiskCache:
    def __init__(self, cache_dir='./data/cache', max_len=255, compress=True,
                 encoding='utf-8', expires=timedelta(days=30)):
        self.cache_dir = cache_dir
        self.max_len = max_len
        self.compress = compress
        self.encoding = encoding
        self.expires = expires

    def url_to_path(self, url):
        """Return file system path string for given URL"""
        components = urlsplit(url)
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # replace invalid characters
        filename = re.sub(r'[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        # restrict maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)


    def __getitem__(self, url):
        """Load data from disk for given url"""
        path = self.url_to_path(url)
        if os.path.exists(path):
            mode = ('rb' if self.compress else 'r')
            with open(path, mode) as fp:
                if self.compress:
                    data = zlib.decompress(fp.read()).decode(self.encoding)
                    
                    data = json.loads(data)

                else:
                    data = json.load(fp)
            exp_date = data.get('expires')
            if exp_date and datetime.strptime(exp_date,
                            '%Y-%m-%dT%H:%M:%S') <= datetime.utcnow():
                print('Cache expired!', exp_date)
                raise KeyError(url + 'has expired.')
            return data
        else:
            # URL has not been cached
            raise KeyError(url + 'does not exist')


    def __setitem__(self, url, result):
        """
        Save data to disk for given url
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        mode = ('wb' if self.compress else 'w')
        # Note: the timespec command requires Py3.6+ (if using 3.X you can
        # export using isoformat() and import with '%Y-%m-%dT%H:%M:%S.%f'
        result['expires'] = (datetime.utcnow() + self.expires).isoformat(timespec='seconds')
        with open(path, mode) as fp:
            if self.compress:
                data = bytes(json.dumps(result), self.encoding)
                fp.write(zlib.compress(data))
            else:
                json.dump(result, fp)
