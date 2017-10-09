FLOAT_ERROR = 0.0000005


def _hue2rgb(v1, v2, vH):
    while vH < 0: vH += 1
    while vH > 1: vH -= 1

    if 6 * vH < 1: return v1 + (v2 - v1) * 6 * vH
    if 2 * vH < 1: return v2
    if 3 * vH < 2: return v1 + (v2 - v1) * ((2.0 / 3) - vH) * 6

    return v1


def _hsl2rgb(hsl):
    h, s, l = [float(v) for v in hsl]

    if not (0.0 - FLOAT_ERROR <= s <= 1.0 + FLOAT_ERROR):
        raise ValueError("Saturation must be between 0 and 1.")
    if not (0.0 - FLOAT_ERROR <= l <= 1.0 + FLOAT_ERROR):
        raise ValueError("Lightness must be between 0 and 1.")

    if s == 0:
        return l, l, l

    if l < 0.5:
        v2 = l * (1.0 + s)
    else:
        v2 = (l + s) - (s * l)

    v1 = 2.0 * l - v2

    r = _hue2rgb(v1, v2, h + (1.0 / 3))
    g = _hue2rgb(v1, v2, h)
    b = _hue2rgb(v1, v2, h - (1.0 / 3))

    return int(r*255), int(g*255), int(b*255)


def _rgb2hsl(rgb):
    r, g, b = (v/255.0 for v in rgb)

    vmin = min(r, g, b)
    vmax = max(r, g, b)
    diff = vmax - vmin

    vsum = vmin + vmax

    l = vsum / 2

    if diff < FLOAT_ERROR:
        return (0.0, 0.0, l)

    if l < 0.5:
        s = diff / vsum
    else:
        s = diff / (2.0 - vsum)

    dr = (((vmax - r) / 6) + (diff / 2)) / diff
    dg = (((vmax - g) / 6) + (diff / 2)) / diff
    db = (((vmax - b) / 6) + (diff / 2)) / diff

    if r == vmax:
        h = db - dg
    elif g == vmax:
        h = (1.0 / 3) + dr - db
    elif b == vmax:
        h = (2.0 / 3) + dg - dr

    if h < 0: h += 1
    if h > 1: h -= 1

    return (h, s, l)


def gradient(begin, end, steps):
    begin_hsl = _rgb2hsl(begin)
    end_hsl = _rgb2hsl(end)

    step = tuple(
        tuple(float(a - b) / steps for a, b in zip(end_hsl, begin_hsl))
    ) if steps > 0 else (0, 0, 0)

    def mul(step, value):
        return tuple([v * value for v in step])

    def add_v(step, step2):
        return tuple([v + step2[i] for i, v in enumerate(step)])

    return [_hsl2rgb(add_v(begin_hsl, mul(step, r))) for r in range(0, steps + 1)]
