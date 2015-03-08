
import requests

class LifesumAPI(object):
    ENDPOINT_URL = 'https://api.lifesum.com/v1/foodipedia/foodstats'
    DEFAULT_HEADERS = {
        'User-Agent': 'LifesumChallenge/1.0',
    }

    def __init__(self, endpoint_url=None):
        self.session = requests.Session()
        self.session.headers.update(LifesumAPI.DEFAULT_HEADERS)
        self.endpoint_url = endpoint_url or LifesumAPI.ENDPOINT_URL

    def foodstats(self, **parameters):
        r = self.session.get(self.endpoint_url, params=parameters)
        if r.status_code != requests.codes.ok:
            raise RuntimeError('Error while fetching API data.')
        return r.json()
