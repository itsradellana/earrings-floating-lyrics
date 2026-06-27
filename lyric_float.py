"""
Floating Lyric Animation — HTML / Browser (Zero Dependencies)
--------------------------------------------------------------
No tkinter, no pygame — just a local web server and your browser.
Open fullscreen (F11 / Cmd+Ctrl+F), click Start, then the cards
will start rising immediately.

Usage:
    1. Edit LYRICS and AUDIO_FILE below.
    2. Run: python3 lyric_float.py
    3. Open the URL shown in your browser.
    4. Go FULLSCREEN (Cmd+Ctrl+F), click Start.
    5. Press Escape or click background to exit.
"""

import http.server
import json
import os
import webbrowser

# ====================== EDIT THIS SECTION ======================

AUDIO_FILE = ""  # path to .mp3 / .wav, or "" to disable
# (set relative to this script's folder, e.g. "song.mp3")

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

BOX_W  = 320
BOX_H  = 160
FONT_SIZE = "24px"
BG_COLOR   = "#fdfdf5"
CARD_BG    = "#ffffff"
CARD_BORDER = "#d4d4d4"
TEXT_COLOR  = "#111111"

RISE_SPEED = 80
SPAWN_COLS = 2
PORT = 8765

# ===============================================================

HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lyric Float</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:C_BG;overflow:hidden;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;width:100vw;height:100vh;user-select:none;-webkit-user-select:none}
#s{position:fixed;z-index:1000;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:C_BG;cursor:pointer}
#s button{font:bold 26px "Helvetica Neue",Helvetica,sans-serif;padding:20px 64px;border:1px solid C_BORDER;background:C_CARD;color:C_TEXT;cursor:pointer;box-shadow:0 4px 20px rgba(0,0,0,0.1)}
#s button:hover{background:#f0f0f0}
.card{
  position:absolute;display:flex;align-items:center;justify-content:center;
  text-align:center;background:C_CARD;border:1px solid C_BORDER;
  box-shadow:0 4px 20px rgba(0,0,0,0.1);color:C_TEXT;
  font-weight:bold;font-size:C_FONT;line-height:1.4;
  padding:20px;word-wrap:break-word;pointer-events:none
}
</style>
</head>
<body>
<div id="s"><button>Start</button></div>

<script>
var LYRICS=LYRICS_JSON;
var BOX_W=CARD_W;var BOX_H=CARD_H;
var RISE=RISE_SPEED;var COLS=SPAWN_COLS;
var AF=AUDIO_FILE_JSON;
var cards=[],ni=0,ci=0,st=null,lt=null,rid=null,aud=null;

function cc(){
  var w=innerWidth,m=60,u=w-m*2,s=u/COLS;
  for(var i=0,r=[];i<COLS;i++)r.push(m+s*(i+.5));
  return r;
}

function mk(t,cx,y){
  var e=document.createElement('div');
  e.className='card';
  e.style.width=BOX_W+'px';
  e.style.height=BOX_H+'px';
  e.style.left=(cx-BOX_W/2)+'px';
  e.style.top=y+'px';
  e._y=y;e._t=t;e._i=0;
  document.body.appendChild(e);
  tw(e);
  return e;
}

function tw(e){
  if(e._i<=e._t.length){
    e.textContent=e._t.slice(0,e._i);
    e._i++;
    setTimeout(function(){tw(e)},50);
  }
}

function tick(ts){
  if(st===null)st=ts;
  var el=(ts-st)/1000;
  if(lt===null)lt=ts;
  var dt=(ts-lt)/1000;lt=ts;
  var cols=cc();
  while(ni<LYRICS.length&&LYRICS[ni][0]<=el){
    var cx=cols[ci%cols.length];ci++;
    var y=innerHeight*.85-BOX_H/2;
    cards.push(mk(LYRICS[ni][1],cx,y));
    ni++;
  }
  var dy=RISE*dt;
  for(var i=0;i<cards.length;i++){
    cards[i]._y-=dy;
    cards[i].style.top=cards[i]._y+'px';
  }
  cards=cards.filter(function(c){
    if(c._y+BOX_H<-10){c.remove();return false}
    return true;
  });
  if(ni<LYRICS.length||cards.length)rid=requestAnimationFrame(tick);
}

document.getElementById('s').addEventListener('click',function(){
  document.getElementById('s').style.display='none';
  if(AF){aud=new Audio(AF);aud.play().catch(function(){})}
  rid=requestAnimationFrame(tick);
});

document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
document.addEventListener('click',function(e){
  if(e.target===document.body||e.target===document.documentElement)close();
});
</script>
</body>
</html>"""


def build():
    return (HTML
            .replace("LYRICS_JSON", json.dumps(LYRICS))
            .replace("CARD_W", str(BOX_W))
            .replace("CARD_H", str(BOX_H))
            .replace("RISE_SPEED", str(RISE_SPEED))
            .replace("SPAWN_COLS", str(SPAWN_COLS))
            .replace("AUDIO_FILE_JSON", json.dumps(AUDIO_FILE))
            .replace("C_BG", BG_COLOR)
            .replace("C_CARD", CARD_BG)
            .replace("C_BORDER", CARD_BORDER)
            .replace("C_TEXT", TEXT_COLOR)
            .replace("C_FONT", FONT_SIZE))


PAGE = build()


class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PAGE.encode("utf-8"))
        elif AUDIO_FILE and self.path.endswith(os.path.basename(AUDIO_FILE)):
            fp = os.path.join(os.path.dirname(__file__), AUDIO_FILE)
            if os.path.isfile(fp):
                self.send_response(200)
                self.send_header("Content-Type",
                                 "audio/mpeg" if fp.endswith(".mp3") else "audio/wav")
                self.end_headers()
                with open(fp, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        pass


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    srv = http.server.HTTPServer(("127.0.0.1", PORT), H)
    url = f"http://127.0.0.1:{PORT}"
    print(f"\n  Open: {url}")
    print(f"  Go FULLSCREEN (Cmd+Ctrl+F) → click Start")
    print(f"  Esc or click to exit\n")
    webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("Done.")
        srv.shutdown()


if __name__ == "__main__":
    main()
