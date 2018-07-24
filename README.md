[![CircleCI](https://circleci.com/gh/d2verb/battery.svg?style=svg)](https://circleci.com/gh/d2verb/battery)

Battery is a blog engine written in python. Note that this project is WIP.

## Features
- [x] post entry
- [x] delete entry
- [x] post comment
- [x] delete comment
- [ ] user registration
- [x] preview
- [ ] TeX extension
- [ ] security features
- [ ] archive
- [ ] upload

## How to use

```
$ pip install -r requirements
$ export FLASK_APP=./battery
$ export FLASK_ENV=development
$ flask run
```

## How to run tests

```
$ python -m pytest
```
## ScreenShots
![entry page](img/entry-page-screenshot.png)

## LICENSE
This software is released under the MIT License, see LICENSE.
