---
sidebar_position: 3
title: "BarJoinedPOCsSignal"
description: "Signal based on consecutive joined POCs within a footprint bar."
---

# BarJoinedPOCsSignal

Detects a specified number of consecutive joined POCs (Point of Control levels within 1 tick of each other) in the current footprint bar. Returns the allowed direction when the condition is met.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `BarJoinedPOCsSignal : Signal`
**Data source:** Level1 | **Calculate:** OnEachTick
**Indicator:** StrategyFootprintIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `POCsCount` | `int` | 2 | Number of consecutive joined POCs required |

## Signal Logic

| Direction | Condition |
|---|---|
| **allowed** | Bar contains >= `POCsCount` consecutive POCs within 1 tick distance |
| **None** | Condition not met |

## Example

```csharp
var signal = new BarJoinedPOCsSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnEachTick);
signal.POCsCount = 3;

pattern.Signals.Root.Add(signal);
```
