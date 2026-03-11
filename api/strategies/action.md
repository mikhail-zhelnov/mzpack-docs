---
sidebar_position: 9
title: "Action"
description: "Reference for Action and RollingProfileAction — decision tree nodes that execute side effects during signal evaluation."
---

# Action

`Action` is a `Signal` subclass that executes a side effect at any position in the decision tree. Unlike regular signals that only determine direction, actions perform work (e.g., creating a rolling volume profile). Because `Action` inherits from `Signal`, it participates in the same tree evaluation order as other nodes.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `Action : Signal`
**Source:** `MZpack.NT8/Algo/Actions/Action.cs`

## Properties

`Action` inherits all properties from [Signal](signals/signal-base.md#signal) (`Strategy`, `MarketDataSource`, `Calculate`, `IsReset`, `Direction`, `EntryPrice`, `ChartRange`, etc.).

## Constructor

```csharp
public Action(Strategy strategy, MarketDataSource source,
    SignalCalculate calculate, bool isReset)
```

## Methods

| Method | Description |
|---|---|
| `OnMarketEvent(object e, MarketDataSource source, bool isFirstTickOfBar, SignalDirection allowed)` | Dispatches to `OnCalculate` based on source type, respecting the `Calculate` property |
| `GetRange(ChartRange range)` | Empty override — actions do not contribute to chart range |

---

## RollingProfileAction

Creates a rolling volume profile over a specified number of bars.

**Inheritance:** `RollingProfileAction : Action`
**Source:** `MZpack.NT8/Algo/Actions/RollingProfileAction.cs`

### Properties

| Property | Type | Description |
|---|---|---|
| `BarsRange` | `int` | Number of bars for the rolling profile |

### Constructor

```csharp
public RollingProfileAction(Strategy strategy,
    StrategyVolumeProfileIndicator indicator,
    StrategyVolumeProfileIndicator outerProfileIndicator)
```

Sets `MarketDataSource = Level1`, `Calculate = OnBarClose`, `IsReset = true`. Switches the indicator to `ProfileCreation.Custom`.

### Behavior

On each bar close, `OnCalculate` creates or rolls the volume profile. Once the profile spans `BarsRange` bars, the action returns `Direction = SignalDirection.Any` to indicate the profile is ready.

`Reset` clears the profile view visibility.

## See Also

- [Pipeline](pipeline.md) — execution order of components
- [Signal Base Classes](signals/signal-base.md) — `Signal` and `Node` base classes
- [Decision Tree](decision-tree.md) — tree structure and evaluation logic
