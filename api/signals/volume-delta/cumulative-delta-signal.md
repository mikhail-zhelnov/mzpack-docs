---
sidebar_position: 2
title: "CumulativeDeltaSignal"
description: "Signal based on session cumulative delta direction."
---

# CumulativeDeltaSignal

Evaluates the cumulative delta of the current session. Positive cumulative delta signals Long, negative signals Short.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `CumulativeDeltaSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose
**Indicator:** StrategyFootprintIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `IsReversed` | `bool` | `false` | Reverse the direction |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Session cumulative delta > 0 |
| **Short** | Session cumulative delta < 0 |

## Example

```csharp
var signal = new CumulativeDeltaSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnBarClose);

pattern.Signals.Root.Add(signal);
```
