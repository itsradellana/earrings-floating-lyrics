"""
Floating Lyric Animation — macOS, Windows, Linux
-------------------------------------------------
Every lyric line appears as a floating card that rises upward on a
fullscreen canvas, synced to a song. All rendering happens inside a
single window — no multi-popup headaches, works everywhere.

Requirements:
    pip install pygame   (optional, for audio playback)

Usage:
    1. Put your song file in the same folder (e.g. "song.mp3")
       and set AUDIO_FILE below. Leave "" to run without audio.
    2. Edit LYRICS: (start_time_seconds, "text")
    3. Run: python3 lyric_float.py
    4. Click "Start", fire up your screen recorder.
    5. Press Escape or click to exit.
"""

import tkinter as tk
import time
import random

try:
    import pygame
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False

# ====================== EDIT THIS SECTION ======================

AUDIO_FILE = ""  # set to your .mp3 / .wav path, or "" to disable

# (start_time_in_seconds, "lyric text")
LYRICS = [
    (5.0,  "Her love is in your head"),
    (8.2,  "You lost your earrings in her bed"),
    (11.5, "You couldn't tell her that you lost 'em"),
    (14.8, "'Cause you're scared and you're not talking"),
    (17.9, "So you think of what to say"),
    (21.1, "Then save it for another day"),
    (23.4, "'Cause you just never had the heart"),
    (26.2, "Now they just drift further apart"),
    (29.0, "From You...."),
]

BOX_W  = 320
BOX_H  = 160
FONT   = ("Helvetica", 24, "bold")
FONT_BTN = ("Helvetica", 22, "bold")

BG_COLOR      = "#fdfdf5"
CARD_BG       = "#ffffff"
CARD_BORDER   = "#d4d4d4"
FG_COLOR      = "#111111"
SHADOW_COLOR  = "#cccccc"

RISE_SPEED        = 80       # pixels per second
CARD_GAP          = 20       # vertical gap
BOTTOM_SPAWN_Y    = 0.85     # spawn at 85 % of screen height
SPAWN_COLS        = 2        # alternating columns

# ===============================================================


class LyricCard:
    """A floating lyric card drawn on the canvas."""

    def __init__(self, canvas, text, cx, y, card_w, card_h):
        self.canvas = canvas
        self.card_w = card_w
        self.card_h = card_h
        self.x = cx - card_w // 2
        self.y = float(y)
        self._full_text = text
        self._char_index = 0

        shadow_offset = 4

        # shadow
        self.shadow = canvas.create_rectangle(
            self.x + shadow_offset, self.y + shadow_offset,
            self.x + card_w + shadow_offset, self.y + card_h + shadow_offset,
            fill=SHADOW_COLOR, outline="", tags="card",
        )
        # card body
        self.card = canvas.create_rectangle(
            self.x, self.y, self.x + card_w, self.y + card_h,
            fill=CARD_BG, outline=CARD_BORDER, width=1, tags="card",
        )
        # text
        self.text_id = canvas.create_text(
            self.x + card_w // 2, self.y + card_h // 2,
            text="", font=FONT, fill=FG_COLOR,
            width=card_w - 40, anchor="center", tags="card",
        )
        self._typewriter()

    def _typewriter(self):
        if self._char_index <= len(self._full_text):
            shown = self._full_text[:self._char_index]
            self.canvas.itemconfig(self.text_id, text=shown)
            self._char_index += 1
            self.canvas.after(70, self._typewriter)

    def rise(self, dy):
        self.y -= dy
        sx, sy = 4, 4  # shadow offsets
        self.canvas.coords(self.shadow,
                           self.x + sx, self.y + sy,
                           self.x + self.card_w + sx, self.y + self.card_h + sy)
        self.canvas.coords(self.card,
                           self.x, self.y,
                           self.x + self.card_w, self.y + self.card_h)
        self.canvas.coords(self.text_id,
                           self.x + self.card_w // 2,
                           self.y + self.card_h // 2)

    def off_screen(self):
        return self.y + self.card_h < -10

    def destroy(self):
        self.canvas.delete(self.shadow)
        self.canvas.delete(self.card)
        self.canvas.delete(self.text_id)


class LyricFloatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyric Float")
        self.root.configure(bg=BG_COLOR)

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        ctrl_w, ctrl_h = 300, 200
        cx = (self.screen_w - ctrl_w) // 2
        cy = (self.screen_h - ctrl_h) // 2
        self.root.geometry(f"{ctrl_w}x{ctrl_h}+{cx}+{cy}")
        self.root.resizable(False, False)

        self.start_btn = tk.Button(
            root, text="Start", font=FONT_BTN, bg=BG_COLOR, fg=FG_COLOR,
            relief="flat", command=self.start,
        )
        self.start_btn.pack(expand=True, fill="both", padx=30, pady=30)

    # ---------- helpers ----------

    def _column_centers(self):
        margin = 60
        usable = self.screen_w - margin * 2
        spacing = usable / SPAWN_COLS
        return [margin + spacing * (i + 0.5) for i in range(SPAWN_COLS)]

    # ---------- start ----------

    def start(self):
        self.start_btn.pack_forget()

        # maximise window to cover the screen WITHOUT switching Spaces
        # (macOS fullscreen= new Space = user can't see the animation)
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.screen_w}x{self.screen_h}+0+0")
        self.root.lift()
        self.root.configure(bg=BG_COLOR)

        self.canvas = tk.Canvas(
            self.root, bg=BG_COLOR, highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # exit on click anywhere (overrideredirect blocks keyboard on macOS)
        self.canvas.bind("<Button-1>", lambda e: self.root.destroy())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.next_idx = 0
        self.cards = []
        self.col_index = 0
        self.start_time = time.time()
        self.last_time = self.start_time

        if HAS_AUDIO and AUDIO_FILE:
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(AUDIO_FILE)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Audio error: {e}")

        self._tick()

    # ---------- animation loop ----------

    def _tick(self):
        now = time.time()
        elapsed = now - self.start_time
        dt = now - self.last_time
        self.last_time = now

        cols = self._column_centers()

        # spawn due lyrics
        while self.next_idx < len(LYRICS) and LYRICS[self.next_idx][0] <= elapsed:
            _, text = LYRICS[self.next_idx]
            cx = cols[self.col_index % len(cols)]
            self.col_index += 1
            y = int(self.screen_h * BOTTOM_SPAWN_Y) - BOX_H // 2
            card = LyricCard(self.canvas, text, cx, y, BOX_W, BOX_H)
            self.cards.append(card)
            self.next_idx += 1

        # rise all
        dy = RISE_SPEED * dt
        for c in self.cards:
            c.rise(dy)

        # remove off-screen
        keep = []
        for c in self.cards:
            if c.off_screen():
                c.destroy()
            else:
                keep.append(c)
        self.cards = keep

        if self.next_idx < len(LYRICS) or self.cards:
            self.root.after(16, self._tick)
        else:
            # show end text
            self.canvas.create_text(
                self.screen_w // 2, self.screen_h // 2,
                text="— End —", font=FONT_BTN,
                fill=FG_COLOR, anchor="center",
            )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    LyricFloatApp(tk.Tk()).run()
