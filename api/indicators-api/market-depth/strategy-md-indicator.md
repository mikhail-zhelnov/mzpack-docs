---
sidebar_position: 2
title: "StrategyMarketDepthIndicator"
description: "Reference for StrategyMarketDepthIndicator — the strategy wrapper for mzMarketDepth providing DOM data access in automated strategies."
---

# StrategyMarketDepthIndicator

`StrategyMarketDepthIndicator` wraps [mzMarketDepth](/docs/indicators/mzMarketDepth) for use inside MZpack strategies. It implements [IMarketDepthIndicator](imarket-depth-indicator.md).

**Namespace:** `MZpack.NT8.Algo.Indicators`
**Inheritance:** `StrategyMarketDepthIndicator : mzMarketDepth, IMarketDepthIndicator`
**Conditional:** `#if !FREE`
**Data level:** Level 2
**Source:** `[INSTALL PATH]/API/Indicators/StrategyMarketDepthIndicator.cs`

:::warning
Requires Level 2 data — live or replay only. DOM data is not available in historical backtesting without replay.
:::

## Setup in a Strategy

```csharp
public class MyStrategy : MZpackStrategyBase
{
    StrategyMarketDepthIndicator mdIndicator;

    protected override void OnStateChange()
    {
        if (State == State.Configure)
        {
            mdIndicator = new StrategyMarketDepthIndicator(this, "MD");

            // Configure depth
            mdIndicator.MaxMarketDepth = 10;
            mdIndicator.ShowImbalance = true;
            mdIndicator.ImbalancePercentage = 150;
        }
    }
}
```

## Accessing Data

```csharp
protected override void OnBarUpdate()
{
    // Read real-time DOM
    IRealtimeOrderBook book = mdIndicator.RealtimeOrderBook;
    if (book == null) return;

    // Bid/ask imbalance
    long totalBids = book.GetTotalVolume(TradeSide.Bid);
    long totalAsks = book.GetTotalVolume(TradeSide.Ask);

    if (totalAsks > 0)
    {
        double ratio = (double)totalBids / totalAsks;

        if (ratio > 1.5)
        {
            // Strong bid support — potential buying pressure
        }
        else if (ratio < 0.67)
        {
            // Strong ask pressure — potential selling pressure
        }
    }

    // Read liquidity migration
    if (mdIndicator.OverallMigrations.ContainsKey(CurrentBar))
    {
        IBarLiquidity migration = mdIndicator.OverallMigrations[CurrentBar];
        // Analyze liquidity shifts
    }
}
```

## Exported Values

| Category | Values |
|---|---|
| **Depth** | MarketDepth, RealMarketDepth |
| **Real-time** | RealtimeBid, RealtimeOffer, BestBid, BestOffer |
| **Totals** | RealtimeBidsTotal, RealtimeOffersTotal |
| **Quantitative** | HQA, UQ, AC, UpdatesNumber |

## See Also

- [IMarketDepthIndicator](imarket-depth-indicator.md) — interface reference
