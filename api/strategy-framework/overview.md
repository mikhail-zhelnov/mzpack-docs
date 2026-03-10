---
sidebar_position: 1
title: "Strategy Framework Overview"
description: "Overview of the MZpack strategy framework — two approaches to building automated trading strategies on NinjaTrader 8."
---

# Strategy Framework Overview

The MZpack strategy framework sits on top of NinjaTrader 8's strategy API and provides order flow-aware trading automation. Every MZpack strategy inherits from `MZpackStrategyBase`, which handles indicator lifecycle, market data routing, and chart rendering.

## Inheritance Hierarchy

```
NinjaTrader.NinjaScript.Strategies.Strategy
    └── StrategyRenderBase              (SharpDX/Direct2D chart rendering)
        └── MZpackStrategyBase          (MZpack indicator management, data routing)
            └── Your strategy class
```

## Two Approaches

MZpack offers two ways to build strategies, depending on how much control you need:

### 1. Custom Strategy (MZpackStrategyBase directly)

You override `OnBarUpdate()` and write all trading logic in C#. Full control over indicator access, order submission, and position management.

```csharp
public class MyCustomStrategy : MZpackStrategyBase
{
    StrategyFootprintIndicator footprint;

    // Create indicators
    OnCreateIndicators = () => {
        footprint = new StrategyFootprintIndicator(this, "FP");
        return new List<TickIndicator> { footprint };
    };

    // Trading logic in OnBarUpdate
    protected override void OnBarUpdate()
    {
        IFootprintBar bar = footprint.FootprintBars[CurrentBar];
        if (bar.Delta > 1000)
            EnterLong();
    }
}
```

**Best for:** backtesting-only strategies, simple rules, direct NinjaTrader API usage, full C# control.

### 2. Algo.Strategy (Pattern-Oriented)

You declare patterns with signals, filters, and decision trees. The framework evaluates them automatically on each market event and manages entries/exits.

```csharp
OnCreateAlgoStrategy = () =>
{
    var strategy = new Strategy("MyAlgo", this);
    var signal = new BigTradeSignal(strategy, MarketDataSource.Level1,
        SignalCalculate.OnEachTick);
    var pattern = new Pattern(strategy, Logic.And, new Range(),
        isShortCircuitANDEvaluation: true);
    pattern.Signals.Root.Add(signal);
    strategy.Initialize(pattern);
    return strategy;
};
```

**Best for:** signal combination, real-time trading, ATM integration, visual pattern display on charts.

## Which Approach to Choose

| Criteria | Custom Strategy | Algo.Strategy |
|---|---|---|
| **Logic style** | Imperative C# code | Declarative signals + decision tree |
| **Signal combination** | Manual if/else | AND/OR/CONJUNCTION tree |
| **Entry types** | Manual order calls | Market, Limit, StopLimit via Entry class |
| **Exit management** | Manual | Built-in Exit + Trail |
| **Risk management** | Manual | Built-in RiskManagement class |
| **Backtesting** | OnBarClose supported | OnBarClose + OnEachTick |
| **Real-time trading** | Full control | Pattern validation + ATM |
| **Chart visualization** | Manual SharpDX | Automatic pattern markers |
| **Complexity** | Lower for simple rules | Lower for multi-signal strategies |

Most production strategies use `Algo.Strategy` because it handles signal evaluation, position management, and chart rendering automatically. Use `MZpackStrategyBase` directly when you need backtesting with simple rules or full manual control.

## Strategy Lifecycle

```
OnStateChange(SetDefaults)     → Set default property values
OnStateChange(Configure)       → OnCreateIndicators(), OnCreateAlgoStrategy()
OnStateChange(DataLoaded)      → Indicators initialized, data series ready
OnStateChange(Historical)      → Backtesting begins
OnStateChange(Transition)      → Historical → Realtime switch
OnStateChange(Realtime)        → Live trading
OnStateChange(Terminated)      → Cleanup
```

During execution, market data flows through:

```
OnBarUpdate()                  → Bar close events (all data series)
OnMarketData(e)                → Level 1 tick events
OnMarketDepth(e)               → Level 2 DOM events
OnOrderUpdate(...)             → Order state changes
OnPositionUpdate(...)          → Position changes
OnExecutionUpdate(...)         → Fill events
```

## See Also

- [MZpackStrategyBase](mzpack-strategy-base.md) — base class reference
- [Algo.Strategy](algo-strategy.md) — pattern-oriented framework
- [Strategy Pipeline](../strategy-pipeline/overview.md) — pipeline components (Action, Entry, Exit, Trail)
