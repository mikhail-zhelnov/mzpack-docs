---
sidebar_position: 4
title: "IOrderFlowIndicator"
description: "Reference for ITickIndicator and IOrderFlowIndicator — market data access, order flow calculation, tape reconstruction, and iceberg detection."
---

# IOrderFlowIndicator

Extends `ITickIndicator` with order flow configuration: calculation mode, tape reconstruction, and iceberg detection algorithm. This is the base interface for all order flow indicators (Footprint, BigTrade, VolumeDelta, DeltaDivergence).

**Namespace:** `MZpack`
**Inheritance:** `IOrderFlowIndicator : ITickIndicator : IIndicator`

## ITickIndicator

Real-time market data access and volume conversion utilities. Inherited by all tick-processing indicators.

### Price & Side

| Property | Type | Description |
|---|---|---|
| `BestBid` | `double` | Current best bid price |
| `BestAsk` | `double` | Current best ask price |
| `LastPrice` | `double` | Last trade price |
| `PriorPrice` | `double` | Previous trade price |
| `LastTradeSide` | `TradeSide` | Side of the last trade (`Ask`, `Bid`, `NA`) |
| `SideChanged` | `bool` | `true` if last trade side differs from previous |

### Volume Access

| Method | Returns | Description |
|---|---|---|
| `BestBidVolume()` | `long` | Current volume at best bid |
| `BestAskVolume()` | `long` | Current volume at best ask |
| `BestBidPriorVolume()` | `long` | Previous volume at best bid |
| `BestAskPriorVolume()` | `long` | Previous volume at best ask |

### Volume Conversion

Handles volume representation differences between standard instruments and cryptocurrencies.

| Method | Returns | Description |
|---|---|---|
| `FromInternalVolume(long)` | `double` | Convert internal long volume to display volume |
| `FromInternalVolume(double)` | `double` | Convert internal double volume to display volume |
| `VolumeToCryptoCurrency(long)` | `double` | Convert to cryptocurrency volume (decimal) |
| `VolumeToCryptoCurrency(double)` | `double` | Convert to cryptocurrency volume (decimal) |
| `VolumeFromCryptoCurrency(double)` | `long` | Convert cryptocurrency volume back to internal format |
| `VolumeToString(double, string, bool)` | `string` | Format volume as string using crypto decimal places |

| Property | Type | Description |
|---|---|---|
| `CryptoCurrencyVolumeDecimalPlaces` | `int` | Decimal places for cryptocurrency volume display |

## IOrderFlowIndicator

Configuration for order flow calculation and tape reconstruction.

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `OrderflowCalculationMode` | `OrderflowCalculationMode` | — | How bid/ask volumes are assigned to trades |
| `ReconstructTape` | `bool` | `true` | Enable tape reconstruction (aggregates individual trades into big trades) |
| `ReconstructTape_UseTimestampsOnly` | `bool` | `false` | Use only timestamps for tape reconstruction; Level 1 (best bid/ask) events are ignored, including for live data. Trades with equal timestamps are merged. Enable for exact match between reconstructed historical and live data. Iceberg detection, DOM pressure, and DOM support are unavailable when enabled |
| `OrderflowApplyMode` | `OrderflowApplyMode` | — | When mode changes take effect |
| `IcebergAlgo` | `IcebergAlgo` | — | Iceberg detection algorithm |
| `ReconstructTapeChangedUI` | `bool` | — | UI state flag: tape reconstruction setting changed |
| `OrderflowApplyModeChangedUI` | `bool` | — | UI state flag: apply mode setting changed |

## Enums

### OrderflowCalculationMode

| Value | Description |
|---|---|
| `BidAsk` | Bid/Ask calculation. Use for futures and stock markets. Requires Tick Replay for historical data |
| `UpDownTick` | Up/Down tick calculation. Use for Forex and crypto |
| `Hybrid` | UpDownTick for historical data, BidAsk for live. Use for NSE and similar markets |

### OrderflowApplyMode

| Value | Description |
|---|---|
| `ChartReload` | Changes applied on chart reload |
| `OnTheFly` | Changes applied immediately |

### IcebergAlgo

| Value | Description |
|---|---|
| `Hard` | Strict iceberg detection — requires exact volume match patterns |
| `Soft` | Relaxed iceberg detection — allows approximate matching |

## Derived Interfaces

| Interface | Adds |
|---|---|
| [IFootprintIndicator](footprint/ifootprint-indicator.md) | Footprint bars, sessions, imbalance/absorption data |
| [IBigTradeIndicator](big-trade/ibig-trade-indicator.md) | Filtered large trades, iceberg detection, DOM pressure |
| [IVolumeDeltaIndicator](volume-delta/ivolume-delta-indicator.md) | Delta per bar, cumulative delta |
| [IDeltaDivergenceIndicator](delta-divergence/idelta-divergence-indicator.md) | ZigZag breakpoints, divergence signals |
