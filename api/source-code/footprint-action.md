---
sidebar_position: 1
title: "Footprint Action"
description: "Source code walkthrough of the FootprintAction built-in strategy — 10 delta and order flow signals, AND/OR decision tree with mandatory signal grouping, EMA indicator, control panel, and data export."
---

# Footprint Action

Production built-in strategy that combines 10 footprint-based trading signals using configurable AND/OR logic with mandatory signal grouping. This is the most feature-rich built-in strategy and demonstrates advanced decision tree construction, runtime signal enable/disable, and per-signal bar filter overrides.

**Source:** `[INSTALL PATH]/API/Strategies/FootprintAction/FootprintAction.cs`
**Signals:** `[INSTALL PATH]/API/Strategies/FootprintAction/*.cs` (10 signal files + ExportDataSchema.cs)

## What It Covers

- Custom `Algo.Strategy` subclass with `SuspendAfterTrade` and `OnPositionUpdate`
- Footprint indicator + EMA(5) indicator setup
- 10 independent signal implementations with per-signal bar filter overrides
- AND/OR decision tree with mandatory signal grouping
- Runtime signal enable/disable via `OnPropertyChanged` with pattern restructuring
- 5-button Control Panel (Trade, Auto suspend, Break Even, Trail, Close)
- Data export with `ExportDataSchema` mapping each signal to a feature column
- Up to 3 entries for position scaling

## Architecture

```
FootprintAction : MZpackStrategyBase
 ├── FootprintActionAlgoStrategy : Algo.Strategy
 │    ├── SuspendAfterTrade logic
 │    └── OnPositionUpdate → auto-suspend
 ├── Entry Pattern
 │    ├── When OR + mandatory signals:
 │    │    ├── AND LogicalNode (mandatory signals)
 │    │    └── OR LogicalNode (other signals)
 │    └── When AND or no mandatory:
 │         └── Root node with selected logic
 │              ├── DeltaDivergenceSignal
 │              ├── DeltaTailSignal
 │              ├── DeltaSurgeDropSignal
 │              ├── DeltaFlipSignal
 │              ├── DeltaTrapSignal
 │              ├── DeltaSlingshotSignal
 │              ├── AboveBelowPOCSignal
 │              ├── StackedImbalanceSignal
 │              ├── VolumeSequencingSignal
 │              └── HammerWithAbsorption
 ├── Entry "FA1" / "FA2" / "FA3" (up to 3 entries)
 ├── StrategyFootprintIndicator (SaveSettings = true)
 └── EMA(5) (visible, yellow stroke)
```

## Strategy Setup

### Constructor

The constructor wires delegates for strategy and indicator creation:

```csharp
public FootprintAction() : base()
{
    OnCreateAlgoStrategy = new OnCreateAlgoStrategyDelegate(CreateAlgoStrategy);
    OnCreateIndicators = new OnCreateIndicatorsDelegate(CreateIndicators);
}
```

### Custom Algo Strategy

`FootprintActionAlgoStrategy` extends `Algo.Strategy` to add auto-suspend behavior — when `SuspendAfterTrade` is enabled, trading pauses automatically after each position is opened:

```csharp
class FootprintActionAlgoStrategy : MZpack.NT8.Algo.Strategy
{
    public bool SuspendAfterTrade { get; set; } = false;

    public FootprintActionAlgoStrategy(string name, FootprintAction MZpackStrategy)
        : base(name, MZpackStrategy) { }

    public override void OnPositionUpdate(Position position, double averagePrice,
        int quantity, MarketPosition marketPosition)
    {
        base.OnPositionUpdate(position, averagePrice, quantity, marketPosition);

        if (marketPosition != MarketPosition.Flat)
        {
            if (SuspendAfterTrade == true)
            {
                IsOpeningPositionEnabled = false;
                (MZpackStrategy as FootprintAction).UpdateButtons();
            }
        }
    }
}
```

### CreateAlgoStrategy

Creates the strategy with trading times and risk management:

