---
sidebar_position: 4
title: "BarIcebergsSignal"
description: "Signal based on iceberg order detection by volume threshold."
---

# BarIcebergsSignal

Detects iceberg orders in the current bar. Icebergs on the bid side signal Long (hidden buying), icebergs on the ask side signal Short (hidden selling).

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `BarIcebergsSignal : Signal`
**Data source:** Level1 | **Calculate:** OnEachTick
**Indicator:** StrategyVolumeDeltaIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `MinIcebergVolume` | `double` | 1 | Minimum iceberg volume threshold |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Bid-side icebergs >= `MinIcebergVolume` |
| **Short** | Ask-side icebergs >= `MinIcebergVolume` |
| **None** | Both sides have icebergs above threshold |

## Example

```csharp
var signal = new BarIcebergsSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnEachTick);
signal.MinIcebergVolume = 500;

pattern.Signals.Root.Add(signal);
```
