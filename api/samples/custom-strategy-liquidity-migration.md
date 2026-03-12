---
sidebar_position: 20
title: "Custom Strategy — Liquidity Migration"
description: "Liquidity migration from StrategyMarketDepthIndicator (1 Tick, live/replay)"
---

# Custom Strategy — Liquidity Migration

Demonstrates liquidity migration data from `StrategyMarketDepthIndicator`. Use on a 1 Tick chart, live or replay only. This is a custom strategy without Algo.Strategy.

**Source:** `[INSTALL PATH]/API/Samples/MZpackCustomStrategy6.cs`
**Class:** `MZpackCustomStrategy6 : MZpackStrategyBase`

## What It Covers

- `OnMarketDepthHandler` for DOM events
- Liquidity migration calculation: sum bid vs offer migration volumes from blocks
- Entry when migration ratio exceeds threshold
- Migration filters: added volume, bars count, ratio

## Indicator Setup

```csharp
marketDepthIndicator = new StrategyMarketDepthIndicator(this, @"MarketDepth 6")
{
    ShowHistoricalDOM = true,
    ShowImbalance = false,
    ShowRealtimeOrderBook = false,
    ShowCumulativeLevelII = false,
    ShowLiquidityMigration = true,
    MarketDepthFilteringMode = MarketDepthFilteringMode.Percentage,
    UseAboveExpectedAlert = false,
};
```

## Strategy Logic

The `OnMarketDepthHandler` sums bid and offer migration volumes from blocks that meet the added-volume and bars-count filters, then enters when the ratio between the two sides exceeds the threshold.

```csharp
protected void StrategyOnMarketDepthHandler(MarketDepthEventArgs e, int currentBarIdx)
{
    if (Position.MarketPosition == MarketPosition.Flat
        && signalLong == null && signalShort == null)
    {
        MarketDepthBlocks blocks;
        if (marketDepthIndicator.Blocks.TryGetValue(CurrentBar, out blocks))
        {
            float bidMigration = blocks
                .Where(x => x.Value.Descriptor.Side == TradeSide.Bid
                    && x.Value.Delta >= Strategy_MigrationAddedVolume
                    && x.Value.Descriptor.StopBarIdx - x.Value.Descriptor.StartBarIdx
                        >= Strategy_MigrationBarsCount)
                .Sum(x => x.Value.Delta);

            float offerMigration = blocks
                .Where(x => x.Value.Descriptor.Side == TradeSide.Ask
                    && x.Value.Delta > Strategy_MigrationAddedVolume
                    && x.Value.Descriptor.StopBarIdx - x.Value.Descriptor.StartBarIdx
                        >= Strategy_MigrationBarsCount)
                .Sum(x => x.Value.Delta);

            if (bidMigration > 0 || offerMigration > 0)
            {
                float ratio = (bidMigration == 0 || offerMigration == 0)
                    ? int.MaxValue
                    : Math.Max(bidMigration, offerMigration)
                        / Math.Min(bidMigration, offerMigration);

                if (ratio >= Strategy_MigrationRatio)
                {
                    if (bidMigration > offerMigration)
                    {
                        // Enter LONG...
                    }
                    else
                    {
                        // Enter SHORT...
                    }
                }
            }
        }
    }
}
```

## Configurable Properties

### Entry

| Property | Default | Description |
|---|---|---|
| `Entry_TakeProfitTicks` | `4` | Take profit ticks |
| `Entry_StopLossTicks` | `4` | Stop loss ticks |

### Strategy

| Property | Default | Description |
|---|---|---|
| `Strategy_MigrationAddedVolume` | `40` | Min added volume for migration |
| `Strategy_MigrationBarsCount` | `10` | Min bars in migration block |
| `Strategy_MigrationRatio` | `1.5` | Bid/offer migration ratio threshold |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
