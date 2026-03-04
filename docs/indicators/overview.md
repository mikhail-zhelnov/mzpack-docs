---
sidebar_position: 1
title: "Indicators Overview"
description: "Overview of all MZpack indicators for order flow analysis and volume profiling in NinjaTrader 8"
---

# Indicators Overview

MZpack provides six indicators for NinjaTrader 8, each focused on a different aspect of order flow and volume analysis. All indicators render directly on the chart using hardware-accelerated Direct2D graphics and process real-time tick data.

## Available Indicators

| Indicator | Purpose | Data Required |
|---|---|---|
| [mzFootprint](mzFootprint.md) | Order flow footprint charts with bid/ask clusters, imbalances, and absorption | Level 1 (tick data) |
| [mzVolumeProfile](mzVolumeProfile.md) | Volume distribution profiles with TPO, POC, value area, and VWAP | Level 1 (tick data) |
| [mzVolumeDelta](mzVolumeDelta.md) | Volume delta analysis with histograms, candles, and cumulative delta | Level 1 (tick data) |
| [mzBigTrade](mzBigTrade.md) | Large trade detection with tape, markers, and trade volume profiles | Level 1 (tick data) |
| [mzMarketDepth](mzMarketDepth.md) | Level 2 order book visualization with liquidity migration tracking | Level 2 (DOM data) |
| [mzDeltaDivergence](mzDeltaDivergence.md) | Delta-price divergence signal detection | Level 1 (tick data) |

## Adding an Indicator

1. Right-click on a NinjaTrader 8 chart
2. Select **Indicators**
3. Search for the indicator name (e.g., `mzFootprint`)
4. Click **Add**, then **OK**

For a step-by-step walkthrough, see [Your First Indicator](../getting-started/first-indicator.md).

## Common Concepts

### Order Flow Calculation Modes

Most MZpack indicators reconstruct order flow from tick data. The calculation mode determines how trades are classified as buying or selling:

| Mode | Description | Best For |
|---|---|---|
| **BidAsk** | Classifies trades based on whether they hit the bid or lifted the ask | Live trading with Tick Replay enabled |
| **UpDownTick** | Classifies based on price direction (uptick = buy, downtick = sell) | Historical data analysis |
| **Hybrid** | Uses UpDownTick for historical bars, switches to BidAsk for live data | Mixed use cases |

### Color Modes

All indicators that display volume data support multiple color modes:

| Mode | Description |
|---|---|
| **Solid** | Single uniform color |
| **Saturation** | Color intensity scales with value magnitude |
| **Heatmap** | Multi-color gradient (red = high, blue = low) |
| **GrayScale Heatmap** | Monochrome intensity gradient |
| **Custom** | User-defined color thresholds |

### Alerts and Notifications

Each indicator supports real-time alerts:

- **Sound alerts** — play a WAV file when a threshold is crossed
- **Email notifications** — send an email on triggered conditions
- Alerts can be configured per metric (volume, delta, trades, etc.) with custom thresholds

### Performance

MZpack indicators are optimized for real-time tick-level processing:

- Minimal allocations in hot paths (no LINQ per tick)
- Direct2D hardware-accelerated rendering
- Configurable render throttling via **MaximalRenderMs** to balance visual refresh rate vs. CPU usage

## Editions and Feature Availability

Not all features are available in every edition:

| Feature | FREE | TRIAL | Indicators License |
|---|---|---|---|
| Basic footprint display | Yes | Yes | Yes |
| Imbalance / Absorption | — | Yes | Yes |
| S/R Zones | — | Yes | Yes |
| Volume Profile Levels | — | Yes | Yes |
| Statistics Grid | — | Yes | Yes |
| Delta Divergence signals | — | Yes | Yes |
| Alerts and notifications | — | Yes | Yes |

See [Licensing](../getting-started/licensing.md) for details.
