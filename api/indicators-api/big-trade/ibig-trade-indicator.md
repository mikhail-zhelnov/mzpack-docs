---
sidebar_position: 1
title: "IBigTradeIndicator"
description: "Reference for the IBigTradeIndicator interface — access to filtered trades, iceberg detection, DOM pressure, and trade presentation."
---

# IBigTradeIndicator

`IBigTradeIndicator` provides programmatic access to the [mzBigTrade](/docs/indicators/mzBigTrade) chart indicator. It exposes filtered trade lists, trade filter configuration (volume, iceberg, DOM pressure, aggression), and presentation settings.

**Namespace:** `MZpack`
**Inheritance:** `IBigTradeIndicator : IOrderFlowIndicator : ITickIndicator : IIndicator`
**Source:** `MZpackBase/mzBigTrade/IBigTradeIndicator.cs`

## Key Data Properties

These properties are available in `#if DATA` builds only.

| Property | Type | Description |
|---|---|---|
| `Trades` | `List<ITrade>` | All trades that pass the current filter |
| `ChartTrades` | `SortedDictionary<int, List<ITradeView>>` | Filtered trades as displayed on the chart, indexed by bar |
| `SingleTrades` | `List<ITrade>` | All single (unfiltered) trades |
| `ReconstructedTrades` | `List<ITrade>` | All reconstructed (unfiltered) trades |

## Trade Filter Properties

| Property | Type | Description |
|---|---|---|
| `TradeFilterType` | `TradeFilterType` | Type of filter |
| `FilterLogic` | `TradeFilterLogic` | ALL (all filters must match) or ANY (any filter matches) |
| `TradeFilterEnable` | `bool` | Enable volume filter |
| `TradeFilterMin` | `double` | Minimum volume threshold |
| `TradeFilterMax` | `double` | Maximum volume threshold |
| `TradeMultipleOfFilterEnable` | `bool` | Enable multiple-of filter |
| `TradeMultipleOfFilterValue` | `double` | Volume must be a multiple of this value |

## Iceberg Filter Properties

| Property | Type | Description |
|---|---|---|
| `IcebergFilterEnable` | `bool` | Enable iceberg detection filter |
| `IcebergFilterMin` | `double` | Minimum iceberg volume |

## DOM Pressure and Support Filters

| Property | Type | Description |
|---|---|---|
| `DomPressureFilterEnable` | `bool` | Enable DOM pressure filter |
| `DomPressureFilterMin` | `double` | Minimum DOM pressure |
| `DomPressureFilterMax` | `double` | Maximum DOM pressure |
| `DomSupportFilterEnable` | `bool` | Enable DOM support filter |
| `DomSupportFilterMin` | `double` | Minimum DOM support |
| `DomSupportFilterMax` | `double` | Maximum DOM support |

## Aggression and Smart Filters

| Property | Type | Description |
|---|---|---|
| `AggressionFilterEnable` | `bool` | Enable aggression filter |
| `AggressionFilterMin` | `int` | Minimum aggression ticks |
| `AggressionFilterMax` | `int` | Maximum aggression ticks |
| `SmartFilterEnable` | `bool` | Enable smart trade filter |

## Auto Filter Properties

| Property | Type | Description |
|---|---|---|
| `TradeFilterSelectionEnable` | `bool` | Enable auto filter selection |
| `TradeFilterSelection` | `TradeFilterSelection` | Auto filter mode |
| `TradeFilterSelection_PercentOfVolumes` | `double` | Percentage of volumes for auto filter |
| `TradeFilterSelection_PercentOfNumber` | `double` | Percentage of trade count for auto filter |
| `AutoFilterDays` | `int` | Number of days for auto filter calculation |
| `AutoFilterTradesPerDay` | `int` | Target trades per day |

## Presentation Properties

| Property | Type | Description |
|---|---|---|
| `PresentationType` | `PresentationType` | Trade marker presentation style |
| `MarkerType` | `TradeMarkerType` | Trade marker shape |
| `MarkerPosition` | `TradeMarkerPosition` | Marker position on chart |
| `ColorMode` | `ColorMode` | Color coding scheme |
| `ShowDomPressure` | `bool` | Show DOM pressure with trades |
| `ShowDomSupport` | `bool` | Show DOM support with trades |
| `ShowTradePOC` | `bool` | Show trade POC |

## Example: Read Filtered Trades

```csharp
IBigTradeIndicator btIndicator = ...;

// Get all filtered trades
foreach (ITrade trade in btIndicator.Trades)
{
    double price = trade.Price;
    long volume = trade.Volume;
    TradeSide side = trade.Side;
    DateTime time = trade.Time;
}

// Get trades for a specific bar
if (btIndicator.ChartTrades.ContainsKey(CurrentBar))
{
    foreach (ITradeView tradeView in btIndicator.ChartTrades[CurrentBar])
    {
        // Process trades on this bar
    }
}
```

## See Also

- [StrategyBigTradeIndicator](strategy-bigtrade-indicator.md) — strategy wrapper class
