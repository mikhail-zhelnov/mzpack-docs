---
sidebar_position: 10
title: "Fibonacci Retracement Entry"
description: "Fibonacci retracement entry strategy using FiboRetracementEntry with swing high/low from previous bar"
---

# Fibonacci Retracement Entry

Demonstrates the `FiboRetracementEntry` class by assigning swing high/low from the previous bar in `OnPositionOpenFilter`. This is a strategy subclass (not `MZpackStrategyBase`) — it must be used with a `MZpackStrategyBase` host that configures entries with `FiboRetracementEntry` objects.

**Source:** `[INSTALL PATH]/API/Samples/Built-in/FiboRetracementEntry.cs`
**Class:** `FiboRetracementEntryStrategy : MZpack.NT8.Algo.Strategy`

## What It Covers

- Subclass of `Algo.Strategy` (not `MZpackStrategyBase`)
- `OnPositionOpenFilter` override to set `FiboRetracementEntry` swing levels
- Uses previous bar's High/Low as swing for Fibonacci retracement calculation

## Source Code

```csharp
public class FiboRetracementEntryStrategy : MZpack.NT8.Algo.Strategy
{
    public FiboRetracementEntryStrategy(string name, MZpackStrategyBase strategy)
        : base(name, strategy) { }

    public override bool OnPositionOpenFilter(DateTime time)
    {
        MZpack.NT8.Algo.Position position = Positions.FirstOrDefault();
        if (position != null)
        {
            foreach (var e in position.Entries)
            {
                if (e is FiboRetracementEntry)
                {
                    ((FiboRetracementEntry)e).SwingHigh = MZpackStrategy.Highs[0][1];
                    ((FiboRetracementEntry)e).SwingLow = MZpackStrategy.Lows[0][1];
                }
            }
            return true;
        }
        return false;
    }
}
```

## Key Points

- `FiboRetracementEntry` requires swing levels to calculate retracement entry prices
- `OnPositionOpenFilter` fires before position opens — the ideal place to set dynamic swing levels
- `Highs[0][1]` and `Lows[0][1]` reference the previous bar (1 bar ago) for on-bar-close strategies

## See Also

- [Algo.Strategy](../strategies/algo-strategy.md) — strategy base class
- [Entry](../strategies/entry.md) — entry types
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
