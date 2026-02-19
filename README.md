# Pjsekai Result Append Script

A simple CLI script to append Project Sekai play results into a CSV log file.

## Usage

### Non-interactive mode

```bash
python pjsekai_result_append.py \
  --song "Tell Your World" \
  --difficulty EXPERT \
  --score 1023456 \
  --perfect 980 \
  --great 12 \
  --good 4 \
  --bad 0 \
  --miss 0 \
  --max-combo 996 \
  --clear-status "FULL COMBO" \
  --output data/pjsekai_results.csv
```

### Interactive mode

```bash
python pjsekai_result_append.py --interactive --output data/pjsekai_results.csv
```

## Output

The script appends rows with these columns:

- `timestamp` (UTC ISO-8601)
- `song`
- `difficulty`
- `score`
- `perfect`
- `great`
- `good`
- `bad`
- `miss`
- `max_combo`
- `clear_status`

If the output file does not exist, the script automatically creates it and writes headers.
