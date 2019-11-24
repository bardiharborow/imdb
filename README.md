# imdb

[![Build Status](https://travis-ci.org/bardiharborow/imdb.svg?branch=master)](https://travis-ci.org/bardiharborow/imdb) [![Coverage Status](https://coveralls.io/repos/github/bardiharborow/imdb/badge.svg?branch=master)](https://coveralls.io/github/bardiharborow/imdb?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/5defb91a89c1bc741183/maintainability)](https://codeclimate.com/github/bardiharborow/imdb/maintainability) [![Python Package](https://img.shields.io/static/v1?label=test%20pypi&message=v0.1.1&color=blue)](https://test.pypi.org/project/imdb-cli/)

A command-line tool for retrieving an artist's filmography from [IMDb](https://www.imdb.com/).

## Usage

```shell
$ imdb --name "Octavia Spencer"
```

```shell
$ imdb --name "Octavia Spencer" --reverse --json
```

```shell
$ imdb --id nm0818055
```

## Install

To avoid polluting the main PyPI index, this project is published on the staging PyPI. To install, follow this process.

```shell
$ pip install requests
$ pip install --index-url https://test.pypi.org/simple/ --no-deps imdb-cli
```

## Caution

This project is provided for educational purposes only and is not affiliated with IMDb. You should request explicit permission from IMDb before using the software. If you plan to engage in large-scale scraping, IMDb's [downloadable datasets](https://www.imdb.com/interfaces/) may be more suitable.

## Licence

Licensed under the [MIT License](https://github.com/bardiharborow/imdb/blob/master/LICENSE). This software is provided on an "as is" basis, without warranties of any kind.
