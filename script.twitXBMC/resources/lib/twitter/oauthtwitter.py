#!/usr/bin/env python
# 
'''
Requires:
  simplejson
  oauth
'''

__author__ = "Eraser"
__version__ = "0.1"

import urllib
import urllib2
import simplejson
import oauth2 as oauth

class OAuthApi(object):
    
    def __init__(self, consumer_key, consumer_secret, access_token=None, base_url=None):
        self._urllib         = urllib2
        if base_url is None:
            self.REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
            self.ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
            self.AUTHORIZATION_URL = 'https://twitter.com/oauth/authorize'
            self.SIGNIN_URL = 'https://twitter.com/oauth/authenticate'
        else:
            self.REQUEST_TOKEN_URL = '%s/oauth/request_token'%(base_url)
            self.ACCESS_TOKEN_URL = '%s/oauth/access_token'%(base_url)
            self.AUTHORIZATION_URL = '%s/oauth/authorize'%(base_url)
            self.SIGNIN_URL = '%s/oauth/authenticate'%(base_url)
        self._Consumer = oauth.Consumer(consumer_key, consumer_secret)
        self._signature_method = oauth.SignatureMethod_HMAC_SHA1()
        self._access_token = access_token

    def _GetOpener(self):
        opener = self._urllib.build_opener()
        return opener

    def _FetchUrl(self,
                    url,
                    post_data=None,
                    parameters=None,
                    no_cache=None):
        '''Fetch a URL, optionally caching for a specified time.
    
        Args:
          url: The URL to retrieve
          post_data: 
            A dict of (str, unicode) key/value pairs.  If set, POST will be used.
          parameters:
            A dict whose key/value pairs should encoded and added 
            to the query string. [OPTIONAL]
          no_cache: If true, overrides the cache on the current request
    
        Returns:
          A string containing the body of the response.
        '''
        # Build the extra parameters dict
        extra_params = {}
        if parameters:
          extra_params.update(parameters)
    
        # Add key/value parameters to the query string of the url
        #url = self._BuildUrl(url, extra_params=extra_params)
    
        if post_data:
            http_method = "POST"
            extra_params.update(post_data)
        else:
            http_method = "GET"
        
        req = self._makeOAuthRequest(url, parameters=extra_params, 
                                                    http_method=http_method)
        self._signRequest(req, self._signature_method)

        
        # Get a url opener that can handle Oauth basic auth
        opener = self._GetOpener()
        
        #encoded_post_data = self._EncodePostData(post_data)

        if post_data:
            encoded_post_data = req.to_postdata()
            url = req.get_normalized_http_url()
        else:
            url = req.to_url()
            encoded_post_data = ""
            
        no_cache=True
        # Open and return the URL immediately if we're not going to cache
        # OR we are posting data
        if encoded_post_data or no_cache:
          if encoded_post_data:
              url_data = opener.open(url, encoded_post_data).read()
          else:
              url_data = opener.open(url).read()
          opener.close()
        else:
          # Unique keys are a combination of the url and the username
          if self._username:
            key = self._username + ':' + url
          else:
            key = url
    
          # See if it has been cached before
          last_cached = self._cache.GetCachedTime(key)
    
          # If the cached version is outdated then fetch another and store it
          if not last_cached or time.time() >= last_cached + self._cache_timeout:
            url_data = opener.open(url).read()
            opener.close()
            self._cache.Set(key, url_data)
          else:
            url_data = self._cache.Get(key)
    
        # Always return the latest version
        return url_data
    
    def _makeOAuthRequest(self, url, token=None,
                                        parameters=None, http_method="GET"):
        '''Make a OAuth request from url and parameters
        
        Args:
          url: The Url to use for creating OAuth Request
          parameters:
             The URL parameters
          http_method:
             The HTTP method to use
        Returns:
          A OAauthRequest object
        '''
        if not token:
            token = self._access_token
        request = oauth.Request.from_consumer_and_token(
                            self._Consumer, token=token, 
                            http_url=url, parameters=parameters, 
                            http_method=http_method)
        return request

    def _signRequest(self, req, signature_method=oauth.SignatureMethod_HMAC_SHA1()):
        '''Sign a request
        
        Reminder: Created this function so incase
        if I need to add anything to request before signing
        
        Args:
          req: The OAuth request created via _makeOAuthRequest
          signate_method:
             The oauth signature method to use
        '''
        req.sign_request(signature_method, self._Consumer, self._access_token)
    

    def getAuthorizationURL(self, token, url=None):
        '''Create a signed authorization URL
        
        Returns:
          A signed OAuthRequest authorization URL 
        '''
        if url is None:
            url = self.AUTHORIZATION_URL
        req = self._makeOAuthRequest(url, token=token)
        self._signRequest(req)
        return req.to_url()

    def getSigninURL(self, token, url=None):
        '''Create a signed Sign-in URL
        
        Returns:
          A signed OAuthRequest Sign-in URL 
        '''
        if url is None:
            url = self.SIGNIN_URL
        signin_url = self.getAuthorizationURL(token, url)
        return signin_url
    
    def getAccessToken(self, pin, url=None):
        if url is None:
            url = self.ACCESS_TOKEN_URL
        token = self._FetchUrl(url, parameters={'oauth_verifier': pin},
                               no_cache=True)
        return oauth.Token.from_string(token) 

    def getRequestToken(self, url=None):
        '''Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        '''
        if url is None:
            url = self.REQUEST_TOKEN_URL
        resp = self._FetchUrl(url, no_cache=True)
        token = oauth.Token.from_string(resp)
        return token
    
 