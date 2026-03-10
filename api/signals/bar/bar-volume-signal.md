---
sidebar_position: 1
title: "BarVolumeSignal"
description: "Signal based on minimum bar volume threshold."
---

# BarVolumeSignal

Triggers when a bar's total volume meets or exceeds a minimum threshold. The signal returns a pre-configured direction — it acts as a volume filter rather than a directional signal.

**Namespace:** `MZpack.NT8.Algo.Signals`
**Inheritance:** `BarVolumeSignal : Signal`
**Data source:** Level1 | **Calculate:** OnBarClose

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `MinVolume` | `double` | — | Minimum bar volume required to trigger the signal |

## Signal Logic

The signal checks the current bar's total volume against `MinVolume`. If volume is sufficient, it returns the allowed direction configured in the decision tree node. It does not produce an entry price.

This signal is typically used as a **filter** in a decision tree to ensure trades only occur on bars with meaningful activity.

## Example

```csharp
var signal = new BarVolumeSignal(strategy);
signal.MinVolume = 5000;

pattern.Signals.Root.Add(signal);
```
