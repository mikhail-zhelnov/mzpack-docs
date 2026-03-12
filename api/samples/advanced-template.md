---
sidebar_position: 1
title: "Advanced Template"
description: "Production-ready Algo.Strategy template with footprint indicator, dual entries, breakeven, trailing, risk management, trading times, control panel, and XML persistence."
---

# Advanced Template

A production-ready `Algo.Strategy` template that demonstrates most framework features in a single strategy. Use it as a starting point for your own strategies — replace the placeholder signal logic with real conditions.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/AdvancedTemplate.cs`
**Signal:** `MZpack.NT8/Algo/Signals/Built-in/AdvancedSignalTemplate.cs`

## What It Covers

- Custom `Algo.Strategy` subclass
- Footprint indicator with XML settings persistence
- Dual entries with independent stop/target
- Breakeven and tick-based trailing stop
- Trading time windows
- Risk management (daily loss, profit, drawdown, trades)
- Control panel buttons (Trading On/Off, Close, Break Even)
- Pattern load/save to XML

## Architecture

```
AdvancedTemplate : MZpackStrategyBase
 ├── AdvancedTemplateStrategy : Algo.Strategy
 │    ├── Entry Pattern (AND root)
 │    │    └── OR LogicalNode
 │    │         ├── AdvancedSignalTemplate "Advanced 1"
 │    │         └── AdvancedSignalTemplate "Advanced 2"
 │    ├── Entry "AT 1" (quantity, stop, target, BE, trail)
 │    ├── Entry "AT 2" (optional second entry)
 │    ├── TradingTimes[] (two configurable windows)
 │    └── RiskManagement (daily limits)
 └── StrategyFootprintIndicator (SaveSettings = true)
