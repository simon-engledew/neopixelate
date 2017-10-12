import operator
import math
import itertools


MAX = 255


def _hue_to_rgb(v1, v2, vH):
    vH %= 1

    if 6 * vH < 1: return v1 + (v2 - v1) * 6 * vH
    if 2 * vH < 1: return v2
    if 3 * vH < 2: return v1 + (v2 - v1) * ((2.0 / 3) - vH) * 6

    return v1


def _scale(value, distance, shallow=True):
    fn = operator.mul if shallow else operator.pow

    intensity = value - fn(distance, 2)

    return min(MAX, max(0, int(intensity)))


def scale((r, g, b), distance, ratio):
    fade = ratio / float(MAX)
    return (
        _scale(r * fade, distance),
        _scale(g * fade, distance),
        _scale(b * fade, distance)
    )


def result(outer):
    def decorator(inner):
        def decorated(*args, **kwargs):
            return outer(inner(*args, **kwargs))
        return decorated
    return decorator


def to_hsl(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    low = min(r, g, b)
    high = max(r, g, b)
    delta = high - low

    if high == low:
        h = 0
    elif high == r:
        h = (g - b) / delta
    elif high == g:
        h = 2 + (b - r) / delta
    elif high == b:
        h = 4 + (r - g) / delta

    h *= 60

    l = (low + high) / 2.0

    if high == low:
        s = 0
    elif l < 0.5:
        s = delta / float(high + low)
    else:
        s = delta / float(2 - high - low)

    return (
        int(round(h)),
        int(round(s * 100)),
        int(round(l * 100))
    )

def to_rgb(h, s, l):
    h /= 360.0
    s /= 100.0
    l /= 100.0

    if s == 0:
        grey = int(round(l * 255))
        return (grey, grey, grey)

    if l < 0.5:
        v2 = l * (1 + s)
    else:
        v2 = l + s - l * s

    v1 = 2 * l - v2

    r = _hue_to_rgb(v1, v2, h + (1.0 / 3))
    g = _hue_to_rgb(v1, v2, h)
    b = _hue_to_rgb(v1, v2, h - (1.0 / 3))

    return (
        int(round(r * 255)),
        int(round(g * 255)),
        int(round(b * 255)),
    )


@result(tuple)
def gradient(begin, end, steps):
    hA, sA, lA = to_hsl(*begin)
    hB, sB, lB = to_hsl(*end)
    dH, dS, dL = (
        (hA - hB) / float(steps - 1),
        (sA - sB) / float(steps - 1),
        (lA - lB) / float(steps - 1),
    )

    for n in xrange(steps - 1):
        yield to_rgb(
            abs(hA - (dH * n)),
            abs(sA - (dS * n)),
            abs(lA - (dL * n)),
        )

    yield end
