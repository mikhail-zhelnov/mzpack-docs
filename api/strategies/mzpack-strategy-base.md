---
sidebar_position: 2
title: "MZpackStrategyBase"
description: "Reference for MZpackStrategyBase — the abstract base class for all MZpack strategies on NinjaTrader 8."
---

# MZpackStrategyBase

`MZpackStrategyBase` is the abstract base class for all MZpack strategies. It extends NinjaTrader's strategy infrastructure with MZpack indicator management, market data routing, and SharpDX chart rendering.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `MZpackStrategyBase : StrategyRenderBase : NinjaTrader.NinjaScript.Strategies.Strategy`
**Source:** `MZpack.NT8/Algo/MZpackStrategyBase.cs`

## Delegates

Set these in your strategy constructor or `OnStateChange(SetDefaults)` to define the strategy and its indicators:

| Delegate | Signature | Purpose |
|---|---|---|
| `OnCreateAlgoStrategy` | `Strategy OnCreateAlgoStrategyDelegate()` | Create and return the `Algo.Strategy` instance |
| `OnCreateIndicators` | `List<TickIndicator> OnCreateIndicatorsDelegate()` | Create and return the list of strategy indicators |
| `OnEachTickHandler` | `void OnTickDelegate(MarketDataEventArgs e, int currentBarIdx)` | Custom tick processing |
| `OnBarCloseHandler` | `void OnTickDelegate(MarketDataEventArgs e, int currentBarIdx)` | Custom bar close processing |
| `OnMarketDepthHandler` | `void OnMarketDepthDelegate(MarketDepthEventArgs e, int currentBarIdx)` | Custom Level 2 processing |

## Core Properties

### Strategy and Indicators

| Property | Type | Description |
|---|---|---|
| `Strategy` | `Strategy` | The `Algo.Strategy` instance (set via `OnCreateAlgoStrategy`) |
| `Indicators` | `ObservableCollection<TickIndicator>` | All strategy indicators |
| `Exports` | `Exports` | Data export handler |

### Data Series Configuration

| Property | Type | Default | Description |
|---|---|---|---|
| `WorkingDataSeriesIdx` | `int` | -1 | Which data series drives pattern logic (-1 = all) |
| `TradingDataSeriesIdx` | `int` | 0 | Where orders are submitted |
| `PatternValidatingDataSeriesIdx` | `int` | 0 | Data series for dashboard display |

### Operating Mode

| Property | Type | Default | Description |
|---|---|---|---|
| `Operating` | `StrategyOperating` | `Auto` | `Auto` = automated entries, `Manual` = chart trader entries |
| `PositionManagement` | `PositionManagement` | `MZpack` | `MZpack` = MZpack manages position, `NinjaTraderATM` = use ATM template |
| `WorkingStateRealtime` | `bool` | `true` | Process data in real-time |
| `WorkingStateHistorical` | `bool` | `false` | Process data on historical bars |
| `EnableBacktesting` | `bool` | `false` | Enable backtesting mode |

### Logging

| Property | Type | Default | Description |
|---|---|---|---|
| `LogLevel` | `LogLevel` | `NONE` | Log verbosity flags |
| `LogTarget` | `LogTarget` | `NinjaScriptOutput` | Output destination (File, NinjaScriptOutput, or All) |

## Key Methods

### Indicator Management

| Method | Return Type | Description |
|---|---|---|
| `GetIndicator<T>(string name)` | `TickIndicator` | Get indicator by type and name |
| `GetIndicator(string name)` | `TickIndicator` | Get indicator by name |
| `RemoveIndicator(TickIndicator indicator)` | `void` | Remove an indicator |

### Data Series

| Method | Return Type | Description |
|---|---|---|
| `AddTickDataSeries()` | `void` | Add 1-tick data series (auto-called if tick replay is off) |
| `AddCustomDataSeries(BarsPeriodType, int)` | `int` | Add custom period data series, returns index |

### Price Helpers

| Method | Return Type | Description |
|---|---|---|
| `RoundToTickSize(double price)` | `double` | Round to valid tick size |
| `PriceDiffTicks(double high, double low)` | `int` | Tick distance between prices |
| `PriceAddTicks(double price, int ticks)` | `double` | Add ticks to price |
| `PriceSubtractTick(double price)` | `double` | Subtract one tick |
| `Compare(double price1, double price2)` | `int` | Tick-aware price comparison |
| `IsPriceApproaching(double price, double level, int ticks)` | `bool` | Check if price is within N ticks of level |

### Candle Access

| Method | Return Type | Description |
|---|---|---|
| `GetCandle(int ago)` | `ICandle` | Get candle from primary data series |
| `GetCandle(int ago, int dataseries)` | `ICandle` | Get candle from specific data series |

### Control Panel

| Method | Return Type | Description |
|---|---|---|
| `CreateControlPanelElements()` | `UIElement[]` | Override to create custom UI controls |
| `ControlPanel_AttachEventHandlers()` | `void` | Override to attach control event handlers |
| `ControlPanel_DetachEventHandlers()` | `void` | Override to detach control event handlers |

## Enums

### StrategyOperating

| Value | Description |
|---|---|
| `Auto` | Entries made automatically when patterns validate |
| `Manual` | Entries made manually from chart trader |

### PositionManagement

| Value | Description |
|---|---|
| `MZpack` | Position managed by MZpack API (Entry/Exit/Trail) |
| `NinjaTraderATM` | Position managed by NinjaTrader ATM template |

## Example: Minimal Custom Strategy

```csharp
public class MyCustomStrategy : MZpackStrategyBase
{
    StrategyFootprintIndicator footprint;
    StrategyVolumeProfileIndicator vpIndicator;

    public MyCustomStrategy()
    {
        // Create indicators
        OnCreateIndicators = () =>
        {
            footprint = new StrategyFootprintIndicator(this, "FP");
            footprint.TicksPerLevel = 1;

            vpIndicator = new StrategyVolumeProfileIndicator(this, "VP");
            vpIndicator.ProfileCreation = ProfileCreation.Session;
            vpIndicator.ProfileAccuracy = ProfileAccuracy.Minute;

            return new List<TickIndicator> { footprint, vpIndicator };
        };

        EnableBacktesting = true;
        WorkingStateHistorical = true;
    }

    protected override void OnBarUpdate()
    {
        if (BarsInProgress != TradingDataSeriesIdx) return;
        if (CurrentBar < 10) return;

        IFootprintBar bar = footprint.FootprintBars[CurrentBar];
        IVolumeProfile profile = vpIndicator.GetProfile(0);
        if (profile == null) return;

        // Buy when delta is positive and price is below VWAP
        if (bar.Delta > 0 && Close[0] < profile.VWAP)
        {
            EnterLong();
        }
    }
}
```

## See Also

- [Strategy Framework Overview](overview.md) — choosing between Custom and Algo approaches
- [Algo.Strategy](algo-strategy.md) — pattern-oriented framework
- [Advanced Template](../samples/advanced-template.md) — full strategy template sample
