---
sidebar_position: 1
title: "BigTradeSignal"
description: "Signal based on large trade detection with optional direction inversion."
---

# BigTradeSignal

Triggers when a big trade is detected by the mzBigTrade indicator. By default, a sell (bid-side) big trade returns Long (large seller absorbed = support), and a buy (ask-side) big trade returns Short (large buyer absorbed = resistance). This can be inverted.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `BigTradeSignal : Signal`
**Data source:** Level1 | **Calculate:** OnEachTick
**Indicator:** StrategyBigTradeIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `IsInverted` | `bool` | `false` | Invert the direction (follow the big trade instead of fading it) |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Sell (bid) big trade detected |
| **Short** | Buy (ask) big trade detected |

When `IsInverted = true`, directions are swapped.

Trade filtering (volume, iceberg, DOM pressure, aggression) is configured on the `StrategyBigTradeIndicator` itself.

## Example

```csharp
var signal = new BigTradeSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnEachTick);
signal.IsInverted = false; // fade the big trade

pattern.Signals.Root.Add(signal);
```
