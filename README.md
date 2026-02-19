# Pjsekai Result Append Script

A simple CLI script to append Project Sekai play results into a JSON Lines (`.jsonl`) log file.

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
  --output data/pjsekai_results.jsonl
```

### Interactive mode

```bash
python pjsekai_result_append.py --interactive --output data/pjsekai_results.jsonl
```

## Output

Each appended line is one JSON object with these fields:

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

Example line:

```json
{"timestamp":"2026-02-19T09:45:00+00:00","song":"Tell Your World","difficulty":"EXPERT","score":1023456,"perfect":980,"great":12,"good":4,"bad":0,"miss":0,"max_combo":996,"clear_status":"FULL COMBO"}
```
