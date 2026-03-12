---
sidebar_position: 3
title: "Data Export"
description: "Source code walkthrough of the Data_Export built-in strategy — utility for exporting footprint, volume profile, big trade, and market depth indicator data to CSV files with conditional indicator creation and per-indicator export schemas."
---

# Data Export

Utility strategy that exports indicator data to CSV files — no trading, no decision tree. Demonstrates conditional indicator creation based on enabled export groups, per-indicator `IndicatorExport` objects with independent data schemas, and the `ExportDataSource`/`ExportGranularity` system.

**Source:** `MZpack.NT8/Algo/Strategies/Data_Export/Data_Export.cs`

## What It Covers

- Non-trading strategy (no `OnCreateAlgoStrategy` delegate)
- Conditional indicator creation — only enabled indicators are instantiated
- Per-indicator `IndicatorExport` with `DataSchema` builder methods
- Export configuration: temporality (Historical/Realtime), granularity (Bar/Tick/Update), signed volumes
- `OnStateChange` DataLoaded phase for export setup and schema building

## Architecture

```
Data_Export : MZpackStrategyBase
 ├── StrategyFootprintIndicator (conditional)
 │    └── IndicatorExport (Level 1, Bar granularity)
 │         └── DataSchema with ~30 footprint fields
 ├── StrategyVolumeProfileIndicator (conditional)
 │    └── IndicatorExport (Level 1, Bar or Tick granularity)
 │         └── DataSchema with profile fields
 ├── StrategyBigTradeIndicator (conditional)
 │    └── IndicatorExport (Level 1, Tick granularity)
 │         └── DataSchema with trade fields
 └── StrategyMarketDepthIndicator (conditional)
      └── IndicatorExport (Level 2, Update granularity)
           └── DataSchema with DOM fields
```

## Strategy Setup

### Constructor

The constructor only wires the indicator creation delegate — there is no `OnCreateAlgoStrategy` since this strategy doesn't trade:

```csharp
public Data_Export() : base()
{
    OnCreateIndicators = new OnCreateIndicatorsDelegate(CreateIndicators);
}
```

### CreateIndicators

Indicators are created conditionally based on which export groups are enabled:

```csharp
protected List<TickIndicator> CreateIndicators()
{
    List<TickIndicator> indicators = new List<TickIndicator>();

    if (Footprint_Enable)
    {
        footprintIndicator = new StrategyFootprintIndicator(this, FOOTPRINT)
        {
            SaveSettings = true,
            ShowVersionInfo = false
        };
        indicators.Add(footprintIndicator);
    }

    if (VolumeProfile_Enable)
    {
        volumeProfileIndicator = new StrategyVolumeProfileIndicator(this, VOLUMEPROFILE)
        {
            SaveSettings = true,
            ShowVersionInfo = false
        };
        indicators.Add(volumeProfileIndicator);
    }

    if (BigTrade_Enable)
    {
        bigTradeIndicator = new StrategyBigTradeIndicator(this, BIGTRADE)
        {
            SaveSettings = true,
            ShowVersionInfo = false
        };
        indicators.Add(bigTradeIndicator);
    }

    if (MarketDepth_Enable)
    {
        marketDepthIndicator = new StrategyMarketDepthIndicator(this, MARKETDEPTH)
        {
            SaveSettings = true,
            ShowVersionInfo = false
        };
        indicators.Add(marketDepthIndicator);
    }

    return indicators;
}
```

### Export Setup (DataLoaded)

During `State.DataLoaded`, each enabled indicator gets an `IndicatorExport` object with its own data schema. The footprint export demonstrates the schema builder pattern:

