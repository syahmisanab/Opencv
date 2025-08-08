#!/usr/bin/env python3
"""
MAX7219 8x8 LED matrix demo (luma.led_matrix)

Patterns:
  1) Corners + center
  2) Cross (horizontal + vertical lines)
  3) Intensity sweep (low → medium → high)

Press Ctrl+C to stop. Display is cleared on exit.
"""

import time
import sys
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

# ---- Config ----
CASCADED = 1     # number of chained 8x8 modules
ROTATE = 2       # 0,1,2,3 → multiples of 90°
DELAY_S = 2.0    # pause between patterns

# ---- Init ----
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=CASCADED, rotate=ROTATE)


def clear():
    """Turn off all pixels."""
    with canvas(device) as draw:
        draw.rectangle((0, 0, device.width - 1, device.height - 1), fill="black")


def draw_corners_and_center():
    """Corners + center pixel."""
    max_x, max_y = device.width - 1, device.height - 1
    cx, cy = max_x // 2, max_y // 2
    with canvas(device) as draw:
        draw.point((0, 0), fill="white")              # top-left
        draw.point((max_x, 0), fill="white")          # top-right
        draw.point((0, max_y), fill="white")          # bottom-left
        draw.point((max_x, max_y), fill="white")      # bottom-right
        draw.point((cx, cy), fill="white")            # center
    time.sleep(DELAY_S)


def draw_cross():
    """Cross through the matrix center."""
    max_x, max_y = device.width - 1, device.height - 1
    cx, cy = max_x // 2, max_y // 2
    with canvas(device) as draw:
        draw.line((0, cy, max_x, cy), fill="white")   # horizontal
        draw.line((cx, 0, cx, max_y), fill="white")   # vertical
    time.sleep(DELAY_S)


def intensity_sweep():
    """Fill at low, medium, high brightness."""
    for level in (1, 128, 255):
        device.contrast(level)
        with canvas(device) as draw:
            draw.rectangle((0, 0, device.width - 1, device.height - 1), fill="white")
        time.sleep(DELAY_S)


def main():
    try:
        while True:
            print("Pattern: corners + center")
            draw_corners_and_center()

            print("Pattern: cross")
            draw_cross()

            print("Pattern: intensity sweep")
            intensity_sweep()
    except KeyboardInterrupt:
        print("\nStopping…")
    finally:
        device.contrast(1)
        clear()


if __name__ == "__main__":
    main()
