---
sidebar_position: 4
title: "Pattern"
description: "Reference for Pattern and Patterns — top-level containers that hold decision trees, entries, and drive signal evaluation."
---

# Pattern

`Pattern` is the top-level container in the strategy framework. It holds two decision trees — `SignalsTree` for signal evaluation and `FiltersTree` for post-validation gating — and drives the evaluation loop on each market event. An `Algo.Strategy` can have multiple patterns of different types.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `Pattern : StrategyItem`
**Source:** `[INSTALL PATH]/API/Pattern.cs`

## Pattern Types

Each pattern serves a distinct role in position lifecycle:

| PatternType | Description |
|---|---|
| `Entry` | Opens a new position when flat |
| `Exit` | Closes the current position on signal |
| `Reversal` | Closes the current position and opens the opposite direction |
| `ScaleIn` | Adds contracts to an existing position |
| `ScaleOut` | Reduces contracts from an existing position |

A typical strategy has at least an Entry pattern. Exit, Reversal, ScaleIn, and ScaleOut patterns are optional and evaluated independently.

## Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Type` | `PatternType` | `Entry` | Pattern type |
| `AllowedDirection` | `SignalDirection` | `Any` | Constrain pattern to Long, Short, or Any |
| `IsShortCircuitANDEvaluation` | `bool` | — | If true, AND signals are validated in sequence (left to right) |
| `Signals` | `SignalsTree` | — | Signals decision tree |
| `Filters` | `FiltersTree` | — | Filters decision tree (evaluated after signals validate) |

### Read-Only State

| Property | Type | Description |
|---|---|---|
| `Direction` | `SignalDirection` | Resulting direction after evaluation (`None`, `Long`, `Short`) |
| `Strategy` | `Strategy` | Parent Algo.Strategy |
| `ViewItems` | `ObservableCollection\<Node>` | View items for visual constructor |

## Constructor

```csharp
public Pattern(Strategy strategy, Logic rootLogic, Range signalsRange,
    Logic filtersLogic, Range filtersRange, bool isShortCircuitANDEvaluation)
```

Creates both `SignalsTree` and `FiltersTree` with the specified root logic and range constraints.

Simplified overload (no filters):

```csharp
public Pattern(Strategy strategy, Logic rootLogic, Range signalsRange,
    bool isShortCircuitANDEvaluation)
```

## Evaluation

On every market event, the pattern evaluates in two phases:

```
Pattern.Evaluate()
 ├── [1] SignalsTree.OnMarketEvent()
 │        └── Root LogicalNode evaluates all child signals
 │             → Direction: Long | Short | None
 │
 └── [2] FiltersTree.OnMarketEvent()    ← only if signals validated
          └── Root LogicalNode evaluates all child filters
               → Pass (Any) or Block (None)
```

If `SignalsTree` returns `None`, the pattern short-circuits — `FiltersTree` is not evaluated. If `FiltersTree` blocks, the pattern direction resets to `None`.

### Short-Circuit AND Evaluation

When `IsShortCircuitANDEvaluation = true`, the AND root node validates signals in sequence. Each signal must validate before the next is evaluated. This is useful when signals have dependencies or when you want to avoid unnecessary computation.

## Patterns Collection

`Patterns` manages all pattern instances within an `Algo.Strategy`.

**Inheritance:** `Patterns : StrategyItem`

| Method | Description |
|---|---|
| `Get(PatternType type)` | Get pattern by type |
| `Set(Pattern pattern, PatternType type)` | Set pattern for a type |
| `Initialize(Strategy strategy, bool isInConstructor)` | Initialize all patterns |
| `Reset(List\<MarketDataSource> sources, bool resetView, bool isSessionBreak)` | Reset all patterns |
| `CheckSyntax()` | Validate all pattern trees |

## Example: Entry + Reversal Patterns

```csharp
OnCreateAlgoStrategy = () =>
{
    var strategy = new Strategy("MyStrategy", this);

    // Entry pattern: open position on signal A AND signal B
    var entryPattern = new Pattern(strategy,
        Logic.And, new Range { Bars = 5 },
        isShortCircuitANDEvaluation: true);
    entryPattern.Signals.Root.Add(signalA);
    entryPattern.Signals.Root.Add(signalB);

    // Reversal pattern: reverse position on signal C
    var reversalPattern = new Pattern(strategy,
        Logic.And, new Range(),
        isShortCircuitANDEvaluation: false);
    reversalPattern.Type = PatternType.Reversal;
    reversalPattern.Signals.Root.Add(signalC);

    var entry = new Entry(strategy)
    {
        StopLossTicks = 20,
        ProfitTargetTicks = 40
    };

    strategy.Initialize(entryPattern, null,
        new Entry[] { entry }, attempts: 1);
    strategy.Patterns.Set(reversalPattern, PatternType.Reversal);

    return strategy;
};
```

## See Also

- [Algo.Strategy](algo-strategy.md) — parent strategy class
- [Decision Tree](decision-tree.md) — SignalsTree, FiltersTree, LogicalNode, RangeNode
- [Pipeline](pipeline.md) — execution order of components
- [Signal Base Classes](signals/signal-base.md) — Node and Signal base classes
- [Entry](entry.md) — order submission
