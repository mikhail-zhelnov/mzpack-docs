---
sidebar_position: 2
title: "TradesClusterSignal"
description: "Signal based on a cluster of trades matching volume, count, and range criteria."
---

# TradesClusterSignal

Detects a cluster of trades on a specific side (bid or ask) that meet volume, count, aggression, and range criteria. The direction is fixed at construction (Long or Short).

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `TradesClusterSignal : Signal`
**Data source:** Level1 | **Calculate:** OnEachTick
**Indicator:** StrategyBigTradeIndicator
**Source:** `[INSTALL PATH]/API/Signals/TradesClusterSignal.cs`

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `Side` | `TradeSide` | — | Side of trades to collect (Bid or Ask) |
| `Range` | `Range` | — | Bar/tick range constraint for the cluster |
| `MinVolume` | `long` | 0 | Minimum total volume in the cluster |
| `MinCount` | `long` | 0 | Minimum number of trades in the cluster |
| `MinAggression` | `int` | 0 | Minimum aggression (ticks) per trade |
| `VolumeCountLogic` | `Logic` | `And` | How volume and count filters combine: `And` or `Or` |

## Signal Logic

The signal collects trades matching the `Side` and `MinAggression` criteria within the specified `Range`. When the collected cluster meets both (or either, per `VolumeCountLogic`) the `MinVolume` and `MinCount` thresholds, the pre-defined direction is returned.

## Example

```csharp
var signal = new TradesClusterSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnEachTick);
signal.Side = TradeSide.Bid;
signal.MinVolume = 500;
signal.MinCount = 5;
signal.Range = new Range { Bars = 3 };

pattern.Signals.Root.Add(signal);
```
