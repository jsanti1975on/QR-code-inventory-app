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







<img width="1920" height="543" alt="inventory-app" src="https://github.com/user-attachments/assets/a2f618d5-be8d-4216-9f7a-458836414047" />
