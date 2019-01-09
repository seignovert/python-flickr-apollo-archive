# -*- coding: utf-8 -*-
import os
import wget
from multiprocessing import Pool
from tqdm import tqdm

from .vars import USER_ID
from .flickr import User

def sync(user_id=USER_ID, username=None, album=None, overwrite=False, ncpu=1):
    '''Sync user folders'''
    user = User(user_id, username)
    albums = user.albums

    if album is not None:
        albums = [albums[album]]

    for album in albums:
        folder = album.slug
        if not os.path.isdir(folder):
            os.mkdir(folder)
        
        jpgs = 0
        for f in os.listdir(folder):
            if f.endswith('jpg'):
                jpgs += 1
        
        if overwrite or len(album) != jpgs:
            imgs = []
            for photo in tqdm(album.photos, desc=f'Sync {album.slug}', position=0):
                img = Image(folder, photo)
                if overwrite or not img.exists:
                    img.url # dummy (sync load url)
                    imgs.append(img)

            if len(imgs) > 0:
                # Async download
                pool = Pool(ncpu)
                pool.map(download, imgs)
                pool.close()
                pool.join()
                print('') # Slip line

def download(img, verbose=True, bar=None):
    if verbose:
        print(f'> Download: {img.slug}')

    # Overwrite file if exists
    if os.path.exists(img.filename):
        os.remove(img.filename)
    
    wget.download(img.url, out=img.filename, bar=bar)
    return img

class Image(object):
    '''Image file'''
    def __init__(self, folder, photo):
        self.folder = folder
        self.photo = photo

    def __repr__(self):
        return f'Image: {self.slug}'

    @property
    def filename(self):
        return os.path.join(self.folder, self.photo.filename)

    @property
    def exists(self):
        return os.path.exists(self.filename)

    @property
    def url(self):
        return self.photo.url

    @property
    def slug(self):
        return self.photo.slug