```

## Strategy Setup

### Constructor

The constructor wires delegates for strategy and indicator creation:

```csharp
public AdvancedTemplate() : base()
{
    OnCreateAlgoStrategy = new OnCreateAlgoStrategyDelegate(CreateAlgoStrategy);
    OnCreateIndicators = new OnCreateIndicatorsDelegate(CreateIndicators);
}
```

### CreateAlgoStrategy

Creates the `AdvancedTemplateStrategy`, configures trading times and risk management:

```csharp
protected Strategy CreateAlgoStrategy()
{
    AdvancedTemplateStrategy strategy = new AdvancedTemplateStrategy(
        @"Advanced Template v1.2", this)
    {
        OppositePatternAction = General_OppositePatternAction,
        LogLevel = LogLevel,
        LogTarget = LogTarget,
        LogTime = LogTime
    };

    // Trading times
    if (Time1_Enable)
        strategy.TradingTimes.Add(new TradingTime()
        {
            Begin = TryParseDateTime(Time1_Begin),
            End = TryParseDateTime(Time1_End)
        });

    // Risk management
    strategy.RiskManagement = new RiskManagement(strategy)
    {
        Currency = Currency.UsDollar,
        EntryName = ENTRY1,
        DailyLossLimitEnable = Risk_DailyLossLimit_Enable,
        DailyLossLimit = Risk_DailyLossLimit,
        DailyProfitLimitEnable = Risk_DailyProfitLimit_Enable,
        DailyProfitLimit = Risk_DailyProfitLimit,
        DailyTradesLimitEnable = Risk_DailyTradesLimit_Enable,
        DailyTradesLimit = Risk_DailyTradesLimit,
        DailyMaxDrawdownEnable = Risk_DailyMaxDrawdown_Enable,
        DailyMaxDrawdown = Risk_DailyMaxDrawdown
    };

    // No session break when time schedule is enabled
    strategy.SessionBreak = !(Time1_Enable || Time2_Enable);

    return strategy;
}
```

### CreateIndicators

Creates a `StrategyFootprintIndicator` with `SaveSettings = true` so indicator configuration persists to XML between sessions:

```csharp
protected List<TickIndicator> CreateIndicators()
{
    List<TickIndicator> indicators = new List<TickIndicator>();

    indicators.Add(new StrategyFootprintIndicator(this, FOOTPRINT)
    {
        SaveSettings = true,
        // Uncomment and configure footprint features:
        // LeftFootprintStyle = FootprintStyle.Bid,
        // RightFootprintStyle = FootprintStyle.Ask,
        // ShowImbalance = true,
        // ShowBarPOC = true,
        // StatisticGridShow = true,
        ShowVersionInfo = false
    });

    return indicators;
}
```

## Entry and Pattern Setup

The `prepareStrategy` method builds entries and the decision tree:

```csharp
void prepareStrategy(int entriesCount)
{
    // Create entries
    Entry[] entries = new Entry[entriesCount];
    entries[0] = new Entry(Strategy)
    {
        EntryMethod = General_EntryMethod,
        Quantity = Position_Quantity1,
        SignalName = ENTRY1,
        StopLossTicks = Position_StopLoss1,
        ProfitTargetTicks = Position_ProfitTarget1,
        IsBreakEven = Position_IsBE,
        BreakEvenAfterTicks = Position_BEAfterTicks,
        BreakEvenShiftTicks = Position_BEShiftTicks,
        Trail = Position_IsTrail
            ? new Trail(Position_TrailAfter, Position_TrailDistance, Position_TrailStep)
            : null
    };

    // Optional second entry with independent stop/target
    if (Position_Quantity2 > 0)
    {
        entries[1] = new Entry(Strategy)
        {
            EntryMethod = General_EntryMethod,
            Quantity = Position_Quantity2,
            SignalName = ENTRY2,
            StopLossTicks = Position_StopLoss2,
            ProfitTargetTicks = Position_ProfitTarget2,
            IsBreakEven = Position_IsBE,
            BreakEvenAfterTicks = Position_BEAfterTicks,
            BreakEvenShiftTicks = Position_BEShiftTicks,
            Trail = Position_IsTrail
                ? new Trail(Position_TrailAfter, Position_TrailDistance, Position_TrailStep)
                : null
        };
    }

    // Load pattern from XML or create new
    Pattern entryPattern = General_LoadSavePatterns
        ? Pattern.LoadFromXml(Strategy, PatternType.Entry) : null;

    if (entryPattern == null)
    {
        entryPattern = new Pattern(Strategy, Logic.And, null, true)
        {
            Type = PatternType.Entry
        };
        entryPattern.AllowedDirection = Position_Direction;

        // Decision tree: OR node with two signal instances
        if (Strategy_SignalEnable)
        {
            Node logic = new LogicalNode(Logic.Or);
            entryPattern.Signals.Root.AddChild(logic);
            logic.AddChild(new AdvancedSignalTemplate(Strategy) { Name = "Advanced 1" });
            logic.AddChild(new AdvancedSignalTemplate(Strategy) { Name = "Advanced 2" });
        }
    }

    Strategy.Initialize(entryPattern, null, entries);
}
```

Key points:
- Two entries allow split position management (e.g., 1 contract tight target + 1 contract runner)
- `Pattern.LoadFromXml` restores the decision tree from a previous session
- The decision tree root is AND, with an OR sub-node containing two signal instances

## Signal Template

`AdvancedSignalTemplate` is a placeholder signal that evaluates on bar close. Replace the `if (true)` conditions with your trading logic:

```csharp
public class AdvancedSignalTemplate : Signal
{
    public AdvancedSignalTemplate(Strategy strategy)
        : base(strategy, MarketDataSource.Level1, SignalCalculate.OnBarClose, true)
    {
    }

