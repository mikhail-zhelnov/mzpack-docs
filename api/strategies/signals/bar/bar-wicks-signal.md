---
sidebar_position: 2
title: "BarWickSignal"
description: "Signal based on bar wick (shadow) size indicating rejection."
---

# BarWickSignal

Detects bars with a significant wick (shadow) on one side and a close at the opposite extreme, indicating price rejection.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `BarWickSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `MinWickTicks` | `int` | — | Minimum wick size in ticks to qualify |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Close == High **and** lower wick (Open − Low) >= `MinWickTicks` ticks |
| **Short** | Close == Low **and** upper wick (High − Open) >= `MinWickTicks` ticks |

A Long signal indicates a bullish rejection bar (pin bar) where price closed at the high with a long lower shadow. A Short signal indicates the opposite.

## Example

```csharp
var signal = new BarWickSignal(strategy);
signal.MinWickTicks = 8;

pattern.Signals.Root.Add(signal);
```
