---
sidebar_position: 1
title: "DeltaDivergenceSignal"
description: "Signal based on price/delta divergence at ZigZag swing points."
---

# DeltaDivergenceSignal

Detects divergence between price and cumulative delta at ZigZag swing points. A bullish divergence (lower price low, higher delta low) signals Long. A bearish divergence (higher price high, lower delta high) signals Short.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `DeltaDivergenceSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose
**Indicator:** StrategyDeltaDivergenceIndicator
**Source:** `[INSTALL PATH]/API/Signals/DeltaDivergenceSignal.cs`

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `IsFilter` | `bool` | `false` | When `true`, ignores `Any` direction (both buy and sell divergences) |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Buy divergences detected in the bar |
| **Short** | Sell divergences detected in the bar |
| **Any** | Both buy and sell divergences present (ignored if `IsFilter = true`) |

Divergence detection parameters (ZigZag threshold, price/delta deviation) are configured on the `StrategyDeltaDivergenceIndicator`.

## Example

```csharp
var signal = new DeltaDivergenceSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnBarClose);

pattern.Signals.Root.Add(signal);
```
