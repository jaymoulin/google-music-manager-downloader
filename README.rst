.. image:: https://raw.githubusercontent.com/jaymoulin/google-music-manager-downloader/master/logo.png
    :alt: logo
    :target: http://github.com/jaymoulin/google-music-manager-downloader


=================================
Google Music Manager - Downloader
=================================



.. image:: https://img.shields.io/github/release/jaymoulin/google-music-manager-downloader.svg
    :alt: latest release
    :target: http://github.com/jaymoulin/google-music-manager-downloader/releases
.. image:: https://img.shields.io/pypi/v/google-music-manager-downloader.svg
    :alt: PyPI version
    :target: https://pypi.org/project/google-music-manager-downloader/
.. image:: https://github.com/jaymoulin/jaymoulin.github.io/raw/master/ppl.png
    :alt: PayPal donation
    :target: https://www.paypal.me/jaymoulin
.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
    :alt: Buy me a coffee
    :target: https://www.buymeacoffee.com/3Yu8ajd7W
.. image:: https://badgen.net/badge/become/a%20patron/F96854
    :alt: Become a Patron
    :target: https://patreon.com/jaymoulin

(This product is available under a free and permissive license, but needs financial support to sustain its continued improvements. In addition to maintenance and stability there are many desirable features yet to be added.)

This program will replace former Google MusicManager to upload your music library to Google Music

This work is based upon `Simon Weber's Google Music API <https://github.com/simon-weber/gmusicapi>`_.

Installation
------------

This program needs `netifaces` Python library to work.

.. code::

    apt-get install python3-pip build-essential
    pip3 install google-music-manager-downloader


Once installed, You have to authenticate to Google Music via the `google-music-auth` command

.. code::

    # Usage google-music-auth [path_to_oauth_cred_file=~/oauth]


If first parameter is not defined, the script will try to store/load your oauth credentials through the `~/oauth` file.

Then follow prompted instructions.

You will be asked to go to a Google URL to allow the connection:

.. code::

    Visit the following url:
        https://accounts.google.com/o/oauth2/v2/auth?client_id=XXXXXXXXXXX.apps.googleusercontent.com&access_type=offline&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fmusicmanager&response_type=code&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob
    Follow the prompts, then paste the auth code here and hit enter:

Usage
-----

Downloader
~~~~~~~~~~

This program will download all your uploaded musics from Google Music to a given directory.

.. code::

    usage: google-music-download [-h] [--directory DIRECTORY] [--oauth OAUTH]

    optional arguments:
        -h, --help            show this help message and exit
        --directory DIRECTORY, -d DIRECTORY
                            Music Folder to download to (default: .)
        --oauth OAUTH, -a OAUTH
                            Path to oauth file (default: ~/oauth)
        --device_id DEVICE_ID, -i DEVICE_ID
                            Device identification (should be an uppercase MAC
                            address) (default: <current eth0 MAC address>)


=====
About
=====

Requirements
------------

Google Music Uploader works with Python 3 or above.
It requires `Simon Weber's Google Music API <https://github.com/simon-weber/gmusicapi>`_.

Submitting bugs and feature requests
------------------------------------

Bugs and feature request are tracked on GitHub

Author
------

Jay MOULIN jaymoulin@gmail.com See also the list of contributors which participated in this program.

License
-------

Google Music Uploader is licensed under the MIT License
