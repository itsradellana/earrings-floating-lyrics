"""
Floating Lyric Windows Animation — macOS Compatible
----------------------------------------------------
Every lyric line appears in its own popup window. All windows are the
same fixed size and font as the "Start" button window. Boxes never
disappear or fade. Each new box spawns at a random safe X position
near the bottom of the screen; as new boxes appear below, every
existing box shifts upward smoothly, creating a continuous rising
stack of lyric windows, synced to a song.

Tested on macOS, Windows, and Linux.

Requirements:
    pip install pygame   (optional, for audio playback)

Usage:
    1. Put your song file in the same folder (e.g. "song.mp3")
       and set AUDIO_FILE below. Leave "" to run without audio.
    2. Edit LYRICS: (start_time_seconds, "text")
    3. Run: python3 lyric_float.py
    4. Start your screen recorder, then click "Start"
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

BOX_W, BOX_H = 300, 250
FONT = ("Helvetica", 22, "bold")
BG_COLOR = "#fdfdf5"
FG_COLOR = "#111111"

RISE_SPEED = 90           # pixels per second every box moves upward
SPAWN_INTERVAL_MIN = 0    # not used directly; spawning follows LYRICS times
SAFE_EDGE_MARGIN = 220    # min distance from left/right screen edges
BOTTOM_SPAWN_OFFSET = 150 # how far above the bottom edge new boxes spawn

# ===============================================================


class LyricBox:
    """A single fixed-size lyric popup that rises forever and stays visible."""

    def __init__(self, master, text, x, y):
        self.master = master
        self.win = tk.Toplevel(master)
        self.win.overrideredirect(True)   # no title bar
        self.win.attributes("-topmost", True)
        self.win.configure(bg=BG_COLOR)
        self.win.geometry(f"{BOX_W}x{BOX_H}+{int(x)}+{int(y)}")
        self.win.resizable(False, False)

        self.full_text = text

        self.label = tk.Label(
            self.win,
            text="",
            font=FONT,
            bg=BG_COLOR,
            fg=FG_COLOR,
            wraplength=BOX_W - 30,
            justify="center",
        )
        self.label.pack(expand=True, fill="both", padx=15, pady=15)

        # macOS fix: force the window to render immediately
        self.win.update_idletasks()
        self.win.lift()

        self.typewriter_index = 0
        self._typewriter()

        self.x = x
        self.y = float(y)

    def rise(self, dy):
        self.y -= dy
        self.win.geometry(f"{BOX_W}x{BOX_H}+{int(self.x)}+{int(self.y)}")

    def is_offscreen(self):
        return self.y + BOX_H < -50

    def _typewriter(self):
        if self.typewriter_index <= len(self.full_text):
            self.label.config(text=self.full_text[:self.typewriter_index])
            self.typewriter_index += 1
            self.win.after(100, self._typewriter)


class LyricFloatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyric Float Controller")

        # Controller "Start" window uses the SAME fixed size/font
        # as every lyric box, per the same style.
        self.root.geometry(f"{BOX_W}x{BOX_H}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.start_btn = tk.Button(
            root, text="Start", font=FONT, bg=BG_COLOR, fg=FG_COLOR,
            relief="flat", command=self.start,
        )
        self.start_btn.pack(expand=True, fill="both", padx=15, pady=15)

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        self.next_lyric_idx = 0
        self.boxes = []
        self.last_frame_time = None
        self.current_side = "left"

    def random_safe_x(self):
        """Alternate between left and right positions."""
        center_x = self.screen_w // 2
        spacing = BOX_W + 60

        left_x = center_x - spacing
        right_x = center_x + 60

        if self.current_side == "left":
            self.current_side = "right"
            return left_x
        else:
            self.current_side = "left"
            return right_x

    def start(self):
        self.start_btn.pack_forget()

        # macOS fix: DON'T iconify the root window — it can hide all
        # overrideredirect Toplevels on macOS. Instead, shrink it to a
        # tiny size and move it off-screen / keep it as anchor.
        self.root.geometry("1x1+0+0")

        self.start_time = time.time()
        self.last_frame_time = self.start_time

        if HAS_AUDIO and AUDIO_FILE:
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(AUDIO_FILE)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Audio failed to load: {e}")

        self._tick()

    def _tick(self):
        now = time.time()
        elapsed = now - self.start_time
        dt = now - self.last_frame_time
        self.last_frame_time = now

        # Spawn any lyric windows whose time has come
        while (self.next_lyric_idx < len(LYRICS) and
               LYRICS[self.next_lyric_idx][0] <= elapsed):
            t, text = LYRICS[self.next_lyric_idx]
            x = self.random_safe_x()
            y = self.screen_h - BOX_H - BOTTOM_SPAWN_OFFSET
            box = LyricBox(self.root, text, x, y)
            self.boxes.append(box)
            self.next_lyric_idx += 1

        # Continuously rise ALL existing boxes upward
        dy = RISE_SPEED * dt
        for box in self.boxes:
            box.rise(dy)

        # Remove boxes that have scrolled fully off the top
        still_visible = []
        for box in self.boxes:
            if box.is_offscreen():
                try:
                    box.win.destroy()
                except tk.TclError:
                    pass
            else:
                still_visible.append(box)
        self.boxes = still_visible

        # Keep looping as long as there are lyrics left or boxes on screen
        if self.next_lyric_idx < len(LYRICS) or self.boxes:
            self.root.after(16, self._tick)  # ~60fps
        else:
            # Restore root window so user can close cleanly
            self.root.geometry(f"{BOX_W}x{BOX_H}")
            self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = LyricFloatApp(root)
    root.mainloop()
