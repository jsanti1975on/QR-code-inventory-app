# Simple Flask Inventory App

A minimal inventory tracking system built with **Flask** and plain filesystem storage.  
Each inventory item is stored as a text file in `data/COLOR/SIZE.txt` with the quantity inside.  
Includes a helper Bash script to print a clean inventory summary.

---

## Features
- **Add Inventory** via a simple HTML form
- **Filesystem Storage** — no database required
- **Easy Backup** — inventory is stored in plain text files
- **Bash Summary Script** (`list_inventory.sh`) to view inventory in the terminal

---

## 🛠 Project Structure

```Bash
inventory-app/
├── app.py # Flask web app
├── requirements.txt # Python dependencies
├── templates/
│ └── index.html # Input form
├── data/ # Created automatically to store inventory
└── list_inventory.sh # Bash script to print inventory
```

```Bash
Seed a record from the VM:
curl -X POST -d "color=GREEN&size=SMALL&quantity=8" http://127.0.0.1:5000
```

```Bash
Print the inventory:
./list_inventory.sh
```


```Bash
Keep it running in the background (optional)
nohup bash -c "source venv/bin/activate && python app.py" >/tmp/inventory.log 2>&1 &
```

## After installing the virtual environment, update and install of modules

```Bash
wget this repo down | image shows running the bash script and a count of 8 small green shirts.
```

# 1. Download as zip
wget -O QR-code-inventory-app.zip https://github.com/jsanti1975on/QR-code-inventory-app/archive/refs/heads/main.zip

# 2. Unzip
unzip inventory-app.zip

# 3. Move into folder (GitHub names it inventory-app-main by default)

```Bash
mv inventory-app-main inventory-app
cd inventory-app
```
<img width="1072" height="741" alt="QR-inventory-app-image" src="https://github.com/user-attachments/assets/6b84b4e5-8998-40a6-971d-feceb50f1559" />

<img width="754" height="598" alt="github-image-815" src="https://github.com/user-attachments/assets/86ebfd93-40ef-4e7b-9113-76a117f6f110" />





