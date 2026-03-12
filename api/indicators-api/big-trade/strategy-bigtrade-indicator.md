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

## Exported Values

| Category | Values |
|---|---|
| **Price** | Open (StartPrice), Close (StopPrice), High, Low, RangeTicks |
| **Volume** | Volume, IcebergVolume |
| **POC** | POC, POCVolume |
| **DOM** | DomSupportVolume, DomPressureVolume |
| **Characteristics** | Side, Smart, TicksNumber |

## See Also

- [IBigTradeIndicator](ibig-trade-indicator.md) — interface reference
