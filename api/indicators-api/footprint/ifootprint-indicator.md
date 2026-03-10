---
sidebar_position: 1
title: "IFootprintIndicator"
description: "Reference for the IFootprintIndicator interface — access to footprint bars, sessions, imbalance/absorption zones, and cluster data."
---

# IFootprintIndicator

`IFootprintIndicator` provides programmatic access to the [mzFootprint](/docs/indicators/mzFootprint) chart indicator. It exposes footprint bar data, trading sessions, S/R zones, cluster zones, and all indicator settings.

**Namespace:** `MZpack`
**Inheritance:** `IFootprintIndicator : IOrderFlowIndicator : ITickIndicator : IIndicator`
**Source:** `MZpackBase/mzFootprint/IFootprintIndicator.cs`

## Key Data Properties

These properties are available in `#if DATA` builds only.

| Property | Type | Description |
|---|---|---|
| `FootprintBars` | `Dictionary<int, IFootprintBar>` | All footprint bars indexed by bar index |
| `Sessions` | `List<ISession>` | Trading sessions defined by Trading Hours |

## Key Data Methods

| Method | Return Type | Description |
|---|---|---|
| `GetSession(DateTime time)` | `ISession` | Get the session containing the specified time |
| `LiveSRZones(SRZoneType type, TradeSide side)` | `List<ISRZone>` | Get active S/R zones by type (Imbalance or Absorption) and side |
| `LiveClusterZones(int footprint)` | `List<IClusterZone>` | Get active cluster zones for a footprint index (0 = left, 1 = right) |
| `EndedClusterZones(int footprint)` | `List<IClusterZone>` | Get ended cluster zones for a footprint index |
| `RefreshModel(RefreshModelArgs args)` | `void` | Force a model refresh |

## Footprint Configuration Properties

| Property | Type | Description |
|---|---|---|
| `FootprintPresentation` | `FootprintPresentation[]` | Left and right footprint presentation modes |
| `LeftFootprintStyle` | `FootprintStyle` | Style of the left footprint column |
| `RightFootprintStyle` | `FootprintStyle` | Style of the right footprint column |
| `TicksPerLevel` | `int` | Number of ticks per price level (level aggregation) |
| `TradeFilterMin` | `double` | Minimum trade size filter |
| `TradeFilterMax` | `double` | Maximum trade size filter |
| `DisplayValueFilter` | `double` | Minimum value to display in cells |

## Bar Statistics Properties

| Property | Type | Description |
|---|---|---|
| `ShowBarVolume` | `bool` | Show total volume per bar |
| `ShowBarDelta` | `bool` | Show delta per bar |
| `ShowBarMinMaxDelta` | `bool` | Show min/max delta per bar |
| `ShowBarDeltaPercent` | `bool` | Show delta as percentage |
| `ShowBarCOT` | `bool` | Show COT (Commitment of Traders) |
| `ShowBarAbsoluteDeltaAverage` | `bool` | Show absolute delta average |
| `ShowBarRatioNumbers` | `bool` | Show ratio of buy/sell trade counts |
| `ShowBarPOC` | `bool` | Show bar POC level |
| `ShowBarPOCCount` | `int` | Number of POC levels to show |
| `ShowBarVA` | `bool` | Show bar Value Area |
| `BarVAPercentage` | `float` | Value Area percentage (e.g. 0.70 for 70%) |

## Session Properties

| Property | Type | Description |
|---|---|---|
| `ShowSessionPOC` | `bool` | Show session POC level |
| `SessionPOCIsDeveloping` | `bool` | POC updates in real-time |
| `ShowSessionVA` | `bool` | Show session Value Area |
| `SessionVAIsDeveloping` | `bool` | Value Area updates in real-time |
| `SessionVAPercentage` | `float` | Session Value Area percentage |

## Imbalance Properties

| Property | Type | Description |
|---|---|---|
| `ShowImbalance` | `bool` | Enable imbalance detection |
| `ImbalancePercentage` | `double` | Imbalance ratio threshold |
| `ImbalanceFilter` | `double` | Minimum volume for imbalance |
| `ImbalanceMarker` | `FootprintImbalanceMarker` | Marker style |
| `ImbalanceMarkerType` | `FootprintImbalanceMarkerType` | Marker type |
| `ShowImbalanceSRZones` | `bool` | Show imbalance-based S/R zones |
| `ImbalanceSRZonesConsecutiveLevels` | `int` | Minimum stacked levels to form a zone |
| `ImbalanceSRZonesVolumeFilter` | `double` | Volume filter for S/R zones |

## Absorption Properties

| Property | Type | Description |
|---|---|---|
| `ShowAbsorption` | `bool` | Enable absorption detection |
| `AbsorptionPercentage` | `double` | Absorption ratio threshold |
| `AbsorptionDepth` | `int` | Depth of absorption analysis |
| `AbsorptionFilter` | `double` | Minimum volume for absorption |
| `ShowAbsorptionSRZones` | `bool` | Show absorption-based S/R zones |
| `AbsorptionSRZonesConsecutiveLevels` | `int` | Minimum stacked levels to form a zone |

## Example: Access Footprint Data

```csharp
IFootprintIndicator footprint = ...; // from strategy or chart

// Get footprint bar for the current bar
IFootprintBar bar = footprint.FootprintBars[CurrentBar];

// Read bar-level data
long delta = bar.Delta;
double poc = bar.POC;
long volume = bar.Volume;
long buyVol = bar.BuyVolume;
long sellVol = bar.SellVolume;

// Iterate over price levels
foreach (var kvp in bar.Volumes)
{
    double price = kvp.Key;
    long levelVolume = kvp.Value;
    long buyVolume = bar.BuyVolumes[price];
    long sellVolume = bar.SellVolumes[price];
}

// Get current session
ISession session = footprint.GetSession(DateTime.Now);
double sessionPOC = session.POC;

// Get live imbalance S/R zones
List<ISRZone> buyZones = footprint.LiveSRZones(SRZoneType.Imbalance, TradeSide.Ask);
```

## See Also

- [IFootprintBar / ISession](ifootprint-bar.md) — footprint bar and session data structures
- [StrategyFootprintIndicator](strategy-footprint-indicator.md) — strategy wrapper class
- [Data Access — mzFootprint](../../samples/data-access-footprint.md) — sample code
