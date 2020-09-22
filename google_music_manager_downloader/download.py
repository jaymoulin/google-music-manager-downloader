#!/usr/bin/env python
# coding: utf-8

import argparse
import concurrent.futures
import logging
import netifaces
import os
import sys
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from gmusicapi import Musicmanager

__DEFAULT_IFACE__ = netifaces.gateways()['default'][netifaces.AF_INET][1]
__DEFAULT_MAC__ = netifaces.ifaddresses(__DEFAULT_IFACE__)[netifaces.AF_LINK][0]['addr'].upper()
__DEFAULT_OAUTH_PATH__ = os.path.join(os.environ['HOME'], 'oauth')

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

Song = namedtuple('Song', ['artist', 'album', 'track_number', 'title', 'id'])


def _download(
        song: Song,
        api: Musicmanager,
        base_dir: str,
        thread_logger: logging.Logger = None
) -> None:
    folder = os.path.join(base_dir, song.artist, song.album)
    file_path = os.path.join(folder, '%s - %s.mp3' % (song.track_number, song.title))

    if not os.path.exists(file_path):
        if thread_logger:
            thread_logger.debug("Downloading song '%s'" % song.title)
        filename, audio = api.download_song(song.id)
        if not os.path.exists(folder):
            if thread_logger:
                thread_logger.debug("Creating folder '%s'" % folder)
            os.makedirs(folder)
        with open(file_path, 'wb') as file_handler:
            if thread_logger:
                thread_logger.debug("Writing file '%s'" % file_path)
            file_handler.write(audio)


def download(
        directory: str = ".",
        oauth: str = __DEFAULT_OAUTH_PATH__,
        device_id: str = __DEFAULT_MAC__,
        down_logger: logging.Logger = logger
) -> None:
    api = Musicmanager()
    if not api.login(oauth, device_id):
        if down_logger:
            down_logger.error("Error with oauth credentials")
        sys.exit(1)

    if down_logger:
        down_logger.info("Init Daemon - Press Ctrl+C to quit")

    songs = api.get_uploaded_songs()
    songs_total = len(songs)
    if down_logger:
        logger.debug("Downloading '%d' to folder '%s'" % (songs_total, directory))
    future_to_song = {}
    with ThreadPoolExecutor() as executor:
        for song in songs:
            artist = song['album_artist']
            album = song['album']
            track_number = song['track_number']
            title = song['title'].replace('/', '_').replace('?', '_')
            track_id = song['id']
            song_object = Song(artist=artist, album=album, track_number=track_number, title=title, id=track_id)
            future = executor.submit(
                _download,
                song=song_object,
                api=api,
                base_dir=directory,
                thread_logger=down_logger
            )
            future_to_song[future] = song

        succeeded = 0
        failed = 0
        for future in concurrent.futures.as_completed(future_to_song):
            song = future_to_song[future]
            if future.exception():
                if down_logger:
                    down_logger.warning("Failed to download song '%s' because '%s'" % (song.title, future.exception()))
                failed += 1
                continue
            succeeded += 1
        if down_logger:
            down_logger.debug("Completed. Total %d | %d succeeded | %d failed" % (songs_total, succeeded, failed))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", '-d', default='.', help="Music Folder to download to (default: .)")
    parser.add_argument(
        "--oauth",
        '-a',
        default=os.environ['HOME'] + '/oauth',
        help="Path to oauth file (default: ~/oauth)"
    )
    parser.add_argument(
        "--device_id",
        '-i',
        default=__DEFAULT_MAC__,
        help="Device identification (should be an uppercase MAC address) (default: <current eth0 MAC address>)"
    )
    args = parser.parse_args()
    download(args.directory, oauth=args.oauth, device_id=args.device_id)


if __name__ == "__main__":
    main()