    public override void OnCalculate(MarketDataEventArgs e, int barIdx,
        SignalDirection allowed)
    {
        AdvancedTemplate strategy = Strategy.MZpackStrategy as AdvancedTemplate;
        SignalDirection direction = SignalDirection.None;

        if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx,
            out IFootprintBar bar))
            return;

        // Replace with your long conditions
        if (Signal.IsLongAllowed(allowed))
        {
            if (true)  // <-- your condition here
                direction = Signal.ResolveDirection(SignalDirection.Long, allowed);
        }

        // Replace with your short conditions
        if (direction == SignalDirection.None && Signal.IsShortAllowed(allowed))
        {
            if (true)  // <-- your condition here
                direction = Signal.ResolveDirection(SignalDirection.Short, allowed);
        }

        if (Signal.IsDetermined(direction))
        {
            Direction = direction;
            Time = e.Time;
            EntryPrice = GetBestEntryPrice(direction);
            ChartRange = new ChartRange()
            {
                MinBarIdx = barIdx,
                MaxBarIdx = barIdx,
                Low = EntryPrice,
                High = EntryPrice
            };
        }
    }
}
```

## Control Panel

Three buttons are added to the MZpack Control Panel:

```csharp
public override UIElement[] CreateControlPanelElements()
{
    UIElement[] ui = new UIElement[3];
    ui[0] = tradingOnOffButton = new Button() { Content = "Trading: ON" };
    ui[1] = cancelCloseButton = new Button() { Content = "Close" };
    ui[2] = breakEvenButton = new Button() { Content = "Break Even" };
    return ui;
}
```

| Button | Action |
|---|---|
| Trading On/Off | Toggles `Strategy.IsOpeningPositionEnabled` |
| Close | Calls `Strategy.Positions.CancelClose(...)` |
| Break Even | Calls `Strategy.Positions.BreakEven(...)` |

## Configurable Properties

### General

| Property | Default | Description |
|---|---|---|
| `General_OppositePatternAction` | `Close` | What to do on opposite signal |
| `General_EntryMethod` | `Market` | Order type |
| `General_LoadSavePatterns` | `false` | Persist decision tree to XML |

### Position

| Property | Default | Description |
|---|---|---|
| `Position_Direction` | `Any` | Allowed direction (Long, Short, Any) |
| `Position_Quantity1` | `1` | Entry 1 contracts |
| `Position_StopLoss1` | `10` | Entry 1 stop loss ticks |
| `Position_ProfitTarget1` | `20` | Entry 1 profit target ticks |
| `Position_Quantity2` | `0` | Entry 2 contracts (0 = disabled) |
| `Position_StopLoss2` | `10` | Entry 2 stop loss ticks |
| `Position_ProfitTarget2` | `28` | Entry 2 profit target ticks |
| `Position_IsBE` | `false` | Enable breakeven |
| `Position_BEAfterTicks` | `8` | Ticks of profit before breakeven |
| `Position_BEShiftTicks` | `-2` | Breakeven shift (negative = give back ticks) |
| `Position_IsTrail` | `false` | Enable trailing stop |
| `Position_TrailAfter` | `14` | Trail activation ticks |
| `Position_TrailDistance` | `20` | Trail distance ticks |
| `Position_TrailStep` | `2` | Trail step ticks |

### Trading Time

| Property | Default | Description |
|---|---|---|
| `Time1_Enable` | `false` | Enable first time window |
| `Time1_Begin` | `"09:00:00"` | Start time |
| `Time1_End` | `"15:00:00"` | End time |
| `Time2_Enable` | `false` | Enable second time window |
| `Time2_Begin` | `"21:00:00"` | Start time |
| `Time2_End` | `"23:00:00"` | End time |

### Risk Management

| Property | Default | Description |
|---|---|---|
| `Risk_DailyLossLimit_Enable` | `false` | Enable daily loss limit |
| `Risk_DailyLossLimit` | `500` | Daily loss limit (USD) |
| `Risk_DailyProfitLimit_Enable` | `false` | Enable daily profit limit |
| `Risk_DailyProfitLimit` | `2500` | Daily profit limit (USD) |
| `Risk_DailyMaxDrawdown_Enable` | `false` | Enable daily max drawdown |
| `Risk_DailyMaxDrawdown` | `1500` | Daily max drawdown (USD) |
| `Risk_DailyTradesLimit_Enable` | `false` | Enable daily trades limit |
| `Risk_DailyTradesLimit` | `5` | Max trades per day |

## Lifecycle

| State | What Happens |
|---|---|
| `SetDefaults` | Default property values are set |
| `Configure` | Footprint indicator loaded from XML, bar layout applied, `prepareStrategy()` builds entries and pattern |
| `DataLoaded` | `Strategy.IsOpeningPositionEnabled = true` |
| `Terminated` | Bar layout saved, patterns saved to XML (if enabled) |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Pattern](../strategies/pattern.md) — pattern types and evaluation
- [Entry](../strategies/entry.md) — order submission and protective orders
- [Trail](../strategies/trail.md) — trailing stop
- [Risk Management](../strategies/risk-management.md) — daily limits
- [TradingTime](../strategies/trading-time.md) — time windows
- [Custom Signal](../strategies/signals/custom-signal.md) — creating your own signal
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
