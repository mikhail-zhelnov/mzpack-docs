---
sidebar_position: 4
title: "DrawingObjectsExport"
description: "Reference for DrawingObjectsExport and ChartObjectDescriptor classes for exporting chart annotations to CSV."
---

# DrawingObjectsExport

Exports chart drawing objects (arrows, text, dots, regions) as numeric values in CSV format. Each drawing object is matched against a mapping table and converted to a `double` value.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `DrawingObjectsExport : GeneralExport`

## Constructor

```csharp
new DrawingObjectsExport(MZpackStrategyBase strategy, ExportArgs exportArgs)
```

The export uses `ExportDataSource.Level1`, `ExportTemporality.Historical`, and `ExportGranularity.Bar` by default.

## How It Works

1. The export scans `strategy.DrawObjects` for drawing objects at the current time
2. Only objects with anchors and `IsAttachedToNinjaScript = true` are included
3. Each object is passed to `ChartObjectDescriptor.GetValue()` for mapping
4. The mapped value is written as a row in the DataSet

The row timestamp is taken from the first anchor of the drawing object.

## ChartObjectDescriptor

Defines how drawing objects are filtered and mapped to numeric values.

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Script` | `string` | `null` | Filter: only objects drawn by this script (`null` = any) |
| `Tag` | `string` | `null` | Filter: only objects whose tag contains this substring (`null` = any) |
| `Map` | `List<MapItem>` | — | Mapping rules from drawing tool attributes to values |

### MapItem

Each `MapItem` matches a drawing object by tool type, text, and/or color, and maps it to a numeric value.

| Property | Type | Default | Description |
|---|---|---|---|
| `Tool` | `DrawingTool` | `Any` | Drawing tool type to match |
| `Text` | `string` | `null` | Display text to match (`null` = any) |
| `Color` | `string` | `null` | Color name to match (`null` = any) |
| `Value` | `double` | — | Numeric value returned when matched |

The first `MapItem` that matches wins. If no item matches, `double.NaN` is returned.

## DrawingTool Enum

| Value | Description |
|---|---|
| `Any` | Match any drawing tool type |
| `ArrowDown` | Down arrow |
| `ArrowUp` | Up arrow |
| `Diamond` | Diamond shape |
| `Dot` | Dot marker |
| `Region` | Highlighted region |
| `Square` | Square marker |
| `Text` | Text annotation |
| `TextFixed` | Fixed-position text |
| `TriangleDown` | Down triangle |
| `TriangleUp` | Up triangle |

## Example

Export all `ArrowUp` drawing objects with tag "signal" as value `1.0`, and `ArrowDown` as value `−1.0`:

```csharp
var chartDesc = new ChartObjectDescriptor
{
    Tag = "signal",
    Map = new List<ChartObjectDescriptor.MapItem>
    {
        new ChartObjectDescriptor.MapItem
        {
            Tool = DrawingTool.ArrowUp,
            Value = 1.0
        },
        new ChartObjectDescriptor.MapItem
        {
            Tool = DrawingTool.ArrowDown,
            Value = -1.0
        }
    }
};

var args = new ExportArgs
{
    FileName = "signals.csv",
    IsHeader = true,
    IsTime = true
};

var export = new DrawingObjectsExport(strategy, args);

export.DataSet.Schema
    .Append(IndValue.Close)
    .Append(IndValue.Delta)
    .Append("signal", ValueKind.Label, chartDesc);

export.ExportDates(beginTime, endTime);
```

This produces a CSV with columns: `Time, Close, Delta, signal` where `signal` is `1.0` for up arrows, `−1.0` for down arrows, and `NaN` for bars without matching drawing objects.

## See Also

- [Data Export Overview](overview.md) — architecture and Pipeline
- [ValueDescriptor](value-descriptor.md) — column definitions and IndValue enum
- [Export Indicators Values sample](../samples/export-indicators-values.md) — complete working example