```csharp
protected MZpack.NT8.Algo.Strategy CreateAlgoStrategy()
{
    MZpack.NT8.Algo.Strategy strategy = new FootprintActionAlgoStrategy(
        @"Footprint Action v1.5", this)
    {
        IsUnmanaged = Position_Instrument_Enable ? true : false,
        OppositePatternAction = OppositePatternAction,
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
    if (Time2_Enable)
        strategy.TradingTimes.Add(new TradingTime()
        {
            Begin = TryParseDateTime(Time2_Begin),
            End = TryParseDateTime(Time2_End)
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

    strategy.SessionBreak = !(Time1_Enable || Time2_Enable);

    return strategy;
}
```

### CreateIndicators

Creates a `StrategyFootprintIndicator` and an `EMA(5)` used by the Delta Trap signal:

```csharp
protected List<TickIndicator> CreateIndicators()
{
    List<TickIndicator> indicators = new List<TickIndicator>();

    indicators.Add(new StrategyFootprintIndicator(this, FOOTPRINT)
    {
        SaveSettings = true,
        ShowVersionInfo = false
    });

    Ema = new EMA(this, Close, 5);
    Ema.Strokes[0] = new Stroke(Brushes.Yellow);
    Ema.Visible = true;
    indicators.Add(Ema);

    return indicators;
}
```

## Decision Tree Construction

The `prepareStrategy` method builds the decision tree with support for mandatory signal grouping. When using OR logic with mandatory signals, it creates an AND root containing a mandatory AND sub-node and an OR sub-node for optional signals:

```csharp
void prepareStrategy(int entriesCount)
{
    // Create entries (up to 3)
    Entry[] entries = new Entry[entriesCount];
    entries[0] = new Entry(Strategy)
    {
        EntryMethod = EntryMethod.Market,
        Quantity = Position_Quantity1,
        SignalName = ENTRY1,
        StopLossTicks = Position_StopLoss1,
        ProfitTargetTicks = Position_ProfitTarget1,
        IsBreakEven = Position_IsBE,
        BreakEvenAfterTicks = Position_BEAfterTicks,
        BreakEvenShiftTicks = Position_BEShiftTicks,
        Trail = new Trail(Position_TrailAfter, Position_TrailDistance, Position_TrailStep)
            { IsActive = Position_IsTrail }
    };
    // entries[1], entries[2] created similarly when Position_Quantity2/3 > 0

    // Create entry pattern with mandatory signal support
    Pattern entryPattern;
    LogicalNode mandatorySignals = null;
    LogicalNode otherSignals = null;
    if (Strategy_SignalsLogic == Logic.Or && hasMandatory())
    {
        // AND root: mandatory signals AND (any OR signal)
        entryPattern = new Pattern(Strategy, Logic.And, null, false);
        mandatorySignals = new LogicalNode(Logic.And);
        otherSignals = new LogicalNode(Logic.Or);
        entryPattern.Signals.Root.AddChild(mandatorySignals);
        entryPattern.Signals.Root.AddChild(otherSignals);
    }
    else
    {
        entryPattern = new Pattern(Strategy, Strategy_SignalsLogic, null, false);
        mandatorySignals = otherSignals = entryPattern.Signals.Root;
    }

    entryPattern.AllowedDirection = position_Direction;
    entryPattern.Signals.MinValidatedCount = Strategy_MinNumSignals;

    // Add enabled signals to appropriate node
    if (Strategy_DeltaDivergence_Enable)
    {
        DeltaDivergenceSignal = new DeltaDivergenceSignal(Strategy)
            { Name = "Delta Divergence" };
        var node = Strategy_DeltaDivergence_Mandatory
            ? mandatorySignals : otherSignals;
        node.AddChild(DeltaDivergenceSignal);
    }
    // ... same pattern for all 10 signals ...

    if (otherSignals.Nodes.Count == 0)
        otherSignals.Parent.RemoveNode(otherSignals);

    Strategy.Initialize(entryPattern, null, entries);
}
```

## Runtime Signal Enable/Disable

