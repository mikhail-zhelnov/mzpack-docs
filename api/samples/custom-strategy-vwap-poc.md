---
sidebar_position: 17
title: "Custom Strategy — VWAP/POC"
description: "StrategyVolumeProfileIndicator with VWAP/POC rules for backtesting (OnBarClose)"
---

# Custom Strategy — VWAP/POC

Demonstrates a custom strategy (without Algo.Strategy) that uses `StrategyVolumeProfileIndicator` with VWAP standard deviation and a running average POC calculation. Uses NinjaTrader `EnterLong`/`EnterShort` directly with `OnBarCloseHandler` logic, suitable for backtesting in Strategy Analyzer.

**Source:** `[INSTALL PATH]/API/Samples/MZpackCustomStrategy0.cs`
**Class:** `MZpackCustomStrategy0 : MZpackStrategyBase`

## What It Covers

- `StrategyVolumeProfileIndicator` with session profiles and VWAP with standard deviation
- `OnBarCloseHandler` strategy logic: SHORT above positive deviation + above average POC; LONG below negative deviation + below average POC
- Running POC calculation over configurable bars back
- `EnableBacktesting = true` for Strategy Analyzer compatibility
- Profile access via `(sessionVPIndicator.Profiles as Model).GetItemByBarIdx(currentBarIdx)`

## Indicator Setup

```csharp
sessionVPIndicator = new StrategyVolumeProfileIndicator(this, @"Session Volume Profile")
{
    ProfileCreation = ProfileCreation.Session,
    ShowProfileType = ProfileType.VP,
    Sigma1 = VP_Sigma1,
    VWAPMode = VWAPMode.DynamicStdDev1,
    ProfileWidthPercentage = 20,
    POCMode = LevelMode.Developing,
    VAHVALMode = LevelMode.Off,
    StackedProfileCreation1 = ProfileCreation.None,
    StackedProfileCreation2 = ProfileCreation.None,
    StackedProfileCreation3 = ProfileCreation.None
};
```

## Core Strategy Logic

The `OnBarCloseHandler` computes VWAP deviation bands and a running average POC, then enters short when price closes above the positive deviation and above average POC, or enters long when price closes below the negative deviation and below average POC:

```csharp
protected void StrategyOnBarCloseHandler(MarketDataEventArgs e, int currentBarIdx)
{
    IVolumeProfile profile = (sessionVPIndicator.Profiles as Model)
        .GetItemByBarIdx(currentBarIdx) as IVolumeProfile;

    if (profile != null)
    {
        double positiveDeviation1 = profile.VWAP + profile.Deviation * sessionVPIndicator.Sigma1;
        double negativeDeviation1 = profile.VWAP - profile.Deviation * sessionVPIndicator.Sigma1;

        // Running average POC
        if (profile.POCs.Count == 1)
            runningPOC = 0;
        runningPOC += profile.POCs[currentBarIdx];
        if (profile.POCs.Count > Strategy_AveragePOCBarsBack)
            runningPOC -= profile.POCs[currentBarIdx - (Strategy_AveragePOCBarsBack - 1)];
        double averagePOC = runningPOC / Math.Min(Strategy_AveragePOCBarsBack, profile.POCs.Count);

        // Short
        if (Close[1] > positiveDeviation1 && averagePOC < Close[1])
        {
            string signalShort = string.Format("stdDev1:{0:N2} av.POC:{1:N2}",
                positiveDeviation1, averagePOC);
            SetProfitTarget(signalShort, CalculationMode.Ticks, Strategy_TakeProfitTicks);
            SetStopLoss(signalShort, CalculationMode.Ticks, Strategy_StopLossTicks, false);
            EnterShort(signalShort);
        }
        // Long
        else if (Close[1] < negativeDeviation1 && averagePOC > Close[1])
        {
            string signalLong = string.Format("stdDev1:{0:N2} av.POC:{1:N2}",
                negativeDeviation1, averagePOC);
            SetProfitTarget(signalLong, CalculationMode.Ticks, Strategy_TakeProfitTicks);
            SetStopLoss(signalLong, CalculationMode.Ticks, Strategy_StopLossTicks, false);
            EnterLong(signalLong);
        }
    }
}
```

## Configurable Properties

### Strategy

| Property | Default | Description |
|---|---|---|
| `Strategy_AveragePOCBarsBack` | `30` | Bars back for average POC calculation |
| `Strategy_TakeProfitTicks` | `90` | Take profit ticks |
| `Strategy_StopLossTicks` | `12` | Stop loss ticks |

### Volume Profile

| Property | Default | Description |
|---|---|---|
| `VP_ProfileMode` | `Volume` | Profile mode |
| `VP_TicksPerLevel` | `1` | Ticks per level |
| `VP_Sigma1` | `1` | Standard deviation multiplier |
| `VP_VWAPStroke` | Red, Dash, 3 | VWAP line style |
| `VP_Deviation1Stroke` | Green | 1st deviation line style |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzVolumeProfile](data-access-volume-profile.md) — volume profile data access
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
