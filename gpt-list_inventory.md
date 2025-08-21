# list_inventory.sh (pretty table to stdout, optional CSV)

> Prints a compact table: COLOR x SIZES with row/column totals + grand total.
> Works with adult or youth sizes in any mix.
> --csv prints a tidy CSV (or --csv file.csv writes to a file).


```bash
#!/usr/bin/env bash
set -euo pipefail

# Floor-count reporter for inventory kept under data/COLOR/SIZE.txt
# Usage:
#   ./list_inventory.sh                # pretty table to stdout
#   ./list_inventory.sh --csv          # CSV to stdout
#   ./list_inventory.sh --csv out.csv  # CSV to file
#   DATA_DIR=/path/to/data ./list_inventory.sh

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${DATA_DIR:-"$SCRIPT_DIR/data"}"

if [[ ! -d "$DATA_DIR" ]]; then
  echo "data/ not found: $DATA_DIR" >&2
  exit 1
fi

# Preferred display order for common sizes; others will follow alphabetically.
declare -a SIZE_ORDER=(
  "YS" "YM" "YL"
  "YSMALL" "YMEDIUM" "YLARGE"
  "SMALL" "MEDIUM" "LARGE" "XL" "2XL" "3XL" "4XL"
)

# --- collect colors and sizes -----------------------
declare -A SEEN_SIZE
declare -a COLORS

while IFS= read -r -d '' cdir; do
  color="$(basename "$cdir")"
  COLORS+=("$color")
  while IFS= read -r -d '' f; do
    sz="$(basename "${f%.*}")"
    SEEN_SIZE["$sz"]=1
  done < <(find "$cdir" -maxdepth 1 -type f -name '*.txt' -print0)
done < <(find "$DATA_DIR" -mindepth 1 -maxdepth 1 -type d -print0)

# Build final size list: preferred order first, then any others alpha.
declare -a SIZES=()
for s in "${SIZE_ORDER[@]}"; do [[ ${SEEN_SIZE[$s]+x} ]] && SIZES+=("$s"); done
# add extras not in preferred list
for s in "${!SEEN_SIZE[@]}"; do
  skip=""
  for k in "${SIZE_ORDER[@]}"; do [[ "$k" == "$s" ]] && { skip=1; break; }; done
  [[ -z "$skip" ]] && SIZES+=("$s")
done
IFS=$'\n' SIZES=($(printf '%s\n' "${SIZES[@]}" | awk 'NF' | sort -u)) # unique/sort extras

if [[ ${#COLORS[@]} -eq 0 || ${#SIZES[@]} -eq 0 ]]; then
  echo "No colors or sizes discovered under $DATA_DIR" >&2
  exit 0
fi
IFS=$'\n' COLORS=($(printf '%s\n' "${COLORS[@]}" | sort -u))

# Helper: qty for color/size
qty() {
  local color="$1" size="$2" f="$DATA_DIR/$color/$size.txt"
  if [[ -f "$f" ]]; then
    awk 'NR==1{q=$0+0; if(q<0) q=0; print q; exit} END{if(NR==0) print 0}' "$f"
  else
    echo 0
  fi
}

# --- CSV path? --------------------------------------
CSV_OUT=""
if [[ "${1:-}" == "--csv" ]]; then
  CSV_OUT="${2:-}"
fi

if [[ -n "$CSV_OUT" || "${1:-}" == "--csv" ]]; then
  # CSV mode
  if [[ -n "$CSV_OUT" ]]; then
    exec >"$CSV_OUT"
  fi
  echo -n "Color,Size,Qty"
  echo
  grand=0
  for color in "${COLORS[@]}"; do
    for sz in "${SIZES[@]}"; do
      q=$(qty "$color" "$sz")
      [[ "$q" -gt 0 ]] && { echo "$color,$sz,$q"; grand=$((grand+q)); }
    done
  done
  # A footer row can be useful for Excel imports:
  echo "TOTAL,,${grand}"
  exit 0
fi

# --- Pretty table mode ------------------------------
# width calc
colw=16
printf "Listing: %s\n\n" "$DATA_DIR"
printf "%-${colw}s" "COLOR"
declare -a colTotals
for i in "${!SIZES[@]}"; do
  printf " %6s" "${SIZES[$i]}"
  colTotals[$i]=0
done
printf " %8s\n" "ROW_TTL"
printf -- "%-${colw}s" "$(printf '%.0s-' {1..$colw})"
for _ in "${SIZES[@]}"; do printf " %6s" "------"; done
printf " %8s\n" "--------"

grand=0
for color in "${COLORS[@]}"; do
  rowTotal=0
  printf "%-${colw}s" "$color"
  for i in "${!SIZES[@]}"; do
    q=$(qty "$color" "${SIZES[$i]}")
    printf " %6d" "$q"
    rowTotal=$((rowTotal+q))
    colTotals[$i]=$((colTotals[$i]+q))
  done
  grand=$((grand+rowTotal))
  printf " %8d\n" "$rowTotal"
done

# footer totals
printf "%-${colw}s" "SIZE_TTL:"
for i in "${!SIZES[@]}"; do printf " %6d" "${colTotals[$i]}"; done
printf " %8d\n" "$grand"
```

# save_snapshot.sh (write timestamped CSV + echo path)

> Calls the same logic as list_inventory.sh --csv and saves to snapshots/.

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${DATA_DIR:-"$SCRIPT_DIR/data"}"
SNAP_DIR="${SNAP_DIR:-"$SCRIPT_DIR/snapshots"}"
mkdir -p "$SNAP_DIR"

stamp="$(date +'%Y%m%d_%H%M')"
out="$SNAP_DIR/floor_snapshot_${stamp}.csv"

"$SCRIPT_DIR/list_inventory.sh" --csv "$out"

echo "Saved snapshot -> $out"
```

# reset_inventory.sh (safe, keeps data/)

> This empties all color folders and files so you can start the next basket cleanly.

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${DATA_DIR:-"$SCRIPT_DIR/data"}"

if [[ ! -d "$DATA_DIR" ]]; then
  mkdir -p "$DATA_DIR"
  echo "Created '$DATA_DIR'."
  exit 0
fi

# Remove files and subdirs under data/ but keep data/ itself.
shopt -s dotglob nullglob
contents=("$DATA_DIR"/*)
if (( ${#contents[@]} )); then
  rm -rf -- "${contents[@]}"
  echo "Inventory reset: Emptied '$DATA_DIR'."
else
  echo "'$DATA_DIR' is already empty."
fi
```
