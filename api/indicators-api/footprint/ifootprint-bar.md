---
sidebar_position: 2
title: "IFootprintBar / ISession"
description: "Reference for IFootprintBar and ISession — footprint bar structure with per-level bid/ask volumes, delta, imbalance, and absorption data."
---

# IFootprintBar / ISession

`IFootprintBar` represents a single footprint bar with per-price-level bid/ask volumes, delta, imbalance, absorption, and bar statistics. `ISession` extends `IFootprintBar` with session-level aggregations.

**Namespace:** `MZpack`
**Inheritance:** `IFootprintBar : IModelItem, IBaseVisual`
**Source:** `MZpackBase/mzFootprint/IFootprintBar.cs`

## OHLC and Time Properties

| Property | Type | Description |
|---|---|---|
| `Open` | `double` | Bar open price |
| `Close` | `double` | Bar close price |
| `Hi` | `double` | Bar high price |
| `Lo` | `double` | Bar low price |
| `Time` | `DateTime` | Bar close time |
| `OpenTime` | `DateTime` | Bar open time |
| `BarIdx` | `int` | Bar index in the chart |
| `RangeTicks` | `int` | Bar range in ticks |
| `RangeLevels` | `int` | Number of price levels in the bar |
| `DurationMs` | `double` | Bar duration in milliseconds |
| `IsFirstBarOfSession` | `bool` | Whether this bar starts a new session |

## Volume and Delta Properties

| Property | Type | Description |
|---|---|---|
| `Volume` | `long` | Total volume |
| `BuyVolume` | `long` | Buy (ask) volume |
| `SellVolume` | `long` | Sell (bid) volume |
| `Delta` | `long` | Delta (BuyVolume - SellVolume) |
| `POC` | `double` | Point of Control price |
| `POCVolume` | `long` | Volume at POC |
| `POCVolumes` | `long[]` | POC volumes for left/right footprint |
| `VAH` | `double` | Value Area High |
| `VAL` | `double` | Value Area Low |
| `TradesNumber` | `long` | Number of trades |
| `TradesNumbers` | `SortedDictionary<double, int>` | Trade count per price level |
| `Session` | `ISession` | Parent session |

## Per-Level Data

| Property | Type | Description |
|---|---|---|
| `Volumes` | `SortedDictionary<double, long>` | Total volume at each price level |
| `BuyVolumes` | `SortedDictionary<double, long>` | Buy volume at each price level |
| `SellVolumes` | `SortedDictionary<double, long>` | Sell volume at each price level |
| `Deltas` | `SortedDictionary<double, long>` | Delta at each price level |

## Advanced Delta Properties

| Property | Type | Description |
|---|---|---|
| `MinDelta` | `long` | Minimum delta reached during bar |
| `MaxDelta` | `long` | Maximum delta reached during bar |
| `DeltaPercentage` | `double` | Delta as percentage of volume |
| `AbsoluteDeltaAverage` | `long` | Average absolute delta per level |
| `DeltaCumulative` | `long` | Cumulative delta from session start |
| `DeltaChange` | `long` | Delta change from previous bar |
| `DeltaRate` | `long` | Delta rate of change |
| `COTHigh` | `long` | COT value at bar high |
| `COTLow` | `long` | COT value at bar low |
| `RatioNumbers` | `double` | Ratio of buy to sell trade counts |
| `UnfinishedAuctionHigh` | `double` | Unfinished auction at high |
| `UnfinishedAuctionLow` | `double` | Unfinished auction at low |

## Imbalance and Absorption

