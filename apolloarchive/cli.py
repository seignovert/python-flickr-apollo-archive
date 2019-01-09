# -*- coding: utf-8 -*-
import argparse

from .download import sync

def cli_sync(argv=None):
    '''CLI sync flickr folders'''
    parser = argparse.ArgumentParser(description='Sync Flickr folder(s)')
    parser.add_argument('--user-id', '-i', help='User ID', type=str)
    parser.add_argument('--username', '-u', help='Username', type=str)
    parser.add_argument('--album', '-a', help='Album number to sync', type=int)
    parser.add_argument('--ncpu', '-n', help='Number of thread during for download', type=int, default=1)
    parser.add_argument('--overwrite', '-o', action='store_true', help='Re-download all')

    args, others = parser.parse_known_args(argv)
    if args.user_id is None:
        delattr(args, 'user_id')

    sync(**vars(args))
