# Tested at lunch and corrected below 

```bash
#!/usr/bin/env bash
set -euo pipefail

# Root of the app; default DATA_DIR is ./data unless you pass one in
ROOT="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="${1:-$ROOT/data}"

# Preferred size order. We'll include only those that actually exist.
KNOWN_ORDER=(YS YM YL SMALL MEDIUM LARGE XL 2XL 3XL)

# Discover which sizes exist across all colors
declare -A seen
if [[ -d "$DATA_DIR" ]]; then
  while IFS= read -r -d '' f; do
    bn="$(basename "$f")"        # e.g. SMALL.txt
    sz="${bn%.*}"                # -> SMALL
    seen["$sz"]=1
  done < <(find "$DATA_DIR" -mindepth 2 -maxdepth 2 -type f -name '*.txt' -print0)
fi

# Build the columns we will print, in preferred order; fall back to SMALL
cols=()
for s in "${KNOWN_ORDER[@]}"; do
  if [[ ${seen[$s]+x} ]]; then cols+=("$s"); fi
done
if ((${#cols[@]} == 0)); then cols=(SMALL); fi

# Header (CSV so you can redirect to a file)
printf "COLOR"
for s in "${cols[@]}"; do printf ",%s" "$s"; done
printf ",ROW_TTL\n"

# No data dir? Print nothing else and exit successfully
if [[ ! -d "$DATA_DIR" ]]; then
  echo "data directory not found: $DATA_DIR" >&2
  exit 0
fi

shopt -s nullglob
for cdir in "$DATA_DIR"/*/; do
  color="$(basename "$cdir")"
  row_total=0
  printf "%s" "$color"
  for s in "${cols[@]}"; do
    val=0
    f="$cdir/$s.txt"
    if [[ -f "$f" ]]; then
      # Read digits only; treat blanks as 0
      v="$(tr -cd '0-9' < "$f")"
      [[ -n "$v" ]] && val="$v"
    fi
    printf ",%s" "$val"
    (( row_total += val ))
  done
  printf ",%s\n" "$row_total"
done
```

# Review First additional script to Add a “totals row” (per-size + grand total)

> Append this block to the end of list_inventory.sh right after the color loop:

```bash
# ---- optional totals row ----
# compute per-size totals and a grand total across all colors
declare -A size_tot=()
grand=0
while IFS=, read -r color "${cols[@]/#/v_}" row_ttl; do
  # skip header line
  [[ "$color" == "COLOR" ]] && continue
  idx=0
  for s in "${cols[@]}"; do
    val="${!((idx+2))}"   # v_* vars are positional; use indirect
    : "${val:=0}"
    (( size_tot["$s"] += val ))
    (( grand += val ))
    ((idx++))
  done
done < <(./list_inventory.sh)

# print totals row (label "TOTALS")
printf "TOTALS"
for s in "${cols[@]}"; do printf ",%s" "${size_tot[$s]:-0}"; done
printf ",%s\n" "$grand"
```
