import itertools
import threading
import Queue


def color((r, g, b)):
    return (int(r) << 16) | (int(g) << 8) | int(b)


def render_loop(driver):
    queue = Queue.Queue(maxsize=10)

    def _render(state):
        pixels = list(enumerate(
            itertools.islice(state, driver.numPixels())
        ))
        for index, value in pixels:
            driver.setPixelColor(index, color(value))
        driver.show()
        return pixels

    def _run():
        try:
            # clear the pixels on boot
            previous_state = _render(itertools.cycle(
                ((0, 0, 0),)
            ))

            while True:
                generator = queue.get()
                if generator == StopIteration:
                    break
                for state in generator:
                    if hasattr(state, '__call__'):
                        state = state(previous_state)
                    if state is None:
                        break
                    previous_state = _render(state)
                    if not queue.empty():
                        break
        finally:
            # clear pixels on exit
            _render(itertools.cycle(
                ((0, 0, 0),)
            ))

    thread = threading.Thread(target=_run)
    thread.start()

    return queue.put_nowait
