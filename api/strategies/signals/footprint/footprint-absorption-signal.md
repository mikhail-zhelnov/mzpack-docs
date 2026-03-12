---
sidebar_position: 2
title: "FootprintAbsorptionSignal"
description: "Detects passive absorption at footprint bar price extremes."
---

# FootprintAbsorptionSignal

Detects absorption levels in the current footprint bar. Absorption indicates passive limit orders absorbing aggressive market orders. Direction is inverted: sell absorption signals buying support (Long), buy absorption signals selling resistance (Short).

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `FootprintAbsorptionSignal : Signal`
**Data source:** Level1 | **Calculate:** OnEachTick
**Indicator:** StrategyFootprintIndicator
**Source:** `[INSTALL PATH]/API/Signals/FootprintAbsoprtionSignal.cs`

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `MinCount` | `long` | 1 | Minimum number of absorption levels in the bar |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Sell absorption count >= `MinCount` (bid side absorbing sells) |
| **Short** | Buy absorption count >= `MinCount` (ask side absorbing buys) |
| **None** | Both sides have absorptions, or neither side qualifies |

## Example

```csharp
var signal = new FootprintAbsorptionSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnEachTick);
signal.MinCount = 2;

pattern.Signals.Root.Add(signal);
```
