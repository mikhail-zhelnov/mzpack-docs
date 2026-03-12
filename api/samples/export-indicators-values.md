---
sidebar_position: 9
title: "Export Indicator Values"
description: "Export indicator values with Historical/Realtime temporality"
---

# Export Indicator Values

Demonstrates how to export MZpack indicator data to CSV files using the `IndicatorExport` and `DataSchema` classes. Set `ExportTemporality` to `Historical` for chart data or `Realtime` for live data. Saving begins when the strategy is disabled.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/ExportIndicatorsValues.cs`
**Class:** `ExportIndicatorsValues : MZpackStrategyBase`

## What It Covers

- `StrategyFootprintIndicator` and `StrategyVolumeProfileIndicator` with `SaveSettings`
- `IndicatorExport` with `ExportArgs` (file, delimiter, time, header)
- `DataSchema` with `IndValue` enum for column selection
- Two exports: footprint (open, close, volume, delta, POC, session POC) and volume profile (high, low, volume, delta, VAH, VAL, POC, VWAP, std deviations, TPO POC)
- `ExportTemporality.Historical` for backtesting, `Realtime` for live

## Indicator Setup

```csharp
indicators.Add(new StrategyFootprintIndicator(this, FOOTPRINT)
{
    SaveSettings = true,
    ShowVersionInfo = false
});

indicators.Add(new StrategyVolumeProfileIndicator(this, VOLUMEPROFILE)
{
    SaveSettings = true,
    ShowVersionInfo = false,
    ShowProfileType = ProfileType.VP,
    StackedShowProfileType1 = ProfileType.None,
    VWAPMode = VWAPMode.Dynamic
});
```

## Export Setup

### Footprint Export

```csharp
IndicatorExport footprintDataExport = new IndicatorExport(this,
    footprintIndicator,
    ExportDataSource.Level1,
    ExportTemporality,
    ExportGranularity.Bar,
    new ExportArgs()
    {
        IsFile = true,
        BaseDirectory = BaseDir,
        FileName = FootprintFile,
        Delimiter = ';',
        IsTime = true,
        IsHeader = true
    });

DataSchema schema = new DataSchema(footprintDataExport.DataSet)
    .Append(IndValue.Open)
    .Append(IndValue.Close)
    .Append(IndValue.Volume)
    .Append(IndValue.Delta)
    .Append(IndValue.POC)
    .Append(IndValue.SessionPOC);
if (ExportVAH)
    schema.Append(IndValue.VAH);
footprintDataExport.DataSet.Schema = schema;

Register(footprintDataExport);
```

### Volume Profile Export Schema

```csharp
schema = new DataSchema(volumeProfileDataExport.DataSet)
    .Append(IndValue.High)
    .Append(IndValue.Low)
    .Append(IndValue.Volume)
    .Append(IndValue.Delta)
    .Append(IndValue.VAH)
    .Append(IndValue.VAL)
    .Append(IndValue.POC)
    .Append(IndValue.VWAP)
    .Append(IndValue._1StdDeviationPos)
    .Append(IndValue._1StdDeviationNeg)
    .Append(IndValue.TPO_POC);
```

## Configurable Properties

| Property | Default | Description |
|---|---|---|
| `ExportTemporality` | `Historical` | Historical or Realtime export |
| `BaseDir` | — | Override base directory (default: `Documents\NinjaTrader 8\mzpack\...`) |
| `FootprintFile` | `"footprint.csv"` | Footprint export filename |
| `VolumeProfileFile` | `""` | Volume profile filename (empty = random name) |
| `ExportVAH` | `false` | Include VAH in footprint export |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzFootprint](data-access-footprint.md) — footprint data
- [Data Access — mzVolumeProfile](data-access-volume-profile.md) — volume profile data
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