| Property | Type | Description |
|---|---|---|
| `Imbalances` | `SortedDictionary<double, long>[]` | Imbalance levels [0]=buy, [1]=sell |
| `BuyImbalanceCount` | `int` | Number of buy imbalance levels |
| `SellImbalanceCount` | `int` | Number of sell imbalance levels |
| `Absorptions` | `SortedDictionary<double, long>[]` | Absorption levels [0]=buy, [1]=sell |
| `BuyAbsorptionCount` | `int` | Number of buy absorption levels |
| `SellAbsorptionCount` | `int` | Number of sell absorption levels |
| `ImbalanceSRZones` | `IBarSRZones` | Imbalance-based S/R zones |
| `AbsorptionSRZones` | `IBarSRZones` | Absorption-based S/R zones |

## Predicted Values

These properties extrapolate current bar data to estimate final values:

| Property | Type | Description |
|---|---|---|
| `VolumePredicted` | `long` | Predicted total volume |
| `BuyVolumePredicted` | `long` | Predicted buy volume |
| `SellVolumePredicted` | `long` | Predicted sell volume |
| `DeltaCumulativePredicted` | `long` | Predicted cumulative delta |
| `TradesNumberPredicted` | `long` | Predicted trade count |
| `VolumePerSecond` | `double` | Current volume rate |
| `VolumePerSecondPredicted` | `double` | Predicted volume rate |

## Bar Direction Methods

| Method | Return Type | Description |
|---|---|---|
| `IsBullish()` | `bool` | Close > Open |
| `IsBearish()` | `bool` | Close < Open |
| `IsDoji()` | `bool` | Close == Open |

## Example: Iterate Over Footprint Levels

```csharp
IFootprintBar bar = footprint.FootprintBars[CurrentBar];

// Read each price level
foreach (double price in bar.Volumes.Keys)
{
    long totalVol = bar.Volumes[price];
    long buyVol = bar.BuyVolumes.ContainsKey(price) ? bar.BuyVolumes[price] : 0;
    long sellVol = bar.SellVolumes.ContainsKey(price) ? bar.SellVolumes[price] : 0;
    long delta = bar.Deltas.ContainsKey(price) ? bar.Deltas[price] : 0;
}

// Check imbalance levels
if (bar.BuyImbalanceCount >= 3)
{
    // Stacked buy imbalances — aggressive buying
    foreach (var kvp in bar.Imbalances[0]) // [0] = buy side
    {
        double price = kvp.Key;
        long volume = kvp.Value;
    }
}
```

---

## ISession

`ISession` extends `IFootprintBar` with session-level aggregated data. A session represents a full trading session (defined by Trading Hours) and inherits all footprint bar properties — its `Volume`, `Delta`, `POC`, etc. are aggregated across all bars in the session.

**Inheritance:** `ISession : IFootprintBar`
**Source:** `MZpackBase/mzFootprint/ISession.cs`

### Session-Specific Properties

| Property | Type | Description |
|---|---|---|
| `BeginTime` | `DateTime` | Session start time |
| `EndTime` | `DateTime` | Session end time |
| `BeginBarIdx` | `int` | First bar index in the session |
| `EndBarIdx` | `int` | Last bar index in the session |
| `POCs` | `SortedDictionary<int, double>` | Developing POC by bar index |
| `VAHs` | `SortedDictionary<int, double>` | Developing VAH by bar index |
| `VALs` | `SortedDictionary<int, double>` | Developing VAL by bar index |
| `DeltasCumulative` | `SortedDictionary<int, long>` | Cumulative delta by bar index |

### Example: Read Session Data

```csharp
ISession session = footprint.GetSession(DateTime.Now);

// Session-level aggregates (inherited from IFootprintBar)
double sessionPOC = session.POC;
double sessionVAH = session.VAH;
double sessionVAL = session.VAL;
long sessionDelta = session.Delta;
long sessionVolume = session.Volume;

// Developing POC history
foreach (var kvp in session.POCs)
{
    int barIdx = kvp.Key;
    double pocAtBar = kvp.Value;
}
```

## See Also

- [IFootprintIndicator](ifootprint-indicator.md) — parent indicator interface
- [StrategyFootprintIndicator](strategy-footprint-indicator.md) — strategy wrapper class
