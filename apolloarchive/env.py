# -*- coding: utf-8 -*-
import os

ENV = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))
EXAMPLE = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env.example'))

KEYS = {}

def input_key(key):
    return input(key + ': ')

def setup():
    '''Configure ENV file if needed'''
    global KEYS

    if os.path.exists(ENV):
        KEYS = read(ENV)
    else:
        if not os.path.exists(EXAMPLE):
            raise FileExistsError('`.env.example` not found')

        for key in read(EXAMPLE).keys():
            if not key in os.environ:
                KEYS[key] = None

        if len(KEYS) > 0:
            print('Warning: Some environnement variables are missing.')
            print('>> Go to https://www.flickr.com/services/api/keys/ to setup your keys.')
            for key in KEYS.keys():
                KEYS[key] = input_key(key)
            with open(ENV, 'w') as f:
                f.write('\n'.join(f'{key}={val}' for key, val in KEYS.items()))

def read(fname):
    '''Read dot env file: KEY=VALUE)'''
    keys = {}
    with open(fname, 'r') as f:
        for line in f.readlines():
            if line[0] == '#':
                continue

            key = line.split('=')[0]
            val = line.split('=')[-1].replace('\n','')
            keys[key] = val
    return keys


def getEnv(key):
    '''Get env value from global env or `.env` file'''
    if key in os.environ:
        return os.environ[key]
    else:
        if len(KEYS) == 0:
            setup()
        if key in KEYS:
            return KEYS[key]
        else:
            raise IOError(f'Key: {key} not found in global variable or in `.env` file')

def clean_KEYS():
    global KEYS
    KEYS = {}