`OnPropertyChanged` handles runtime toggling of signals by closing positions and rebuilding the decision tree:

```csharp
protected override void OnPropertyChanged(object sender, PropertyChangedEventArgs args)
{
    if (args.PropertyName == "Strategy_SignalsLogic" ||
        args.PropertyName == "Strategy_DeltaDivergence_Enable" ||
        /* ... all 10 signal enable properties ... */)
    {
        if (Operating == StrategyOperating.Auto)
        {
            if (Strategy != null)
                Strategy.Positions.CancelClose(false, "Pattern restructure",
                    DateTime.MinValue);
        }

        if (Strategy != null)
        {
            try
            {
                lock (Sync)
                    prepareStrategy(EntriesPerDirection);
            }
            catch (Exception e)
            {
                if (e is DecisionTreeException)
                    invertSignalEnabledProp(args);  // Revert the toggle
                else
                    throw e;
            }
        }
    }

    base.OnPropertyChanged(sender, args);
}
```

## Bar Filters

Global and per-signal bar filters validate footprint bar metrics before signal evaluation:

```csharp
public bool CheckBarGlobalFilters(IFootprintBar bar)
{
    return bar.Volume >= Strategy_MinBarVolume
        && Math.Abs(bar.Delta) >= Strategy_MinBarDelta
        && Math.Abs(bar.DeltaPercentage) >= Strategy_MinBarDeltaPercent;
}

public bool CheckBarFilters(IFootprintBar bar, bool isOverride,
    long minBarVol, long minBarDelta, double minBarDeltaPerc)
{
    if (isOverride)
        return bar.Volume >= minBarVol
            && Math.Abs(bar.Delta) >= minBarDelta
            && Math.Abs(bar.DeltaPercentage) >= minBarDeltaPerc;
    else
        return CheckBarGlobalFilters(bar);
}
```

## Signal Implementations

All signals extend `Signal` with `MarketDataSource.Level1`, `SignalCalculate.OnBarClose`, and follow the same pattern: get footprint bar, apply bar filters, evaluate conditions, set `Direction`, `Time`, `EntryPrice`, and `ChartRange`.

### Delta Divergence

Trend reversal — price makes a new extreme while delta moves in the opposite direction:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;
    SignalDirection direction = SignalDirection.None;
    IFootprintBar bar;

    if (barIdx < 1) return;

    ICandle candle = Strategy.MZpackStrategy.GetCandle(1);    // Closed candle
    ICandle candle_1 = Strategy.MZpackStrategy.GetCandle(2);  // Before closed

    if (candle_1 == null || candle == null) return;
    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out bar)) return;
    if (!strategy.CheckBarFilters(bar, strategy.Strategy_DeltaDivergence_OverrideFilters,
        strategy.Strategy_DeltaDivergence_MinBarVolume,
        strategy.Strategy_DeltaDivergence_MinBarDelta,
        strategy.Strategy_DeltaDivergence_MinBarDeltaPercent)) return;

    // LONG: bullish candle + positive delta + new low
    if (candle.IsBullish() && bar.Delta > 0 && candle.Low < candle_1.Low)
        direction = Signal.ResolveDirection(SignalDirection.Long, allowed);
    // SHORT: bearish candle + negative delta + new high
    else if (candle.IsBearish() && bar.Delta < 0 && candle.High > candle_1.High)
        direction = Signal.ResolveDirection(SignalDirection.Short, allowed);

    if (Signal.IsDetermined(direction))
    {
        Direction = direction;
        Time = e.Time;
        EntryPrice = GetBestEntryPrice(direction);
        ChartRange = new ChartRange()
        {
            MinBarIdx = barIdx, MaxBarIdx = barIdx,
            Low = EntryPrice, High = EntryPrice
        };
        Description = $" => Delta = {bar.Delta}";
    }
}
```

### Delta Tail

Bar has delta concentrated at the extreme — negative delta at all levels except the bottom (long) or vice versa:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;
    SignalDirection direction = SignalDirection.None;
    IFootprintBar bar;
    ICandle candle = Strategy.MZpackStrategy.GetCandle(1);

    if (candle == null) return;
    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out bar)) return;
    if (!strategy.CheckBarFilters(bar, ...)) return;

    // LONG: bullish bar, positive delta at all levels except bottom
    if (candle.IsBullish())
    {
        foreach (var x in bar.Deltas)
        {
            if (x.Key > bar.Lo)
            {
                if (x.Value <= 0) return;  // Must be positive
            }
            else if (x.Key == bar.Lo)
            {
                if (x.Value >= 0) return;  // Must be negative (the "tail")
            }
        }
        direction = Signal.ResolveDirection(SignalDirection.Long, allowed);
    }
    // SHORT: mirror logic for bearish bars
    // ...
}
```

