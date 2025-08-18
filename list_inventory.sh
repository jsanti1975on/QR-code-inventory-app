#!/bin/bash
DATA_DIR="data"

if [ ! -d "$DATA_DIR" ]; then
  echo "No inventory data found. Directory '$DATA_DIR' does not exist."
  exit 1
fi

echo "Inventory Summary:"
echo "------------------"

for color_dir in "$DATA_DIR"/*/; do
  [ -d "$color_dir" ] || continue
  color=$(basename "$color_dir")
  echo "Color: $color"
  for size_file in "$color_dir"/*.txt; do
    [ -f "$size_file" ] || continue
    size=$(basename "$size_file" .txt)
    qty=$(cat "$size_file")
    echo "  Size: $size - Quantity: $qty"
  done
  echo
done

