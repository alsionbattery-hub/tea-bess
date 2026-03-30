#!/usr/bin/env python3
"""Download DK1 2025 datasets for BESS backtesting.

Uses Energi Data Service's public download API and stores CSV files in data/raw.
No external dependencies required.
"""
from __future__ import annotations

import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.energidataservice.dk/dataset/{dataset}/download"
OUT_DIR = pathlib.Path("data/raw")


DATASETS = [
    {
        "dataset": "Elspotprices",
        "filename": "elspotprices_dk1_2025.csv",
        "params": {
            "start": "2025-01-01T00:00",
            "end": "2026-01-01T00:00",
            "filter": {"PriceArea": ["DK1"]},
            "sort": "HourUTC",
            "timezone": "dk",
            "format": "csv",
        },
        "description": "Day-ahead prices (DK1)",
    },
    {
        "dataset": "FcrReservesDK1",
        "filename": "fcrreserves_dk1_2025.csv",
        "params": {
            "start": "2025-01-01T00:00",
            "end": "2026-01-01T00:00",
            "sort": "HourUTC",
            "timezone": "dk",
            "format": "csv",
        },
        "description": "FCR reserve market prices/results (DK1)",
    },
    {
        "dataset": "mFRRReservesDK1",
        "filename": "mfrrreserves_dk1_2025.csv",
        "params": {
            "start": "2025-01-01T00:00",
            "end": "2026-01-01T00:00",
            "sort": "HourUTC",
            "timezone": "dk",
            "format": "csv",
        },
        "description": "mFRR reserve prices/results (DK1)",
    },
    {
        "dataset": "RealtimeMarket",
        "filename": "realtimemarket_dk1_2025.csv",
        "params": {
            "start": "2025-01-01T00:00",
            "end": "2026-01-01T00:00",
            "sort": "HourUTC",
            "timezone": "dk",
            "format": "csv",
        },
        "description": "Balancing / realtime market data",
    },
]


def encode_params(params: dict) -> str:
    prepared: dict[str, str] = {}
    for k, v in params.items():
        if isinstance(v, (dict, list)):
            prepared[k] = json.dumps(v, separators=(",", ":"))
        else:
            prepared[k] = str(v)
    return urllib.parse.urlencode(prepared)


def download_dataset(spec: dict) -> tuple[bool, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    query = encode_params(spec["params"])
    url = BASE.format(dataset=spec["dataset"]) + "?" + query
    output_path = OUT_DIR / spec["filename"]

    try:
        with urllib.request.urlopen(url, timeout=120) as response:
            data = response.read()
        output_path.write_bytes(data)
        return True, f"saved {output_path} ({len(data)} bytes)"
    except urllib.error.HTTPError as err:
        return False, f"HTTP {err.code} for {spec['dataset']}: {err.reason}"
    except urllib.error.URLError as err:
        return False, f"URL error for {spec['dataset']}: {err.reason}"


def main() -> int:
    print("Downloading DK1 2025 market datasets...\n")
    failures = 0

    for spec in DATASETS:
        print(f"- {spec['dataset']}: {spec['description']}")
        ok, message = download_dataset(spec)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {message}\n")
        if not ok:
            failures += 1

    if failures:
        print(f"Completed with {failures} failed dataset(s).")
        return 1

    print("All datasets downloaded successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
