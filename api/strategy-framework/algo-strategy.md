---
sidebar_position: 3
title: "Algo.Strategy"
description: "Reference for Algo.Strategy — the pattern-oriented strategy class with decision trees, signals, and automatic position management."
---

# Algo.Strategy

`Algo.Strategy` is the pattern-oriented strategy engine. You define patterns containing signals and filters organized into decision trees. The framework evaluates them on each market event and manages entries, exits, and trailing stops automatically.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `Strategy : ViewModelBase`
**Source:** `MZpack.NT8/Algo/Strategy.cs`

## Architecture

```
Strategy
├── Patterns
│   ├── Entry Pattern
│   │   ├── SignalsTree (Decision Tree)
│   │   │   └── Root LogicalNode
│   │   │       ├── Signal A (AND)
│   │   │       ├── Signal B (AND)
│   │   │       └── OR Node
│   │   │           ├── Signal C
│   │   │           └── Signal D
│   │   └── FiltersTree (Decision Tree)
│   │       └── Root LogicalNode
│   │           └── Filter X
│   └── Exit Pattern
│       └── SignalsTree
│           └── Signal E
├── Positions
│   └── Position
│       ├── Entry[] (Market / Limit / StopLimit)
│       ├── Exit (Stop Loss, Profit Target)
│       └── Trail (Trailing Stop)
├── TradingTimes[]
└── RiskManagement
```

## Core Properties

| Property | Type | Description |
|---|---|---|
| `Name` | `string` | Strategy name |
| `MZpackStrategy` | `MZpackStrategyBase` | Parent NinjaTrader strategy |
| `Patterns` | `Patterns` | Collection of entry/exit patterns |
| `Pattern` | `Pattern` | Entry pattern (shortcut to `Patterns.Get(PatternType.Entry)`) |
| `ExitPattern` | `Pattern` | Exit pattern (shortcut) |
| `Positions` | `Positions` | Position management collection |
| `TradingTimes` | `List<TradingTime>` | Time windows when trading is allowed |
| `RiskManagement` | `RiskManagement` | Daily limits (loss, drawdown, profit, trade count) |
| `SessionBreak` | `bool` | Reset strategy on new session (default: `true`) |
| `IsOpeningPositionEnabled` | `bool` | Allow opening positions (default: `true`) |
| `OppositePatternAction` | `OppositePatternAction` | What to do when opposite signal fires |
| `Dashboard` | `DashboardView` | Dashboard visualization |

## Initialization

Use `Initialize()` to wire up patterns, entries, and positions:

```csharp
// Basic: entry pattern only
strategy.Initialize(entryPattern);

// Entry + exit patterns
strategy.Initialize(entryPattern, exitPattern);

// Entry + exit + custom entries
strategy.Initialize(entryPattern, exitPattern, new Entry[] { entry1, entry2 });

// Entry + exit + entries + attempt count
strategy.Initialize(entryPattern, exitPattern, entries, attempts: 1);
```

## Lifecycle

```
OnBarUpdate / OnMarketData / OnMarketDepth
    │
    ▼
Pattern.OnMarketEvent(e, source, isFirstTickOfBar)
    │
    ├── SignalsTree.OnMarketEvent()     ← evaluate signals decision tree
    │   └── each Signal.OnMarketEvent()
    │       └── SignalCalculate → direction (Long / Short / None)
    │
    ├── FiltersTree.OnMarketEvent()     ← evaluate filters (if signals passed)
    │   └── each Filter.OnMarketEvent()
    │
    ▼ pattern validated?
    │
    ├── YES → Strategy.OnEntryPatternValidated()
    │         └── Position.Enter(direction, time)
    │             └── Entry.Submit() → NinjaTrader order
    │
    └── NO  → Strategy.OnEntryPatternNotValidated()
```

## Virtual Methods (Override Points)

