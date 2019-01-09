# -*- coding: utf-8 -*-
import pytest
import os

from apolloarchive.env import ENV, EXAMPLE, input_key, setup, getEnv, clean_KEYS

BK = ENV + '.bk'
TMP = EXAMPLE.replace('.example', '.tmp')

@pytest.fixture
def value():
    return '1234567890'


def test_input_key(monkeypatch, value):
    monkeypatch.setattr('builtins.input', lambda x: value)
    assert input_key('test') == value

def test_bakup_env():
    if os.path.exists(ENV):
        os.rename(ENV, BK)
    assert not os.path.exists(ENV)

def test_create_fake_env(value):
    with open(ENV, 'w') as f:
        f.write('KEY=' + value)
    assert os.path.exists(ENV)

def test_env(value):
    clean_KEYS()
    assert getEnv('KEY') == value

def test_missing_key():
    with pytest.raises(IOError):
        getEnv('MISSING_KEY')

def test_remove_frake_env():
    os.remove(ENV)
    clean_KEYS()
    assert not os.path.exists(ENV)


def test_backup_env_example(monkeypatch, value):
    os.rename(EXAMPLE, TMP)
    assert not os.path.exists(EXAMPLE)

    with pytest.raises(FileExistsError):
        setup()

    monkeypatch.setattr('apolloarchive.env.input_key', lambda x: value)
    with open(EXAMPLE, 'w') as f:
        f.write('#Fake example\nFOO=foo')
    assert os.path.exists(EXAMPLE)
    
    setup()
    assert getEnv('FOO') == value
    assert os.path.exists(ENV)

def test_restore_env_example():
    os.remove(EXAMPLE)
    assert not os.path.exists(EXAMPLE)
    os.rename(TMP, EXAMPLE)

def test_restore_env():
    os.remove(ENV)
    assert not os.path.exists(ENV)
    if os.path.exists(BK):
        os.rename(BK, ENV)
