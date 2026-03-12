---
sidebar_position: 1
title: "IMarketDepthIndicator"
description: "Reference for the IMarketDepthIndicator interface — access to DOM snapshots, liquidity, liquidity migration, and Level II histogram."
---

# IMarketDepthIndicator

`IMarketDepthIndicator` provides programmatic access to the [mzMarketDepth](/docs/indicators/mzMarketDepth) chart indicator. It exposes the real-time order book, historical DOM blocks, liquidity data, liquidity migration, and Level II histogram configuration.

**Namespace:** `MZpack`
**Inheritance:** `IMarketDepthIndicator : ITickIndicator : IIndicator`
**Conditional:** `#if !FREE`
**Source:** `MZpackBase/mzMarketDepth/IMarketDepthIndicator.cs`

:::warning
Requires Level 2 data — live or replay only. Historical backtesting without Level 2 data will have empty DOM data.
:::

## Key Data Properties

| Property | Type | Description |
|---|---|---|
| `RealtimeOrderBook` | `IRealtimeOrderBook` | Current real-time DOM snapshot |
| `Blocks` | `Dictionary<int, MarketDepthBlocks>` | Historical DOM blocks indexed by bar |
| `OverallLiquidity` | `SortedDictionary<int, IBarLiquidity>` | Aggregated DOM liquidity per bar |
| `OverallMigrations` | `SortedDictionary<int, IBarLiquidity>` | Liquidity migration per bar |
| `OverallMigrationsClose` | `Series<double>` | Migration close values as a NinjaTrader Series |

## IRealtimeOrderBook

The real-time order book interface exposes the current DOM state:

| Property | Type | Description |
|---|---|---|
| `Time` | `DateTime` | Snapshot time |
| `MarketDepth` | `int` | Configured depth |
| `RealMarketDepth` | `int` | Actual available depth |
| `BestBid` | `double` | Best bid price |
| `BestOffer` | `double` | Best offer (ask) price |
| `Result` | `MarketDepthResult` | Snapshot result status |
| `Rows` | `List<OrderBookPosition>[]` | Raw order book rows |

| Method | Return Type | Description |
|---|---|---|
| `GetVolume(TradeSide side)` | `long` | Total volume on bid or ask side |
| `GetVolume(int position, TradeSide side)` | `long` | Volume at a specific depth level |
| `GetPrice(int position, TradeSide side)` | `double` | Price at a specific depth level |
| `GetTotalVolume(TradeSide side)` | `long` | Total volume across all levels |
| `GetTotalVolumeDepth(TradeSide side)` | `long` | Total volume within configured depth |
| `AggregateCloneRows(TradeSide side)` | `List<OrderBookPosition>` | Clone and aggregate rows for a side |

## DOM Configuration Properties

| Property | Type | Description |
|---|---|---|
| `MaxMarketDepth` | `int` | Maximum supported DOM depth |
| `MultipleMarketMaker` | `bool` | Support for multiple market makers |
| `ShowHistoricalDOM` | `bool` | Show historical DOM visualization |
| `HistoryDepthBars` | `int` | Number of historical bars with DOM data |
| `MarketDepthFilteringMode` | `MarketDepthFilteringMode` | Filtering mode for DOM display |

## Volume Display Properties

| Property | Type | Description |
|---|---|---|
| `CodeExtremeVolume` | `bool` | Highlight extreme volumes |
| `DisplayVolume` | `double` | Display volume threshold |
| `ExtremeVolume` | `double` | Extreme volume threshold |
| `DisplayVolumePercentage` | `int` | Display volume as percentage |
| `ExtremeVolumePercentage` | `int` | Extreme volume as percentage |
| `ShowVolumes` | `bool` | Show volume values |
| `ShowMaxVolumes` | `bool` | Show maximum volumes |

## Liquidity Properties

| Property | Type | Description |
|---|---|---|
| `ShowOverallLiquidity` | `bool` | Show aggregated liquidity |
| `ShowLiquidityMigration` | `bool` | Show per-bar migration |
| `ShowOverallLiquidityMigration` | `bool` | Show overall migration |
| `OverallLiquidityType` | `OverallLiquidityMigrationType` | Liquidity aggregation type |
| `OverallLiquidityMigrationType` | `OverallLiquidityMigrationType` | Migration aggregation type |
| `OverallLiquidityMigrationCumulate` | `bool` | Cumulate migration values |
| `AddedVolumeFilter` | `double` | Filter for added volume |
| `RemovedVolumeFilter` | `double` | Filter for removed volume |
| `HoldHigherVolume` | `bool` | Hold higher volume levels |
| `HoldLevels` | `bool` | Hold levels on chart |

## Imbalance Properties

| Property | Type | Description |
|---|---|---|
| `ShowImbalance` | `bool` | Show DOM bid/ask imbalance |
| `ImbalancePercentage` | `double` | Imbalance ratio threshold |

## Level II Histogram Properties

| Property | Type | Description |
|---|---|---|
| `ShowLevelIIHistogram` | `bool` | Show Level II ladder histogram |
| `LevelIIWidth` | `int` | Histogram width in pixels |
| `ShowLevelIIVolumes` | `bool` | Show volume labels |
| `ShowLevelIISideTotalPercent` | `bool` | Show bid/ask total percentage |
| `ShowLevelIIImbalance` | `bool` | Show Level II imbalance |
| `LevelIIImbalanceRatio` | `float` | Imbalance ratio |
| `ShowCumulativeLevelII` | `bool` | Show cumulative Level II |

## Example: Read DOM Bid/Ask Imbalance

```csharp
IMarketDepthIndicator mdIndicator = ...;

IRealtimeOrderBook book = mdIndicator.RealtimeOrderBook;
if (book == null) return;

// Total volume on each side
long totalBids = book.GetTotalVolume(TradeSide.Bid);
long totalAsks = book.GetTotalVolume(TradeSide.Ask);
double ratio = (double)totalBids / totalAsks;

// Read individual levels
for (int i = 0; i < book.RealMarketDepth; i++)
{
    double bidPrice = book.GetPrice(i, TradeSide.Bid);
    long bidVol = book.GetVolume(i, TradeSide.Bid);
    double askPrice = book.GetPrice(i, TradeSide.Ask);
    long askVol = book.GetVolume(i, TradeSide.Ask);
}

// Best bid/ask
double bestBid = book.BestBid;
double bestAsk = book.BestOffer;
```

## See Also

- [StrategyMarketDepthIndicator](strategy-md-indicator.md) — strategy wrapper class
