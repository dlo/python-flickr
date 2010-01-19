#!/usr/bin/env python

from baseconv import BaseConverter
import urllib
import httplib
import json

base58 = BaseConverter('123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMN\
PQRSTUVWXYZ')

FLICKR_KEY = None
FLICKR_SECRET = None
FLICKR_DOMAIN = "api.flickr.com"
FLICKR_REST = "/services/rest/?"
FLICKR_STATIC = "http://farm%(farm)s.static.flickr.com/%(server)s/%(id)s_%(secret)s.jpg"

def urlencode(**params):
    return "&".join("%s=%s" % (k, urllib.quote(v))
            for k, v in params.iteritems())

class FlickrClient():
    def __init__(self):
        self.conn = httplib.HTTPConnection(FLICKR_DOMAIN)

    def get_call(self, method, api_key = FLICKR_KEY, format = 'json', **params):
        params.update({
            'method': method,
            'api_key': api_key,
            'format': format,
            'nojsoncallback': '1',
            })
        return urlencode(**params)

    def call_api(self, method, api_key = FLICKR_KEY, format = 'json', **params):
        call = self.get_call(method, api_key, format, **params)
        self.conn.request("GET", "%s%s" % (FLICKR_REST, call), "", {})
        response = self.conn.getresponse().read()

        #print self.construct_flickr_url(response)
        return json.loads(response)

class FlickrPhoto():
    def __init__(self, farm, id, secret, title, server):
        self.farm = farm
        self.id = id
        self.secret = secret
        self.title = title
        self.server = server

    def __repr__(self):
        return "<FlickrPhoto '%s'>" % self.title

    def get_url(self):
        return FLICKR_STATIC % {'farm': self.farm, 'server': self.server,
                'id': self.id, 'secret': self.secret}

    def get_short_url(self):
        return "flic.kr/%s" % base58.from_decimal(self.id)

    @staticmethod
    def from_flickr_response(photo):
        return FlickrPhoto(photo['farm'], photo['id'], photo['secret'],
                photo['title'], photo['server'])

def main():
    fc = FlickrClient()
    response = fc.call_api('flickr.photos.search', tags = 'cartoons')

    photos = [FlickrPhoto.from_flickr_response(photo)
        for photo in response['photos']['photo']]
    print photos

if __name__ == '__main__':
    main()

