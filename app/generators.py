import time
import itertools


def scroll(pattern):
    """
    Make an iterator rotates pattern.
    """
    index = 0
    while True:
        yield itertools.chain(pattern[index:], pattern[:index])
        index = (index + 1) % len(pattern)


def hertz(hertz, generator):
    """
    Make an iterator that consumes the iterable at hertz items/second.
    """
    while True:
        now = time.time()
        yield next(generator)
        sleep = 1./hertz - (time.time() - now)
        if sleep > 0:
            time.sleep(sleep)


def clamp((r, g, b)):
    """
    Clamp a color between 255 and 0.
    """
    return (
        min(255, max(0, r)),
        min(255, max(0, g)),
        min(255, max(0, b))
    )


def _linear_gradient(begin, end, steps):
    rB, gB, bB = begin
    rE, gE, bE = end
    rD = (rE - rB) / float(steps - 1)
    gD = (gE - gB) / float(steps - 1)
    bD = (bE - bB) / float(steps - 1)
    return [
        clamp((
            rB + (rD * step),
            gB + (gD * step),
            bB + (bD * step)
        ))
        for step in xrange(steps)
    ]


def fade(target, steps):
    """
    Fade to target color.
    """
    def _render():
        for step in xrange(1, steps):
            yield (
                gradient[step] for gradient in _render.gradients
            )

    def _init(state):
        _render.gradients = tuple(
            _linear_gradient(pixel, target, steps)
            for _, pixel in state
        )
        return (
            gradient[0] for gradient in _render.gradients
        )

    yield _init
    for state in _render():
        yield state
