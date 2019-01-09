# -*- coding: utf-8 -*-
import flickrapi

from .env import getEnv

API_KEY    = getEnv('FLICKR_API_KEY')
API_SECRET = getEnv('FLICKR_API_SECRET')

FLICKR = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

USERNAME = 'Apollo Image Gallery'
REALNAME = 'Project Apollo Archive'
USER_ID = '136485307@N06'
