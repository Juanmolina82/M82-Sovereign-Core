import subprocess, urllib.parse, sys, re, glob

def get_activity():
    out = subprocess.getoutput("cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER com.mmolina82.app")
    for line in out.splitlines():
        if "com.mmolina82.app/" in line:
            return line.strip()
    return "com.mmolina82.app/.MainActivity"

def send_m82_alert(title, body, desk="M82 Breaking", nid="m82_live"):
    act = get_activity()
    q = urllib.parse.quote(body[:45])
    d = urllib.parse.quote(desk)
    url = f"http://127.0.0.1:8282/?desk={d}&q={q}"
    action_cmd = f"am start --user 0 -n {act} -a android.intent.action.VIEW -d '{url}' || monkey -p com.mmolina82.app -c android.intent.category.LAUNCHER 1"
    subprocess.run([
        "termux-notification",
        "--id", nid,
        "--title", title,
        "--content", body,
        "--priority", "high",
        "--action", action_cmd
    ], check=False)

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "🔴 M82 BREAKING • MACRO & GEOPOLITICS"
    b = sys.argv[2] if len(sys.argv) > 2 else "M82 Quantum Desk Live Dispatch"
    d = sys.argv[3] if len(sys.argv) > 3 else "M82 Sovereign Wire"
    send_m82_alert(t, b, d)
    print("M82_ALERT_DISPATCHED_TO_APP_OK")
