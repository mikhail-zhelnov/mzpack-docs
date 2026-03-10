---
sidebar_position: 2
title: "StrategyVolumeDeltaIndicator"
description: "Reference for StrategyVolumeDeltaIndicator — the strategy wrapper for mzVolumeDelta providing volume and delta data access."
---

# StrategyVolumeDeltaIndicator

`StrategyVolumeDeltaIndicator` wraps [mzVolumeDelta](/docs/indicators/mzVolumeDelta) for use inside MZpack strategies. It implements [IVolumeDeltaIndicator](ivolume-delta-indicator.md).

**Namespace:** `MZpack.NT8.Algo.Indicators`
**Inheritance:** `StrategyVolumeDeltaIndicator : mzVolumeDelta, IVolumeDeltaIndicator`
**Conditional:** `#if !FREE`
**Data level:** Level 1
**Source:** `MZpack.NT8/Algo/Indicators/StrategyVolumeDeltaIndicator.cs`

## Setup in a Strategy

```csharp
public class MyStrategy : MZpackStrategyBase
{
    StrategyVolumeDeltaIndicator vdIndicator;

    protected override void OnStateChange()
    {
        if (State == State.Configure)
        {
            vdIndicator = new StrategyVolumeDeltaIndicator(this, "VD");

            // Configure
            vdIndicator.VolumeDeltaMode = VolumeDeltaMode.Delta;
            vdIndicator.DeltaMode = DeltaMode.PerBar;
            vdIndicator.CumulateSession = true;
            vdIndicator.TradeFilterMin = 0;
        }
    }
}
```

## Accessing Data

```csharp
protected override void OnBarUpdate()
{
    if (CurrentBar < 1) return;

    // Get the current bar's volume/delta data
    IVolumeDeltaBar bar = vdIndicator.VolumeDeltaBars[CurrentBar];

    // Use delta and cumulative delta for trading logic
}
```

## See Also

- [IVolumeDeltaIndicator](ivolume-delta-indicator.md) — interface reference
- [Data Access — mzVolumeDelta](../../samples/data-access-volume-delta.md) — sample code
