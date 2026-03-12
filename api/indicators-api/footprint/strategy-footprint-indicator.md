---
sidebar_position: 3
title: "StrategyFootprintIndicator"
description: "Reference for StrategyFootprintIndicator — the strategy wrapper for mzFootprint providing footprint data access in automated strategies."
---

# StrategyFootprintIndicator

`StrategyFootprintIndicator` wraps [mzFootprint](/docs/indicators/mzFootprint) for use inside MZpack strategies. It implements [IFootprintIndicator](ifootprint-indicator.md), so all data access is identical to the chart indicator.

**Namespace:** `MZpack.NT8.Algo.Indicators`
**Inheritance:** `StrategyFootprintIndicator : mzFootprint, IFootprintIndicator`
**Data level:** Level 1
**Source:** `[INSTALL PATH]/API/Indicators/StrategyFootprintIndicator.cs`

## Setup in a Strategy

```csharp
public class MyStrategy : MZpackStrategyBase
{
    StrategyFootprintIndicator footprint;

    protected override void OnStateChange()
    {
        if (State == State.Configure)
        {
            // Create the indicator
            footprint = new StrategyFootprintIndicator(this, "Footprint");

            // Configure settings
            footprint.TicksPerLevel = 1;
            footprint.TradeFilterMin = 0;
            footprint.ShowImbalance = true;
            footprint.ImbalancePercentage = 300;
            footprint.ShowAbsorption = true;
        }
    }
}
```

## Accessing Data

```csharp
protected override void OnBarUpdate()
{
    if (CurrentBar < 1) return;

    // Get the current footprint bar
    IFootprintBar bar = footprint.FootprintBars[CurrentBar];

    // Bar-level data
    long delta = bar.Delta;
    double poc = bar.POC;
    long volume = bar.Volume;
    long buyVolume = bar.BuyVolume;
    long sellVolume = bar.SellVolume;

    // Per-level data
    foreach (var kvp in bar.Volumes)
    {
        double price = kvp.Key;
        long levelVolume = kvp.Value;
    }

    // Imbalance check
    if (bar.BuyImbalanceCount >= 3)
    {
        // Stacked buy imbalances detected
    }

    // Session data
    ISession session = footprint.GetSession(Time[0]);
    double sessionPOC = session.POC;
    long sessionDelta = session.Delta;
}
```

## Exported Values

StrategyFootprintIndicator exports 50+ values for use in data export and strategy plots:

| Category | Values |
|---|---|
| **OHLC** | Open, High, Low, Close |
| **Volume** | Volume, BuyVolume, SellVolume |
| **Delta** | Delta, MinDelta, MaxDelta, DeltaChange, DeltaCumulative, DeltaRate |
| **Value Area** | POC, POCVolume, VAH, VAL |
| **Session** | SessionPOC, SessionVAH, SessionVAL, SessionOpen, SessionClose, SessionHigh, SessionLow |
| **Per-level** | Volumes, Deltas, Bids, Asks, TradesNumbers (as arrays) |

## See Also

- [IFootprintIndicator](ifootprint-indicator.md) — interface reference
- [IFootprintBar / ISession](ifootprint-bar.md) — data structures
- [Data Access — mzFootprint](../../samples/data-access-footprint.md) — sample code
