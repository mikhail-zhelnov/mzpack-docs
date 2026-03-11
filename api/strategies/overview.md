---
sidebar_position: 1
title: "Strategies Overview"
description: "Overview of the MZpack strategy system — two approaches, component architecture, and reading order."
---

# Strategies Overview

The MZpack strategy framework sits on top of NinjaTrader 8's strategy API and provides order flow-aware trading automation. Every MZpack strategy inherits from `MZpackStrategyBase`, which handles indicator lifecycle, market data routing, and chart rendering.

## Two Approaches

| Approach | Class | When to Choose |
|---|---|---|
| **Custom Strategy** | `MZpackStrategyBase` | Full C# control, simple rules, backtesting-only scenarios |
| **Algo.Strategy** | `Algo.Strategy` + `Pattern` | Declarative signal combination, real-time trading, ATM integration |

Most production strategies use `Algo.Strategy` because it handles signal evaluation, position management, and chart rendering automatically. Use `MZpackStrategyBase` directly when you need backtesting with simple rules or full manual control.

## Component Architecture

```
MZpackStrategyBase
 └── Algo.Strategy
      ├── Entry Pattern
      │    ├── Signals (Decision Tree)
      │    │    ├── Actions — side effects (e.g. rolling profile)
      │    │    ├── Filters — confirm or reject signals
      │    │    └── LogicalNode — AND / OR / CONJUNCTION
      │    └── Entry — order submission (Market, Limit, StopLimit)
      │         └── Exit / Trail — stop loss, profit target, trailing stop
      ├── Reversal Pattern
      ├── ScaleIn Pattern
      ├── ScaleOut Pattern
      └── Risk Management — daily limits
```

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
OnExecutionUpdate(...)         → Fill events
```

## Reading Order

1. [MZpackStrategyBase](mzpack-strategy-base.md) — base class and lifecycle
2. [Algo.Strategy](algo-strategy.md) — pattern-oriented framework
3. [Pattern](pattern.md) — pattern types and evaluation
4. [Position](position.md) — position management
5. [Signals Overview](signals/overview.md) — signal system and all built-in signals
6. [Pipeline](pipeline.md) — Action, Filter, Decision Tree components
7. [Entry](entry.md) / [Exit](exit.md) / [Trail](trail.md) — order management
8. [Risk Management](risk-management.md) — daily limits and caps
