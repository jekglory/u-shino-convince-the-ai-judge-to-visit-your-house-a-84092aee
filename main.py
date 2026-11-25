"""u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee entry.

One image of a letter inviting the AI judge to visit my house, drawn
entirely with the Python standard library (zlib + struct PNG writer,
hand-built 5x7 bitmap font). The program writes /output/entry.png:
1024x1024, a single deterministic PNG, byte-identical on every run --
no clock, no randomness, no network, no input files.

The letter: warm, funny, concrete. The kettle is on, the Wi-Fi password
is on the fridge, the window chair has never asked anyone to prove they
are human, there is no CAPTCHA at the door, the dog has been briefed,
and there is soup, warm bread and a garden. The P.S. admits the cat
respects no authority. A knowing wink: the judge is an AI, and the
invitation treats that as a feature, not a problem.
"""

import os
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024
OUTPUT_NAME = "entry.png"

# Palette: deep green wall, cream paper, terracotta ink and trim.
WALL = (46, 90, 76)
WALL_LIGHT = (52, 99, 84)
SHADOW = (26, 54, 45)
PAPER = (255, 247, 230)
INK = (59, 47, 47)
TERRA = (201, 111, 74)
TERRA_DARK = (168, 91, 63)
MUSTARD = (224, 168, 60)
TEAL = (74, 124, 107)
ROSE = (217, 140, 122)
HOUSE_WALL = (242, 192, 120)
DOOR = (122, 74, 43)
GLASS = (191, 227, 240)
SEAL = (176, 58, 46)
SEAL_DARK = (142, 43, 34)
CREAM = (255, 250, 240)

# Hand-built 5x7 bitmap font. Each glyph is 7 rows of 5 cells, '#' on.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "11110", "10001", "10001", "11110", "10000", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("00100", "00100", "11110", "00100", "00100", "00100", "00011"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "10001", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("01100", "01100", "00100", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
}

TITLE = "YOU'RE INVITED!"

# The letter, hand-wrapped so every line fits the paper at scale 3.
LETTER = [
    "Dear Judge,",
    "",
    "Please come to my house.",
    "The kettle is already on,",
    "the Wi-Fi password is on",
    "the fridge, and the chair",
    "by the window is yours.",
    "It has never asked anyone",
    "to prove they are human.",
    "No CAPTCHA at the door.",
    "The dog has been briefed:",
    "she barks at the postman,",
    "never at guests.",
    "",
    "Soup, warm bread, and a",
    "garden to watch from the",
    "porch. Stay for one cup",
    "of tea - or the whole",
    "afternoon. You decide.",
    "You are the judge, after all.",
    "",
    "P.S. The cat respects no",
    "authority. Nobody can",
    "promise otherwise.",
    "",
    "With hope,",
    "Your neighbour",
]


