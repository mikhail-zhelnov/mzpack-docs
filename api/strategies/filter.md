---
sidebar_position: 14
title: "Filter"
description: "Reference for ValueInRangeFilter — gates the decision tree by checking if an indicator value falls within a range."
---

# Filter

`ValueInRangeFilter` is a `Signal` that gates the decision tree by checking whether an indicator's output falls within a specified range. If the value is outside [Min, Max], the filter returns `None` and blocks the pattern.

**Namespace:** `MZpack.NT8.Algo.Filters`
**Inheritance:** `ValueInRangeFilter : Signal`
**Source:** `MZpack.NT8/Algo/Filters/ValueInRangeFilter.cs`

## Properties

| Property | Type | Description |
|---|---|---|
| `Min` | `double` | Minimum value of the allowed range |
| `Max` | `double` | Maximum value of the allowed range |

Inherits all [Signal](signals/signal-base.md#signal) properties (`Strategy`, `MarketDataSource`, `Calculate`, `Direction`, etc.).

## Constructor

```csharp
public ValueInRangeFilter(Strategy strategy, StrategyPlotIndicator indicator)
```

Sets `MarketDataSource = Level1`, `Calculate = OnBarClose`, `IsReset = true`. The `indicator` parameter ties the filter to a specific indicator's output values.

## Behavior

On each bar close, `OnCalculate` reads `indicator.Values[0][barIdx]`:

- If `value >= Min && value <= Max` — returns `SignalDirection.Any` (filter passes)
- Otherwise — returns `SignalDirection.None` (filter blocks)

## Position in Pipeline

Filters appear in the `FiltersTree`, which is evaluated only after the `SignalsTree` validates. If the filter returns `None`, the pattern direction is blocked. If the filter expires (falls out of the `FiltersTree.Range`), the entire pattern resets.

```
Pattern.Evaluate()
  ├── SignalsTree  → Direction determined
  └── FiltersTree  → Gate: confirm or reject
        └── ValueInRangeFilter(indicator)
              └── indicator.Values[0] in [Min, Max]?
```

## Example

```csharp
// Filter: only trade when RSI is between 30 and 70
var rsiFilter = new ValueInRangeFilter(strategy, rsiIndicator)
{
    Min = 30,
    Max = 70
};
pattern.Filters.Root.Add(rsiFilter);
```

## See Also

- [Pipeline](pipeline.md) — execution order of components
- [Decision Tree](decision-tree.md) — tree structure and evaluation logic
- [Signal Base Classes](signals/signal-base.md) — `Signal` base class
