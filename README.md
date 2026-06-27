# 🎵 earrings-floating-lyrics

A lyric visualization tool that turns song lyrics into a cinematic
floating-window animation — each line appears in its own popup and
drifts upward in sync with the music. Built for screen recording and
sharing on social media.

---

> "Biar lirik gak cuma terdengar, tapi terlihat."

## ✨ What It Does

- **Multi-Window Float Stack** — Every lyric line spawns as its own
  borderless window. As new lines appear at the bottom, existing ones
  rise upward smoothly. Nothing fades, nothing disappears — a clean,
  continuous visual flow.
- **Typewriter Reveal** — Text types out character-by-character on each
  window for that cinematic, beat-matched feel.
- **Audio-Synced Timing** — Lyric windows spawn at exact timestamps.
  Drop any `.mp3` or `.wav`, set the timings, and hit Start.
- **Dynamic Layout** — Boxes alternate between left and right positions,
  keeping the composition balanced without manual placement.
- **Fully Customizable** — Font, colors, box size, rise speed, spawn
  position, number of columns — all exposed as variables at the top of
  the script. No digging through code.

## 🚀 Get Started

```bash
git clone https://github.com/itsradellana/earrings-floating-lyrics.git
cd earrings-floating-lyrics

# For audio sync (optional)
pip install pygame

# Run it
python3 lyric_float.py
```

Click **Start**, open your screen recorder, and let it play.

Press **Escape** or click anywhere to exit.

> On Linux, you may need: `sudo apt install python3-tk`

## ⚡ Make It Your Own

Open `lyric_float.py` and edit the section at the top:

```python
AUDIO_FILE = "lagu-kamu.mp3"      # or "" to skip audio

LYRICS = [
    (0.0,  "First line"),
    (4.2,  "Second line"),
    (8.1,  "Keep going..."),
]

BOX_W, BOX_H = 300, 250           # window size
RISE_SPEED = 90                   # pixels per second
FONT = ("Helvetica", 22, "bold")
BG_COLOR = "#fdfdf5"              # background
FG_COLOR = "#111111"              # text
```

## 🖥️ Compatibility

| Platform | Status |
|----------|--------|
| macOS    | Fully supported |
| Windows  | Works out of the box |
| Linux    | Needs `python3-tk` |

## ⚖️ License

MIT — do whatever you want. [LICENSE](LICENSE)
