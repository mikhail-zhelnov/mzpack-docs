---
sidebar_position: 2
title: "StrategyBigTradeIndicator"
description: "Reference for StrategyBigTradeIndicator — the strategy wrapper for mzBigTrade providing filtered trade data access."
---

# StrategyBigTradeIndicator

`StrategyBigTradeIndicator` wraps [mzBigTrade](/docs/indicators/mzBigTrade) for use inside MZpack strategies. It implements [IBigTradeIndicator](ibig-trade-indicator.md).

**Namespace:** `MZpack.NT8.Algo.Indicators`
**Inheritance:** `StrategyBigTradeIndicator : mzBigTrade, IBigTradeIndicator`
**Data level:** Level 1
**Source:** `[INSTALL PATH]/API/Indicators/StrategyBigTradeIndicator.cs`

## Setup in a Strategy

```csharp
public class MyStrategy : MZpackStrategyBase
{
    StrategyBigTradeIndicator btIndicator;

    protected override void OnStateChange()
    {
        if (State == State.Configure)
        {
            btIndicator = new StrategyBigTradeIndicator(this, "BigTrade");

            // Configure trade filter
            btIndicator.TradeFilterEnable = true;
            btIndicator.TradeFilterMin = 100;
            btIndicator.FilterLogic = TradeFilterLogic.All;

            // Optional: enable iceberg detection
            btIndicator.IcebergFilterEnable = true;
            btIndicator.IcebergFilterMin = 200;

            // Optional: DOM pressure filter
            btIndicator.DomPressureFilterEnable = true;
            btIndicator.DomPressureFilterMin = 1.5;
        }
    }
}
```

## Accessing Data

```csharp
protected override void OnBarUpdate()
{
    if (CurrentBar < 1) return;

    // Get the last N filtered trades
    List<ITrade> trades = btIndicator.Trades;
    int count = trades.Count;
    if (count == 0) return;

    // Most recent trade
    ITrade lastTrade = trades[count - 1];
    double price = lastTrade.Price;
    long volume = lastTrade.Volume;
    TradeSide side = lastTrade.Side;

    // Check for trades on the current bar
    if (btIndicator.ChartTrades.ContainsKey(CurrentBar))
    {
        var barTrades = btIndicator.ChartTrades[CurrentBar];
        long totalBuyVolume = 0;
        long totalSellVolume = 0;

        foreach (ITradeView tv in barTrades)
        {
            // Aggregate buy/sell volume
        }
    }
}
```

## Methods

| Method | Returns | Description |
|---|---|---|
| `DomPressureSignaturePassesFilter(ITrade trade)` | `bool` | Whether the trade's DOM pressure signature passes the current DOM pressure filters — enable, min/max absolute volume, min traded-sig volume, min hold duration, and min/max intensity. Returns `false` when the DOM pressure filter is disabled or the trade carries no DOM pressure |

Use it to gate strategy logic on DOM-pressure-confirmed trades without re-implementing the filter thresholds:

```csharp
protected override void OnBarUpdate()
{
    if (CurrentBar < 1) return;

    List<ITrade> trades = btIndicator.Trades;
    if (trades.Count == 0) return;

    ITrade lastTrade = trades[trades.Count - 1];

    // Act only on trades whose DOM pressure signature passes the configured filters
    if (btIndicator.DomPressureSignaturePassesFilter(lastTrade))
    {
        // e.g. absorption at the level — DomPressureVolume > 0 means liquidity was refilled
        double pressure = lastTrade.DomPressureVolume;
    }
}
```

:::note
DOM pressure detection is feed-time based and runs on live data and Market Replay only. Requires MZpack API 2.4.18+.
:::

## Exported Values

| Category | Values |
|---|---|
| **Price** | Open (StartPrice), Close (StopPrice), High, Low, RangeTicks |
| **Volume** | Volume, IcebergVolume |
| **POC** | POC, POCVolume |
| **DOM** | DomSupportVolume, DomPressureVolume, DomPressurePassesFilter |
| **Characteristics** | Side, Smart, TicksNumber |

## See Also

- [IBigTradeIndicator](ibig-trade-indicator.md) — interface reference
