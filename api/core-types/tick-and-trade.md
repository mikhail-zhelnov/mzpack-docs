---
sidebar_position: 2
title: "Tick, Trade & TradeList"
description: "Reference for Tick, TickVolume, ITrade, Trade, and TradeList types used for market data processing in MZpack."
---

# Tick, Trade & TradeList

Low-level types representing individual market ticks and aggregated/reconstructed trades.

**Namespace:** `MZpack`

## Tick (struct)

A single market tick with price, volume, and bar context.

| Field | Type | Description |
|---|---|---|
| `Price` | `double` | Tick price |
| `Volume` | `long` | Tick volume |
| `BarIdx` | `int` | Bar index where the tick occurred |
| `IsFirstTickOfBar` | `bool` | `true` if this is the first tick of the bar |

## TickVolume (struct)

Breakdown of volume components for a single tick/price level.

| Field | Type | Description |
|---|---|---|
| `Volume` | `long` | Total volume |
| `IcebergVolume` | `int` | Hidden (iceberg) volume detected |
| `DomPressureVolume` | `int` | DOM pressure volume |
| `MarketLimitVolume` | `int` | Limit portion of Market-Limit orders |

## ITrade (interface)

Contract for a trade entity — either a single execution or a reconstructed aggregate trade.

### Identification

| Property | Type | Description |
|---|---|---|
| `Id` | `long` | Unique trade identifier (immutable during indicator load-unload cycle) |
| `Side` | `TradeSide` | Trade side: `Ask`, `Bid`, or `NA` |
| `Time` | `DateTime` | Trade timestamp |
| `Reconstructed` | `bool` | `true` if the trade is reconstructed from multiple executions |
| `Smart` | `bool` | Smart order flag |

### Price & Volume

| Property | Type | Description |
|---|---|---|
| `Volume` | `long` | Total trade volume |
| `IcebergVolume` | `int` | Iceberg volume component |
| `DomPressureVolume` | `int` | DOM pressure volume component |
| `DomSupportVolume` | `int` | DOM support volume component |
| `StartPrice` | `double` | Trade entry price |
| `StopPrice` | `double` | Trade exit price |
| `Hi` | `double` | Highest price level |
| `Lo` | `double` | Lowest price level |
| `POC` | `double` | Point of Control (price with highest volume) |
| `RangeTicks` | `int` | Number of distinct price levels |

### Bar Context

| Property | Type | Description |
|---|---|---|
| `StartBarIdx` | `int` | Bar index where trade began |
| `StopBarIdx` | `int` | Bar index where trade ended |
| `HiBarIdx` | `int` | Bar index with highest price |
| `LoBarIdx` | `int` | Bar index with lowest price |

### Data

| Property | Type | Description |
|---|---|---|
| `Ticks` | `List<Tick>` | Individual ticks composing the trade |
| `TickProfile` | `Dictionary<double, long>` | Price-to-volume mapping |
| `Trades` | `Dictionary<long, ITrade>` | Sub-trades (for reconstructed trades) |
| `View` | `ITradeView` | Chart visualization |

### Methods

| Method | Returns | Description |
|---|---|---|
| `Equals(ITrade)` | `bool` | Compare trades by `Id` |

## Trade (class)

**Inheritance:** `Trade : ITrade`

Concrete implementation of `ITrade`. Provides constructors for building trades from execution events.

### Constructor

```csharp
new Trade(TradeSide side, DateTime time, bool reconstructed, bool tapeSupport)
```

Use the constants `Trade.RECONSTRUCTED_TRADE` / `Trade.SINGLE_TRADE` and `Trade.TAPE_SUPPORT` for readability.

### Key Methods

| Method | Returns | Description |
|---|---|---|
| `AddTick(ExecutionEventArgs)` | `void` | Add a tick from an execution event |
| `AddTick(Tick)` | `void` | Add a `Tick` struct |
| `AddTick(bool, double, long, int)` | `void` | Add a tick with explicit parameters |
| `AddSingleTrade(Trade)` | `void` | Aggregate another single trade into this reconstructed trade |
| `Intersects(Trade)` | `bool` | Check price range intersection with another trade |
| `Intersects(double, double)` | `bool` | Check intersection with a price range (hi, lo) |
| `GetRange()` | `double` | Return Hi − Lo |

## TradeList (class)

**Inheritance:** `TradeList : List<Trade>, ITradeList`

A list of `Trade` objects with convenience methods and `IEnumerable<ITrade>` support.

### Methods

| Method | Returns | Description |
|---|---|---|
| `GetHighest()` | `Trade` | Trade with the highest price level |
| `GetLowest()` | `Trade` | Trade with the lowest price level |
| `Add(Trade, int)` | `void` | Add a trade with a max count limit (removes oldest if exceeded) |
| `ContainsRange(TradeList)` | `bool` | Check if all trades from another list are present |
| `OutOfTime(DateTime, int)` | `bool` | Check if any trade is older than `period` seconds |

## TradeSide Enum

| Value | Description |
|---|---|
| `Ask` | Ask-side (buy) trade |
| `Bid` | Bid-side (sell) trade |
| `NA` | Side not applicable |