| Method | When to Override |
|---|---|
| `OnValidateEntryPatternFilter(object e, MarketDataSource source)` | Add custom entry validation logic beyond the decision tree |
| `OnValidateExitPatternFilter(object e, MarketDataSource source)` | Add custom exit validation logic |
| `OnPositionOpenFilter(DateTime time)` | Block position opening based on custom conditions |
| `OnEntryPatternValidated(Pattern sender, DateTime time)` | Custom action when entry pattern validates |
| `OnExitPatternValidated(Pattern sender, DateTime time)` | Custom action when exit pattern validates |
| `OnOrderFilled(Order order)` | Custom logic when an order fills |
| `OnOrderUpdate(Order order, OrderState orderState)` | Custom logic on order state changes |
| `OnPositionUpdate(Position, double, int, MarketPosition)` | Custom logic on position changes |
| `OnRender(ChartControl, ChartScale)` | Custom chart rendering |

## Logging

| Method | Description |
|---|---|
| `Log(LogLevel level, DateTime time, string text)` | Write to log if level is enabled |
| `LogHeader()` | Log strategy header info |
| `LogNinjaScriptProperties()` | Log all NinjaScript properties |

## Enums

### OppositePatternAction

| Value | Description |
|---|---|
| `None` | Keep current position, ignore opposite signal |
| `Close` | Close current position |
| `Reverse` | Close current position and open opposite |
| `Unmanaged` | Position direction managed by signals |

### LogLevel (Flags)

| Value | Description |
|---|---|
| `NONE` | No logging |
| `NV_PATTERN_OBC` | Not-validated pattern on bar close |
| `V_PATTERN` | Validated pattern |
| `ORDER` | Order events |
| `ENTRY` | Entry events |
| `POSITION` | Position state changes |
| `PROPERTIES` | NinjaScript properties |
| `ALL` | All of the above |

### LogTarget (Flags)

| Value | Description |
|---|---|
| `None` | No output |
| `File` | Write to log file |
| `NinjaScriptOutput` | Write to NinjaTrader Output window |
| `All` | Both file and output window |

## Example: Algo.Strategy with BigTradeSignal

```csharp
public class MyAlgoStrategy : MZpackStrategyBase
{
    StrategyBigTradeIndicator btIndicator;

    public MyAlgoStrategy()
    {
        OnCreateIndicators = () =>
        {
            btIndicator = new StrategyBigTradeIndicator(this, "BT");
            btIndicator.TradeFilterEnable = true;
            btIndicator.TradeFilterMin = 100;
            return new List<TickIndicator> { btIndicator };
        };

        OnCreateAlgoStrategy = () =>
        {
            var strategy = new Strategy("BigTradeAlgo", this);
            strategy.OppositePatternAction = OppositePatternAction.Close;
            strategy.SessionBreak = true;

            // Create entry signal
            var signal = new BigTradeSignal(strategy,
                MarketDataSource.Level1,
                SignalCalculate.OnEachTick);

            // Create entry pattern with AND logic
            var entryPattern = new Pattern(strategy,
                Logic.And, new Range(),
                isShortCircuitANDEvaluation: true);
            entryPattern.Signals.Root.Add(signal);

            // Create entries with stop loss and profit target
            var entry = new Entry(strategy);
            entry.Quantity = 1;
            entry.EntryMethod = EntryMethod.Market;
            entry.StopLossTicks = 20;
            entry.ProfitTargetTicks = 40;

            strategy.Initialize(entryPattern, null,
                new Entry[] { entry }, attempts: 1);
            return strategy;
        };
    }
}
```

## See Also

- [Strategy Framework Overview](overview.md) — choosing between Custom and Algo approaches
- [MZpackStrategyBase](mzpack-strategy-base.md) — base class reference
- [Position](position.md) — position management
- [TradingTime](trading-time.md) — time-based trading restrictions
- [Algo Strategy — ATM + TradesCluster](../samples/algo-strategy-atm.md) — sample
- [Algo Strategy — Patterns + ATM](../samples/algo-strategy-patterns.md) — sample
