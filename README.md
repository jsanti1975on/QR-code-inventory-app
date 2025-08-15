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

## After venv and update and intall of modules

```Bash
wget this repo down | image shows running the bash script and a count of 8 small green shirts.
```

<img width="754" height="598" alt="github-image-815" src="https://github.com/user-attachments/assets/3d72e3ed-90f9-4b9e-9b48-abe320e5761c" />



<img width="754" height="598" alt="github-image-815" src="https://github.com/user-attachments/assets/86ebfd93-40ef-4e7b-9113-76a117f6f110" />





