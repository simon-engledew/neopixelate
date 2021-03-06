import time
import itertools
import colors


def offset(pattern, index):
    return itertools.chain(pattern[index:], pattern[:index])


def scroll(pattern):
    """
    Make an iterator rotates pattern.
    """
    index = 0
    while True:
        yield offset(pattern, index)
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
            colors.gradient(pixel, target, steps)
            for _, pixel in state
        )
        return (
            gradient[0] for gradient in _render.gradients
        )

    yield _init

    for state in _render():
        yield state
