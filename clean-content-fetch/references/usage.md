# Usage

## Basic
```bash
python3 scripts/scrapling_fetch.py <url> 30000
```

## JSON output
```bash
python3 scripts/scrapling_fetch.py <url> 30000 --json
```

## Wrapper
```bash
scripts/fetch-web-content <url> 30000
```

## Batch mode
```bash
python3 scripts/scrapling_fetch.py --batch urls.txt 20000 --json
```

## Site selector overrides
```bash
python3 scripts/scrapling_fetch.py <url> 30000 --selectors /path/to/site-overrides.json
```