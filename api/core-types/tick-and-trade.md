---
sidebar_position: 2
title: "Tick & ITrade"
description: "Reference for Tick, TickVolume, and ITrade types used for market data processing in MZpack."
---

# Tick & ITrade

Low-level types representing individual market ticks and trade data.

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

## TradeSide Enum

| Value | Description |
|---|---|
| `Ask` | Ask-side (buy) trade |
| `Bid` | Bid-side (sell) trade |
| `NA` | Side not applicable |
