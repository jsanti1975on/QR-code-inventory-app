# Testing

> Wire Reset Inventory button so it archives to permanent_archive/ first,
> then clears data/ inside Flask (no external shell), so permissions are simpler and it works BYOO VM/tablet.

# Changed app.py

# Drop in index.html

```html
<form id="resetForm" onsubmit="return false;">
  <button type="button" id="resetBtn">Reset Inventory (Archive → Clear)</button>
  <span id="resetMsg" style="margin-left:8px; font-size:14px;"></span>
</form>

<script>
document.getElementById('resetBtn').onclick = async () => {
  const msg = document.getElementById('resetMsg');
  msg.textContent = "Archiving and clearing…";
  try {
    const res = await fetch("/reset", { method: "POST" });
    const j = await res.json();
    if (j.ok) {
      msg.textContent = `Saved: ${j.archived} — data cleared.`;
    } else {
      msg.textContent = `Error: ${j.error || 'Unknown'}`;
    }
  } catch (e) {
    msg.textContent = "Request failed: " + e;
  }
};
</script>
```

# (Optional) Add an archive browser => drop in app.py

```Python
from flask import send_from_directory

@app.route("/archive")
def list_archive():
    ensure_dirs()
    files = sorted((fn for fn in os.listdir(ARCHIVE_DIR) if fn.endswith(".csv")), reverse=True)
    html = ["<h3>Archived Inventory CSVs</h3><ul>"]
    for fn in files:
        html.append(f'<li><a href="/archive/{fn}">{fn}</a></li>')
    html.append("</ul>")
    return "\n".join(html)

@app.route("/archive/<path:fname>")
def get_archive_file(fname):
    ensure_dirs()
    return send_from_directory(ARCHIVE_DIR, fname, as_attachment=True)
```

# Update: app.py drop in

```Python
# --- imports (add if not present) ---
import csv, shutil, time
from flask import jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARCHIVE_DIR = os.path.join(BASE_DIR, "permanent_archive")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

def archive_counts_to_csv() -> str:
    """
    Walk data/<COLOR>/<SIZE>.txt and write
    permanent_archive/inventory_YYYY-mm-dd_HH-MM-SS.csv
    Returns the CSV path (absolute).
    """
    ensure_dirs()
    ts = time.strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = os.path.join(ARCHIVE_DIR, f"inventory_{ts}.csv")

    # collect rows
    rows = []
    if os.path.isdir(DATA_DIR):
        for color in sorted(os.listdir(DATA_DIR)):
            cdir = os.path.join(DATA_DIR, color)
            if not os.path.isdir(cdir):
                continue
            for fn in sorted(os.listdir(cdir)):
                if not fn.lower().endswith(".txt"):
                    continue
                size = os.path.splitext(fn)[0]
                fpath = os.path.join(cdir, fn)
                try:
                    with open(fpath, "r") as f:
                        qty_txt = (f.read() or "").strip()
                    qty = int(qty_txt) if qty_txt else 0
                except Exception:
                    qty = 0
                rows.append((color, size, qty))

    # write CSV (always include header)
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Color", "Size", "Quantity"])
        for color, size, qty in rows:
            w.writerow([color, size, qty])
    return csv_path

def clear_data_dir():
    """Empties data/ contents but keeps the folder."""
    ensure_dirs()
    for name in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, name)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception:
            # best-effort; keep going
            pass

# ==== Reset endpoint: archive THEN clear ====
@app.route("/reset", methods=["POST"])
def reset():
    ensure_dirs()
    csv_path = archive_counts_to_csv()
    clear_data_dir()
    rel_csv = os.path.relpath(csv_path, BASE_DIR)
    return jsonify({"ok": True, "archived": rel_csv})
```





