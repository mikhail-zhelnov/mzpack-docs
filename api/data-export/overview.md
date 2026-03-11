---
sidebar_position: 1
title: "Data Export Overview"
description: "Overview of the MZpack data export system — Pipeline, IndicatorExport, DrawingObjectsExport, and configuration."
---

# Data Export Overview

The MZpack data export system provides a composable pipeline for exporting indicator values and chart drawing objects to CSV files or the NinjaScript Output panel.

**Namespace:** `MZpack.NT8.Algo`

## Two Export Scenarios

### 1. IndicatorExport — Indicator Values

Exports calculated values from MZpack indicators (footprint metrics, volume profile levels, delta, etc.) to CSV. Each row represents a bar, with columns defined by a [DataSchema](data-schema.md).

### 2. DrawingObjectsExport — Chart Drawing Objects

Exports chart annotations (arrows, text, dots, etc.) placed by strategies. Each drawing object is mapped to a numeric value via a [ChartObjectDescriptor](drawing-objects-export.md), enabling signal labeling for analysis or machine learning.

## Architecture

```
Pipeline
 ├── IndicatorExport          (indicator values → CSV)
 │    ├── ExportedIndicator   (data source)
 │    └── DataSet             (rows of values)
 │         └── DataSchema     (column definitions)
 │              └── ValueDescriptor[]
 │
 └── DrawingObjectsExport     (drawing objects → CSV)
      ├── ChartObjectDescriptor (object → value mapping)
      └── DataSet
           └── DataSchema
```

### Pipeline

`Pipeline` is the central orchestrator. It chains one or more `IndicatorExport` instances and drives per-bar export across all of them. Adjacent exports are linked via `PipelinePrior` / `PipelineNext` for synchronized processing.

```csharp
var args = new ExportArgs
{
    FileName = "ES_footprint.csv",
    IsHeader = true,
    IsTime = true
};

var pipeline = new Pipeline(strategy, args);

var fpExport = new IndicatorExport(strategy, fpIndicator,
    ExportDataSource.Level1, ExportTemporality.Historical,
    ExportGranularity.Bar, args);

fpExport.DataSet.Schema
    .Append(IndValue.POC)
    .Append(IndValue.Delta)
    .Append(IndValue.Volume);

pipeline.Add(true, fpExport);
pipeline.ExportDates(beginTime, endTime);
```

## Enums

### ExportTemporality

```csharp
[Flags]
public enum ExportTemporality
{
    Historical = 1,
    Realtime = 2
}
```

| Value | Description |
|---|---|
| `Historical` | Export historical bar data after loading |
| `Realtime` | Export data as it arrives in real time |

### ExportDataSource

| Value | Description |
|---|---|
| `Level1` | Level 1 (trade/tick) data |
| `Level2` | Level 2 (market depth) data |
| `Custom` | Custom data source |

### ExportGranularity

| Value | Description |
|---|---|
| `Tick` | One row per tick |
| `Bar` | One row per bar |
| `Update` | One row per update event |

### ExportMode

| Value | Description |
|---|---|
| `Save` | Write data to output |
| `Load` | Read data from file |

## ExportArgs

Configuration object passed to all export constructors.

| Property | Type | Default | Description |
|---|---|---|---|
| `FileName` | `string` | — | Output file name (e.g., `"data.csv"`) |
| `BaseDirectory` | `string` | `null` | Root directory (`null` = strategy default `\data`) |
| `SubDirectory` | `string` | — | Subdirectory within base |
| `IsHeader` | `bool` | `false` | Include column header row |
| `IsTime` | `bool` | `false` | Include Time column |
| `IsFile` | `bool` | `true` | Write to file |
| `IsNinjaScriptOutput` | `bool` | `false` | Write to NinjaScript Output panel |
| `IsExportWhileCollecting` | `bool` | `false` | Stream rows as they are added |
| `IsBatch` | `bool` | `false` | Create numbered batch files |
| `Delimiter` | `char` | `,` | Column delimiter |
| `SignedVolume` | `bool` | `false` | Prefix volumes with sign (+buy, −sell) |
| `Shift` | `int` | `0` | Bar shift for exported items |

## Constants

| Constant | Value | Description |
|---|---|---|
| `Export.DELIMITER` | `,` | Default delimiter |
| `Export.TIME_FORMAT` | `yyyy-MM-ddTHH:mm:ss.fff` | Timestamp format |
| `Export.APPEND` | `true` | Append mode flag |

## See Also

- [DataSchema / DataSet](data-schema.md) — defining output structure
- [ValueDescriptor](value-descriptor.md) — column definitions and delegates
- [DrawingObjectsExport](drawing-objects-export.md) — exporting chart annotations
- [Export Indicators Values sample](../samples/export-indicators-values.md) — complete working example
