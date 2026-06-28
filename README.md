# earrings-floating-lyrics

A lyric visualization tool that renders song lyrics as animated
floating cards on a transparent overlay window — ideal for screen
recording and social media lyric edits.

---

## Features

- **Transparent Overlay** — Rendered on a native borderless overlay window
  so your desktop, code editor, or any background remains visible.
- **Floating Card Animation** — Each lyric line appears as a white card
  and rises upward smoothly in a zig-zag alternating pattern.
- **Typewriter Text Effect** — Text types out character-by-character
  for a cinematic reveal.
- **Audio-Synced Timing** — Lyric cards spawn at configurable timestamps.
  Drop any audio file and the animation syncs automatically.
- **Fully Configurable** — Card size, font, colors, rise speed, spawn
  position, column layout — all exposed as variables at the top of
  the script.

## Installation

```bash
git clone https://github.com/itsradellana/earrings-floating-lyrics.git
cd earrings-floating-lyrics
pip3 install pyglet
```

## Usage

```bash
python3 lyric_float.py
```

Cards begin floating immediately. Press **Escape** or click to exit.

> On macOS, audio playback uses the built-in `afplay` — no additional
> dependencies required. On Windows and Linux, the default system
> player is used.

## Configuration

Edit the variables at the top of `lyric_float.py`:

```python
AUDIO_FILE = "lagu.mp3"          # path to audio, or "" to disable

LYRICS = [
    (0.0,  "First line"),
    (2.8,  "Second line"),
    (5.6,  "Third line"),
]

CARD_W, CARD_H = 500, 240        # card dimensions
FONT_SIZE = 38                    # text size
TEXT_COLOR  = (30, 30, 30, 255)  # dark text (R, G, B, A)
CARD_BG     = (255, 255, 255, 255)  # solid white background

RISE_SPEED    = 145               # pixels per second
SPAWN_COLS    = 2                 # 1 = single centred, 2 = zig-zag
BOTTOM_SPAWN_Y = 0.20            # spawn height (0 = bottom, 1 = top)
```

## Compatibility

| Platform | Renderer | Audio |
|----------|----------|-------|
| macOS    | Pyglet (native Cocoa) | afplay (built-in) |
| Windows  | Pyglet (native Win32) | Default player |
| Linux    | Pyglet (X11/Wayland) | xdg-open |

## Requirements

- **Python** 3.9+
- **pyglet** — `pip3 install pyglet`

## License

MIT — see [LICENSE](LICENSE).