### Delta Surge/Drop

4-bar signal tracking consecutive increasing or decreasing delta:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;
    SignalDirection direction = SignalDirection.None;
    SignalDirection barsDirection = SignalDirection.None;
    IFootprintBar bar = null, bar_1 = null;

    for (int i = 3; i >= 0; i--)
    {
        if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx - i, out bar))
            return;
        if (!strategy.CheckBarFilters(bar, ...)) return;

        if (i < 3)
        {
            if (bar.Delta > bar_1.Delta)
            {
                if (barsDirection == SignalDirection.Short) return;
                barsDirection = SignalDirection.Long;
            }
            else if (bar.Delta < bar_1.Delta)
            {
                if (barsDirection == SignalDirection.Long) return;
                barsDirection = SignalDirection.Short;
            }
        }
        bar_1 = bar;
    }

    if (bar != null && !strategy.CheckBarGlobalFilters(bar)) return;
    direction = Signal.ResolveDirection(barsDirection, allowed);
    // ... set Direction, Time, EntryPrice, ChartRange
}
```

### Delta Flip

2-bar reversal signal detecting a sudden delta shift. Uses a precision parameter for approximate comparison:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;
    IFootprintBar bar, bar_1;

    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx - 1, out bar_1)) return;
    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out bar)) return;
    // Both bars must pass filters

    // LONG: bar_1 closes at MinDelta≈Delta, MaxDelta≈0;
    //       bar closes at MaxDelta≈Delta, MinDelta≈0
    if (equal(bar_1.MinDelta, bar_1.Delta, strategy.Strategy_DeltaFlip_Precision)
        && equal(bar_1.MaxDelta, 0, strategy.Strategy_DeltaFlip_Precision)
        && equal(bar.MaxDelta, bar.Delta, strategy.Strategy_DeltaFlip_Precision)
        && equal(bar.MinDelta, 0, strategy.Strategy_DeltaFlip_Precision))
    {
        direction = Signal.ResolveDirection(SignalDirection.Long, allowed);
    }
    // SHORT: mirror conditions
}

bool equal(long val1, long val2, long precision)
{
    return Math.Abs(val1 - val2) <= precision;
}
```

### Delta Trap

