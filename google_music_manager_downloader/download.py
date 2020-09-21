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
from pathlib import Path
from typing import Callable

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

__DEFAULT_IFACE__ = netifaces.gateways()['default'][netifaces.AF_INET][1]
__DEFAULT_MAC__ = netifaces.ifaddresses(__DEFAULT_IFACE__)[netifaces.AF_LINK][0]['addr'].upper()
__DEFAULT_CREDS_DIR__ = os.path.join(os.environ['HOME'], '.gmusicdownloader')
__DEFAULT_CREDS__ = os.path.join(__DEFAULT_CREDS_DIR__, 'creds')
if not Path(__DEFAULT_CREDS_DIR__).exists():
    logger.debug(f"Creating {__DEFAULT_CREDS_DIR__}")
    os.makedirs(__DEFAULT_CREDS_DIR__)
if not Path(__DEFAULT_CREDS__).exists():
    logger.debug(f"Creating {__DEFAULT_CREDS__}")
    open(__DEFAULT_CREDS__, 'w').close()


def download(
    base_dir: str = ".",
    creds: str = __DEFAULT_CREDS__,
    device_id: str = __DEFAULT_MAC__
) -> None:
    api = Musicmanager()
    if not api.login(creds, device_id):
        logger.error("Error with oauth credentials")
        sys.exit(1)

    Song = namedtuple('Song', ['artist', 'album', 'track', 'title', 'id'])

    def _download(song: Song, downloader: Callable) -> None:
        logger.debug(f"Downloading song '{song.title}'")
        f, audio = downloader(song.id)

        folder = os.path.join(base_dir, song.artist, song.album)
        if not os.path.exists(folder):
            logger.debug(f"Creating folder '{folder}'")
            os.makedirs(folder)
        file = os.path.join(folder, f'{song.track}-{song.title}.mp3')
        with open(file, 'wb') as f:
            logger.debug(f"Writing file '{file}'")
            f.write(audio)

    songs = api.get_uploaded_songs()
    n = len(songs)
    logger.debug(f"Downloading '{n}' to folder '{base_dir}'")
    future_to_song = {}
    with ThreadPoolExecutor() as executor:
        for song in songs:
            artist = song['album_artist']
            album = song['album']
            track = song['track_number']
            title = song['title'].replace('/', '_').replace('?', '_')
            iden = song['id']
            s = Song(artist=artist, album=album, track=track, title=title, id=iden)
            future = executor.submit(_download, song=s, downloader=api.download_song)
            future_to_song[future] = s

        succeeded = 0
        failed = 0
        for future in concurrent.futures.as_completed(future_to_song):
            s = future_to_song[future]
            if future.exception():
                logger.warning(f"Failed to download song '{s.title}' because '{future.exception()}'")
                failed += 1
                continue
            succeeded += 1
        logger.debug(f"Completed. Total {n} succeded {succeeded} failed {failed}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", '-d', default='.', help="Music Folder to download to (default: .)")
    parser.add_argument(
        "--oauth",
        '-a',
        default=__DEFAULT_CREDS__,
        help="Path to oauth file (default: ~/.gmusicdownloader/creds)"
    )
    parser.add_argument(
        "--device_id",
        '-i',
        default=__DEFAULT_MAC__,
        help="Device identification (should be an uppercase MAC address) (default: <current eth0 MAC address>)"
    )
    args = parser.parse_args()

    logger.info("Downloading. Press Ctrl+C to quit")
    download(args.directory, creds=args.oauth, device_id=args.device_id)


if __name__ == "__main__":
    main()
