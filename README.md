[![CircleCI](https://circleci.com/gh/d2verb/battery.svg?style=svg)](https://circleci.com/gh/d2verb/battery)

Battery is a blog engine written in python. Note that this project is WIP.

## Features
- [x] post entry
- [x] delete entry
- [x] post comment
- [x] delete comment
- [x] preview
- [x] TeX extension
- [ ] security features
- [x] archive
- [x] upload
- [x] save as draft
- [ ] category

## How to run
You can run battery easily in your local machine. If you want to run battery on your server with apache, please see doc/INSTALL.md
```
$ pip install -r requirements
$ export FLASK_APP=./battery

# development mode
$ export FLASK_ENV=development
$ flask run

# production mode
$ export FLASK_ENV=development
$ flask run
```

You can override the default configuration by createing instance/config.py. Battery will automatically load it if it exists.

## How to run tests

```
$ export FLASK_ENV=testing
$ python -m pytest
```
## ScreenShots
[Top Page](img/toppage.png)

[Blog Entry Page](img/entrypage.png)

[Upload Page](img/uploadpage.png)

## LICENSE
This software is released under the MIT License, see LICENSE.
