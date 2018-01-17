#!/usr/bin/env python3
# encoding: utf-8

_HELP_TEXT = """
redditimagedownloader.py - Mass download images on reddit. Choose the minimum karma, the subreddits,
and how many to download. Will also download imgur albums.
Apache License 2.0
Copyright Matthew Livernoche <mattalivernoche@gmail.com>
"""

import sys
import argparse
import redditimagedownloader

_PARSER = argparse.ArgumentParser(description=_HELP_TEXT)
_PARSER.add_argument('--subreddits', nargs='*', help='a list of the subreddits to download from.')
_PARSER.add_argument('--ext', nargs='*', default=['.jpg', '.png', '.gif', '.jpeg', '.gifv', '.webm', '.mp4'],
                    help='a file types that can be downloaded. they must begin with a period (".").')
_PARSER.add_argument('--auto', action='store_true', default=False,
                    help='whether or not to download imgur albums automatically.')
_PARSER.add_argument('--minkarma', type=int, default=1, help='the minimum amount of karma a post must have for it to be downloaded.')
_PARSER.add_argument('--loc', type=str, help='the directory where files and folders will be saved and created.')
_PARSER.add_argument('--min', type=int, default=50,
                    help='the minimum target for the amount of images to be downloaded. once this is hit, downloading will stop.')
_PARSER.add_argument('--max', type=int, default=100,
                    help='the maximum amount of images that will be considered for download. once this is hit, downloading will stop.')
_PARSER.add_argument('--skipafter', type=int, default=10,
                    help='stop scanning subreddit after we have skipped over so many images.')

_RESULTS = _PARSER.parse_args()

# image source information
_SKIP = _RESULTS.skipafter
_MIN_IMAGES = _RESULTS.min
_MAX_IMAGES = _RESULTS.max
_AUTO_DOWNLOAD = _RESULTS.auto
_URL_LIST = _RESULTS.subreddits
_MIN_KARMA = _RESULTS.minkarma
_SUPPORTED_FILE_TYPES = _RESULTS.ext

# image saving information
_SAVE_DIR = _RESULTS.loc

if _URL_LIST == None or _SAVE_DIR == None:
    print("No URL or save DIR provided. Exiting.")
    sys.exit()

for url in _URL_LIST:
    redditimagedownloader.downloadimages(url, _SUPPORTED_FILE_TYPES, _SAVE_DIR,
                    minimumkarma=_MIN_KARMA,
                    autodownloadalbums=_AUTO_DOWNLOAD,
                    minimum=_MIN_IMAGES,
                    maximum=_MAX_IMAGES,
                    skipafter=_SKIP)

sys.exit(0)
