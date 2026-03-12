---
sidebar_position: 11
title: "Multi-DataSeries Advanced"
description: "Algo.Strategy trading on a secondary instrument/data series in unmanaged mode."
---

# Multi-DataSeries Advanced

Demonstrates trading on a second data series using `Algo.Strategy` in unmanaged mode. Adds a secondary instrument/timeframe via `AddDataSeries` and routes trade execution to it.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/MultiDataSeriesAdvancedStrategy.cs`
**Class:** `MultiDataSeriesAdvancedStrategy : MZpackStrategyBase`

## What It Covers

- `Algo.Strategy` with `IsUnmanaged = true` (required for multi-dataseries)
- `WorkingDataSeriesIdx = -1` to pass all data series to the core
- `TradingDataSeriesIdx = 1` to route entries to the secondary series
- `UpDownBarSignal` for simple entry logic

## Strategy Setup

```csharp
protected MZpack.NT8.Algo.Strategy CreateAlgoStrategy()
{
    MZpack.NT8.Algo.Strategy strategy = new MZpack.NT8.Algo.Strategy(
        @"Multi-DataSeries Advanced", this)
    {
        IsUnmanaged = Strategy_Instrument_Enable ? true : false,
    };
    return strategy;
}
```

## Configuration

When the secondary instrument is enabled, `WorkingDataSeriesIdx` is set to `-1` so the core processes all data series, and `TradingDataSeriesIdx` routes entries to the secondary series:

```csharp
if (Strategy_Instrument_Enable)
{
    WorkingDataSeriesIdx = -1;  // Pass all dataseries to the core
    AddDataSeries(Strategy_Instrument_Name,
        Strategy_Instrument_BarsPeriodType,
        Strategy_Instrument_BarsPeriodValue);
    TradingDataSeriesIdx = 1;  // Route entries to secondary series
}

Entry[] entries = new Entry[EntriesPerDirection];
entries[0] = new Entry(Strategy)
{
    Quantity = 1,
    SignalName = "MDSA",
    StopLossCalculationMode = CalculationMode.Ticks,
    StopLossTicks = 10,
    ProfitTargetCalculationMode = CalculationMode.Ticks,
    ProfitTargetTicks = 20,
};

Pattern entryPattern = new Pattern(Strategy, Logic.And, null, true);
entryPattern.Signals.Root.AddChild(new UpDownBarSignal(Strategy) { Name = "Up/Down" });
Strategy.Initialize(entryPattern, exitPattern, entries);
```

## Configurable Properties

| Property | Default | Description |
|---|---|---|
| `Strategy_Instrument_Enable` | `true` | Enable secondary instrument |
| `Strategy_Instrument_Name` | `"MES 12-24"` | Secondary instrument name |
| `Strategy_Instrument_BarsPeriodType` | `Minute` | Secondary instrument period type |
| `Strategy_Instrument_BarsPeriodValue` | `1` | Secondary instrument period value |

## Key Points

- `IsUnmanaged = true` is mandatory for multi-dataseries strategies
- `WorkingDataSeriesIdx = -1` tells the core to process all data series, not just the primary
- `TradingDataSeriesIdx` sets which data series receives the trade entries

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Entry](../strategies/entry.md) — entry configuration
- [Multi-DataSeries Strategy](multi-dataseries-strategy.md) — indicators on multiple data series
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
