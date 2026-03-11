---
sidebar_position: 12
title: "Trail"
description: "Reference for TrailBase, Trail, and BarHiLoTrail — trailing stop management after position entry."
---

# Trail

`TrailBase` is the abstract base for trailing stops. A trail is attached to an [Entry](entry.md) and manages the stop loss dynamically after position entry. Two built-in implementations cover tick-based and bar-based trailing.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `TrailBase` (abstract)
**Source:** `MZpack.NT8/Algo/Extensions/Trails/TrailBase.cs`

## TrailBase Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Calculate` | `Calculate` | `OnEachTick` | When to evaluate: `OnEachTick` or `OnBarClose` |
| `IsActive` | `bool` | `true` | Enable/disable the trail |

### Read-Only State

| Property | Type | Description |
|---|---|---|
| `IsTrailed` | `bool` | True once trailing has begun |
| `TrailingPrice` | `double` | Current trailing stop price |

## TrailBase Methods

| Method | Description |
|---|---|
| `OnExecution(Entry entry, MarketDataEventArgs e)` | Main loop: checks `IsActive`, calls `IsBeginTrailing`/`IsTrailingStep`, submits stop via `entry.SubmitStopLoss()` |
| `IsBeginTrailing(MarketPosition position, Entry entry)` | Abstract — return `true` when trailing should activate |
| `IsTrailingStep(MarketPosition position, Entry entry)` | Abstract — return `true` when the stop should move |
| `GetTrailingPrice(MarketPosition position, Entry entry)` | Abstract — return the new trailing stop price |
| `Reset()` | Reset `IsTrailed`, `TrailingPrice`, and internal state |

---

## Trail (Tick-Based)

Activates after a profit threshold, then moves the stop every N ticks at a fixed distance behind the current price.

**Inheritance:** `Trail : TrailBase`
**Source:** `MZpack.NT8/Algo/Extensions/Trails/Trail.cs`

### Properties

| Property | Type | Description |
|---|---|---|
| `TrailAfterTicks` | `int` | Ticks of profit before trailing starts |
| `TrailDistanceTicks` | `int` | Distance in ticks behind current price |
| `TrailStepTicks` | `int` | Minimum tick movement before stop is moved (1 = every tick) |

### Constructor

```csharp
public Trail(int trailAfterTicks, int trailDistanceTicks, int trailStepTicks)
```

### Behavior

- **Activation:** PnL in ticks >= `TrailAfterTicks`
- **Step:** price moved >= `TrailStepTicks` from last trailed price
- **Price (Long):** `RoundToTickSize(Bid - TicksToPrice(TrailDistanceTicks))`
- **Price (Short):** `RoundToTickSize(Ask + TicksToPrice(TrailDistanceTicks))`

---

## BarHiLoTrail (Bar-Based)

Trails the stop to the high or low of a bar N bars ago, with an optional tick shift.

**Inheritance:** `BarHiLoTrail : TrailBase`
**Source:** `MZpack.NT8/Algo/Extensions/Trails/BarHiLoTrail.cs`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `BarsAgo` | `int` | `1` | Reference bar (0 = current, 1 = previous) |
| `ShiftTicks` | `int` | `0` | Tick shift from bar high/low |

### Behavior

- **Activation:** `BarsAgo <= BarsSinceEntryExecution(SignalName)`
- **Step (Long):** `Low[BarsAgo] > TrailingPrice` (bar low moved up)
- **Step (Short):** `High[BarsAgo] < TrailingPrice` (bar high moved down)
- **Price (Long):** `Min(CurrentBid, RoundToTickSize(Low[BarsAgo] - ShiftTicks))`
- **Price (Short):** `Max(CurrentAsk, RoundToTickSize(High[BarsAgo] + ShiftTicks))`

## See Also

- [Pipeline](pipeline.md) — execution order of components
- [Entry](entry.md) — order submission and protective orders
- [Exit](exit.md) — exit conditions
