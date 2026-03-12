---
sidebar_position: 12
title: "Multi-DataSeries Strategy"
description: "StrategyFootprintIndicator and StrategyVolumeProfileIndicator on different data series with manual on-bar-close emulation."
---

# Multi-DataSeries Strategy

Demonstrates using indicators attached to different data series. A `StrategyFootprintIndicator` runs on the primary data series and a `StrategyVolumeProfileIndicator` runs on a secondary 30-minute series. Prints bar data from both indicators on bar close.

**Source:** `[INSTALL PATH]/API/Samples/MultiDataSeriesStrategy.cs`
**Class:** `MultiDataSeriesStrategy : MZpackStrategyBase`

## What It Covers

- Two indicators on different `DataSeriesIndex` values
- `AddDataSeries(BarsPeriodType.Minute, 30)` for the secondary series
- `OnEachTickHandler` with manual on-bar-close emulation (`BarsInProgress == 0 && currentBarIdx > lastBarIdx`)
- Footprint with full feature set (imbalances, SR zones, absorptions, cluster zones, statistic grid)
- Volume profile with session profiles and developing POC
- `EnableBacktesting = true`

## Indicator Setup

### Footprint (Primary Data Series)

```csharp
footprintIndicator = new StrategyFootprintIndicator(this, @"Footprint")
{
    DataSeriesIndex = 0,  // Primary data series (default)
    LeftFootprintStyle = FootprintStyle.Delta,
    RightFootprintStyle = FootprintStyle.Volume,
    TicksPerLevel = 1,
    ShowSessionPOC = true,
    ShowSessionVA = true,
    SessionDailyProfileMode = SessionDailyProfileMode.Session,
    SessionVAIsDeveloping = true,
    ShowBarVA = true,
    BarVAPercentage = 70,
    ShowBarPOC = true,
    ShowBarPOCCount = 3,
    ShowBarVolume = true,
    ShowBarDelta = true,
    ShowBarCOT = true,
    ShowBarRatioNumbers = true,
    ShowImbalance = true,
    ImbalancePercentage = 200,
    ImbalanceFilter = 20,
    ImbalanceMarker = FootprintImbalanceMarker.Always,
    ShowImbalanceSRZones = true,
    ImbalanceSRZonesConsecutiveLevels = 2,
    ImbalanceSRZonesVolumeFilter = 200,
    ImbalanceSRZoneEnding = SRZoneEnding.ByBarPOC,
    ShowAbsorption = true,
    AbsorptionPercentage = 300,
    AbsorptionDepth = 2,
    AbsorptionFilter = 200,
    ShowUnfinishedAuction = true
};
```

### Cluster Zones and Statistic Grid

```csharp
footprintIndicator.FootprintPresentation[FootprintBaseMVC.RIGHT_FOOTPRINT]
    .ClusterZonesShow = true;
footprintIndicator.FootprintPresentation[FootprintBaseMVC.RIGHT_FOOTPRINT]
    .ClusterZonesFilterMin = 4000;

footprintIndicator.StatisticGridShow = true;
footprintIndicator.StatisticGridPredictedValuesShow = true;
footprintIndicator.StatisticGridPredictedValuesGaugeShow = true;
```

### Volume Profile (Secondary Data Series)

```csharp
volumeProfileIndicator = new StrategyVolumeProfileIndicator(this, @"VolumeProfile")
{
    DataSeriesIndex = 1,  // Secondary data series
    Calculate = Calculate.OnBarClose,
    ShowProfileType = ProfileType.VP,
    ProfileCreation = ProfileCreation.Session,
    POCMode = LevelMode.Developing,
    VAHVALMode = LevelMode.On,
    VWAPMode = VWAPMode.DynamicStdDev1,
    ProfileWidthPercentage = 20,
    Values1KDivider = false,
    StackedProfileCreation1 = ProfileCreation.None,
    StackedProfileCreation2 = ProfileCreation.None,
    StackedProfileCreation3 = ProfileCreation.None
};
```

## Configuration

In `State.Configure`, add the secondary data series and set the footprint to on-bar-close:

```csharp
AddDataSeries(BarsPeriodType.Minute, 30);
footprintIndicator.Calculate = Calculate.OnBarClose;
```

## Data Access

`IsFirstTickOfBar` does not work correctly in `OnMarketData` for multi-series strategies. Use `BarsInProgress == 0 && currentBarIdx > lastBarIdx` to emulate on-bar-close behavior:

```csharp
protected void StrategyOnEachTickHandler(MarketDataEventArgs e, int currentBarIdx)
{
    if (BarsInProgress == 0 && currentBarIdx > lastBarIdx)
    {
        if (footprintIndicator.FootprintBars.ContainsKey(lastBarIdx))
        {
            IFootprintBar bar = footprintIndicator.FootprintBars[lastBarIdx];
            Print("Footprint (" + footprintIndicator.Instrument.FullName
                + ") bar volume : " + footprintIndicator.FromInternalVolume(bar.Volume));

            IVolumeProfile last = volumeProfileIndicator.Profiles.LastOrDefault()
                as IVolumeProfile;
            if (last != null)
                Print("Volume profile (" + volumeProfileIndicator.Instrument.FullName
                    + ") total volume : " + volumeProfileIndicator.FromInternalVolume(last.Volume));
        }
        lastBarIdx = currentBarIdx;
    }
}
```

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzFootprint](data-access-footprint.md) — footprint data access
- [Data Access — mzVolumeProfile](data-access-volume-profile.md) — volume profile data access
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
