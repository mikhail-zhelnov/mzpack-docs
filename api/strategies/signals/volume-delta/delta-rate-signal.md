---
sidebar_position: 3
title: "DeltaRateSignal"
description: "Signal based on delta rate of change with minimum threshold."
---

# DeltaRateSignal

Evaluates the delta rate of change of the current bar. Positive rate signals Long, negative rate signals Short.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `DeltaRateSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose
**Indicator:** StrategyFootprintIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `MinAbsDeltaRate` | `double` | 0 | Minimum absolute delta rate (0 = returns allowed direction) |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Delta rate > 0 AND abs(rate) >= `MinAbsDeltaRate` |
| **Short** | Delta rate < 0 AND abs(rate) >= `MinAbsDeltaRate` |
| **allowed** | When `MinAbsDeltaRate` = 0, returns allowed direction |

## Example

```csharp
var signal = new DeltaRateSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnBarClose);
signal.MinAbsDeltaRate = 100;

pattern.Signals.Root.Add(signal);
```
