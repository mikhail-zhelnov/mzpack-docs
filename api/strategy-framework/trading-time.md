---
sidebar_position: 5
title: "TradingTime"
description: "Reference for TradingTime — restrict strategy trading to specific time windows."
---

# TradingTime

`TradingTime` defines a time window during which the strategy is allowed to trade. Outside these windows, the strategy will not open new positions. Multiple `TradingTime` instances can be added to `Strategy.TradingTimes` for complex schedules.

**Namespace:** `MZpack.NT8.Algo`
**Source:** `MZpack.NT8/Algo/TradingTime.cs`

## Properties

| Property | Type | Description |
|---|---|---|
| `Begin` | `DateTime` | Start time of the trading window (time-of-day portion is used) |
| `End` | `DateTime` | End time of the trading window (time-of-day portion is used) |

## Methods

| Method | Return Type | Description |
|---|---|---|
| `IsTrade(DateTime time)` | `bool` | Returns `true` if the given time is inside the trading window |
| `IsIdle(DateTime time)` | `bool` | Returns `true` if the given time is outside the trading window |

## Example: Trade RTH Session Only

```csharp
OnCreateAlgoStrategy = () =>
{
    var strategy = new Strategy("RTH_Only", this);

    // Only trade during Regular Trading Hours (9:30 AM - 4:00 PM ET)
    strategy.TradingTimes = new List<TradingTime>
    {
        new TradingTime
        {
            Begin = DateTime.Parse("09:30"),
            End = DateTime.Parse("16:00")
        }
    };

    // ... configure patterns, entries, etc.
    strategy.Initialize(entryPattern);
    return strategy;
};
```

## Example: Multiple Trading Windows

```csharp
// Trade morning and afternoon sessions, skip lunch
strategy.TradingTimes = new List<TradingTime>
{
    new TradingTime
    {
        Begin = DateTime.Parse("09:30"),
        End = DateTime.Parse("11:30")
    },
    new TradingTime
    {
        Begin = DateTime.Parse("13:00"),
        End = DateTime.Parse("15:45")
    }
};
```

## Integration with Strategy

The strategy checks `TradingTimes` via `Strategy.IsTrade(DateTime time, out string reason)`. If the current time is outside all trading windows, `IsTrade` returns `false` and the strategy skips position opening. The `TradingDays` property on `Strategy` provides day-of-week filtering separately.

## See Also

- [Algo.Strategy](algo-strategy.md) — parent strategy class
- [Trading Times](../samples/trading-times.md) — sample code