3-bar signal — delta reversal followed by renewed strength, using EMA(5) for trend confirmation:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;
    IFootprintBar bar1, bar2, bar3;

    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx - 2, out bar1)) return;
    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx - 1, out bar2)) return;
    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out bar3)) return;
    if (!strategy.CheckBarFilters(bar3, ...)) return;

    // LONG: bar1 big negative delta, bar2 big positive delta,
    //       EMA rising over 3 bars, bar3 big positive delta or VA gap up
    if (bar1.Delta <= -strategy.Strategy_MinBarDelta
        && bar2.Delta >= strategy.Strategy_MinBarDelta)
    {
        if (strategy.Ema.Values[0][barIdx] > strategy.Ema.Values[0][barIdx - 2])
        {
            if (bar3.Delta >= strategy.Strategy_MinBarDelta
                || (bar3.VAL > bar2.VAH
                    && strategy.PriceDiffTicks(bar3.VAL, bar2.VAH) > 1))
            {
                direction = Signal.ResolveDirection(SignalDirection.Long, allowed);
            }
        }
    }
    // SHORT: mirror conditions
}
```

### Delta Slingshot

Multi-bar signal with configurable lookback — detects when extreme delta gets overrun by the opposite extreme:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;
    IFootprintBar closedBar;
    IFootprintBar lookbackBar = null;

    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out closedBar)) return;
    if (!strategy.CheckBarFilters(closedBar, ...)) return;

    for (int i = 1; i <= strategy.Strategy_DeltaSlingshot_Lookback; i++)
    {
        if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx - i, out lookbackBar))
            return;

        direction = checkBars(closedBar, lookbackBar, allowed);
        if (Signal.IsDetermined(direction))
        {
            if (strategy.CheckBarGlobalFilters(lookbackBar))
                break;
            direction = SignalDirection.None;
        }
    }
    // ... set Direction, Time, EntryPrice, ChartRange
}

SignalDirection checkBars(IFootprintBar closedBar, IFootprintBar lookbackBar,
    SignalDirection allowed)
{
    ICandle closedCandle = Strategy.MZpackStrategy.GetCandle(GetCurrentBarAgo(0));
    ICandle lookbackCandle = Strategy.MZpackStrategy.GetCandle(
        GetCurrentBarAgo(closedBar.BarIdx - lookbackBar.BarIdx));

    // LONG: lookback bearish with negative delta,
    //       closed bullish with positive delta, close > lookback high
    if (closedCandle.IsBullish())
    {
        if (lookbackBar.Delta < 0 && closedBar.Delta > 0
            && lookbackCandle.IsBearish()
            && closedCandle.Close > lookbackCandle.High)
        {
            return Signal.ResolveDirection(SignalDirection.Long, allowed);
        }
    }
    // SHORT: mirror conditions
    return SignalDirection.None;
}
```

### Above/Below POC

Bar opens and closes on the same side of its Point of Control:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;

    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out IFootprintBar bar))
        return;
    if (!strategy.CheckBarFilters(bar, ...)) return;

    ICandle candle = strategy.GetCandle(GetCurrentBarAgo(0));
    if (candle == null) return;

    // LONG: open and close both above POC
    if (candle.Open > bar.POC && candle.Close > bar.POC)
        direction = Signal.ResolveDirection(SignalDirection.Long, allowed);

    // SHORT: open and close both below POC
    if (direction == SignalDirection.None)
    {
        if (candle.Open < bar.POC && candle.Close < bar.POC)
            direction = Signal.ResolveDirection(SignalDirection.Short, allowed);
    }
    // ...
}
```

### Stacked Imbalances

Multiple imbalances stacked at consecutive price levels, with optional POC filter and reverse option:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;
    IFootprintBar bar;

    if (strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out bar))
    {
        if (!strategy.CheckBarFilters(bar, ...)) return;

        // Undefined direction — both bid and ask imbalances present
        if (bar.ImbalanceSRZones.Zones[(int)TradeSide.Bid].Count > 0
            && bar.ImbalanceSRZones.Zones[(int)TradeSide.Ask].Count > 0)
            return;

        // SHORT: sell imbalance zones (optionally reversed)
        if (bar.ImbalanceSRZones.Zones[(int)TradeSide.Bid].Count > 0)
        {
            // Optional POC filter: POC must be above highest zone
            if (strategy.Strategy_StackedImbalances_AboveBelowPOC)
            {
                var highestZone = bar.ImbalanceSRZones.Zones[(int)TradeSide.Bid]
                    .OrderBy(x => x.Hi).Last();
                if (bar.POC <= highestZone.Hi) return;
            }
            direction = ResolveDirection(
                strategy.Strategy_StackedImbalances_Reverse
                    ? SignalDirection.Long : SignalDirection.Short, allowed);
        }
        // LONG: buy imbalance zones
        // ...
    }
}
```

### Volume Sequencing

