# -*- coding: utf-8 -*-
import pytest

from apolloarchive.vars import USERNAME, USER_ID
from apolloarchive.flickr import User

@pytest.fixture
def photo():
    photo = User().albums[0].photos[0]
    return photo

@pytest.fixture
def url(photo):
    return photo.url

def test_user_id():
    assert User(USER_ID).username == USERNAME

def test_photo_sizes_changed_order(photo, url):
    photo.sizes.append(photo.sizes[0])
    assert photo.url == url

def test_photo_sizes_missing_original(photo, url):
    photo.sizes.pop()
    with pytest.raises(ValueError):
        assert photo.url
    
