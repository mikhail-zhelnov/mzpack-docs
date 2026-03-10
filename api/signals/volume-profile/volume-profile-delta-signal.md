---
sidebar_position: 2
title: "VolumeProfileDeltaSignal"
description: "Signal based on volume profile delta direction with volume and range filters."
---

# VolumeProfileDeltaSignal

Evaluates the delta of the most recent volume profile. A negative profile delta suggests buying pressure (Long), a positive delta suggests selling pressure (Short).

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `VolumeProfileDeltaSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose
**Indicator:** StrategyVolumeProfileIndicator

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `IsInverted` | `bool` | `false` | Invert the direction |
| `MinRangeTicks` | `int` | 0 | Minimum profile range in ticks |
| `MaxRangeTicks` | `int` | -1 | Maximum profile range (-1 = no limit) |
| `MinVolume` | `double` | 0 | Minimum total volume in profile |
| `AbsMinDelta` | `double` | 0 | Minimum absolute delta in profile |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Profile delta < 0 (or inverted) AND volume/range/delta filters pass |
| **Short** | Profile delta > 0 (or inverted) AND volume/range/delta filters pass |

## Example

```csharp
var signal = new VolumeProfileDeltaSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnBarClose);
signal.MinVolume = 10000;
signal.AbsMinDelta = 500;

pattern.Signals.Root.Add(signal);
```
