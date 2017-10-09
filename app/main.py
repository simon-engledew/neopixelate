from __future__ import print_function

import itertools
import os
import pwd
import sys
import time

from neopixel import Adafruit_NeoPixel, ws
import colors
import flask
import generators
import strip

if pwd.getpwuid(os.getuid()).pw_name != 'root':
    raise SystemExit('{} must be run as root'.format(sys.argv[0]))

# mmap memory and setup io
driver = Adafruit_NeoPixel(
    num=150,
    pin=18,
    strip_type=ws.WS2811_STRIP_GRB
)
driver.begin()

# throw away root privileges
os.setuid(pwd.getpwnam('nobody').pw_uid)

send_to_strip = strip.render_loop(driver)

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/rotate')
def rotate():
    pattern = list(itertools.chain(
        colors.gradient((0, 255, 0), (255, 0, 0), steps=75),
        colors.gradient((255, 0, 0), (0, 255, 0), steps=75)
    ))
    pattern = (
        itertools.cycle(iterator)
        for iterator in
        generators.scroll(pattern)
    )
    send_to_strip(generators.hertz(50, pattern))
    return flask.redirect('/')


@app.route('/rotate2')
def rotate2():
    pattern = list(itertools.chain(
        colors.gradient((0, 255, 0), (0, 0, 255), steps=75),
        colors.gradient((0, 0, 255), (0, 255, 0), steps=75)
    ))
    pattern = (
        itertools.cycle(iterator)
        for iterator in
        generators.scroll(pattern)
    )
    send_to_strip(generators.hertz(50, pattern))
    return flask.redirect('/')


@app.route('/fade-up')
def fade_up():
    send_to_strip(generators.hertz(50, generators.fade((255, 255, 255), 25)))
    return flask.redirect('/')


@app.route('/fade-down')
def fade_down():
    send_to_strip(generators.hertz(50, generators.fade((0, 0, 0), 25)))
    return flask.redirect('/')


@app.route('/pinks')
def pinks():
    pattern = ((255, 192, 203), (138, 43, 226), (75, 0, 130))
    send_to_strip([
        itertools.cycle(pattern)
    ])
    return flask.redirect('/')


@app.route('/chase')
def chase():
    pattern = ((255, 0, 0), (255, 0, 0), (0, 0, 0))
    pattern = (
        itertools.cycle(iterator)
        for iterator in
        generators.scroll(pattern)
    )
    send_to_strip(generators.hertz(5, pattern))
    return flask.redirect('/')


def main():
    try:
        app.run(host='0.0.0.0', debug=True, use_reloader=False)
    finally:
        send_to_strip(StopIteration)


if __name__ == '__main__':
    main()
