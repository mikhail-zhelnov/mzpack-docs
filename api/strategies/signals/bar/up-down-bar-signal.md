---
sidebar_position: 5
title: "UpDownBarSignal"
description: "Signal based on whether the bar closed up (bullish) or down (bearish)."
---

# UpDownBarSignal

Returns a direction based on whether the current bar is bullish (Close > Open) or bearish (Close < Open). Optionally reverses the direction for counter-trend strategies.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `UpDownBarSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `IsReverse` | `bool` | `false` | Reverse the direction (bearish bar → Long, bullish bar → Short) |

## Signal Logic

| Direction | Condition |
|---|---|
| **Long** | Close > Open (bullish bar) |
| **Short** | Close < Open (bearish bar) |

When `IsReverse = true`, directions are swapped: a bearish bar returns Long and a bullish bar returns Short.

## Example

```csharp
var signal = new UpDownBarSignal(strategy);
signal.IsReverse = false; // trade with the bar direction

pattern.Signals.Root.Add(signal);
```
