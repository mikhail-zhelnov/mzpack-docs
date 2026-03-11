---
sidebar_position: 1
title: "ICandle"
description: "Reference for the ICandle interface representing OHLCV bar data in MZpack."
---

# ICandle

Interface representing a single OHLCV bar with computed body/wick metrics and candlestick pattern detection.

**Namespace:** `MZpack`

## Properties

### Price

| Property | Type | Description |
|---|---|---|
| `Open` | `double` | Opening price |
| `Close` | `double` | Closing price |
| `High` | `double` | Highest price |
| `Low` | `double` | Lowest price |

### Size & Structure

| Property | Type | Description |
|---|---|---|
| `Size` | `int` | Full candle range in ticks (High − Low) |
| `Body` | `int` | Body size in ticks |
| `UpperBody` | `double` | Upper body price (max of Open, Close) |
| `LowerBody` | `double` | Lower body price (min of Open, Close) |
| `UpperWick` | `int` | Upper wick size in ticks |
| `LowerWick` | `int` | Lower wick size in ticks |

### Other

| Property | Type | Description |
|---|---|---|
| `Time` | `DateTime` | Bar close time |
| `Volume` | `double` | Bar volume |

## Methods

| Method | Returns | Description |
|---|---|---|
| `IsBullish()` | `bool` | `true` if Close > Open |
| `IsBearish()` | `bool` | `true` if Close \< Open |
| `IsDoji()` | `bool` | `true` if candle is a doji pattern |
| `IsHammer()` | `bool` | `true` if candle is a hammer pattern |
| `GetUpperWickPercent()` | `int` | Upper wick as percentage of full range |
| `GetLowerWickPercent()` | `int` | Lower wick as percentage of full range |
