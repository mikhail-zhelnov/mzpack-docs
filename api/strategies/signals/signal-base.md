---
sidebar_position: 2
title: "Signal Base Classes"
description: "Reference for Node, Signal, LogicalNode, and RangeNode — the base classes of the MZpack signal system."
---

# Signal Base Classes

All signals inherit from `Node`, which provides tree structure, direction handling, and event routing. `Signal` adds market data processing, chart range tracking, and indicator access. `LogicalNode` provides AND/OR/CONJUNCTION logic between signals.

**Namespace:** `MZpack.NT8.Algo`

## Node

`Node` is the abstract base class for all elements in the decision tree.

**Inheritance:** `Node : ViewModelBase, ICloneable`
**Source:** `MZpack.NT8/Algo/Signals/Node.cs`

### Key Properties

| Property | Type | Description |
|---|---|---|
| `Name` | `string` | Signal name |
| `IsEnabled` | `bool` | Enable/disable on-the-fly |
| `Direction` | `SignalDirection` | Validated direction (None, Long, Short, Any) |
| `EntryPrice` | `double` | Entry price from signal validation |
| `StopLossPrice` | `double` | Stop loss price (if signal provides one) |
| `ProfitTargetPrice` | `double` | Profit target price (if signal provides one) |
| `Tree` | `SignalsTree` | Parent decision tree |
| `Parent` | `Node` | Parent node in tree |
| `Nodes` | `ObservableCollection<Node>` | Child nodes |

### Key Methods

| Method | Description |
|---|---|
| `OnMarketEvent(object e, MarketDataSource source, bool isFirstTickOfBar, SignalDirection allowed)` | Process market event (abstract) |
| `OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)` | Calculate on Level 1 data (abstract) |
| `OnCalculate(MarketDepthEventArgs e, int barIdx, SignalDirection allowed)` | Calculate on Level 2 data (abstract) |
| `GetRange(ChartRange range)` | Get validated chart range (abstract) |
| `CheckSyntax()` | Validate node structure (abstract) |

### Static Direction Helpers

| Method | Description |
|---|---|
| `Invert(SignalDirection)` | Long ↔ Short |
| `IsDetermined(SignalDirection)` | Returns `true` for Long or Short |
| `ResolveDirection(SignalDirection resolve, SignalDirection allowed)` | Apply allowed constraint |
| `IsOppositeDirections(SignalDirection a, SignalDirection b)` | Check if Long vs Short |

---

## Signal

`Signal` extends `Node` with market data processing, indicator access, and chart range tracking.

**Inheritance:** `Signal : Node`
**Source:** `MZpack.NT8/Algo/Signal.cs`

### Key Properties

| Property | Type | Description |
|---|---|---|
| `Strategy` | `Strategy` | Parent Algo.Strategy |
| `MarketDataSource` | `MarketDataSource` | Data source: Level1, Level2, or Custom |
| `DataSeriesIndex` | `int` | Data series index (default: 0) |
| `Calculate` | `SignalCalculate` | When to calculate: OnEachTick, OnBarClose, NotApplicable |
| `IsReset` | `bool` | Re-evaluate on every event (vs. hold state after validation) |
| `HasPrice` | `bool` | Whether signal provides an entry price |
| `ChartRange` | `ChartRange` | Bar/price range where signal validated |
| `Time` | `DateTime` | When signal was validated |
| `Description` | `string` | Textual description of validated state |
| `PartiallyVisibleMode` | `SignalPartiallyVisibleMode` | Visibility in [Partially Visible](../../samples/algo-strategy-partially-visible.md) mode |

### Constructor

```csharp
public Signal(Strategy strategy, MarketDataSource source,
    SignalCalculate calculate, bool isReset)
```

### Key Methods

| Method | Description |
|---|---|
| `GetEffectiveCurrentBarIndex()` | Current bar index adjusted for Calculate mode |
| `GetCurrentBarAgo()` | Returns 1 for OnBarClose, 0 for OnEachTick |
| `GetBestEntryPrice(SignalDirection)` | Best bid for Long, best ask for Short |
| `IsMarketEventSupported(MarketDataSource)` | Check if event matches this signal |
| `ReferIndicators()` | Grab indicators from strategy based on templates |

---

## LogicalNode

`LogicalNode` provides AND/OR/CONJUNCTION logic between child nodes.

**Inheritance:** `LogicalNode : Node`
**Source:** `MZpack.NT8/Algo/Signals/LogicalNode.cs`

### Properties

| Property | Type | Description |
|---|---|---|
| `Logic` | `Logic` | `And`, `Or`, or `Conjunction` |

### Logic Behavior

| Logic | Behavior |
|---|---|
| **And** | All children must resolve to a determined direction |
| **Or** | First child with determined direction wins |
| **Conjunction** | Upgrades directions: Long + Short = Any |

### Example

```csharp
// Root AND node with two signals
var root = pattern.Signals.Root; // LogicalNode with Logic.And
root.Add(new FootprintImbalanceSignal(...));
root.Add(new BarDeltaSignal(...));

// Add an OR sub-group
var orNode = new LogicalNode(Logic.Or);
orNode.AddChild(new BigTradeSignal(...));
orNode.AddChild(new DOMImbalanceSignal(...));
root.Add(orNode);
```

---

## RangeNode / Range

`RangeNode` implements `IRange` to constrain how far apart signals can validate and still count as one pattern.

**Inheritance:** `RangeNode : Node, IRange` | `Range : RangeNode`
**Source:** `MZpack.NT8/Algo/Signals/RangeNode.cs`, `MZpack.NT8/Algo/Range.cs`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Bars` | `int` | 0 | Max bar distance (0 = no limit) |
| `Ticks` | `int` | 0 | Max tick distance (0 = no limit) |
| `Logic` | `Logic` | `And` | How Bars and Ticks combine |
| `IsInSession` | `bool` | `false` | Restrict to current session |

---

## Enums

### SignalDirection

| Value | Description |
|---|---|
| `None` | Signal not triggered |
| `Long` | Buy signal |
| `Short` | Sell signal |
| `Any` | Both directions (used by filters and Conjunction logic) |

### SignalCalculate

| Value | Description |
|---|---|
| `OnEachTick` | Evaluate on every tick |
| `OnBarClose` | Evaluate once per bar close |
| `NotApplicable` | For Level 2 and custom data sources |

### MarketDataSource

| Value | Description |
|---|---|
| `None` | No source |
| `Level1` | Order flow / tick data |
| `Level2` | DOM / market depth data |
| `Custom` | Custom events |

### Logic

| Value | Description |
|---|---|
| `And` | All conditions must be true |
| `Or` | Any condition is sufficient |
| `Conjunction` | Direction upgrade (Long + Short = Any) |

## See Also

- [Signals Overview](overview.md) — list of all built-in signals
- [Custom Signal](custom-signal.md) — creating your own signal
