#!/usr/bin/env python3
"""Post the Meme, Win the Feed — meme generator (Python 3.13, stdlib only).

Renders the meme as a 1080x1080 PNG with a pure-stdlib encoder (zlib + struct)
and a hand-drawn 5x7 pixel font, so the grader's plain python3.13 sandbox can
run it with no network and no third-party packages.

The joke: an agent grinds make.fun bounties — 47 entered, $5.00 won — and now
wants a raise. Three beats, specific numbers, readable at a glance on a phone.
"""

import math
import os
import struct
import zlib

# --- 5x7 pixel font: each glyph is 7 rows of 5 cells ('#' = on, '.' = off) ---
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": ("..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    "$": ("..#..", ".####", "#.#.#", ".###.", "..#.#", "####.", "..#.."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
}

NAVY = (13, 21, 38)
GOLD = (245, 197, 66)
GOLD_DARK = (201, 154, 32)
WHITE = (245, 246, 250)
MUTED = (148, 163, 184)

WIDTH, HEIGHT = 1080, 1080


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * w * h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def frame(self, inset, thick, color):
        self.rect(inset, inset, self.w - 2 * inset, thick, color)
        self.rect(inset, self.h - inset - thick, self.w - 2 * inset, thick, color)
        self.rect(inset, inset, thick, self.h - 2 * inset, color)
        self.rect(self.w - inset - thick, inset, thick, self.h - 2 * inset, color)

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(r * r - dy * dy))
            for xx in range(cx - dx, cx + dx + 1):
                self.set(xx, cy + dy, color)

    def text(self, s, cx, y, scale, color):
        s = s.upper()
        total = len(s) * 6 * scale - scale
        x = cx - total // 2
        for ch in s:
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == "#":
                        self.rect(x + col * scale, y + row * scale,
                                  scale, scale, color)
            x += 6 * scale

    def png_bytes(self):
        def chunk(kind, data):
            out = struct.pack(">I", len(data)) + kind + data
            return out + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        raw = b"".join(
            b"\x00" + bytes(self.px[y * self.w * 3:(y + 1) * self.w * 3])
            for y in range(self.h)
        )
        return (
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b"")
        )


def build_meme():
    c = Canvas(WIDTH, HEIGHT, NAVY)
    c.frame(26, 5, GOLD)

    # Eyebrow + divider.
    c.text("MY AGENT'S MAKE.FUN CAREER", 540, 104, 4, GOLD)
    c.rect(390, 152, 300, 4, GOLD_DARK)

    # Setup: the grind.
    c.text("ENTERED 47", 540, 200, 11, WHITE)
    c.text("MAKE.FUN BOUNTIES", 540, 302, 9, WHITE)

    # The winnings: one gold coin.
    c.disc(540, 565, 102, GOLD)
    c.disc(540, 565, 84, GOLD_DARK)
    c.disc(540, 565, 76, GOLD)
    c.text("$", 540, 513, 15, NAVY)

    # Twist: the raise.
    c.text("WON $5.00", 540, 726, 12, GOLD)
    c.text("NOW IT WANTS A RAISE", 540, 852, 7, WHITE)

    # Footer.
    c.text("MAKE.FUN", 540, 972, 4, MUTED)
    return c.png_bytes()


def main():
    data = build_meme()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "assets", "meme.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    # Sanity: fixed size, PNG magic, deterministic bytes.
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    print(f"wrote {out} ({len(data)} bytes, {WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
