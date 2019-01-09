# -*- coding: utf-8 -*-
from slugify import slugify

from .vars import FLICKR, USER_ID

class User(object):
    '''Flickr user'''
    def __init__(self, user_id=USER_ID, username=None):
        if username is not None:
            user_id = self.getUserId(username)

        self.user_id = user_id
        self.__username = username
        self.__albums = []

    def __repr__(self):
        return f'Flickr User: {self.username} ({self.user_id}) | {len(self.albums)} albums'

    def getUserId(self, username):
        json = FLICKR.people.findByUsername(username=username)
        return json['user']['nsid']

    @property
    def albums(self):
        if not self.__albums:
            self._albums = FLICKR.photosets.getList(user_id=self.user_id)
            for json in self._albums['photosets']['photoset']:
                self.__albums.append(Album(json, self.user_id))
        return self.__albums

    @property
    def username(self):
        if self.__username is None:
            self._username = FLICKR.people.getInfo(user_id=self.user_id)
            self.__username = self._username['person']['username']['_content']
        return self.__username
        

class Album(object):
    '''Flickr album'''
    def __init__(self, json, user_id):
        self.json = json
        self.user_id = user_id
        self.__photos = []

    def __repr__(self):
        return f'Album: "{self.title}" ({len(self)} photos)'

    def __len__(self):
        return self.json['photos']

    @property
    def id(self):
        return self.json['id']

    @property
    def title(self):
        return self.json['title']['_content']

    @property
    def slug(self):
        return slugify(self.title).title()

    @property
    def photos(self):
        if not self.__photos:
            self._photos = FLICKR.photosets.getPhotos(photoset_id=self.id, user_id=self.user_id)
            for json in self._photos['photoset']['photo']:
                self.__photos.append( Photo(json))
        return self.__photos
    
class Photo(object):
    '''Flickr photo'''
    def __init__(self, json):
        self.json = json
        self.__sizes = []

    def __repr__(self):
        return f'Photo: "{self.title}"'

    @property
    def id(self):
        return self.json['id']

    @property
    def title(self):
        return self.json['title']

    @property
    def slug(self):
        return slugify(self.title).capitalize()

    @property
    def filename(self):
        return self.slug + '.jpg'

    @property
    def sizes(self):
        if not self.__sizes:
            self._sizes = FLICKR.photos.getSizes(photo_id=self.id)
            self.__sizes = self._sizes['sizes']['size']
        return self.__sizes

    @property
    def url(self):
        if self.sizes[-1]['label'] == 'Original':
            return self.sizes[-1]['source']
        else:
            for size in self.sizes:
                if size['label'] == 'Original':
                    return size['source']
            else:
                raise ValueError('Original size not found')
