# earrings-floating-lyrics

A lyric visualization tool that turns song lyrics into a cinematic
floating animation. Each line appears as a white card and rises
upward in a zig-zag pattern — all on a transparent overlay so your
code editor stays visible behind it.

---

> "Biar lirik gak cuma terdengar, tapi terlihat."

## Run It

```bash
pip3 install pyglet
python3 lyric_float.py
```

Press **Esc** or click to exit.

## Make It Yours

Open `lyric_float.py`, edit the config section:

```python
AUDIO_FILE = "lagu.mp3"   # or "" to skip

LYRICS = [
    (0.0,  "First line"),
    (2.8,  "Second line"),
    ...
]

CARD_W, CARD_H = 500, 240   # card size
RISE_SPEED = 145             # scroll speed
SPAWN_COLS = 2               # 1 = centred, 2 = zig-zag
BOTTOM_SPAWN_Y = 0.20        # spawn height
```

## Requirements

| Dependency | Notes |
|-----------|-------|
| Python 3.9+ | Built-in |
| pyglet | `pip3 install pyglet` |
| Audio | Uses `afplay` (macOS), no extra install |

## License

MIT — [LICENSE](LICENSE)
