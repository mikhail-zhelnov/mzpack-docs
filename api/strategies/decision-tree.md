---
sidebar_position: 14
title: "Decision Tree"
description: "Reference for Pattern, SignalsTree, FiltersTree, LogicalNode, and RangeNode — the decision tree that evaluates trade signals."
---

# Decision Tree

The decision tree evaluates signals, filters, and actions to determine a trade direction. A `Pattern` holds two trees — `SignalsTree` for signal evaluation and `FiltersTree` for post-validation gating.

**Namespace:** `MZpack.NT8.Algo`

## Evaluation Flow

```
Pattern.Evaluate()
 ├── SignalsTree
 │    └── Root (LogicalNode: AND/OR)
 │         ├── Signal A         → Long
 │         ├── LogicalNode (OR)
 │         │    ├── Signal B    → Short
 │         │    └── Signal C    → None (not triggered)
 │         ├── Action           → side effect
 │         └── RangeNode        → max 5 bars, 20 ticks
 │
 └── FiltersTree (evaluated only if SignalsTree validates)
      └── Root (LogicalNode: AND)
           └── ValueInRangeFilter → Any (pass) or None (block)
```

---

## Pattern

Top-level container that holds both trees and drives evaluation.

**Inheritance:** `Pattern : StrategyItem`
**Source:** `MZpack.NT8/Algo/Pattern.cs`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Type` | `PatternType` | `Entry` | Pattern type |
| `AllowedDirection` | `SignalDirection` | `Any` | Constrain pattern to Long, Short, or Any |
| `IsShortCircuitANDEvaluation` | `bool` | — | If true, AND signals are validated in sequence |
| `Signals` | `SignalsTree` | — | Signals decision tree |
| `Filters` | `FiltersTree` | — | Filters decision tree |

### Read-Only State

| Property | Type | Description |
|---|---|---|
| `Direction` | `SignalDirection` | Resulting direction after evaluation (`None`, `Long`, `Short`) |
| `Strategy` | `Strategy` | Parent Algo.Strategy |

### Constructor

```csharp
public Pattern(Strategy strategy, Logic rootLogic, Range signalsRange,
    Logic filtersLogic, Range filtersRange, bool isShortCircuitANDEvaluation)
```

Creates both `SignalsTree` and `FiltersTree` with the specified root logic and range constraints.

---

## SignalsTree

Wraps a root `LogicalNode` and evaluates all signals on each market event.

**Inheritance:** `SignalsTree : ViewModelBase`
**Source:** `MZpack.NT8/Algo/SignalsTree.cs`

### Properties

| Property | Type | Description |
|---|---|---|
| `Root` | `LogicalNode` | Root node of the tree |
| `Range` | `Range` | Bar/tick range constraint for signal proximity |
| `ChartRange` | `ChartRange` | Combined bar/price range of validated signals |
| `ValidatedCount` | `int` | Number of validated signals |
| `Height` | `int` | Tree depth |

### Constructor

```csharp
public SignalsTree(Pattern pattern, Logic rootLogic, Range range)
```

### Key Methods

| Method | Description |
|---|---|
| `OnMarketEvent(object e, MarketDataSource source, bool isFirstTickOfBar, SignalDirection allowed)` | Propagate market event through the tree |
| `Initialize(Pattern pattern, bool isInConstructor)` | Bind to pattern |
| `UpdateChartRange()` | Recalculate combined chart range from all signals |
| `HasSignal(MarketDataSource source)` | Check if the tree contains signals for a data source |

---

## FiltersTree

Evaluated only after `SignalsTree` validates. If the filter expires (out of range), the entire pattern resets.

**Inheritance:** `FiltersTree : SignalsTree`
**Source:** `MZpack.NT8/Algo/FiltersTree.cs`

### Behavior

- `UpdateChartRange` sets `MinBarIdx` to `Pattern.Signals.ChartRange.MaxBarIdx` — filters are anchored to the signal validation point
- `OnMarketEvent` checks the bar range; if signals are out of `Range.Bars`, the pattern resets
- Filters use `SignalDirection.Any` to pass and `SignalDirection.None` to block

---

## LogicalNode

AND/OR combiner node in the decision tree.

**Inheritance:** `LogicalNode : Node`
**Source:** `MZpack.NT8/Algo/Signals/LogicalNode.cs`

### Properties

| Property | Type | Description |
|---|---|---|
| `Logic` | `Logic` | Combination logic |

### Logic Behavior

| Logic | Behavior |
|---|---|
| **And** | All children must resolve to a determined direction |
| **Or** | First child with a determined direction wins |
| **Conjunction** | Upgrades directions: Long + Short = Any |

### Constructor

```csharp
public LogicalNode(Logic logic)
```

Allowed child types: `LogicalNode`, `Signal`, `RangeNode`.

### Key Methods

| Method | Description |
|---|---|
| `CheckSyntax()` | Validates that the node has at least one child |
| `GetSignals(MarketDataSource source)` | Recursively collects all signals for the given data source |
| `OnPatternValidated()` | Propagates validation event to all children |

---

## RangeNode

Constrains how far apart signals can validate (in bars and ticks) and still count as one pattern.

**Inheritance:** `RangeNode : Node, IRange`
**Source:** `MZpack.NT8/Algo/Signals/RangeNode.cs`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Bars` | `int` | `0` | Max bar distance (0 = no limit) |
| `Ticks` | `int` | `0` | Max tick distance (0 = no limit) |
| `Logic` | `Logic` | `And` | How Bars and Ticks combine |
| `IsInSession` | `bool` | `false` | Restrict to current session |

### Key Methods

| Method | Description |
|---|---|
| `IsInRange(int bars, int ticks)` | Returns `true` if within constraints (AND: both must pass; OR: either passes) |
| `CheckSyntax()` | Validates that range nodes have no children |

---

## Enums

### PatternType

| Value | Description |
|---|---|
| `Entry` | Standard entry pattern |
| `Exit` | Exit pattern |
| `Reversal` | Reverse position |
| `ScaleIn` | Add to position |
| `ScaleOut` | Reduce position |

### Logic

| Value | Description |
|---|---|
| `And` | All conditions must be true |
| `Or` | Any condition is sufficient |
| `Conjunction` | Direction upgrade (Long + Short = Any) |

## See Also

- [Pipeline](pipeline.md) — execution order of components
- [Signal Base Classes](signals/signal-base.md) — `Node`, `Signal`, `LogicalNode`, `RangeNode`
- [ChartRange](chart-range.md) — bar/price range tracking
- [Filter](filter.md) — `ValueInRangeFilter`
- [Action](action.md) — side effect nodes
