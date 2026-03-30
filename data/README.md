# DK1 2025 BESS backtest data

This folder stores raw input files for a Denmark West (DK1) 2025 BESS simulation.

## Included downloader

Run:

```bash
python scripts/fetch_2025_dk1_data.py
```

Downloaded files are saved in `data/raw/`.

## Dataset coverage

The script attempts to fetch:

- `Elspotprices` (day-ahead prices, DK1)
- `FcrReservesDK1` (FCR reserve prices/results, DK1)
- `mFRRReservesDK1` (mFRR reserve prices/results, DK1)
- `RealtimeMarket` (balancing/realtime market series)

All from Energi Data Service API:
- https://api.energidataservice.dk/

## Additional data you likely need

For a realistic SOC/revenue model, also collect:

1. **Frequency trace** (1s or similar resolution) for 2025 (Nordic synchronous area).
2. **Tariffs and fees** applied to your connection and balancing settlement.
3. **Your technical constraints** (efficiency curve, min/max SOC, degradation assumptions).

Those are usually not fully covered by one open dataset and may require TSO documentation or specific contracts.
