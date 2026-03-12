---
sidebar_position: 6
title: "Data Access — mzFootprint"
description: "Access StrategyFootprintIndicator data — bar stats, POC/VA, delta, imbalances, SR zones, cluster zones, and session profile."
---

# Data Access — mzFootprint

Demonstrates how to access footprint bar data from `StrategyFootprintIndicator`. The `OnBarCloseHandler` prints bar statistics, POC/VA levels, imbalances, SR zones, cluster zones, and session profile values.

**Source:** `[INSTALL PATH]/API/Samples/Built-in/DataAccess_mzFootprint.cs`
**Class:** `DataAccess_mzFootprint : MZpackStrategyBase`

## Indicator Setup

```csharp
footprintIndicator = new StrategyFootprintIndicator(this, @"Footprint")
{
    LeftFootprintStyle = FootprintStyle.Delta,
    RightFootprintStyle = FootprintStyle.Volume,
    TicksPerLevel = 1,

    // Session profile levels
    ShowSessionPOC = true,
    ShowSessionVA = true,
    SessionDailyProfileMode = SessionDailyProfileMode.Session,
    SessionVAIsDeveloping = true,

    // Bar POC/VA
    ShowBarVA = true,
    BarVAPercentage = 70,
    ShowBarPOC = true,
    ShowBarPOCCount = 3,

    // Bar stats
    ShowBarVolume = true,
    ShowBarDelta = true,
    ShowBarCOT = true,
    ShowBarRatioNumbers = true,
    BarRatioNumbersBoundsLow = 0.4,
    BarRatioNumbersBoundsHigh = 77,

    // Imbalances
    ShowImbalance = true,
    ImbalancePercentage = 200,
    ImbalanceFilter = 20,
    ImbalanceMarker = FootprintImbalanceMarker.Always,

    // Imbalance SR Zones
    ShowImbalanceSRZones = true,
    ImbalanceSRZonesConsecutiveLevels = 2,
    ImbalanceSRZonesVolumeFilter = 200,
    ImbalanceSRZoneEnding = SRZoneEnding.ByBarPOC,
    ImbalanceSRZonesBreakOnSession = true,

    // Absorptions
    ShowAbsorption = true,
    AbsorptionPercentage = 300,
    AbsorptionDepth = 2,
    AbsorptionFilter = 200,

    // Unfinished Auction
    ShowUnfinishedAuction = true
};

// Cluster zones on right footprint
footprintIndicator.FootprintPresentation[FootprintBaseMVC.RIGHT_FOOTPRINT]
    .ClusterZonesShow = true;
footprintIndicator.FootprintPresentation[FootprintBaseMVC.RIGHT_FOOTPRINT]
    .ClusterZonesFilterMin = 4000;

// Statistic Grid with predicted values
footprintIndicator.StatisticGridShow = true;
footprintIndicator.StatisticGridPredictedValuesShow = true;
```

Important: set `footprintIndicator.Calculate = Calculate.OnBarClose` in `State.Configure` when using `OnBarCloseHandler`.

## Accessing IFootprintBar

```csharp
void StrategyOnBarCloseHandler(MarketDataEventArgs e, int currentBarIdx)
{
    if (footprintIndicator.FootprintBars.ContainsKey(currentBarIdx))
    {
        IFootprintBar bar = footprintIndicator.FootprintBars[currentBarIdx];
        // ...
    }
}
```

### Bar Statistics

```csharp
bar.RangeTicks          // Bar range in ticks
bar.RangeLevels         // Bar range in levels (depends on TicksPerLevel)
bar.Volume              // Total volume (use FromInternalVolume() for crypto)
bar.Delta               // Total delta
bar.COTHigh             // COT high
bar.COTLow              // COT low
bar.DeltaRate           // Delta rate
bar.DeltaRateHigh       // Delta rate high
bar.DeltaRateLow        // Delta rate low
```

For crypto, convert volumes: `footprintIndicator.FromInternalVolume(bar.Volume)`.

### Predicted Values (Real-Time Only)

```csharp
if (State == State.Realtime)
{
    bar.VolumePredicted     // Predicted volume
    bar.COTHighPredicted    // Predicted COT high
    bar.COTLowPredicted     // Predicted COT low
}
```

### POC and Value Area

```csharp
// Single POC
bar.POC           // POC price
bar.POCVolume     // POC volume
bar.VAH           // Value Area High
bar.VAL           // Value Area Low

// Multiple POCs (ordered by volume)
foreach (var poc in bar.MultiplePOC)
{
    double price = poc.Key;
    long volume = poc.Value;
}
```

### Imbalances

```csharp
// Sell imbalances (bid side)
foreach (var item in bar.Imbalances[(int)TradeSide.Bid])
{
    long volume = item.Value;
    double price = item.Key;
}

// Buy imbalances (ask side)
foreach (var item in bar.Imbalances[(int)TradeSide.Ask])
{
    long volume = item.Value;
    double price = item.Key;
}
```

### Imbalance SR Zones

```csharp
// Bar-level zones
foreach (ISRZone zone in bar.ImbalanceSRZones.Zones[(int)TradeSide.Ask])
{
    long volume = zone.Volume;
    double high = zone.Hi;
    double low = zone.Lo;
}

// Total volume using LINQ
if (bar.ImbalanceSRZones.HasZones(TradeSide.Ask))
{
    long total = bar.ImbalanceSRZones.Zones[(int)TradeSide.Ask]
        .Sum(z => z.Volume);
}

// Live zones (not yet ended)
List<ISRZone> liveZones = footprintIndicator
    .LiveSRZones(SRZoneType.Imbalance, TradeSide.Ask);

// Ended zones (broken by price)
foreach (ISRZone zone in bar.ImbalanceSRZones.EndedZones[(int)TradeSide.Ask])
{
    // zone.Hi, zone.Lo, zone.Volume
}
```

### Cluster Zones

```csharp
// Live cluster zones
foreach (IClusterZone zone in footprintIndicator
    .LiveClusterZones(FootprintBaseMVC.RIGHT_FOOTPRINT))
{
    double value = zone.Value;
    double price = zone.Price;
    int beginBar = zone.BeginBar.BarIdx;
}

// Ended cluster zones
foreach (IClusterZone zone in footprintIndicator
    .EndedClusterZones(FootprintBaseMVC.RIGHT_FOOTPRINT))
{
    int beginBar = zone.BeginBar.BarIdx;
    int endBar = zone.EndBar.BarIdx;
}
```

### Session Profile

```csharp
ISession currentSession = footprintIndicator.Sessions.LastOrDefault();
if (currentSession != null)
{
    double poc = currentSession.POC;
    double vah = currentSession.VAH;
    double val = currentSession.VAL;
}
```

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzVolumeDelta](data-access-volume-delta.md) — volume delta data
- [Data Access — mzVolumeProfile](data-access-volume-profile.md) — volume profile data
- [Custom Plots](custom-plots.md) — plotting footprint data
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
