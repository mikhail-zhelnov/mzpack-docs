---
sidebar_position: 2
title: "DOMBlockSignal"
description: "Signal based on persistent large orders (blocks) in the DOM."
---

# DOMBlockSignal

Detects persistent large orders (blocks) in the DOM that have been present for a minimum time, are within a specified distance from the current price, and exceed a volume threshold.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `DOMBlockSignal : Signal`
**Data source:** Level2 | **Calculate:** NotApplicable
**Indicator:** StrategyMarketDepthIndicator

:::warning
Requires Level 2 data — live or replay only. Not available in historical backtesting.
:::

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `TimeSeconds` | `int` | 5 | Minimum time in seconds the block must persist in DOM |
| `DistanceTicks` | `int` | 10 | Maximum distance from current price in ticks |
| `Volume` | `long` | 100 | Minimum volume of the block |
| `EntryPriceOffsetTicks` | `int` | 0 | Entry price offset from block price in ticks |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Bid-side block meets all criteria (time, distance, volume) |
| **Short** | Ask-side block meets all criteria |

## Example

```csharp
var signal = new DOMBlockSignal(strategy,
    MarketDataSource.Level2, SignalCalculate.NotApplicable);
signal.Volume = 500;
signal.TimeSeconds = 10;
signal.DistanceTicks = 5;

pattern.Signals.Root.Add(signal);
```
