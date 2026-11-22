import json, os, threading
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, request, send_from_directory, abort, jsonify

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE, "events.jsonl")
ADMIN_KEY = os.environ.get("ADMIN_KEY", "")
IST = ZoneInfo("Asia/Kolkata")

LABELS = {
    "page_open": "👀 Priyanka ne page khola",
    "screen_1": "💗 'Kholo' dabaya",
    "haan_try": "😤 'Haan, hoon' ke paas gayi",
    "screen_2": "🥹 'Nahi' dabaya, letter khula",
    "letter_read": "💌 Poora letter padh liya",
    "screen_3": "❤️ Maafi meter khola",
    "meter_full": "🥰 Maafi meter 100% ho gaya",
    "screen_4": "🎁 Peace offerings page par pahunchi",
    "offer": "🎁 Claim kiya",
    "screen_5": "📜 Treaty page par pahunchi",
    "signed": "✍️ Treaty SIGN kar di! SEALED 🎉",
    "hug_pressed": "🤗 Aakhri 'tight hug' dabaya",
}
OFFERS = {"flower": "🌷 Fresh flowers", "chai": "☕ Chai / coffee date",
          "coffee": "☕ Chai / coffee date", "chocolate": "🍫 Chocolate + hug"}
events = []
lock = threading.Lock()


def load():
    if os.path.exists(LOG):
        for line in open(LOG, encoding="utf-8"):
            try:
                events.append(json.loads(line))
            except ValueError:
                pass


@app.get("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.post("/track")
def track():
    d = request.get_json(silent=True) or {}
    ev = str(d.get("event", ""))
    if ev not in LABELS:
        return jsonify(ok=False), 400
    detail = ""
    if ev == "offer":
        raw = str(d.get("detail", "")).lower()
        detail = next((v for k, v in OFFERS.items() if k in raw), "")
    now = datetime.now(IST)
    rec = {"t": now.strftime("%d %b %I:%M:%S %p"), "event": ev, "detail": detail}
    with lock:
        events.append(rec)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return jsonify(ok=True)


@app.get("/admin")
def admin():
    if not ADMIN_KEY or request.args.get("key") != ADMIN_KEY:
        abort(404)
    with lock:
        evs = list(events)
    claimed = sorted({e["detail"] for e in evs if e["event"] == "offer" and e["detail"]})
    signed = any(e["event"] == "signed" for e in evs)
    rows = "".join(
        f"<tr><td>{e['t']}</td><td>{LABELS[e['event']]} {e['detail']}</td></tr>"
        for e in reversed(evs))
    return f"""<meta name=viewport content="width=device-width,initial-scale=1">
<body style="font-family:system-ui;max-width:640px;margin:20px auto;padding:0 12px">
<h2>Priyanka ne kya kiya 💗</h2>
<p><b>Claim kiye:</b> {', '.join(claimed) or 'abhi kuch nahi'}</p>
<p><b>Treaty sign:</b> {'✅ haan' if signed else '❌ abhi nahi'}</p>
<table cellpadding=6 border=1 style="border-collapse:collapse;width:100%">{rows}</table>"""


load()
