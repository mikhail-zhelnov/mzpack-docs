---
sidebar_position: 6
title: "ChartRange"
description: "Reference for ChartRange and IRange — define bar/price ranges for signal validation in the decision tree."
---

# ChartRange

`ChartRange` defines the bar index and price range of validated signals within a decision tree. When signals in a pattern validate at different bars or prices, `ChartRange` tracks the combined range so that entries can be placed relative to the validated zone.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `ChartRange : ICloneable`
**Source:** `MZpack.NT8/Algo/ChartRange.cs`

## Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `BeginSessionIdx` | `int` | -1 | Session index when the range started |
| `MinBarIdx` | `int` | -1 | Earliest bar index among validated signals |
| `MaxBarIdx` | `int` | -1 | Latest bar index among validated signals |
| `High` | `double` | 0 | Highest price among validated signals |
| `Low` | `double` | 0 | Lowest price among validated signals |

## Methods

| Method | Return Type | Description |
|---|---|---|
| `Reset()` | `void` | Reset all values to defaults |
| `AddRange(ChartRange range)` | `void` | Merge another range into this range (expand bounds) |
| `GetMaxBarIdx(int idx)` | `int` | Return the larger of current max and given index |
| `GetMinBarIdx(int idx)` | `int` | Return the smaller of current min and given index |
| `GetMaxHigh(ChartRange range)` | `double` | Return the higher of two highs |
| `GetMinLow(ChartRange range)` | `double` | Return the lower of two lows |
| `Clone()` | `object` | Deep copy of the range |

## IRange Interface

`IRange` defines the constraints for how far apart signals can be (in bars and ticks) and still count as part of the same pattern.

**Source:** `MZpack.NT8/Algo/IRange.cs`

| Property | Type | Default | Description |
|---|---|---|---|
| `Bars` | `int` | 0 | Maximum bar distance between signals (0 = no limit) |
| `Ticks` | `int` | 0 | Maximum tick distance between signals (0 = no limit) |
| `Logic` | `Logic` | `And` | How Bars and Ticks constraints combine |
| `IsInSession` | `bool` | `false` | Restrict range to current session only |

When `Logic` is `And`, both bar and tick constraints must be satisfied. When `Or`, either constraint is sufficient.

## How It Works

1. Each `SignalsTree` has a `Range` property (IRange) defining the allowed spread between signals
2. As signals validate, `ChartRange` accumulates their bar indices and prices
3. Before the pattern is considered validated, the tree checks that `ChartRange` fits within the `Range` constraints
4. If `ChartRange` exceeds the range, earlier signals are expired and must re-validate

## Exceptions

| Exception | Description |
|---|---|
| `DecisionTreeSignalChartRangeIsNullException` | A signal's `ChartRange` is null when the tree requires range tracking |
| `DecisionTreeSignalChartRangeIsInvalidException` | A signal's `ChartRange` has invalid values (e.g. High < Low) |

Both extend `DecisionTreeException : StrategyException`.

## Example: Range-Limited Pattern

```csharp
// Signals must validate within 5 bars and 20 ticks of each other
var range = new Range();
range.Bars = 5;
range.Ticks = 20;
range.Logic = Logic.And;

var pattern = new Pattern(strategy, Logic.And, range,
    isShortCircuitANDEvaluation: true);
```

## See Also

- [Algo.Strategy](algo-strategy.md) — strategy class
- [Decision Tree](./decision-tree.md) — signal/filter tree structure
