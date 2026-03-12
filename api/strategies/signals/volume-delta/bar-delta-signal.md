---
sidebar_position: 1
title: "BarDeltaSignal"
description: "Signal based on bar delta direction with minimum threshold."
---

# BarDeltaSignal

Evaluates the delta of the current bar. Positive delta signals Long, negative delta signals Short.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `BarDeltaSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose
**Indicator:** StrategyFootprintIndicator or StrategyVolumeDeltaIndicator
**Source:** `[INSTALL PATH]/API/Signals/BarDeltaSignal.cs`

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `MinAbsDelta` | `double` | 0 | Minimum absolute delta required |
| `IsReverse` | `bool` | `false` | Reverse the direction |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Bar delta > 0 AND abs(delta) >= `MinAbsDelta` |
| **Short** | Bar delta < 0 AND abs(delta) >= `MinAbsDelta` |

## Example

```csharp
var signal = new BarDeltaSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnBarClose);
signal.MinAbsDelta = 500;

pattern.Signals.Root.Add(signal);
```
