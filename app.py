# cat > app.py <<'EOF'
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
DATA_DIR = 'data'

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
        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
# EOF


