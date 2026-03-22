---
sidebar_position: 2
title: "IVolumeProfile / Profile2"
description: "Reference for IVolumeProfile and Profile2 — volume profile data with POC, Value Area, VWAP, standard deviations, and TPO metrics."
---

# IVolumeProfile / Profile2

`IVolumeProfile` defines the data contract for a single volume profile. `Profile2` is the concrete implementation that calculates POC, Value Area, VWAP, standard deviations, TPO, and per-level volume data.

**Namespace:** `MZpack`
**Inheritance:** `IVolumeProfile : IModelItem2`
**Implementation:** `Profile2 : ProfileBase, IModelItem2, IVolumeProfile`
**Source:** `MZpackBase/mzVolumeProfile/IVolumeProfile.cs`, `MZpackBase/mzVolumeProfile/Profile2.cs`

## Key Level Properties

| Property | Type | Description |
|---|---|---|
| `POC` | `double` | Point of Control — price with highest volume |
| `TickPOC` | `double` | Tick-level POC (finer than TicksPerLevel) |
| `VAH` | `double` | Value Area High |
| `VAL` | `double` | Value Area Low |
| `VWAP` | `double` | Volume Weighted Average Price |
| `MID` | `double` | Midpoint of the profile range |

## Standard Deviations

| Property | Type | Description |
|---|---|---|
| `Deviation` | `double` | Standard deviation value |
| `_1StdDeviationPos` | `double` | VWAP + 1 standard deviation |
| `_1StdDeviationNeg` | `double` | VWAP - 1 standard deviation |
| `_2StdDeviationPos` | `double` | VWAP + 2 standard deviations |
| `_2StdDeviationNeg` | `double` | VWAP - 2 standard deviations |

## OHLC and Range

| Property | Type | Description |
|---|---|---|
| `Open` | `double` | Profile open price |
| `Close` | `double` | Profile close price |
| `High` | `double` | Profile high price |
| `Low` | `double` | Profile low price |
| `RangeTicks` | `int` | Profile range in ticks |
| `DurationMs` | `double` | Profile duration in milliseconds |

## Volume and Delta

| Property | Type | Description |
|---|---|---|
| `Volume` | `long` | Total volume |
| `BuyVolume` | `long` | Buy (ask) volume |
| `SellVolume` | `long` | Sell (bid) volume |
| `Delta` | `long` | Delta (BuyVolume - SellVolume) |
| `DeltaPercentage` | `double` | Delta as percentage of volume |
| `POCVolume` | `long` | Volume at POC |
| `BuyPOCVolume` | `long` | Buy volume at POC |
| `SellPOCVolume` | `long` | Sell volume at POC |
| `VAVolume` | `long` | Total volume within Value Area |
| `TradesNumber` | `long` | Number of trades |

## TPO Properties

| Property | Type | Description |
|---|---|---|
| `TPO_POC` | `double` | TPO-based Point of Control |
| `TPO_VAH` | `double` | TPO-based Value Area High |
| `TPO_VAL` | `double` | TPO-based Value Area Low |
| `TPOLettersCount` | `int` | Number of TPO letters/periods |
| `IBHigh` | `double` | Initial Balance High |
| `IBLow` | `double` | Initial Balance Low |

## LVN/HVN Data

| Property | Type | Description |
|---|---|---|
| `LVNs` | `IReadOnlyList<IVolumeNode>` | Low Volume Nodes detected in the profile |
| `HVNs` | `IReadOnlyList<IVolumeNode>` | High Volume Nodes detected in the profile |

### IVolumeNode

| Property | Type | Description |
|---|---|---|
| `Price` | `double` | Price level of the node |
| `Volume` | `long` | Volume at the node price level |

## Per-Level Data

| Property | Type | Description |
|---|---|---|
| `Volumes` | `SortedDictionary<double, long>` | Total volume per price level |
| `BuyVolumes` | `SortedDictionary<double, long>` | Buy volume per price level |
| `SellVolumes` | `SortedDictionary<double, long>` | Sell volume per price level |
| `Deltas` | `SortedDictionary<double, long>` | Delta per price level |

## Developing Data (by bar index)

These dictionaries track how profile levels evolve over time:

| Property | Type | Description |
|---|---|---|
| `VWAPs` | `SortedDictionary<int, double>` | VWAP at each bar index |
| `Deviations` | `SortedDictionary<int, double>` | Standard deviation at each bar index |
| `POCs` | `SortedDictionary<int, double>` | POC at each bar index |
| `VAHs` | `SortedDictionary<int, double>` | VAH at each bar index |
| `VALs` | `SortedDictionary<int, double>` | VAL at each bar index |

## Time Range (from IModelItem2)

| Property | Type | Description |
|---|---|---|
| `Begin` | `DateTime` | Profile start time |
| `End` | `DateTime` | Profile end time |
| `BeginBarIdx` | `int` | First bar index |
| `EndBarIdx` | `int` | Last bar index |
| `IsDeveloping` | `bool` | Whether the profile is still being built |
| `IsEmpty` | `bool` | Whether the profile has no data |

## Methods

| Method | Return Type | Description |
|---|---|---|
| `IsRTH()` | `bool` | Whether the profile is within Regular Trading Hours |
| `IsETH()` | `bool` | Whether the profile is within Extended Trading Hours |
| `AssignRange(int beginBarIdx, int endBarIdx)` | `bool` | Assign the profile to a bar range |
| `AssignRange(DateTime begin, DateTime end)` | `bool` | Assign the profile to a time range |
| `Intersects(IVolumeProfile profile)` | `bool` | Check if two profiles overlap in time |
| `RefreshViewModel()` | `void` | Refresh the visual representation |

## Example: Read POC and VWAP

```csharp
IVolumeProfile profile = vpIndicator.GetProfile(0);

double poc = profile.POC;
double vwap = profile.VWAP;
double vah = profile.VAH;
double val = profile.VAL;

// Volume breakdown at POC
long pocBuyVol = profile.BuyPOCVolume;
long pocSellVol = profile.SellPOCVolume;

// Standard deviations around VWAP
double upper1SD = profile._1StdDeviationPos;
double lower1SD = profile._1StdDeviationNeg;
double upper2SD = profile._2StdDeviationPos;
double lower2SD = profile._2StdDeviationNeg;

// Iterate volume ladder
foreach (var kvp in profile.Volumes)
{
    double price = kvp.Key;
    long volume = kvp.Value;
    long delta = profile.Deltas.ContainsKey(price) ? profile.Deltas[price] : 0;
}
```

## See Also

- [IVolumeProfileIndicator](ivolume-profile-indicator.md) — parent indicator interface
- [ChartProfilesModel](chart-profiles-model.md) — model and creation modes
