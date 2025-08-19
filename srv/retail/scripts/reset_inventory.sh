#!/bin/bash
# reset_inventory.sh
# Empties the data directory but keeps it in place for reuse

DATA_DIR="data"

if [ -d "$DATA_DIR" ]; then
  rm -rf "$DATA_DIR"/*
  echo "Inventory reset: '$DATA_DIR' has been emptied."
else
  echo "No data directory found. Creating..."
  mkdir -p "$DATA_DIR"
  echo "New '$DATA_DIR' directory created."
fi