Multiple price levels with increasing volume on the aggressive side:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;
    IFootprintBar bar;
    ICandle candle = Strategy.MZpackStrategy.GetCandle(1);

    if (candle == null) return;
    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out bar)) return;
    if (!strategy.CheckBarFilters(bar, ...)) return;

    List<long> levels = new List<long>();
    // LONG: bullish bar with increasing buy volume across price levels
    if (candle.IsBullish())
    {
        foreach (var x in bar.Volumes)
        {
            long volume = bar.BuyVolumes.ContainsKey(x.Key) ? bar.BuyVolumes[x.Key] : 0;
            if (levels.Count == 0 || volume > levels.Last())
                levels.Add(volume);
            else
                levels.Clear();

            if (levels.Count >= strategy.Strategy_VolumeSequencing_Levels)
            {
                direction = Signal.ResolveDirection(SignalDirection.Long, allowed);
                break;
            }
        }
    }
    // SHORT: bearish bar with increasing sell volume (descending price order)
    // ...
}
```

### Hammer with Absorption

Absorption (trapped sellers/buyers) detected in the wick of a hammer candle pattern:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    FootprintAction strategy = (FootprintAction)Strategy.MZpackStrategy;

    if (!strategy.FootprintIndicator.FootprintBars.TryGetValue(barIdx, out IFootprintBar bar))
        return;
    if (!strategy.CheckBarFilters(bar, ...)) return;

    ICandle candle = strategy.GetCandle(GetCurrentBarAgo(0));
    if (candle == null) return;

    // LONG: bullish hammer (no upper wick, lower wick >= threshold)
    //       with sell absorption in the wick
    if (candle.IsBullish() && candle.UpperWick == 0
        && candle.GetLowerWickPercent() >= strategy.Strategy_HammerAbsorption_WickPercent)
    {
        if (bar.Absorptions[(int)TradeSide.Bid].Count > 0)
        {
            // Optional POC filter
            if (strategy.Strategy_HammerAbsorption_POC
                && bar.Absorptions[(int)TradeSide.Bid].First().Key > bar.POC)
                return;

            direction = Signal.ResolveDirection(SignalDirection.Long, allowed);
        }
    }
    // SHORT: bearish hammer with buy absorption in the upper wick
    // ...
}
```

## Data Export Schema

`ExportDataSchema` maps each signal's direction to a numeric feature column (1.0 = Long, -1.0 = Short, 0 = None), plus the combined pattern direction:

```csharp
public class ExportDataSchema : DataSchema
{
    FootprintAction strategy;

    public ExportDataSchema(DataSet dataSet, FootprintAction strategy) : base(dataSet)
    {
        this.strategy = strategy;

        if (strategy.Strategy_DeltaDivergence_Enable)
            Append("DeltaDivergence", ValueKind.Feature,
                new CalculateExportValueDelegate(GetDeltaDivergence));
        if (strategy.Strategy_DeltaTail_Enable)
            Append("DeltaTail", ValueKind.Feature,
                new CalculateExportValueDelegate(GetDeltaTail));
        // ... all 10 signals ...

        Append("Pattern", ValueKind.Feature,
            new CalculateExportValueDelegate(GetPattern));
    }

    public double GetDeltaDivergence(GeneralExport export, ValueDescriptor desc, object data)
        => directionToDouble(strategy.DeltaDivergenceSignal.Direction);
    // ... one getter per signal ...

    public double GetPattern(GeneralExport export, ValueDescriptor desc, object data)
        => directionToDouble(strategy.Strategy.Pattern.Direction);

    double directionToDouble(SignalDirection d)
    {
        if (d == SignalDirection.Long) return 1.0;
        else if (d == SignalDirection.Short) return -1.0;
        else return 0;
    }
}
```

## Control Panel

Five buttons for runtime control:

```csharp
public override UIElement[] CreateControlPanelElements()
{
    UIElement[] ui = new UIElement[5];
    ui[0] = tradingOnOffButton = new Button() { Content = "Trade" };
    ui[1] = suspendAfterTradeButton = new Button() { Content = "Auto suspend" };
    ui[2] = breakEvenButton = new Button() { Content = "Break Even" };
    ui[3] = trailButton = new Button() { Content = "Trail" };
    ui[4] = cancelCloseButton = new Button() { Content = "Close" };
    return ui;
}
```

