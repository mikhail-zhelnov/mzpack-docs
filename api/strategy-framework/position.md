---
sidebar_position: 4
title: "Position"
description: "Reference for Position and Positions — position management within MZpack strategy patterns."
---

# Position

`Position` manages the lifecycle of a trading position within a pattern: entry submission, fill tracking, stop loss, profit target, trailing, and close. `Positions` is a collection of `Position` instances (typically one per pattern).

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `Position : StrategyItem` | `Positions : StrategyItem`
**Source:** `MZpack.NT8/Algo/Position.cs`, `MZpack.NT8/Algo/Positions.cs`

## Position Properties

| Property | Type | Description |
|---|---|---|
| `Strategy` | `Strategy` | Parent Algo.Strategy |
| `State` | `PositionState` | Current position state (flags) |
| `Direction` | `SignalDirection` | Position direction (Long, Short, None) |
| `IsActive` | `bool` | Activated from associated signal |
| `IsScaleIn` | `bool` | Whether this is a scale-in position |
| `Entries` | `ObservableCollection<EntryBase>` | Collection of entry orders |

## Position Methods

### Order Management

| Method | Description |
|---|---|
| `Enter(SignalDirection direction, DateTime time, bool isReversing)` | Submit entry orders in the given direction |
| `Close(bool isReverse, string reason, DateTime time)` | Close the position |
| `CancelClose(bool isReverse, string reason, DateTime time)` | Cancel pending orders or close position |
| `CancelPendingEntries(string reason, DateTime time)` | Cancel all pending entry orders |
| `HasPendingLimitOrders()` | Check for pending limit orders |

### Stop Management

| Method | Description |
|---|---|
| `BreakEven(string reason, DateTime time)` | Move stop loss to break-even price |
| `ActivateTrail(bool isActive)` | Activate or deactivate trailing stop |
| `HasTrailedEntries()` | Check if any entries have active trails |

### Event Handlers

| Method | Description |
|---|---|
| `OnExecution(MarketDataEventArgs e)` | Process market data for exit/trail logic |
| `OnMarketDepth(MarketDepthEventArgs e)` | Process Level 2 data |
| `OnOrderUpdate(Order, OrderState)` | Handle order state changes |
| `OnPositionUpdate(Position, double, int, MarketPosition)` | Handle NinjaTrader position changes |
| `OnExecutionUpdate(Execution, ...)` | Handle fill events |

### Helpers

| Method | Return Type | Description |
|---|---|---|
| `GetEntryBySignalName(string name)` | `Entry` | Find entry by signal name |
| `IsEntryOrder(Order order)` | `bool` | Check if order belongs to this position |
| `Reset()` | `void` | Reset all entries |

## PositionState Enum (Flags)

| Value | Description |
|---|---|
| `Flat` | No position |
| `EntrySubmitting` | Entry order being submitted |
| `LongLimitPending` | Long limit order pending |
| `ShortLimitPending` | Short limit order pending |
| `LongMarketPending` | Long market order pending |
| `ShortMarketPending` | Short market order pending |
| `Long` | Long position filled |
| `Short` | Short position filled |
| `LimitPending` | `LongLimitPending \| ShortLimitPending` |
| `Filled` | `Long \| Short` |
| `Longs` | `LongLimitPending \| LongMarketPending \| Long` |
| `Shorts` | `ShortLimitPending \| ShortMarketPending \| Short` |
| `NoDirection` | `Flat \| EntrySubmitting` |

## Positions Collection

`Positions` manages one or more `Position` instances within an `Algo.Strategy`.

| Method | Description |
|---|---|
| `FirstOrDefault()` | Get the first position |
| `Add(Position position)` | Add a position |
| `Enter(SignalDirection, DateTime, bool)` | Enter all activated positions |
| `CancelClose(bool, string, DateTime)` | Cancel/close all positions |
| `BreakEven(string, DateTime)` | Move all positions to break-even |
| `CancelPendingEntries(string, DateTime)` | Cancel all pending entries |
| `HasFlat()` | Check if any position is flat |
| `HasPendingLimitOrders()` | Check if any position has pending limits |

## See Also

- [Algo.Strategy](algo-strategy.md) — parent strategy class
- [Entry](../strategy-pipeline/entry.md) — order submission
- [Exit](../strategy-pipeline/exit.md) — stop loss and profit target
- [Trail](../strategy-pipeline/trail.md) — trailing stop
