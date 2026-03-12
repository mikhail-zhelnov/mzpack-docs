---
sidebar_position: 4
title: "OrdferflowBarMetricsSignal"
description: "Signal based on order flow bar metrics such as volume, absolute delta, and delta percentage."
---

# OrdferflowBarMetricsSignal

Evaluates order flow metrics of a footprint bar (volume, delta) against thresholds. All conditions must be met (AND logic) for the signal to fire. The direction is fixed at construction.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `OrdferflowBarMetricsSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose
**Indicator:** StrategyFootprintIndicator
**Source:** `[INSTALL PATH]/API/Signals/OrderflowBarMetricsSignal.cs`

:::note Class name
The class name contains a typo (`Ordferflow` instead of `Orderflow`) in the source code. Use the exact name `OrdferflowBarMetricsSignal` when referencing this class.
:::

## Constructor

```csharp
new OrdferflowBarMetricsSignal(strategy, footprintIndicator, ago, barMetricsDesc)
```

| Parameter | Type | Description |
|---|---|---|
| `footprintIndicator` | `StrategyFootprintIndicator` | Footprint indicator instance (required) |
| `ago` | `int` | Bars ago to evaluate (0 = current bar) |
| `barMetricsDesc` | `OrderflowBarMetricsDesc[]` | Array of metric descriptors |

## Signal Logic

The signal retrieves the footprint bar from `StrategyFootprintIndicator.FootprintBars` and evaluates each metric. If **any** condition fails, the signal returns no direction. When all conditions pass, it returns the `allowed` direction configured in the descriptor. The signal does not produce an entry price.

## OrderflowBarMetrics Enum

| Value | Description |
|---|---|
| `Volume` | Total footprint bar volume |
| `AbsDelta` | Absolute delta: `|BuyVolume − SellVolume|` |
| `DeltaPercent` | Delta as a percentage of volume (absolute value) |

## MinMax Enum

| Value | Description |
|---|---|
| `Min` | Value must be >= threshold |
| `Max` | Value must be \<= threshold |

## Example

```csharp
var fpIndicator = new StrategyFootprintIndicator(strategy);

var desc = new OrderflowBarMetricsDesc[]
{
    new OrderflowBarMetricsDesc
    {
        OrderflowBarMetrics = OrderflowBarMetrics.Volume,
        MinMax = MinMax.Min,
        Value = 1000
    },
    new OrderflowBarMetricsDesc
    {
        OrderflowBarMetrics = OrderflowBarMetrics.DeltaPercent,
        MinMax = MinMax.Min,
        Value = 30
    }
};

var signal = new OrdferflowBarMetricsSignal(strategy, fpIndicator, 0, desc);

pattern.Signals.Root.Add(signal);
```