| Button | Action |
|---|---|
| Trade | Toggles `Strategy.IsOpeningPositionEnabled` (green = active) |
| Auto suspend | Toggles `SuspendAfterTrade` (crimson = active) |
| Break Even | Calls `Strategy.Positions.BreakEven(...)` |
| Trail | Toggles trailing stop for the current position |
| Close | Calls `Strategy.Positions.CancelClose(...)` |

## Configurable Properties

### Strategy

| Property | Default | Description |
|---|---|---|
| `Strategy_Action` | `Trade` | Trade or Export mode |
| `Strategy_SignalsLogic` | `Or` | AND or OR combination of signals |
| `Strategy_MinBarVolume` | `100` | Global minimum bar volume |
| `Strategy_MinBarDelta` | `100` | Global minimum absolute bar delta |
| `Strategy_MinBarDeltaPercent` | `0` | Global minimum bar delta percentage |
| `Strategy_MinNumSignals` | `0` | Minimum validated signals (OR only) |
| `OppositePatternAction` | `None` | None, Close, or Reverse on opposite signal |
| `Strategy_SuspendAfterTrade` | `false` | Pause after position opens |

### Signal Groups

Each of the 10 signals has:

| Property | Description |
|---|---|
| `Enable` | Enable/disable the signal |
| `Mandatory` | Always required regardless of tree logic |
| `Override filters` | Use per-signal bar filters instead of global |
| `Min bar Volume` | Per-signal minimum bar volume |
| `Min bar Delta` | Per-signal minimum absolute delta |
| `Min bar Delta %` | Per-signal minimum delta percentage |

Additional signal-specific properties:
- **Delta Flip:** `Precision` (default 40) — tolerance for approximate comparison
- **Delta Slingshot:** `Lookback` (default 3) — number of bars to scan backward
- **Stacked Imbalances:** `Percentage` (68), `Number` (3), `Volume Filter`, `Reverse`, `Above/Below POC`
- **Volume Sequencing:** `Levels` — minimum consecutive price levels required
- **Hammer with Absorption:** `Wick %`, `POC filter`

### Position

| Property | Default | Description |
|---|---|---|
| `Position_Direction` | `Any` | Allowed direction |
| `Position_Quantity1` | `1` | Entry 1 contracts |
| `Position_StopLoss1` | `10` | Entry 1 stop loss ticks |
| `Position_ProfitTarget1` | `20` | Entry 1 profit target ticks |
| `Position_Quantity2` | `2` | Entry 2 contracts |
| `Position_StopLoss2` | `10` | Entry 2 stop loss ticks |
| `Position_ProfitTarget2` | `30` | Entry 2 profit target ticks |
| `Position_Quantity3` | `0` | Entry 3 contracts (0 = disabled) |
| `Position_IsBE` | `false` | Enable breakeven |
| `Position_BEAfterTicks` | `10` | Ticks before breakeven |
| `Position_BEShiftTicks` | `1` | Breakeven shift |
| `Position_IsTrail` | `false` | Enable trailing stop |
| `Position_TrailAfter` | `15` | Trail activation ticks |
| `Position_TrailDistance` | `10` | Trail distance ticks |
| `Position_TrailStep` | `1` | Trail step ticks |

## See Also

- [Built-in Strategies](/docs/strategies/built-in-strategies#footprint-action-strategy) — user-facing settings reference
- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Decision Tree](../strategies/decision-tree.md) — AND/OR/CONJUNCTION logic
- [Pattern](../strategies/pattern.md) — pattern types and evaluation
- [Signal](../strategies/signals/custom-signal.md) — creating custom signals
- [Entry](../strategies/entry.md) — order submission and protective orders
- [Trail](../strategies/trail.md) — trailing stop
- [Risk Management](../strategies/risk-management.md) — daily limits
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile
