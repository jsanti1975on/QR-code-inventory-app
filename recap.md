```Bash

Field Workflow (on tablet)

Open the web app (scan the QR on the right panel or use the LAN URL).

Small basket: pull all SMALL shirts, sort by color, and enter rows like:

GREEN, SMALL, 3

YELLOW, SMALL, 2

…repeat until the Small basket is done.

Medium basket: repeat for MEDIUM (e.g., GREEN, MEDIUM, 4, etc.).

Repeat for LARGE / XL / 1XL / 2XL / 3XL or Youth (YS/YM/YL) as needed.

When a shirt style/batch is complete, press Reset Inventory (bottom of the page) to empty data/ so the next batch doesn’t mix.

The app creates files like:

data/
├─ GREEN/
│  ├─ SMALL.txt   (e.g., “3”)
│  └─ MEDIUM.txt  (e.g., “4”)
└─ YELLOW/
   └─ SMALL.txt   (e.g., “2”)

End of Counting (on the VM)

Close the browser/tab on the tablet.

In the project root, run the report script:

./list_inventory.sh
```
