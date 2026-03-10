---
sidebar_position: 4
title: "ClusterZonesSignal"
description: "Detects consecutive cluster zones in footprint bars."
---

# ClusterZonesSignal

Searches for consecutive cluster zones in the footprint. Cluster zones represent areas of significant volume concentration. Can be used as a signal or a filter.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `ClusterZonesSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose
**Indicator:** StrategyFootprintIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `Footprint` | `int` | 0 | Footprint side: 0 = left, 1 = right |
| `MinCount` | `long` | 1 | Minimum number of consecutive cluster zones |
| `IsFilter` | `bool` | `false` | Use absolute values when `true` |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Positive cluster zone values (buying pressure) |
| **Short** | Negative cluster zone values (selling pressure) |

In filter mode, absolute values are used regardless of sign.

## Example

```csharp
var signal = new ClusterZonesSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnBarClose);
signal.Footprint = 0; // left footprint
signal.MinCount = 2;

pattern.Signals.Root.Add(signal);
```
