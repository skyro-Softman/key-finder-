import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Simulated device state (kept in memory; run with a single worker)
state = {
    "alarm": False,
    "status": "DEVICE READY",
    "color": "#2ECC71",
    "message": "",
}


def reply():
    return jsonify(state)


@app.get("/api/status")
def status():
    return reply()


@app.post("/api/find")
def find_key():
    state.update(
        alarm=True,
        status="SEARCHING FOR KEY",
        color="#F1C40F",
        message="Key search activated. The simulated alarm is ON.",
    )
    return reply()


@app.post("/api/stop")
def stop_alarm():
    state.update(
        alarm=False,
        status="DEVICE READY",
        color="#2ECC71",
        message="Alarm successfully stopped.",
    )
    return reply()


@app.post("/api/test")
def test_device():
    state.update(
        status="DEVICE OPERATIONAL",
        color="#3498DB",
        message="Device test successful. All simulated components are working.",
    )
    return reply()


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Smart Key Finder</title>
<style>
  body { margin:0; background:#17202A; color:#fff; font-family:Arial,sans-serif;
         text-align:center; padding:20px; min-height:100vh; box-sizing:border-box; }
  h1 { margin:10px 0 0; font-size:26px; }
  .by { color:#AAB7B8; margin:4px 0; }
  .sub { color:#AAB7B8; font-size:13px; }
  .device { background:#2C3E50; width:220px; height:130px; margin:22px auto;
            display:flex; align-items:center; justify-content:center; font-size:60px;
            border-radius:8px; }
  .ringing { animation: shake .4s infinite; }
  @keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-6px)} 75%{transform:translateX(6px)} }
  #status { font-weight:bold; font-size:17px; }
  #alarm { margin:10px 0; }
  #msg { color:#AAB7B8; font-size:14px; min-height:40px; }
  button { display:block; width:100%; max-width:280px; margin:10px auto; padding:15px;
           border:0; border-radius:4px; color:#fff; font-size:16px; font-weight:bold; }
  .find{background:#E67E22} .stop{background:#C0392B} .test{background:#2980B9}
  footer { color:#85929E; font-size:11px; margin-top:24px; }
</style>
</head>
<body>
  <h1>Smart Key Finder</h1>
  <div class="by">by Ugwu Emmanuel Onyeka</div>
  <div class="sub">Electronic Key Tracking System</div>

  <div class="device" id="device">🔑</div>
  <div id="status">● DEVICE READY</div>
  <div id="alarm">Alarm: OFF</div>
  <div id="msg"></div>

  <button class="find" onclick="act('find')">FIND KEY</button>
  <button class="stop" onclick="act('stop')">STOP ALARM</button>
  <button class="test" onclick="act('test')">TEST DEVICE</button>

  <footer>EMBEDDED SYSTEMS DEVELOPMENT ASSIGNMENT<br>BY UGWU EMMANUEL | 2026</footer>

<script>
  let ctx = null, ringing = false;

  function beep() {
    if (!ctx) return;
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.value = 880; g.gain.value = 0.15;
    o.connect(g); g.connect(ctx.destination);
    o.start(); o.stop(ctx.currentTime + 0.3);
    if (navigator.vibrate) navigator.vibrate(300);
  }

  function render(s) {
    const st = document.getElementById('status');
    st.textContent = '● ' + s.status; st.style.color = s.color;
    const al = document.getElementById('alarm');
    al.textContent = 'Alarm: ' + (s.alarm ? 'ACTIVE' : 'OFF');
    al.style.color = s.alarm ? '#E74C3C' : '#fff';
    document.getElementById('msg').textContent = s.message;
    document.getElementById('device').classList.toggle('ringing', s.alarm);
    ringing = s.alarm;
  }

  async function act(name) {
    // Audio must be unlocked by a tap
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    const r = await fetch('/api/' + name, { method: 'POST' });
    render(await r.json());
  }

  async function poll() {
    try { render(await (await fetch('/api/status')).json()); } catch (e) {}
  }

  setInterval(() => { if (ringing) beep(); }, 800);
  setInterval(poll, 2000);
  poll();
</script>
</body>
</html>"""


@app.get("/")
def home():
    return render_template_string(PAGE)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
