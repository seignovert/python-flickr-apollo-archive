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
            for i in tqdm(range(len(album)), desc=f'Sync {album.slug}', position=0):
                img = Image(folder, album.photos[i], i+1)
                if overwrite or not img.exists:
                    img.url # dummy (sync load url)
                    imgs.append(img)

            if len(imgs) > 0:
                if ncpu > 1:
                    # Async download
                    pool = Pool(ncpu)
                    pool.map(download, imgs)
                    pool.close()
                    pool.join()
                else:
                    for img in imgs:
                        download(img)
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
    def __init__(self, folder, photo, n=None):
        self.folder = folder
        self.photo = photo
        self.n = n

    def __repr__(self):
        return f'Image: {self.slug}'

    @property
    def filename(self):
        prefix = '' if self.n is None else str(self.n) + '-'
        return os.path.join(self.folder, prefix + self.photo.filename)

    @property
    def exists(self):
        return os.path.exists(self.filename)

    @property
    def url(self):
        return self.photo.url

    @property
    def slug(self):
        return self.photo.slug
