---
sidebar_position: 1
title: "IVolumeDeltaIndicator"
description: "Reference for the IVolumeDeltaIndicator interface — access to volume/delta bars, cumulative delta, and iceberg detection."
---

# IVolumeDeltaIndicator

`IVolumeDeltaIndicator` provides programmatic access to the [mzVolumeDelta](/docs/indicators/mzVolumeDelta) chart indicator. It exposes per-bar volume and delta data, cumulative delta, iceberg alerts, and display settings.

**Namespace:** `MZpack`
**Inheritance:** `IVolumeDeltaIndicator : IOrderFlowIndicator : ITickIndicator : IIndicator`
**Conditional:** `#if !FREE`
**Source:** `MZpackBase/mzVolumeDelta/IVolumeDeltaIndicator.cs`

## Key Data Properties

| Property | Type | Description |
|---|---|---|
| `VolumeDeltaBars` | `Dictionary<int, IVolumeDeltaBar>` | Volume/delta bars indexed by bar index |

## Configuration Properties

| Property | Type | Description |
|---|---|---|
| `VolumeDeltaMode` | `VolumeDeltaMode` | Display mode |
| `TradeFilterMin` | `double` | Minimum trade size filter |
| `TradeFilterMax` | `double` | Maximum trade size filter |
| `VolumeDeltaDisplayFilter` | `double` | Minimum display value |
| `ZeroLine` | `bool` | Show zero reference line |

## Volume Properties

| Property | Type | Description |
|---|---|---|
| `VolumeMode` | `VolumeMode` | Volume display mode |
| `VolumeAlign` | `VolumeAlign` | Volume bar alignment |
| `VolumeColorCode` | `VolumeColorCode` | Color coding scheme |
| `BarMaxValue` | `BarMaxValue` | Maximum bar value reference |

## Delta Properties

| Property | Type | Description |
|---|---|---|
| `DeltaMode` | `DeltaMode` | Delta calculation mode |
| `CumulateSession` | `bool` | Reset cumulative delta on session start |

## Alert Properties

| Property | Type | Description |
|---|---|---|
| `UseVolumeAlert` | `bool` | Enable volume threshold alert |
| `VolumeAlertThreshold` | `double` | Volume alert threshold |
| `VolumeAlertSound` | `string` | Volume alert sound file |
| `UseIcebergAlert` | `bool` | Enable iceberg detection alert |
| `IcebergAlertThreshold` | `double` | Iceberg alert threshold |
| `IcebergAlertSound` | `string` | Iceberg alert sound file |

## Custom Filter Properties

| Property | Type | Description |
|---|---|---|
| `CustomValueLessFilter` | `double` | Filter for values below this threshold |
| `CustomValueFilter1` | `double` | Custom color filter level 1 |
| `CustomValueFilter2` | `double` | Custom color filter level 2 |
| `CustomValueFilter3` | `double` | Custom color filter level 3 |

## Example: Read Delta Per Bar

```csharp
IVolumeDeltaIndicator vdIndicator = ...;

// Get the current bar data
IVolumeDeltaBar bar = vdIndicator.VolumeDeltaBars[CurrentBar];

// Read volume and delta
// (IVolumeDeltaBar properties depend on VolumeDeltaMode)
```

## See Also

- [StrategyVolumeDeltaIndicator](strategy-vd-indicator.md) — strategy wrapper class
- [IDeltaDivergenceIndicator](../delta-divergence/idelta-divergence-indicator.md) — extends this interface with divergence detection
