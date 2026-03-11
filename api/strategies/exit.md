---
sidebar_position: 11
title: "Exit"
description: "Reference for ExitBase and BarCloseTarget — exit conditions that close positions based on market events."
---

# Exit

`ExitBase` is the abstract base for exit conditions. Each exit is attached to an [Entry](entry.md) and checked on every market event. When the exit condition is met, all positions are closed.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `ExitBase` (abstract)
**Source:** `MZpack.NT8/Algo/Extensions/Exits/ExitBase.cs`

## ExitBase Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Calculate` | `Calculate` | `OnEachTick` | When to check the exit condition: `OnEachTick` or `OnBarClose` |

## ExitBase Methods

| Method | Description |
|---|---|
| `OnExecution(Entry entry, MarketDataEventArgs e)` | Checks timing (first tick of bar or each tick), calls `CheckExit`, closes all positions if exit triggers |
| `CheckExit(MarketDataEventArgs e, Entry entry, MarketPosition marketPosition, out string reason)` | Abstract — return `true` to trigger exit, set `reason` for logging |
| `ClosePosition(Position position, string reason, DateTime time)` | Virtual — calls `position.CancelClose(false, reason, time)` |

---

## BarCloseTarget

Closes the position on the first bar close after the entry bar.

**Inheritance:** `BarCloseTarget : ExitBase`

### Constructor

```csharp
public BarCloseTarget()
```

Sets `Calculate = OnBarClose`.

### Behavior

`CheckExit` returns `true` when `CurrentBar > entry.FilledBarIdx` — i.e., the bar after the entry fill closes. Reason: `"Bar close"`.

---

## Custom Exit

To create a custom exit condition, subclass `ExitBase` and implement `CheckExit`:

```csharp
public class MyExit : ExitBase
{
    public override bool CheckExit(MarketDataEventArgs e, Entry entry,
        MarketPosition marketPosition, out string reason)
    {
        reason = null;

        if (/* your condition */)
        {
            reason = "My exit reason";
            return true;
        }

        return false;
    }
}
```

Attach the exit to an entry via `entry.Exit = new MyExit()`.

## See Also

- [Pipeline](pipeline.md) — execution order of components
- [Entry](entry.md) — order submission and protective orders
- [Trail](trail.md) — trailing stop management
