---
sidebar_position: 3
title: "ChartProfilesModel"
description: "Reference for ChartProfilesModel and StackedProfileModel — volume profile model with creation modes and delegates."
---

# ChartProfilesModel

`ChartProfilesModel` manages the collection of volume profiles for a chart indicator. It controls **when** new profiles are created through creation mode delegates. `StackedProfileModel` extends it for stacked (overlapping) profiles.

**Namespace:** `MZpack`
**Inheritance:** `ChartProfilesModel : Model` | `StackedProfileModel : ChartProfilesModel`
**Source:** `MZpackBase/mzVolumeProfile/ChartProfilesModel.cs`, `MZpackBase/mzVolumeProfile/StackedProfileModel.cs`

:::warning
Do not modify ChartProfilesModel directly — use the indicator interface (`IVolumeProfileIndicator`) to read and manage profiles.
:::

## Properties

| Property | Type | Description |
|---|---|---|
| `Profiles` | `List<IModelItem2>` | All profiles in the model |
| `Slot` | `int` | Profile slot index |
| `TicksPerLevel` | `int` | Level aggregation |
| `ProfileType` | `ProfileType` | Display type: TPO, VP, VP_TPO, None |
| `Creation` | `ProfileCreation` | Creation mode |
| `CreationValue` | `int` | Threshold for the creation mode |
| `VWAPMode` | `VWAPMode` | VWAP calculation mode |
| `HasTPO` | `bool` | Whether TPO data is being calculated |
| `HasVP` | `bool` | Whether volume profile data is being calculated |

## Creation Delegates

The model uses two delegates to determine when to create a new profile:

- **`IsAddModelItemOnDataItemDelegate`** — evaluated per bar; returns `true` to start a new profile
- **`IsAddModelItemOnDataEventDelegate`** — evaluated per market data event; returns `true` to start a new profile

The active delegate depends on the `ProfileCreation` mode. Time-based modes (Session, Daily, Weekly) use the data item delegate. Volume-based modes (Volume, Delta, Tick) use the data event delegate.

## ProfileCreation Enum

Controls how profiles are segmented. Set via `IVolumeProfileIndicator.ProfileCreation`.

| Value | Description |
|---|---|
| `Custom` | User-defined profile boundaries |
| `Composite` | Composite profile across the entire chart |
| `Continuous` | Single continuous profile that grows indefinitely |
| `Session` | One profile per trading session |
| `Sessions` | One profile per N sessions |
| `Bar` | One profile per bar |
| `Bars` | One profile per N bars |
| `Daily` | One profile per day |
| `Days` | One profile per N days |
| `Weekly` | One profile per week |
| `Weeks` | One profile per N weeks |
| `Monthly` | One profile per month |
| `Months` | One profile per N months |
| `Quarterly` | One profile per quarter |
| `Yearly` | One profile per year |
| `Volume` | New profile when total volume reaches threshold |
| `Delta` | New profile when absolute delta reaches threshold |
| `Tick` | New profile when tick count reaches threshold |
| `RTH_ETH` | Separate profiles for Regular and Extended Trading Hours |
| `None` | No automatic profile creation |

## StackedProfileModel

`StackedProfileModel` extends `ChartProfilesModel` to support up to 3 overlapping profiles on the same chart. Each stacked profile has independent creation settings.

| Property | Type | Description |
|---|---|---|
| `StackedProfile` | `IModelItem2` | The current stacked profile |
| `Ago` | `int` | Profile offset (0 = current) |
| `LastN` | `int` | Number of historical profiles to keep |

## Related Enums

```csharp
public enum ProfileType { TPO, VP, VP_TPO, None }

public enum VWAPMode { Last, Dynamic, DynamicStdDev1, DynamicStdDev2, None }
```

## See Also

- [IVolumeProfileIndicator](ivolume-profile-indicator.md) — indicator interface
- [IVolumeProfile / Profile2](ivolume-profile.md) — profile data structure
