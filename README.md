# earrings-floating-lyrics 

A lyric visualization tool that renders song lyrics as animated
floating cards on a transparent overlay window. Designed for
screen recording, lyric video edits, and social media content —
run it from your terminal, hit record, and the animation plays
on top of your desktop or code editor.

---

## Features

- **Transparent Overlay Window** — Built with Pyglet's native Cocoa
  backend. The animation renders on a borderless overlay window so
  your desktop, code editor, or any application behind it remains
  fully visible.
- **Floating Card Animation** — Each lyric line spawns as a solid white
  card that rises upward smoothly. Cards alternate between left and
  right positions in a zig-zag pattern for dynamic visual flow.
- **Typewriter Text Reveal** — Text renders character-by-character
  with a smooth, cinematic pacing that matches the rhythm of the song.
- **Timestamp-Based Sync** — Lyric cards appear at exact configurable
  timestamps. Drop in any `.mp3` or `.wav` file, set the seconds in
  the `LYRICS` list, and the animation stays locked to the audio.
- **Zero Audio Dependencies** — On macOS, audio playback uses the
  built-in `afplay` command. No pygame, no ffmpeg, no extra installs.
  Cross-platform fallback uses the system default player.
- **Fully Customizable** — Card dimensions, font size, text and
  background colors (RGBA), rise speed, spawn height, and column
  layout are all exposed as variables at the top of the script.
  Change them without touching any logic.

## Quick Start

```bash
git clone https://github.com/itsradellana/earrings-floating-lyrics.git
cd earrings-floating-lyrics
pip3 install pyglet
python3 lyric_float.py
```

Cards start floating immediately on a transparent overlay.
Press **Escape** or click anywhere to exit.

## How It Works

1. **Pyglet** creates a transparent overlay window sized to the
   primary display.
2. A timed loop spawns `LyricCard` objects according to the `LYRICS`
   timestamp array. Each card contains a bordered rectangle (the
   "card" background) and a text label.
3. On every frame (~60 FPS), all active cards shift upward by
   `RISE_SPEED * delta_time` pixels. Cards that scroll past the
   top of the screen are removed.
4. A separate timer (~15 FPS) updates the typewriter effect —
   each card's text is progressively revealed one character at
   a time.
5. If an `AUDIO_FILE` is set, the script spawns the native audio
   player as a subprocess at startup.

## Configuration

Open `lyric_float.py` and edit the section at the top:

```python
# Audio
AUDIO_FILE = "song.mp3"           # path to audio file, or "" to disable

# Lyrics (timestamp in seconds, text)
LYRICS = [
    (0.0,  "Her love is in your head"),
    (2.8,  "You lost your earrings in her bed"),
    (5.6,  "You couldn't tell her that you lost 'em"),
    (8.4,  "'Cause you're scared and you're not talking"),
    (11.2, "So you think of what to say"),
    (14.0, "Then save it for another day"),
]

# Visual
CARD_W, CARD_H = 500, 240        # card width and height in pixels
FONT_SIZE = 38                    # text size
TEXT_COLOR   = (30, 30, 30, 255) # dark text (R, G, B, Alpha)
CARD_BG      = (255, 255, 255, 255)  # solid white card
CARD_BORDER  = (200, 200, 200, 255)  # grey border

# Animation
RISE_SPEED     = 145              # pixels per second
SPAWN_COLS     = 2                # 1 = single centred, 2 = zig-zag
BOTTOM_SPAWN_Y = 0.20            # spawn height (0.0 = bottom, 1.0 = top)
```

## Project Structure

```
earrings-floating-lyrics/
  lyric_float.py    # main script — everything in one file
  README.md
  LICENSE
```

## Compatibility

| Platform | Renderer            | Audio              |
|----------|---------------------|--------------------|
| macOS    | Pyglet (Cocoa)      | afplay (built-in)  |
| Windows  | Pyglet (Win32)      | Default player     |
| Linux    | Pyglet (X11/Wayland)| xdg-open           |

## Requirements

- **Python** 3.9 or later
- **pyglet** — install via pip:

  ```bash
  pip3 install pyglet
  ```

## License

MIT — see [LICENSE](LICENSE).
