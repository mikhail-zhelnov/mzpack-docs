---
sidebar_position: 4
title: "Drawing Objects Export"
description: "Source code walkthrough of the DrawingObjects_Export built-in strategy — minimal utility for exporting chart drawing objects to CSV using XML-defined schemas with ChartObjectDescriptor and MapItem mappings."
---

# Drawing Objects Export

The simplest built-in strategy — a 119-line utility that exports chart drawing objects (indicators that draw on the chart, such as Boss Order Blocks, Imbalance Profile Lidar markers, etc.) to CSV files. Demonstrates `DrawingObjectsExport`, XML schema loading/creation, `ChartObjectDescriptor` with `MapItem` mappings, and the `DataSchema.LoadFromXml`/`SaveToXml` persistence pattern.

**Source:** `[INSTALL PATH]/API/Strategies/DrawingObjects_Export/DrawingObjects_Export.cs`

## What It Covers

- Minimal strategy — no trading, no indicators, no signals
- `DrawingObjectsExport` setup with `ExportArgs`
- XML schema loading from file with fallback to sample schema creation
- `DataSchema` with `ChartObjectDescriptor` and `MapItem` for mapping drawing tool text to numeric values
- `DataSchema.LoadFromXml` / `SaveToXml` for schema persistence

## Architecture

```
DrawingObjects_Export : MZpackStrategyBase
 └── DrawingObjectsExport
      └── DataSchema (loaded from XML or auto-generated sample)
           └── ChartObjectDescriptor[] with MapItem[] mappings
```

## Complete Source

The entire strategy is short enough to show in full:

```csharp
public class DrawingObjects_Export : MZpackStrategyBase
{
    protected override void OnStateChange()
    {
        base.OnStateChange();

        lock (Sync)
        {
            if (State == State.SetDefaults)
            {
                BarsRequiredToTrade = 1;
                EnableBacktesting = true;
                Export_Delimiter = ";";
            }
            else if (State == State.Configure)
            {
            }
            else if (State == State.DataLoaded)
            {
                char delimiter = !string.IsNullOrEmpty(Export_Delimiter)
                    ? Export_Delimiter[0] : Export.DELIMITER;

                // Create DrawingObjectsExport
                var export = new DrawingObjectsExport(this,
                    new ExportArgs()
                    {
                        IsExportWhileCollecting = false,
                        IsHeader = Export_Header,
                        IsTime = Export_Time,
                        Delimiter = delimiter,
                        IsFile = true,
                        FileName = Export_File,
                        IsBatch = Export_Batch,
                    });

                // Load schema from XML file
                string path = GetBasePath(this) + "\\" + Export_SchemaFile;
                if (System.IO.File.Exists(path))
                {
                    export.DataSet.Schema = DataSchema.LoadFromXml(this, path);
                }
                else
                {
                    ShowMessageBoxAsync(
                        $"Schema file not found: {path}",
                        DisplayName, MessageBoxImage.Information);

                    // Create sample schema
                    DataSchema schema = new DataSchema();
                    schema.Append("BOB", ValueKind.Feature,
                        new ChartObjectDescriptor()
                        {
                            Script = "ninZaBossOrderBlock",
                            Map = new List<MapItem>()
                            {
                                new MapItem()
                                    { Tool = DrawingTool.Text, Text = "▲", Value = 1.0 },
                                new MapItem()
                                    { Tool = DrawingTool.Text, Text = "▼", Value = -1.0 }
                            }
                        });

                    schema.SaveToXml(path);

                    ShowMessageBoxAsync(
                        $"Sample schema has been created. Saved to file: {path}.",
                        DisplayName, MessageBoxImage.Information);

                    export.DataSet.Schema = schema;
                }

                Register(export);
            }
        }
    }


    #region Export
    [Display(Name = "Schema file", GroupName = "Export", Order = 1)]
    public string Export_SchemaFile { get; set; } = "schema.xml";

    [Display(Name = "Temporality", GroupName = "Export", Order = 2)]
    public ExportTemporality Export_Temporality { get; set; }
        = ExportTemporality.Historical;

    [Display(Name = "File", GroupName = "Export", Order = 3)]
    public string Export_File { get; set; } = "";

    [Display(Name = "Header", GroupName = "Export", Order = 4)]
    public bool Export_Header { get; set; } = true;

    [Display(Name = "Time", GroupName = "Export", Order = 5)]
    public bool Export_Time { get; set; } = true;

    [Display(Name = "Batch", GroupName = "Export", Order = 6)]
    public bool Export_Batch { get; set; }

    [Display(Name = "Delimiter", GroupName = "Export", Order = 7)]
    public string Export_Delimiter { get; set; }
    #endregion Export
}
```

## Key Concepts

### ChartObjectDescriptor

Defines how to find and map a chart drawing object:

| Field | Description |
|---|---|
| `Script` | NinjaScript indicator name that draws the objects (e.g., `"ninZaBossOrderBlock"`) |
| `Map` | List of `MapItem` rules that convert drawing object properties to numeric values |

### MapItem

Maps a drawing tool's visual properties to a numeric export value:

| Field | Description |
|---|---|
| `Tool` | The `DrawingTool` type to match (e.g., `DrawingTool.Text`) |
| `Text` | The text content to match (e.g., `"▲"` for bullish, `"▼"` for bearish) |
| `Value` | The numeric value to export (e.g., `1.0` for bullish, `-1.0` for bearish) |

### Schema Persistence

The schema is loaded from an XML file at the strategy's base path. If the file doesn't exist, a sample schema is auto-generated and saved:

```
Documents\NinjaTrader 8\mzpack\strategy\...\DrawingObjects_Export\schema.xml
```

This allows users to customize the schema by editing the XML file directly — adding new drawing object descriptors, changing mappings, etc.

## Configurable Properties

| Property | Default | Description |
|---|---|---|
| `Export_SchemaFile` | `"schema.xml"` | XML schema file name |
| `Export_Temporality` | `Historical` | Historical or Realtime export |
| `Export_File` | `""` | Custom output file path (optional) |
| `Export_Header` | `true` | Include column headers |
| `Export_Time` | `true` | Include timestamp column |
| `Export_Batch` | `false` | Batch write mode |
| `Export_Delimiter` | `;` | Column separator |

## See Also

- [Built-in Strategies](/docs/strategies/built-in-strategies#data-export-strategy) — user-facing reference
- [Data Export](data-export.md) — indicator data export strategy
- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile
