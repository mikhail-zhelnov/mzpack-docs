---
sidebar_position: 2
title: "StrategyDeltaDivergenceIndicator"
description: "Reference for StrategyDeltaDivergenceIndicator — the strategy wrapper for mzDeltaDivergence providing divergence signal access."
---

# StrategyDeltaDivergenceIndicator

`StrategyDeltaDivergenceIndicator` wraps [mzDeltaDivergence](/docs/indicators/mzDeltaDivergence) for use inside MZpack strategies. It implements [IDeltaDivergenceIndicator](idelta-divergence-indicator.md) and inherits all volume/delta properties from [IVolumeDeltaIndicator](../volume-delta/ivolume-delta-indicator.md).

**Namespace:** `MZpack.NT8.Algo.Indicators`
**Inheritance:** `StrategyDeltaDivergenceIndicator : mzDeltaDivergence, IDeltaDivergenceIndicator`
**Conditional:** `#if !FREE`
**Data level:** Level 1
**Source:** `[INSTALL PATH]/API/Indicators/StrategyDeltaDivergenceIndicator.cs`

## Setup in a Strategy

```csharp
public class MyStrategy : MZpackStrategyBase
{
    StrategyDeltaDivergenceIndicator ddIndicator;

    protected override void OnStateChange()
    {
        if (State == State.Configure)
        {
            ddIndicator = new StrategyDeltaDivergenceIndicator(this, "DD");

            // ZigZag settings
            ddIndicator.ZigzagDeviationType = DeviationType.Percentage;
            ddIndicator.ZigzagDeviationThreshold = 0.3;
            ddIndicator.ZigzagUseHighLow = true;

            // Delta deviation filter
            ddIndicator.DeltaDeviationType = DeviationType.Value;
            ddIndicator.DeltaDeviationMin = 500;

            // Display
            ddIndicator.BreakPointShow = true;
            ddIndicator.BuySellAreasShow = true;
        }
    }
}
```

## Accessing Data

```csharp
protected override void OnBarUpdate()
{
    if (CurrentBar < 10) return;

    Divergences divergences = ddIndicator.Divergences;
    if (divergences == null || divergences.Count == 0) return;

    // Get the most recent divergence
    IDivergence lastDiv = divergences[divergences.Count - 1];

    if (lastDiv.IsBuy())
    {
        // Bullish divergence detected
        // Price made a lower low while delta made a higher low
        double deltaChange = lastDiv.GetDeltaChange(DeviationType.Value);
        double priceChange = lastDiv.GetPriceChange(DeviationType.Value);
    }
    else if (lastDiv.IsSell())
    {
        // Bearish divergence detected
        // Price made a higher high while delta made a lower high
    }
}
```

## See Also

- [IDeltaDivergenceIndicator](idelta-divergence-indicator.md) — interface reference
