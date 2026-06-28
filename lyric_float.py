"""
Floating Lyric Animation — Pyglet Native (Zero External Deps)
---------------------------------------------------------------
Small lyric cards float upward over your desktop as a transparent
overlay. Run from VS Code terminal — no browser, no tkinter.

Requirements:
    pip3 install pyglet

Usage:
    1. Edit LYRICS and AUDIO_FILE below.
    2. Run: python3 lyric_float.py
    3. Cards start floating. Press Esc or click to exit.
"""

import pyglet
from pyglet import gl
from pyglet.window import key
import subprocess
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

CARD_W  = 500
CARD_H  = 240
FONT_SIZE = 38
TEXT_COLOR   = (30, 30, 30, 255)       # dark text
CARD_BG      = (255, 255, 255, 255)    # solid white card
CARD_BORDER  = (200, 200, 200, 255)    # grey border

RISE_SPEED = 50     # slower = more relaxed sync
SPAWN_COLS = 2
BOTTOM_SPAWN_Y = 0.20    # spawn near bottom, rise upward (0=bottom, 1=top)

# ===============================================================


class LyricCard:
    def __init__(self, text, cx, y, batch):
        self.full_text = text
        self.char_index = 0
        self.done = False
        self.x = cx - CARD_W // 2
        self.y = float(y)
        self.batch = batch

        self.border = pyglet.shapes.Box(
            self.x - 1, self.y - 1, CARD_W + 2, CARD_H + 2,
            color=CARD_BORDER, thickness=1, batch=batch,
        )
        self.body = pyglet.shapes.Rectangle(
            self.x, self.y, CARD_W, CARD_H,
            color=CARD_BG, batch=batch,
        )
        self.label = pyglet.text.Label(
            "",
            font_name="Helvetica Neue", font_size=FONT_SIZE,
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
        self.y += dy
        self.body.y = self.y
        self.border.y = self.y - 1
        self.label.y = self.y + CARD_H // 2

    def off_screen(self, screen_h):
        return self.y > screen_h + 10

    def delete(self):
        self.body.delete()
        self.border.delete()
        self.label.delete()


class LyricFloat:
    def __init__(self):
        display = pyglet.display.get_display()
        screens = display.get_screens()
        self.screen = screens[0]
        self.screen_w = self.screen.width
        self.screen_h = self.screen.height

        self.window = pyglet.window.Window(
            width=self.screen_w, height=self.screen_h,
            style=pyglet.window.Window.WINDOW_STYLE_OVERLAY,
        )
        self.window.set_location(0, 0)

        self.batch = pyglet.graphics.Batch()
        self.cards = []
        self.next_idx = 0
        self.col_idx = 0
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

        self.window.on_draw = self._on_draw
        self.window.on_key_press = self._on_key_press
        self.window.on_mouse_press = self._on_mouse_press
        self.window.on_mouse_motion = self._on_mouse_motion

        pyglet.clock.schedule_interval(self._update, 1 / 60.0)
        pyglet.clock.schedule_interval(self._typewriter_tick, 1 / 15.0)

    def _column_centers(self):
        margin = 120
        usable = self.screen_w - margin * 2
        spacing = usable / SPAWN_COLS
        return [margin + spacing * (i + 0.5) for i in range(SPAWN_COLS)]

    def _update(self, dt):
        if not self.running:
            return
        self.elapsed += dt

        cols = self._column_centers()

        while self.next_idx < len(LYRICS) and LYRICS[self.next_idx][0] <= self.elapsed:
            _, text = LYRICS[self.next_idx]
            cx = cols[self.col_idx % len(cols)]
            self.col_idx += 1
            y = int(self.screen_h * BOTTOM_SPAWN_Y - CARD_H // 2)
            card = LyricCard(text, cx, y, self.batch)
            self.cards.append(card)
            self.next_idx += 1

        dy = RISE_SPEED * dt
        for c in self.cards:
            c.rise(dy)

        self.cards = [c for c in self.cards if not c.off_screen(self.screen_h)]

        if self.next_idx >= len(LYRICS) and not self.cards and self.elapsed > LYRICS[-1][0] + 3:
            self.running = False
            pyglet.app.exit()

    def _typewriter_tick(self, dt):
        for c in self.cards:
            if not c.done:
                c.typewriter(dt)

    def _on_draw(self):
        gl.glClearColor(0, 0, 0, 0)
        self.window.clear()
        self.batch.draw()

    def _on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.running = False
            pyglet.app.exit()

    def _on_mouse_press(self, x, y, button, modifiers):
        self.running = False
        pyglet.app.exit()

    def _on_mouse_motion(self, x, y, dx, dy):
        pass

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    LyricFloat().run()
