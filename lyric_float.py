"""
Floating Lyric Animation — Pyglet Native (macOS, Windows, Linux)
------------------------------------------------------------------
Small transparent lyric cards float upward over your desktop.
Run from VS Code terminal, no browser needed.

Requirements:
    pip3 install pyglet

Usage:
    1. Edit LYRICS and AUDIO_FILE below.
    2. Run: python3 lyric_float.py
    3. Cards start floating immediately.
    4. Press Escape or click to exit.
"""

import pyglet
from pyglet import shapes
from pyglet.window import key
import subprocess
import time
import os
import platform

# ====================== EDIT THIS SECTION ======================

AUDIO_FILE = ""  # path to .mp3 / .wav, or "" to disable

LYRICS = [
    (0.0,  "Her love is in your head"),
    (3.2,  "You lost your earrings in her bed"),
    (6.5,  "You couldn't tell her that you lost 'em"),
    (9.8,  "'Cause you're scared and you're not talking"),
    (12.9, "So you think of what to say"),
    (16.1, "Then save it for another day"),
    (18.4, "'Cause you just never had the heart"),
    (21.2, "Now they just drift further apart"),
    (24.0, "From You...."),
]

CARD_W  = 340
CARD_H  = 140
FONT_NAME = "Helvetica Neue"
FONT_SIZE = 26
TEXT_COLOR = (255, 255, 255, 255)        # white
CARD_BG    = (10, 10, 20, 90)            # dark translucent
CARD_BORDER = (255, 255, 255, 40)         # subtle white border

RISE_SPEED = 80
SPAWN_COLS = 2
BOTTOM_SPAWN_Y = 0.78   # spawn at 78 % of screen height

# ===============================================================


class LyricCard:
    def __init__(self, text, cx, y, batch):
        self.batch = batch
        self.x = cx - CARD_W // 2
        self.y = float(y)
        self.full_text = text
        self.char_index = 0
        self.done = False

        shadow_off = (3, -3)
        self.shadow = shapes.Rectangle(
            self.x + shadow_off[0], self.y + shadow_off[1],
            CARD_W, CARD_H,
            color=(0, 0, 0, 30), batch=batch,
        )
        self.body = shapes.BorderedRectangle(
            self.x, self.y, CARD_W, CARD_H,
            border=1, border_color=CARD_BORDER,
            color=CARD_BG, batch=batch,
        )
        self.label = pyglet.text.Label(
            "", font_name=FONT_NAME, font_size=FONT_SIZE,
            x=self.x + CARD_W // 2, y=self.y + CARD_H // 2,
            anchor_x="center", anchor_y="center",
            color=TEXT_COLOR, width=CARD_W - 30,
            multiline=True, batch=batch,
        )

    def typewriter(self, dt):
        if self.char_index <= len(self.full_text):
            self.label.text = self.full_text[:self.char_index]
            self.char_index += 1
        else:
            self.done = True

    def rise(self, dy):
        self.y -= dy
        self.body.y = self.y
        self.shadow.y = self.y - 3
        self.label.y = self.y + CARD_H // 2

    def off_screen(self):
        return self.y + CARD_H < -10

    def delete(self):
        self.shadow.delete()
        self.body.delete()
        self.label.delete()


class LyricFloat:
    def __init__(self):
        display = pyglet.canvas.get_display()
        screens = display.get_screens()
        self.screen = screens[0]
        self.screen_w = self.screen.width
        self.screen_h = self.screen.height

        self.window = pyglet.window.Window(
            width=self.screen_w, height=self.screen_h,
            style=pyglet.window.Window.WINDOW_STYLE_OVERLAY,
            caption="Lyric Float",
        )
        self.window.set_location(0, 0)

        self.batch = pyglet.graphics.Batch()
        self.cards = []
        self.next_idx = 0
        self.col_idx = 0
        self.start_time = time.time()
        self.last_time = self.start_time
        self.elapsed = 0.0
        self.running = True

        # audio
        if AUDIO_FILE:
            system = platform.system()
            try:
                if system == "Darwin":
                    subprocess.Popen(["afplay", AUDIO_FILE])
                elif system == "Windows":
                    subprocess.Popen(["start", "", AUDIO_FILE], shell=True)
                else:
                    subprocess.Popen(["xdg-open", AUDIO_FILE])
            except Exception:
                pass

        # event handlers
        self.window.on_draw = self._on_draw
        self.window.on_key_press = self._on_key_press
        self.window.on_mouse_press = self._on_mouse_press

        # schedule updates
        pyglet.clock.schedule_interval(self._update, 1 / 60.0)
        pyglet.clock.schedule_interval(self._typewriter_tick, 1 / 15.0)

    def _column_centers(self):
        margin = 80
        usable = self.screen_w - margin * 2
        spacing = usable / SPAWN_COLS
        return [margin + spacing * (i + 0.5) for i in range(SPAWN_COLS)]

    def _update(self, dt):
        if not self.running:
            return
        now = time.time()
        self.elapsed = now - self.start_time
        dt = now - self.last_time
        self.last_time = now

        cols = self._column_centers()

        # spawn due lyrics
        while self.next_idx < len(LYRICS) and LYRICS[self.next_idx][0] <= self.elapsed:
            _, text = LYRICS[self.next_idx]
            cx = cols[self.col_idx % len(cols)]
            self.col_idx += 1
            y = int(self.screen_h * BOTTOM_SPAWN_Y)
            card = LyricCard(text, cx, y, self.batch)
            self.cards.append(card)
            self.next_idx += 1

        # rise all cards
        dy = RISE_SPEED * dt
        for c in self.cards:
            c.rise(dy)

        # remove off-screen
        self.cards = [c for c in self.cards if not c.off_screen()]

        # check done
        if self.next_idx >= len(LYRICS) and not self.cards and self.elapsed > LYRICS[-1][0] + 3:
            self.running = False
            pyglet.app.exit()

    def _typewriter_tick(self, dt):
        for c in self.cards:
            if not c.done:
                c.typewriter(dt)

    def _on_draw(self):
        self.window.clear()
        self.batch.draw()

    def _on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.running = False
            pyglet.app.exit()

    def _on_mouse_press(self, x, y, button, modifiers):
        self.running = False
        pyglet.app.exit()

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    LyricFloat().run()
