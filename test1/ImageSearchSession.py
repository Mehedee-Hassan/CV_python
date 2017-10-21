from py_ms_cognitive import PyMsCognitiveImageSearch
import numpy # Hint to PyInstaller
from CVForwardCompat import cv2
import pprint
import sys

import RequestsUtils


class ImageSearchSession(object):
    
    def __init__(self):
        self.verbose = False
        
        self._query = ''
        self._results = []
        self._offset = 0
        self._numResultsRequested = 0
        self._numResultsReceived = 0
        self._numResultsAvailable = 0
    
    @property
    def query(self):
        return self._query
    
    @property
    def offset(self):
        return self._offset
    
    @property
    def numResultsRequested(self):
        return self._numResultsRequested
    
    @property
    def numResultsReceived(self):
        return self._numResultsReceived
    
    @property
    def numResultsAvailable(self):
        return self._numResultsAvailable
    
    def searchPrev(self):
        if self._offset == 0:
            return
        offset = max(0, self._offset - self._numResultsRequested)
        self.search(self._query, self._numResultsRequested, offset)
    
    def searchNext(self):
        if self._offset + self._numResultsRequested >= \
                self._numResultsAvailable:
            return
        offset = self._offset + self._numResultsRequested
        self.search(self._query, self._numResultsRequested, offset)
    
    def search(self, query, numResultsRequested=50, offset=0):
        # TODO: Replace the x's with the Primary Account Key of your
        # Microsoft Account.
        bingKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        
        self._query = query
        self._numResultsRequested = numResultsRequested
        self._offset = offset
        
        searchService = PyMsCognitiveImageSearch(
                bingKey, query,
                custom_params='?color=ColorOnly&imageType=Photo')
        searchService.current_offset = offset
        
        try:
            self._results = searchService.search(numResultsRequested, 'json')
        except Exception as e:
            print >> sys.stderr, \
                'Error when requesting Bing image search for "%s":' % query
            print >> sys.stderr, e.message
            self._offset = 0
            self._numResultsReceived = 0
            return
        
        json = searchService.most_recent_json
        self._numResultsReceived = len(self._results)
        if self._numResultsRequested < self._numResultsReceived:
            # py_ms_cognitive modified the request to get more results.
            self._numResultsRequested = self._numResultsReceived
        self._numResultsAvailable = int(json[u'totalEstimatedMatches'])
        
        if self.verbose:
            print 'Received results of Bing image search for "%s":' % query
            pprint.pprint(json)
        
    
    def getCvImageAndUrl(self, index, useThumbnail = False):
        if index >= self._numResultsReceived:
            return None, None
        result = self._results[index]
        if useThumbnail:
            url = result.thumbnail_url
        else:
            url = result.content_url
        return RequestsUtils.cvImageFromUrl(url), url

def main():
    session = ImageSearchSession()
    session.verbose = True
    session.search('luxury condo sales')
    image, url = session.getCvImageAndUrl(0)
    cv2.imwrite('image.png', image)

if __name__ == '__main__':
    main()
