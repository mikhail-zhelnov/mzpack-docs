---
sidebar_position: 1
title: "DOMImbalanceSignal"
description: "Signal based on bid/ask ratio imbalance in the order book."
---

# DOMImbalanceSignal

Evaluates the bid/ask volume ratio in the real-time order book (DOM). A high bid/offer ratio signals Long (buying pressure), a high offer/bid ratio signals Short (selling pressure).

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `DOMImbalanceSignal : Signal`
**Data source:** Level2 | **Calculate:** NotApplicable
**Indicator:** StrategyMarketDepthIndicator

:::warning
Requires Level 2 data — live or replay only. Not available in historical backtesting.
:::

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `Ratio` | `double` | 1.5 | Imbalance ratio threshold |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Bid / Offer >= `Ratio` |
| **Short** | Offer / Bid >= `Ratio` |

Entry price: best bid for Long, best offer for Short.

## Example

```csharp
var signal = new DOMImbalanceSignal(strategy,
    MarketDataSource.Level2, SignalCalculate.NotApplicable);
signal.Ratio = 2.0;

pattern.Signals.Root.Add(signal);
```