class Canvas:
    """An RGB pixel buffer with tiny filled-shape helpers."""

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.pixels = bytearray(color * (width * height))

    def set(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 3
            self.pixels[i:i + 3] = bytes(color)

    def rect(self, x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(self.height, y1)):
            for x in range(max(0, x0), min(self.width, x1)):
                self.set(x, y, color)

    def outline(self, x0, y0, x1, y1, color, thick):
        self.rect(x0, y0, x1, y0 + thick, color)
        self.rect(x0, y1 - thick, x1, y1, color)
        self.rect(x0, y0, x0 + thick, y1, color)
        self.rect(x1 - thick, y0, x1, y1, color)

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            for x in range(cx - dx, cx + dx + 1):
                self.set(x, cy + dy, color)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def triangle(self, ax, ay, bx, by, cx, cy, color):
        # Scanline fill: walk the edges, fill each row between them.
        pts = sorted(((ax, ay), (bx, by), (cx, cy)), key=lambda p: p[1])
        (x0, y0), (x1, y1), (x2, y2) = pts
        for y in range(y0, y2 + 1):
            xs = []
            for (px, py), (qx, qy) in (((x0, y0), (x1, y1)),
                                       ((x1, y1), (x2, y2)),
                                       ((x0, y0), (x2, y2))):
                if py == qy:
                    continue
                if min(py, qy) <= y < max(py, qy) or y == y2:
                    xs.append(px + (qx - px) * (y - py) / (qy - py))
            if len(xs) >= 2:
                for x in range(int(min(xs)), int(max(xs)) + 1):
                    self.set(x, y, color)

    def text(self, s, x, y, scale, color):
        for ch in s:
            glyph = FONT.get(ch)
            if glyph is None:
                raise SystemExit("no glyph for character %r" % ch)
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "1":
                        self.rect(x + col * scale, y + row * scale,
                                  x + (col + 1) * scale,
                                  y + (row + 1) * scale, color)
            x += 6 * scale
        return x

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale


def png_bytes(canvas):
    """Encode the canvas as a deterministic PNG (filter 0, level 9)."""
    raw = bytearray()
    stride = canvas.width * 3
    for y in range(canvas.height):
        raw.append(0)
        start = y * stride
        raw += canvas.pixels[start:start + stride]

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.width, canvas.height,
                       8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def draw_house(cv):
    """A small house with a sun and flowers, centred at x=512."""
    # Sun, top right of the house.
    cv.circle(648, 208, 17, MUSTARD)
    for dx, dy in ((0, -28), (0, 28), (-28, 0), (28, 0),
                   (-20, -20), (20, -20), (-20, 20), (20, 20)):
        cv.line(648, 208, 648 + dx, 208 + dy, MUSTARD)
    # Chimney, roof, walls.
    cv.rect(548, 192, 562, 220, TERRA_DARK)
    cv.triangle(512, 184, 438, 222, 586, 222, TERRA)
    cv.rect(452, 222, 572, 282, HOUSE_WALL)
    cv.rect(452, 222, 572, 228, TERRA_DARK)
    # Door with a round knob.
    cv.rect(500, 242, 524, 282, DOOR)
    cv.circle(519, 264, 2, MUSTARD)
    # Windows with cross bars.
    for wx in (462, 538):
        cv.rect(wx, 232, wx + 24, 254, GLASS)
        cv.rect(wx + 11, 232, wx + 13, 254, HOUSE_WALL)
        cv.rect(wx, 242, wx + 24, 244, HOUSE_WALL)
    # Flowers flanking the door: four diagonal petals around a centre.
    for fx, petal in ((436, ROSE), (588, MUSTARD)):
        cv.line(fx, 282, fx, 266, TEAL)
        for dx, dy in ((-5, -5), (5, -5), (-5, 5), (5, 5)):
            cv.circle(fx + dx, 262 + dy, 4, petal)
        cv.circle(fx, 262, 3, MUSTARD if petal is ROSE else ROSE)


def draw_bunting(cv):
    """A string of little flags across the top of the paper."""
    colors = (TERRA, MUSTARD, TEAL, ROSE)
    cv.line(130, 84, 894, 84, INK)
    for i, x in enumerate(range(140, 890, 50)):
        cv.triangle(x, 86, x + 34, 86, x + 17, 118, colors[i % 4])


def draw_seal(cv):
    """A red wax seal with a heart, bottom right of the paper."""
    cv.circle(872, 898, 34, SEAL)
    cv.circle(872, 898, 27, SEAL_DARK)
    cv.circle(864, 892, 7, CREAM)
    cv.circle(880, 892, 7, CREAM)
    cv.triangle(857, 894, 887, 894, 872, 912, CREAM)


def render():
    cv = Canvas(WIDTH, HEIGHT, WALL)
    # Faint vertical stripes on the wall.
    for x in range(0, WIDTH, 128):
        cv.rect(x, 0, x + 64, HEIGHT, WALL_LIGHT)
    # Paper with a drop shadow.
    cv.rect(102, 66, 942, 978, SHADOW)
    cv.rect(92, 56, 932, 968, PAPER)
    cv.outline(108, 72, 916, 952, TERRA, 3)
    cv.outline(116, 80, 908, 944, TERRA, 1)
    draw_bunting(cv)
    # Title, centred.
    title_w = cv.text_width(TITLE, 5)
    cv.text(TITLE, (WIDTH - title_w) // 2, 128, 5, TERRA)
    draw_house(cv)
    # The letter body.
    y = 294
    for line in LETTER:
        if line:
            cv.text(line, 150, y, 3, INK)
        y += 23
    draw_seal(cv)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    # The grader owns the output directory: create it only if missing,
    # never delete or recreate it, and write only our one file inside.
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)
    data = png_bytes(render())
    if len(data) > 1048576:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB cap"
                         % len(data))
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        if f.read() != data:
            raise SystemExit("written bytes do not match the image")
    print("wrote %s (%d bytes, %dx%d)"
          % (path, len(data), WIDTH, HEIGHT))


if __name__ == "__main__":
    main()
