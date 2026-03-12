---
sidebar_position: 1
title: "Indicators API Overview"
description: "Overview of the MZpack indicator interface hierarchy and how to access indicator data from custom code."
---

# Indicators API Overview

The MZpack Indicators API exposes every chart indicator through a typed interface hierarchy. Each interface provides read-only access to the indicator's computed data — footprint bars, volume profiles, trades, DOM snapshots, and divergence signals. Strategy classes wrap the same interfaces, so data access is identical whether you read from a chart indicator or a strategy indicator.

## Interface Hierarchy

```
IIndicator
├── ITickIndicator
│   ├── IOrderFlowIndicator
│   │   ├── IFootprintIndicator
│   │   ├── IBigTradeIndicator
│   │   └── IVolumeDeltaIndicator
│   │       └── IDeltaDivergenceIndicator
│   ├── IMarketDepthIndicator
│   └── IVolumeProfileIndicator (also ILevelsIndicator)
└── ILevelsIndicator
```

### Base Interfaces

| Interface | What It Provides |
|---|---|
| [IIndicator](iindicator.md) | Candle access, tick size helpers, chart coordinate helpers, logging, licensing — the base contract for every MZpack indicator |
| [ITickIndicator](iindicator.md) | Best bid/ask prices, last trade side, volume conversion helpers — extends IIndicator with real-time tick data |
| [IOrderFlowIndicator](iorderflow-indicator.md) | Order flow calculation mode, tape reconstruction settings, iceberg algorithm — shared config for all order flow indicators |
| [ILevelsIndicator](ilevelsindicator.md) | User-drawn price levels, level alerts, mouse drag, keyboard shortcuts — adds interactive level management |

### Per-Indicator Interfaces

| Interface | What It Provides |
|---|---|
| [IFootprintIndicator](footprint/ifootprint-indicator.md) | Footprint bars collection, sessions, imbalance/absorption S/R zones, cluster zones, statistic grid settings |
| [IVolumeProfileIndicator](volume-profile/ivolume-profile-indicator.md) | Volume profiles collection, profile creation modes, stacked profiles, TPO settings, VWAP/Value Area |
| [IVolumeDeltaIndicator](volume-delta/ivolume-delta-indicator.md) | Volume/delta bars, cumulative delta, iceberg detection, volume alerts |
| [IBigTradeIndicator](big-trade/ibig-trade-indicator.md) | Filtered trades list, trade filter settings (volume, iceberg, DOM pressure, aggression), presentation |
| [IMarketDepthIndicator](market-depth/imarket-depth-indicator.md) | Real-time order book, historical DOM blocks, liquidity, liquidity migration, Level II histogram |
| [IDeltaDivergenceIndicator](delta-divergence/idelta-divergence-indicator.md) | Divergences collection, ZigZag settings, price/delta deviation filters |

## Indicator ↔ Strategy Class Mapping

Every chart indicator has a corresponding strategy wrapper class. The strategy class inherits from the chart indicator and implements the same interface, so data access code is identical.

| Interface | Chart Indicator | Strategy Class | Namespace |
|---|---|---|---|
| IFootprintIndicator | mzFootprint | [StrategyFootprintIndicator](footprint/strategy-footprint-indicator.md) | MZpack.NT8.Algo.Indicators |
| IVolumeProfileIndicator | mzVolumeProfile | [StrategyVolumeProfileIndicator](volume-profile/strategy-vp-indicator.md) | MZpack.NT8.Algo.Indicators |
| IVolumeDeltaIndicator | mzVolumeDelta | [StrategyVolumeDeltaIndicator](volume-delta/strategy-vd-indicator.md) | MZpack.NT8.Algo.Indicators |
| IBigTradeIndicator | mzBigTrade | [StrategyBigTradeIndicator](big-trade/strategy-bigtrade-indicator.md) | MZpack.NT8.Algo.Indicators |
| IMarketDepthIndicator | mzMarketDepth | [StrategyMarketDepthIndicator](market-depth/strategy-md-indicator.md) | MZpack.NT8.Algo.Indicators |
| IDeltaDivergenceIndicator | mzDeltaDivergence | [StrategyDeltaDivergenceIndicator](delta-divergence/strategy-dd-indicator.md) | MZpack.NT8.Algo.Indicators |

All interfaces are defined in the `MZpack` namespace. Strategy classes are in `MZpack.NT8.Algo.Indicators`.

## Data Access Pattern

Regardless of which indicator you use, the pattern is the same:

```csharp
// 1. Declare the strategy indicator
StrategyFootprintIndicator footprint;

// 2. Create and configure in strategy setup
footprint = new StrategyFootprintIndicator(this, "Footprint");
footprint.TicksPerLevel = 1;

// 3. Access data through the interface
IFootprintBar bar = footprint.FootprintBars[CurrentBar];
long delta = bar.Delta;
double poc = bar.POC;
```

Strategy indicator classes are not visible on the chart by default — use **Partially Visible** mode to show only the data relevant to validated signals. See [Algo Strategy — Partially Visible](../samples/algo-strategy-partially-visible.md) for a code sample.
