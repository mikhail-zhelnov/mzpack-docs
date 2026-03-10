---
sidebar_position: 3
title: "BarMetricsSignal"
description: "Signal based on bar metrics such as body size, wick percentages, and candlestick patterns."
---

# BarMetricsSignal

Evaluates one or more bar metrics (body size, wick proportions, candlestick patterns) against thresholds. All conditions must be met (AND logic) for the signal to fire. The direction is fixed at construction.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `BarMetricsSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose

## Constructors

Single metric:

```csharp
new BarMetricsSignal(strategy, ago, barMetrics, minMax, value, allowed)
```

Multiple metrics:

```csharp
new BarMetricsSignal(strategy, ago, barMetricsDescArray, allowed)
```

| Parameter | Type | Description |
|---|---|---|
| `ago` | `int` | Bars ago to evaluate (0 = current bar) |
| `barMetrics` | `BarMetrics` | Metric to check |
| `minMax` | `MinMax` | Whether `value` is a minimum or maximum threshold |
| `value` | `int` | Threshold value in ticks |
| `barMetricsDesc` | `BarMetricsDesc[]` | Array of metric descriptors for multi-condition checks |
| `allowed` | `SignalDirection` | Direction returned when all conditions pass |

## Signal Logic

Each metric in the array is checked in sequence. If **any** condition fails, the signal returns no direction. Only when all conditions pass does it return the `allowed` direction. The signal does not produce an entry price.

## BarMetrics Enum

| Value | Description |
|---|---|
| `Body` | Bar body size in ticks |
| `Size` | Full bar range in ticks (High − Low) |
| `UpperWick` | Upper wick size in ticks |
| `LowerWick` | Lower wick size in ticks |
| `BodyPercent` | Body as percentage of full range |
| `UpperWickPercent` | Upper wick as percentage of full range |
| `LowerWickPercent` | Lower wick as percentage of full range |
| `Hammer` | Hammer candlestick pattern (boolean check, no threshold) |
| `Doji` | Doji candlestick pattern (boolean check, no threshold) |

## MinMax Enum

| Value | Description |
|---|---|
| `Min` | Value must be >= threshold |
| `Max` | Value must be \<= threshold |

## Example

```csharp
// Single metric: body >= 4 ticks, 0 bars ago, Long direction
var signal = new BarMetricsSignal(strategy, 0,
    BarMetrics.Body, MinMax.Min, 4, SignalDirection.Long);

pattern.Signals.Root.Add(signal);

// Multiple metrics: body >= 4 ticks AND upper wick <= 2 ticks
var desc = new BarMetricsDesc[]
{
    new BarMetricsDesc { BarMetrics = BarMetrics.Body, MinMax = MinMax.Min, Value = 4 },
    new BarMetricsDesc { BarMetrics = BarMetrics.UpperWick, MinMax = MinMax.Max, Value = 2 }
};
var signal2 = new BarMetricsSignal(strategy, 0, desc, SignalDirection.Short);

pattern.Signals.Root.Add(signal2);
```
