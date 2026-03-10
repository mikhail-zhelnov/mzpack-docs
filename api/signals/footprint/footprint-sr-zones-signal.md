---
sidebar_position: 3
title: "FootprintSRZonesSignal"
description: "Detects active imbalance or absorption S/R zones near current price."
---

# FootprintSRZonesSignal

Detects active support/resistance zones based on imbalance or absorption data. Can operate as a directional signal or as a filter.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `FootprintSRZonesSignal : Signal`
**Data source:** Level1 | **Calculate:** OnEachTick
**Indicator:** StrategyFootprintIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `ZoneType` | `SRZoneType` | `Imbalance` | Type of S/R zone: `Imbalance` or `Absorption` |
| `MinCount` | `long` | 1 | Minimum number of active zones |
| `IsFilter` | `bool` | `false` | When `true`, returns the allowed direction if both sides have zones |

## Signal Logic

For **Imbalance** zones:

| Direction | Condition |
|---|---|
| **Long** | Buy imbalance S/R zones >= `MinCount` |
| **Short** | Sell imbalance S/R zones >= `MinCount` |

For **Absorption** zones (inverted):

| Direction | Condition |
|---|---|
| **Long** | Sell absorption S/R zones >= `MinCount` |
| **Short** | Buy absorption S/R zones >= `MinCount` |

In **filter mode**: if both sides have zones, returns the `allowed` direction instead of `None`.

## Example

```csharp
var signal = new FootprintSRZonesSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnEachTick);
signal.ZoneType = SRZoneType.Imbalance;
signal.MinCount = 1;

pattern.Signals.Root.Add(signal);
```
