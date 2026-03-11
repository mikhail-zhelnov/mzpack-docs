---
sidebar_position: 1
title: "FootprintImbalanceSignal"
description: "Detects stacked bid/ask imbalances in footprint bars."
---

# FootprintImbalanceSignal

Detects stacked imbalances in the current footprint bar. Returns `Long` when buy (ask-side) imbalances are detected, `Short` when sell (bid-side) imbalances are detected.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `FootprintImbalanceSignal : Signal`
**Data source:** Level1 | **Calculate:** OnEachTick
**Indicator:** StrategyFootprintIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `MinCount` | `long` | 1 | Minimum number of imbalance levels in the bar |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Buy imbalance count >= `MinCount` (ask side) |
| **Short** | Sell imbalance count >= `MinCount` (bid side) |
| **None** | Both sides have imbalances, or neither side qualifies |

## Example

```csharp
var signal = new FootprintImbalanceSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnEachTick);
signal.MinCount = 3; // at least 3 stacked imbalances

pattern.Signals.Root.Add(signal);
```
