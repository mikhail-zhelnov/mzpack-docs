---
sidebar_position: 1
title: "IVolumeProfileIndicator"
description: "Reference for the IVolumeProfileIndicator interface — access to volume profiles, creation modes, stacked profiles, and TPO data."
---

# IVolumeProfileIndicator

`IVolumeProfileIndicator` provides programmatic access to the [mzVolumeProfile](/docs/indicators/mzVolumeProfile) chart indicator. It exposes the collection of volume profiles, profile creation settings, stacked profiles, and TPO configuration.

**Namespace:** `MZpack`
**Inheritance:** `IVolumeProfileIndicator : ITickIndicator, ILevelsIndicator, IIndicator`
**Source:** `MZpackBase/mzVolumeProfile/IVolumeProfileIndicator.cs`

:::note
`ILevelsIndicator` is conditionally included (non-FREE builds only), adding interactive price level support.
:::

## Key Data Properties

| Property | Type | Description |
|---|---|---|
| `Profiles` | `IEnumerable<IModelItem2>` | All volume profiles in the indicator |

## Key Data Methods

| Method | Return Type | Description |
|---|---|---|
| `GetProfileByTIndex(int TIndex)` | `IVolumeProfile` | Get profile by T-index |
| `GetProfile(int index)` | `IVolumeProfile` | Get profile by sequential index |
| `GetStackedProfile(int n)` | `IVolumeProfile` | Get stacked profile (1, 2, or 3) |
| `AddProfile()` | `IVolumeProfile` | Add a new empty profile |
| `RemoveProfile(IVolumeProfile profile)` | `void` | Remove a profile |
| `StackedProfileIsPresent(int index)` | `bool` | Check if stacked profile exists |
| `RefreshModel(RefreshModelArgs args)` | `void` | Force a model refresh |

## Profile Creation Properties

| Property | Type | Description |
|---|---|---|
| `ProfileCreation` | `ProfileCreation` | Creation mode (Session, Bar, Volume, etc.) |
| `CreationValue` | `int` | Threshold value for the creation mode |
| `ShowProfileType` | `ProfileType` | Display type: TPO, VP, VP_TPO, or None |
| `ProfileMode` | `ProfileMode` | Profile mode |
| `ProfileAccuracy` | `ProfileAccuracy` | Tick or Minute accuracy |
| `ProfilePresentation` | `ProfilePresentation` | Visual presentation |
| `SessionBreak` | `bool` | Break profile on session boundary |
| `ShowLastProfilesCount` | `int` | Number of recent profiles to display |

## Trading Hours Properties

| Property | Type | Description |
|---|---|---|
| `RTH_Begin` | `TimeSpan` | Regular Trading Hours start |
| `RTH_End` | `TimeSpan` | Regular Trading Hours end |
| `ETH_Enable` | `bool` | Enable Extended Trading Hours |
| `ETH_Begin` | `TimeSpan` | Extended Trading Hours start |
| `ETH_End` | `TimeSpan` | Extended Trading Hours end |

## Value Area and VWAP Properties

| Property | Type | Description |
|---|---|---|
| `VAPercentage` | `float` | Value Area percentage (e.g. 0.70) |
| `Sigma1` | `double` | First standard deviation multiplier |
| `Sigma2` | `double` | Second standard deviation multiplier |
| `VWAPMode` | `VWAPMode` | VWAP mode: Last, Dynamic, DynamicStdDev1, DynamicStdDev2, None |
| `POCMode` | `LevelMode` | POC display mode |
| `VAHVALMode` | `LevelMode` | VAH/VAL display mode |
| `DevelopingTickPOC` | `bool` | Show developing Tick POC |
| `TicksPerLevel` | `int` | Number of ticks per level |

## Stacked Profiles Properties

| Property | Type | Description |
|---|---|---|
| `StackedProfileCreation` | `ProfileCreation[]` | Creation modes for 3 stacked profiles |
| `StackedShowProfileType` | `ProfileType[]` | Display types for stacked profiles |
| `StackedCreationValue` | `int[]` | Creation thresholds for stacked profiles |
| `StackedProfileMode` | `ProfileMode[]` | Modes for stacked profiles |
| `StackedProfilePresentation` | `ProfilePresentation[]` | Presentations for stacked profiles |
| `StackedPOCVAHVALMode` | `LevelMode[]` | POC/VAH/VAL modes for stacked profiles |
| `StackedProfileShowDelta` | `bool[]` | Show delta for stacked profiles |

## TPO Properties

| Property | Type | Description |
|---|---|---|
| `TPOLetterPeriod` | `int` | Minutes per TPO letter |
| `TPOPresentation` | `TPOPresentation` | TPO visual style |
| `TPOShowIB` | `bool` | Show Initial Balance |
| `TPOIBPeriod` | `int` | Initial Balance period in minutes |
| `TPOShowHalfback` | `bool` | Show halfback level |
| `TPOSplit` | `bool` | Split TPO display |
| `TPO_VAPercentage` | `float` | TPO Value Area percentage |

## Example: Read Profile Data

```csharp
IVolumeProfileIndicator vpIndicator = ...;

// Get the most recent profile
IVolumeProfile profile = vpIndicator.GetProfile(0);

// Read key levels
double poc = profile.POC;
double vah = profile.VAH;
double val = profile.VAL;
double vwap = profile.VWAP;
long totalVolume = profile.Volume;

// Standard deviations
double upperDev1 = profile._1StdDeviationPos;
double lowerDev1 = profile._1StdDeviationNeg;

// Check stacked profile
if (vpIndicator.StackedProfileIsPresent(1))
{
    IVolumeProfile stacked = vpIndicator.GetStackedProfile(1);
    double stackedPOC = stacked.POC;
}
```

## See Also

- [IVolumeProfile / Profile2](ivolume-profile.md) — profile data structure
- [ChartProfilesModel](chart-profiles-model.md) — model and creation modes
- [StrategyVolumeProfileIndicator](strategy-vp-indicator.md) — strategy wrapper class
