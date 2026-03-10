---
sidebar_position: 1
title: "RelativeToProfileSignal"
description: "Signal based on price position relative to VWAP, Value Area, or standard deviations."
---

# RelativeToProfileSignal

Evaluates the current price position relative to a volume profile level — VWAP, Value Area (VAH/VAL), or standard deviation bands.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `RelativeToProfileSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose
**Indicator:** IVolumeProfileIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `RelativeToProfile` | `RelativeToProfile` | — | Profile level: `VA` or `VWAP` |
| `VWAPType` | `VWAPMode` | `None` | VWAP variant: `Last`, `Dynamic`, `DynamicStdDev1`, `DynamicStdDev2` |
| `IsReversed` | `bool` | `false` | Reverse signal direction |
| `IsAnyWhenOutside` | `bool` | `false` | Return `Any` direction when price is outside StdDev/VA bands |

## Signal Logic

**VA mode:**

| Direction | Condition |
|---|---|
| **Long** | Price < VAL (below Value Area) |
| **Short** | Price > VAH (above Value Area) |

**VWAP mode:**

| Direction | Condition |
|---|---|
| **Long** | Price < VWAP |
| **Short** | Price > VWAP |

**StdDev mode (DynamicStdDev1/2):**

| Direction | Condition |
|---|---|
| **Long** | Price < lower standard deviation band |
| **Short** | Price > upper standard deviation band |
| **Any** | Price outside bands when `IsAnyWhenOutside = true` |

## Example

```csharp
var signal = new RelativeToProfileSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnBarClose);
signal.RelativeToProfile = RelativeToProfile.VA;

pattern.Signals.Root.Add(signal);
```