```csharp
if (State == State.DataLoaded)
{
    char delimiter = !string.IsNullOrEmpty(Export_Delimiter)
        ? Export_Delimiter[0] : Export.DELIMITER;

    // Footprint export
    if (Footprint_Enable)
    {
        var fpExport = new IndicatorExport(this, footprintIndicator,
            ExportDataSource.Level1,
            Footprint_Export_Temporality,
            ExportGranularity.Bar,
            new ExportArgs()
            {
                IsExportWhileCollecting = false,
                IsFile = true,
                IsHeader = Export_Header,
                IsTime = Export_Time,
                Delimiter = delimiter,
                FileName = Export_File,
                IsBatch = Export_Batch,
                IsNinjaScriptOutput = Export_NinjaScriptOutput,
            });

        // Build schema with enabled fields
        DataSchema schema = new DataSchema();
        if (Footprint_OHLC) schema.Append("Open", ValueKind.Feature, ...);
        if (Footprint_OHLC) schema.Append("Close", ValueKind.Feature, ...);
        if (Footprint_OHLC) schema.Append("High", ValueKind.Feature, ...);
        if (Footprint_OHLC) schema.Append("Low", ValueKind.Feature, ...);
        // ... ~30 fields conditionally added
        if (Footprint_Volume) schema.Append("Volume", ValueKind.Feature, ...);
        if (Footprint_Delta) schema.Append("Delta", ValueKind.Feature, ...);
        if (Footprint_POC) schema.Append("POC", ValueKind.Feature, ...);
        // etc.

        fpExport.DataSet.Schema = schema;
        Register(fpExport);
    }

    // Volume Profile, Big Trade, Market Depth exports follow same pattern
    // ...
}
```

### Footprint Schema Fields

Each field is conditionally added based on a boolean property. The value is read from the footprint bar via a delegate:

```csharp
// Representative schema builder delegates
public double GetOpen(GeneralExport e, ValueDescriptor d, object data)
{
    IFootprintBar bar = data as IFootprintBar;
    return bar != null ? bar.Open : 0;
}

public double GetDelta(GeneralExport e, ValueDescriptor d, object data)
{
    IFootprintBar bar = data as IFootprintBar;
    return bar != null ? bar.Delta : 0;
}

// Volume ladders use signed format when enabled
public string GetVolumes(GeneralExport e, ValueDescriptor d, object data)
{
    IFootprintBar bar = data as IFootprintBar;
    if (bar == null) return "";
    return Footprint_SignedVolume
        ? bar.GetSignedVolumesString()
        : bar.GetVolumesString();
}
```

## Configurable Properties

### Export (Global)

| Property | Default | Description |
|---|---|---|
| `Export_Header` | `true` | Include column headers |
| `Export_Time` | `true` | Include timestamp column |
| `Export_Batch` | `false` | Batch write mode |
| `Export_Delimiter` | `;` | Column separator |
| `Export_File` | `""` | Custom file path (optional) |
| `Export_NinjaScriptOutput` | `false` | Write to NinjaScript output window |

### Footprint

| Property | Default | Description |
|---|---|---|
| `Footprint_Enable` | `true` | Enable footprint export |
| `Footprint_Export_Temporality` | `Historical` | Historical or Realtime |
| `Footprint_OHLC` | `true` | Export Open, Close, High, Low |
| `Footprint_Volume` | `true` | Export bar total volume |
| `Footprint_BuyVolume` | `true` | Export buy volume |
| `Footprint_SellVolume` | `true` | Export sell volume |
| `Footprint_Delta` | `true` | Export bar delta |
| `Footprint_POC` | `true` | Export POC price |
| `Footprint_SignedVolume` | `false` | +/- prefix for buy/sell |

:::note
The Data_Export source file contains 100+ boolean properties for fine-grained control over which fields are exported per indicator. Check the source file for the complete list — the properties follow the naming pattern `Footprint_*`, `VolumeProfile_*`, `BigTrade_*`, `MarketDepth_*`.
:::

### Volume Profile

| Property | Default | Description |
|---|---|---|
| `VolumeProfile_Enable` | `false` | Enable volume profile export |
| `VolumeProfile_Export_Temporality` | `Historical` | Historical or Realtime |

### Big Trade

| Property | Default | Description |
|---|---|---|
| `BigTrade_Enable` | `false` | Enable big trade export |
| `BigTrade_Export_Temporality` | `Realtime` | Historical or Realtime |

### Market Depth

| Property | Default | Description |
|---|---|---|
| `MarketDepth_Enable` | `false` | Enable market depth export (Level 2) |
| `MarketDepth_Export_Temporality` | `Realtime` | Historical or Realtime |

## Output File Location

By default, exported files are saved to:

```
Documents\NinjaTrader 8\mzpack\strategy\...\Data_Export\data\<instrument>_<id>.csv
```

## See Also

- [Built-in Strategies](/docs/strategies/built-in-strategies#data-export-strategy) — user-facing settings reference
- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Export Indicator Values](../samples/export-indicators-values.md) — simpler export sample
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile
