# -*- coding: utf-8 -*-
import pytest
import os

from apolloarchive.cli import cli_sync


@pytest.fixture
def folder():
    return 'Announcements'

@pytest.fixture
def files(folder):
    return [
        os.path.join(folder, '1-Also-follow-project-apollo-archive-on-facebook.jpg'),
        os.path.join(folder, '2-About-the-project-apollo-archive-flickr-gallery.jpg'),
        os.path.join(folder, '3-The-project-apollo-archive-is-best-experienced-in-the-albums-view.jpg'),
    ]

def test_cli_sync(capsys):
    argv = '--album 0'.split()
    cli_sync(argv)
    out, err = capsys.readouterr()

    assert out == '\n'
    assert 'Sync Announcements' in err
    assert '3/3' in err

def test_cli_sync_exists(capsys):
    argv = ['--username', 'Apollo Image Gallery', '--album', '0', '--overwrite']
    cli_sync(argv)
    out, err = capsys.readouterr()

    assert out == '\n'
    assert 'Sync Announcements' in err
    assert '3/3' in err

def test_cli_downloaded_files(folder, files):
    assert os.path.exists(folder)
    
    for f in files:
        assert os.path.exists(f)
        os.remove(f)
        assert not os.path.exists(f)

    os.removedirs(folder)
    assert not os.path.exists(folder)
