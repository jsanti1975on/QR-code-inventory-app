from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import os
import io
import qrcode
import netifaces
import subprocess

app = Flask(__name__)

DATA_DIR = "data"
PORT = 5000  # keep in sync with app.run()

def get_lan_ip() -> str:
    """
    Find a non-loopback IPv4 address for this machine.
    Preference: private ranges (10/8, 172.16/12, 192.168/16).
    Fallback to 127.0.0.1 if nothing else found.
    """
    private_prefixes = (
        "10.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.",
        "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.",
        "172.28.", "172.29.", "172.30.", "172.31.", "192.168."
    )
    try:
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET, [])
            for a in addrs:
                ip = a.get("addr")
                if not ip or ip.startswith("127."):
                    continue
                if ip.startswith(private_prefixes):
                    return ip
        # If no private IP found, return first non-loopback IPv4
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET, [])
            for a in addrs:
                ip = a.get("addr")
                if ip and not ip.startswith("127."):
                    return ip
    except Exception:
        pass
    return "127.0.0.1"

def get_lan_url() -> str:
    return f"http://{get_lan_ip()}:{PORT}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        color = request.form["color"].strip().upper()
        size = request.form["size"].strip().upper()
        quantity = request.form["quantity"].strip()

        color_dir = os.path.join(DATA_DIR, color)
        os.makedirs(color_dir, exist_ok=True)
        size_file = os.path.join(color_dir, f"{size}.txt")
        with open(size_file, "w") as f:
            f.write(quantity)
        return redirect(url_for("index"))

    return render_template("index.html", lan_url=get_lan_url())

@app.route("/qr.png")
def qr_png():
    """
    Generate a PNG QR code for the LAN URL on the fly.
    We disable caching so updated IPs don’t get stuck in the browser cache.
    """
    url = get_lan_url()
    qr = qrcode.QRCode(
        version=None,  # auto size
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,    # ~original visual size
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    resp = make_response(send_file(buf, mimetype="image/png"))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return resp

# ---- NEW: reset endpoint for the button ----
@app.route("/api/reset", methods=["POST"])
def api_reset():
    """
    Run reset_inventory.sh and return its stdout.
    Script should live at project root and be executable.
    """
    script_path = os.path.join(os.path.dirname(__file__), "reset_inventory.sh")
    if not os.path.isfile(script_path):
        return {"ok": False, "error": "reset_inventory.sh not found"}, 500
    try:
        result = subprocess.run(
            ["/bin/bash", script_path],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            timeout=20
        )
        if result.returncode != 0:
            return {"ok": False, "stderr": result.stderr}, 500
        return {"ok": True, "stdout": result.stdout}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Timeout"}, 504

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
