mobify [![Build Status](https://api.travis-ci.org/macbre/mobify.png?branch=master)](http://travis-ci.org/macbre/mobify)
------

Download a webpage as an e-book

## Install

[![PyPI version](https://img.shields.io/pypi/pyversions/mobify.svg)](https://pypi.python.org/pypi/mobify)

```
pip install mobify
```

You may need to run `sudo apt-get install zlib1g-dev` if `lxml` install fails (`python3.4-dev` package is required as well to compile `lxml`).

#### virtualenv

```
virtualenv --system-site-packages env3 -p python3
pip install -U -e .
```

### For Kindle users

You need to install `calibre` package to be able to convert epub to mobi (using `ebook-convert`)

```
apt-get install calibre
```

## Usage

```
mobify "http://histmag.org/william-wallace-bohater-szkotow-bohater-popkultury-11698"
```

Or you can render a multi-chapter ebook from several URLs (simply separate them with spaces):

```
mobify "http://histmag.org/william-wallace-bohater-szkotow-bohater-popkultury-11698" "http://histmag.org/Historia-Szkocji-10-dat-ktore-powinienes-znac-10028"
```

epub and mobi files will be saved in your working directory.

You can force a specific source to be used to parse the URL:

```
mobify 'https://deeplearningsandbox.com/how-to-build-an-image-recognition-system-using-keras-and-tensorflow-for-a-1000-everyday-object-559856e04699#.oqknumtc6' --source MediumSource
```

## Debugging

Simply set `DEBUG` env variable to `1`.

```
DEBUG=1 mobify ...
```

## Supported sources

* Blogspot
* dzieje.pl
* histmag.org
* medium.com
* oreilly.com/ideas
* readthedocs.io
* Tumblr
* Wikipedia
