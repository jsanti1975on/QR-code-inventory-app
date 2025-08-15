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
<img width="1920" height="543" alt="inventory-app" src="https://github.com/user-attachments/assets/a2f618d5-be8d-4216-9f7a-458836414047" />
