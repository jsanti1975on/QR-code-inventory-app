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






};
</script>
