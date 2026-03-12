---
sidebar_position: 19
title: "Custom Strategy — DOM + Footprint"
description: "StrategyMarketDepthIndicator with StrategyFootprintIndicator, DOM imbalance/block/pace rules (Level 2, live/replay)"
---

# Custom Strategy — DOM + Footprint

Demonstrates `StrategyMarketDepthIndicator` with `StrategyFootprintIndicator`, combining DOM imbalance, block, and pace-of-tape rules. Requires Level 2 data (live/replay only). Recommended for ES 5 Min chart during RTH. This is a custom strategy without Algo.Strategy.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/MZpackCustomStrategy4.cs`
**Class:** `MZpackCustomStrategy4 : MZpackStrategyBase`

## What It Covers

- `OnEachTickHandler` for footprint data (pace of tape, session POC)
- `OnMarketDepthHandler` for DOM events (imbalance, block detection)
- 4-rule entry logic: pace of tape, DOM imbalance ratio, large limit order blocks within distance, session POC directional confirmation
- Position enters opposite direction when all rules align on one side

## Indicator Setup

```csharp
marketDepthIndicator = new StrategyMarketDepthIndicator(this, @"Depth Imbalance")
{
    ShowRealtimeOrderBook = false,
    ShowCumulativeLevelII = false,
    ShowHistoricalDOM = true,
    ShowImbalance = false,
    HoldLevels = true,
    MarketDepthFilteringMode = MarketDepthFilteringMode.Absolute,
    DisplayVolume = Strategy_BlockVolumeFilter,
    ExtremeVolume = Strategy_BlockVolumeFilter * 2,
    UseAboveExpectedAlert = false,
};

footprintIndicator = new StrategyFootprintIndicator(this, @"Clusters")
{
    RightFootprintStyle = FootprintStyle.TradesNumber,
    RightClusterStyle = ClusterStyle.Histogram,
    LeftFootprintStyle = FootprintStyle.Delta,
    LeftClusterStyle = ClusterStyle.None,
    ShowSessionPOC = true,
    ShowSessionVA = true,
    SessionDailyProfileMode = SessionDailyProfileMode.Session,
    // All other stat/imbalance/absorption features disabled
};
```

## Pace of Tape (OnEachTickHandler)

Counts trades near bar high and low within `Strategy_ClusterRange` levels. Sets `tradesClusterLo`/`tradesClusterHi` flags and determines direction by session POC.

```csharp
protected void StrategyOnEachTickHandler(MarketDataEventArgs e, int currentBarIdx)
{
    IFootprintBar bar;
    if (footprintIndicator.FootprintBars.TryGetValue(currentBarIdx, out bar))
    {
        double priceLo = bar.Lo, priceHi = bar.Hi;
        int tradesOnLo = 0, tradesOnHi = 0;

        for (int i = 0; i < Strategy_ClusterRange; i++)
        {
            int n;
            bar.TradesNumbers.TryGetValue(priceLo, out n);
            tradesOnLo += n;
            bar.TradesNumbers.TryGetValue(priceHi, out n);
            tradesOnHi += n;
            priceLo = footprintIndicator.RoundToTickSize(priceLo + TickSize);
            priceHi = footprintIndicator.RoundToTickSize(priceHi - TickSize);
        }

        tradesClusterLo = tradesOnLo >= Strategy_TradesNumber;
        tradesClusterHi = tradesOnHi >= Strategy_TradesNumber;
        directionBySessionPOC = e.Price.ApproxCompare(bar.Session.POC) > 0
            ? MarketPosition.Short : MarketPosition.Long;
    }
}
```

## DOM Entry Logic (OnMarketDepthHandler)

Enters when all four rules align: pace-of-tape cluster, DOM bid/offer ratio, block within distance, and session POC direction.

```csharp
protected void StrategyOnMarketDepthHandler(MarketDepthEventArgs e, int currentBarIdx)
{
    if (Position.MarketPosition == MarketPosition.Flat
        && signalLong == null && signalShort == null
        && (tradesClusterLo || tradesClusterHi))
    {
        long bid = marketDepthIndicator.RealtimeOrderBook.GetVolume(TradeSide.Bid);
        long offer = marketDepthIndicator.RealtimeOrderBook.GetVolume(TradeSide.Ask);

        if (bid > 0 && offer > 0)
        {
            if (bid > offer)
            {
                double ratio = (double)bid / offer;
                if (ratio > Strategy_Ratio && tradesClusterLo
                    && directionBySessionPOC == MarketPosition.Long
                    && OrderbookOrderRule(MarketPosition.Long))
                {
                    // Enter LONG...
                }
            }
            // Mirror logic for SHORT...
        }
    }
}
```

## Block Detection Helper

Checks whether any blocks at the current bar meet the volume filter and are within the configured distance from the current price.

```csharp
bool OrderbookOrderRule(MarketPosition direction)
{
    if (marketDepthIndicator.Blocks.ContainsKey(CurrentBar))
    {
        TradeSide depthSide = direction == MarketPosition.Long
            ? TradeSide.Bid : TradeSide.Ask;
        double price = direction == MarketPosition.Long
            ? GetCurrentBid() : GetCurrentAsk();

        List<KeyValuePair<double, IMarketDepthBlock>> blocks =
            marketDepthIndicator.Blocks[CurrentBar]
            .Where(x => GetDistanceTicks(price, x.Key, depthSide)
                <= Strategy_BlockDistanceTicks
                && x.Value.Volume >= Strategy_BlockVolumeFilter).ToList();

        return blocks.Count > 0;
    }
    return false;
}
```

## Configurable Properties

### Entry

| Property | Default | Description |
|---|---|---|
| `Strategy_TakeProfitTicks` | `33` | Take profit ticks |
| `Strategy_StopLossTicks` | `22` | Stop loss ticks |

### Strategy

| Property | Default | Description |
|---|---|---|
| `Strategy_Ratio` | `1.4` | DOM bid/offer imbalance ratio |
| `Strategy_BlockVolumeFilter` | `600` | Block volume filter |
| `Strategy_BlockDistanceTicks` | `8` | Max block distance from price |
| `Strategy_TradesNumber` | `500` | Min trades in cluster range |
| `Strategy_ClusterRange` | `3` | Levels from bar high/low to check |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzFootprint](data-access-footprint.md) — footprint data
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
