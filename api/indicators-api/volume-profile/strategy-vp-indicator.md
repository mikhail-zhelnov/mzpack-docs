---
sidebar_position: 4
title: "StrategyVolumeProfileIndicator"
description: "Reference for StrategyVolumeProfileIndicator — the strategy wrapper for mzVolumeProfile providing volume profile data access in automated strategies."
---

# StrategyVolumeProfileIndicator

`StrategyVolumeProfileIndicator` wraps [mzVolumeProfile](/docs/indicators/mzVolumeProfile) for use inside MZpack strategies. It implements [IVolumeProfileIndicator](ivolume-profile-indicator.md), so all data access is identical to the chart indicator.

**Namespace:** `MZpack.NT8.Algo.Indicators`
**Inheritance:** `StrategyVolumeProfileIndicator : mzVolumeProfile, IVolumeProfileIndicator`
**Data level:** Level 1
**Source:** `MZpack.NT8/Algo/Indicators/StrategyVolumeProfileIndicator.cs`

## Setup in a Strategy

```csharp
public class MyStrategy : MZpackStrategyBase
{
    StrategyVolumeProfileIndicator vpIndicator;

    protected override void OnStateChange()
    {
        if (State == State.Configure)
        {
            vpIndicator = new StrategyVolumeProfileIndicator(this, "VP");

            // Configure profile creation
            vpIndicator.ProfileCreation = ProfileCreation.Session;
            vpIndicator.ShowProfileType = ProfileType.VP;
            vpIndicator.TicksPerLevel = 1;
            vpIndicator.VAPercentage = 0.70f;

            // For backtesting, use Minute accuracy
            vpIndicator.ProfileAccuracy = ProfileAccuracy.Minute;
        }
    }
}
```

:::note
For backtesting with `OnBarClose`, use `ProfileAccuracy.Minute`. Tick accuracy requires Tick Replay or live data.
:::

## Accessing Data

```csharp
protected override void OnBarUpdate()
{
    if (CurrentBar < 1) return;

    // Get the most recent profile
    IVolumeProfile profile = vpIndicator.GetProfile(0);
    if (profile == null || profile.IsEmpty) return;

    // Key levels
    double poc = profile.POC;
    double vah = profile.VAH;
    double val = profile.VAL;
    double vwap = profile.VWAP;

    // Standard deviations
    double upper1SD = profile._1StdDeviationPos;
    double lower1SD = profile._1StdDeviationNeg;

    // Volume data
    long totalVolume = profile.Volume;
    long delta = profile.Delta;

    // Price position relative to Value Area
    double price = Close[0];
    if (price > vah)
    {
        // Price above Value Area
    }
    else if (price < val)
    {
        // Price below Value Area
    }
    else
    {
        // Price inside Value Area
    }

    // Find nearest VAH/VAL from all profiles
    foreach (IModelItem2 item in vpIndicator.Profiles)
    {
        IVolumeProfile p = item as IVolumeProfile;
        if (p == null) continue;

        double pVAH = p.VAH;
        double pVAL = p.VAL;
    }
}
```

## Exported Values

StrategyVolumeProfileIndicator exports 20+ values for data export and strategy plots:

| Category | Values |
|---|---|
| **OHLC** | Open, High, Low, Close, MID |
| **Duration** | DurationMs, RangeTicks |
| **Volume** | Volume, BuyVolume, SellVolume, TradesNumber |
| **Delta** | Delta, DeltaPercentage |
| **Value Area** | VAH, VAL, POC, POCVolume, TickPOC, TickPOCVolume |
| **VWAP** | VWAP, _1StdDeviationPos/Neg, _2StdDeviationPos/Neg |
| **POC breakdown** | BuyPOCVolume, SellPOCVolume, VAVolume |
| **TPO** | TPO_POC, TPO_VAH, TPO_VAL, TPOLettersCount |

## See Also

- [IVolumeProfileIndicator](ivolume-profile-indicator.md) — interface reference
- [IVolumeProfile / Profile2](ivolume-profile.md) — profile data structure
- [Data Access — mzVolumeProfile](../../samples/data-access-volume-profile.md) — sample code
