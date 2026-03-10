---
sidebar_position: 5
title: "Event Arguments"
description: "Reference for OrderflowEventArguments, QuoteEventArgs, ExecutionEventArgs, and OrderBookEventArgs event types in MZpack."
---

# Event Arguments

Event argument types delivered to indicator and strategy callbacks during market data processing.

**Namespace:** `MZpack`

## ExecutionEventArgs (class)

Represents a single trade execution (Level 1 tick). This is the primary event type received in `OnEachTick` and `OnBarClose` handlers.

**Implements:** `IMarketDataEvent`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Price` | `double` | — | Execution price |
| `Volume` | `long` | — | Execution volume |
| `Side` | `TradeSide` | `NA` | Trade side: `Ask`, `Bid`, or `NA` |
| `Time` | `DateTime` | `MinValue` | Execution timestamp |
| `BarIdx` | `int` | −1 | Main data series bar index |
| `MinuteBarIdx` | `int` | −1 | One-minute data series bar index |
| `PriorPrice` | `double` | — | Previous execution price |
| `Gaps` | `SortedDictionary<double, long>` | — | Order flow gaps (price → volume) |
| `FirstTickOfBar` | `bool` | — | First tick in the current bar |
| `FirstBarOfSession` | `bool` | — | First bar of the trading session |
| `FirstTickOfFirstOneMinuteBar` | `bool` | — | First tick of a 1-minute bar inside the main bar |
| `OneMinuteBarOnClose` | `bool` | — | One-minute bar close mode flag |
| `IsBarOpened` | `bool` | — | Computed: `true` when a new bar boundary is detected |
| `OrderflowIgnore` | `bool` | `false` | Skip this event in order flow calculations |
| `Idle` | `bool` | `false` | Indicator is in idle mode |

### Usage

```csharp
// In a strategy's OnEachTick handler
protected override void OnEachTick(MZpack.ExecutionEventArgs e)
{
    double price = e.Price;
    long volume = e.Volume;
    TradeSide side = e.Side;
    int barIndex = e.BarIdx;
}
```

## QuoteEventArgs (class)

Represents a best bid or ask quote update.

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Price` | `double` | — | Quote price |
| `Volume` | `long` | — | Quote volume |
| `Side` | `TradeSide` | `NA` | Quote side: `Ask`, `Bid`, or `NA` |
| `Time` | `DateTime` | `MinValue` | Quote timestamp |
| `BarIdx` | `int` | −1 | Main data series bar index |

### ToString Format

```
"{Side} {Time} {Volume}-Lot @{Price} Bar:{BarIdx}"
```

## OrderBookEventArgs (abstract class)

Represents a Level 2 (market depth) order book update. The concrete implementation `PlatformOrderBookEventArgs` wraps the NinjaTrader `MarketDepthEventArgs`.

### Properties

| Property | Type | Description |
|---|---|---|
| `Price` | `double` | Price level |
| `Volume` | `long` | Volume at the level |
| `Side` | `TradeSide` | `Ask` or `Bid` side |
| `Time` | `DateTime` | Event timestamp |
| `Position` | `int` | Level position in the order book |
| `Operation` | `OrderBookOperation` | `Insert`, `Update`, or `Remove` |
| `MarketMaker` | `string` | Market maker identifier |
| `IsReset` | `bool` | Order book reset flag |
| `Rows` | `List<OrderBookPosition>` | Snapshot of order book rows |
| `PlatformEventArgs` | `object` | Original NinjaTrader event args |

### OrderBookOperation Enum

| Value | Description |
|---|---|
| `Insert` | New level added to the book |
| `Update` | Existing level updated |
| `Remove` | Level removed from the book |

### OrderBookPosition

| Property | Type | Description |
|---|---|---|
| `Price` | `double` | Price level |
| `Volume` | `long` | Volume at the level |
| `Side` | `TradeSide` | `Ask` or `Bid` |
| `MarketMaker` | `string` | Market maker identifier |

## OrderflowEventArguments (struct)

Lightweight event for aggregated order flow data.

### Properties

| Property | Type | Description |
|---|---|---|
| `Price` | `double` | Price level |
| `Volume` | `long` | Aggregated volume |
| `Side` | `TradeSide` | `Ask` or `Bid` |
| `Time` | `DateTime` | Event timestamp |

### Delegate

```csharp
delegate void OrderflowEventHandler(OrderflowEventArguments e);
```
