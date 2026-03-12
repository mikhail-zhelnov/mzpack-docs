---
sidebar_position: 2
title: "Ghost Resistance"
description: "Source code walkthrough of the GhostResistance built-in strategy — 5 signal types, 3 conditional indicators, AND decision tree with OR sub-node for volume profile levels, limit order support, and one-entry-per-bar filtering."
---

# Ghost Resistance

Production built-in strategy targeting liquidity traps — reversals at support/resistance levels where stop orders and breakout entries from trapped traders get absorbed. Combines bar metrics, absorption zones, big trade detection, and volume profile level proximity using AND logic. Demonstrates conditional indicator creation, signal dependency (level signals read absorption direction), limit order entry, and one-entry-per-bar filtering.

**Source:** `[INSTALL PATH]/API/Strategies/GhostResistance/GhostResistance.cs`
**Signals:** `[INSTALL PATH]/API/Strategies/GhostResistance/*.cs` (3 signal files + ExportDataSchema.cs)

## What It Covers

- Custom `Algo.Strategy` subclass with `OnPositionOpenFilter` (one entry per bar)
- Conditional indicator creation — footprint, volume profile, and big trade only when enabled
- AND decision tree with OR sub-node for session vs weekly profile levels
- Built-in signals (`OrdferflowBarMetricsSignal`, `BarMetricsSignal`, `FootprintSRZonesSignal`)
- 3 custom signals: `BigTradeSignal`, `ApproachingToSessionLevelSignal`, `ApproachingToWeeklyLevelSignal`
- Signal dependency — level signals read `AbsorptionSignal.Direction` to determine price side
- Limit order entry with configurable cancel type
- Volume profile RTH/ETH session configuration and weekly stacked profiles

## Architecture

```
GhostResistance : MZpackStrategyBase
 ├── FootprintActionAlgoStrategy : Algo.Strategy
 │    ├── OnPositionOpenFilter → one entry per bar
 │    ├── SuspendAfterTrade logic
 │    └── OnPositionUpdate → auto-suspend
 ├── Entry Pattern (AND root, short-circuit)
 │    ├── OrdferflowBarMetricsSignal (volume, delta, delta%)
 │    ├── BarMetricsSignal (wick%, hammer)
 │    ├── FootprintSRZonesSignal "Absorption" (absorption S/R zones)
 │    ├── BigTradeSignal (big trades at bar extremes)
 │    └── OR LogicalNode (when both session + weekly enabled)
 │         ├── ApproachingToSessionLevelSignal
 │         └── ApproachingToWeeklyLevelSignal
 ├── Entry "GR1" / "GR2" / "GR3" (limit or market)
 ├── StrategyFootprintIndicator (conditional, when Absorption enabled)
 ├── StrategyBigTradeIndicator (conditional, when Big Trade enabled)
 └── StrategyVolumeProfileIndicator (conditional, when Profile Levels enabled)
```

## Strategy Setup

### Constructor

```csharp
public GhostResistance() : base()
{
    OnCreateAlgoStrategy = new OnCreateAlgoStrategyDelegate(CreateAlgoStrategy);
    OnCreateIndicators = new OnCreateIndicatorsDelegate(CreateIndicators);
}
```

### Custom Algo Strategy

The inner `FootprintActionAlgoStrategy` class adds one-entry-per-bar filtering via `OnPositionOpenFilter` — it tracks the bar index of the last entry and rejects entries on the same bar:

```csharp
class FootprintActionAlgoStrategy : MZpack.NT8.Algo.Strategy
{
    int entryBarIdx = -1;

    public bool SuspendAfterTrade { get; set; } = false;

    public FootprintActionAlgoStrategy(string name, GhostResistance MZpackStrategy)
        : base(name, MZpackStrategy) { }

    // One entry per bar maximum
    public override bool OnPositionOpenFilter(DateTime time)
    {
        if (Pattern.Signals.ChartRange.MinBarIdx > entryBarIdx)
        {
            entryBarIdx = Pattern.Signals.ChartRange.MinBarIdx;
            return true;
        }

        Log(LogLevel.POSITION, time,
            "Position open filter: No multiple entries on the bar.");
        return false;
    }

    public override void OnPositionUpdate(Position position, double averagePrice,
        int quantity, MarketPosition marketPosition)
    {
        base.OnPositionUpdate(position, averagePrice, quantity, marketPosition);

        if (marketPosition != MarketPosition.Flat)
        {
            if (SuspendAfterTrade == true)
            {
                IsOpeningPositionEnabled = false;
                (MZpackStrategy as GhostResistance).UpdateButtons();
            }
        }
    }
}
```

### CreateAlgoStrategy

Creates the strategy with trading times and risk management (same pattern as FootprintAction):

```csharp
protected MZpack.NT8.Algo.Strategy CreateAlgoStrategy()
{
    MZpack.NT8.Algo.Strategy strategy = new FootprintActionAlgoStrategy(
        @"Ghost Resistance v1.3", this)
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
        // ... same pattern as FootprintAction
    };

    strategy.SessionBreak = !(Time1_Enable || Time2_Enable);

    return strategy;
}
```

### CreateIndicators

Indicators are created conditionally — only when their signal group is enabled:

```csharp
protected List<TickIndicator> CreateIndicators()
{
    List<TickIndicator> indicators = new List<TickIndicator>();

    if (Strategy_Absorption_Enable)
    {
        indicators.Add(new StrategyFootprintIndicator(this, FOOTPRINT)
        {
            SaveSettings = true,
            ShowVersionInfo = false
        });
    }

    if (Strategy_BigTrade_Enable)
    {
        indicators.Add(new StrategyBigTradeIndicator(this, BIGTRADE)
        {
            SaveSettings = true,
            ShowVersionInfo = false
        });
    }

    if (Strategy_ProfileLevels_Enable)
    {
        indicators.Add(new StrategyVolumeProfileIndicator(this, VOLUME_PROFILE)
        {
            SaveSettings = true,
            ShowVersionInfo = false
        });
    }

    return indicators;
}
```

## Decision Tree Construction

The `prepareStrategy` method builds an AND pattern with all enabled signal groups. Profile level signals use an OR sub-node when both session and weekly levels are enabled:

```csharp
void prepareStrategy(int entriesCount)
{
    // Create entries with limit order support
    Entry[] entries = new Entry[entriesCount];
    entries[0] = new Entry(Strategy)
    {
        EntryMethod = Position_EnterByLimitOrder
            ? EntryMethod.Limit : EntryMethod.Market,
        CancelLimitOrderType = Position_CancelLimitOrderType,
        CancelLimitOrderValue = Position_CancelLimitOrderValue,
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
    // entries[1], entries[2] created similarly

    // Create AND pattern with short-circuit and 1-bar range
    Pattern entryPattern = new Pattern(Strategy, Logic.And,
        new Range() { Bars = 1 }, Strategy_ShortCircuit);

    entryPattern.AllowedDirection = position_Direction;

    // Signal calculation mode (OnBarClose or OnEachTick)
    SignalCalculate calc = Strategy_WaitForBarClose
        ? SignalCalculate.OnBarClose : SignalCalculate.OnEachTick;

    // Bar Metrics signals
    if (Strategy_BarMetrics_Enable)
    {
        OrderflowBarMetricsDesc[] barMetricsDesc = new OrderflowBarMetricsDesc[]
        {
            new OrderflowBarMetricsDesc()
                { Metrics = OrderflowBarMetrics.Volume, MinMax = MinMax.Min,
                  Value = Strategy_MinBarVolume },
            new OrderflowBarMetricsDesc()
                { Metrics = OrderflowBarMetrics.AbsDelta, MinMax = MinMax.Min,
                  Value = Strategy_MinBarDelta },
            new OrderflowBarMetricsDesc()
                { Metrics = OrderflowBarMetrics.DeltaPercent, MinMax = MinMax.Min,
                  Value = Strategy_MinBarDeltaPercent }
        };
        OrdferflowBarMetricsSignal = new OrdferflowBarMetricsSignal(
            Strategy, FootprintIndicator, 0, barMetricsDesc)
            { Name = "Bar metrics", Calculate = calc, IsReset = false };
        entryPattern.Signals.Root.AddChild(OrdferflowBarMetricsSignal);

        // Wick% and Hammer bar metrics
        // ...
    }

    // Absorption signal
    if (Strategy_Absorption_Enable)
    {
        AbsorptionSignal = new FootprintSRZonesSignal(
            Strategy, FootprintIndicator)
            { Name = "Absorption", ZoneType = SRZoneType.Absorption,
              Calculate = calc, IsReset = false, HasPrice = false };
        entryPattern.Signals.Root.AddChild(AbsorptionSignal);
    }

    // Big Trade signal
    if (Strategy_BigTrade_Enable)
    {
        BigTradeSignal = new BigTradeSignal(Strategy)
            { Name = "BigTrade", Calculate = calc,
              HasPrice = true, IsReset = false };
        entryPattern.Signals.Root.AddChild(BigTradeSignal);
    }

    // Profile Levels — OR sub-node for session vs weekly
    if (Strategy_ProfileLevels_Enable)
    {
        Node levelsNode = entryPattern.Signals.Root;
        if (isSessionLevelEnabled() && isWeeklyLevelEnabled())
        {
            levelsNode = new LogicalNode(Logic.Or);
            entryPattern.Signals.Root.AddChild(levelsNode);
        }
        if (isSessionLevelEnabled())
        {
            ApproachingToSessionLevelSignal =
                new ApproachingToSessionLevelSignal(Strategy)
                { Name = "Session Levels", Calculate = calc,
                  IsReset = false, HasPrice = false };
            levelsNode.AddChild(ApproachingToSessionLevelSignal);
        }
        if (isWeeklyLevelEnabled())
        {
            ApproachingToWeeklyProfileLevelSignal =
                new ApproachingToWeeklyLevelSignal(Strategy)
                { Name = "Weekly Levels", Calculate = calc,
                  IsReset = false, HasPrice = false };
            levelsNode.AddChild(ApproachingToWeeklyProfileLevelSignal);
        }
    }

    Strategy.Initialize(entryPattern, null, entries);
}
```

## Custom Signal Implementations

### BigTradeSignal

Detects big trades at bar extremes — sell trades in the lower wick (long) or buy trades in the upper wick (short). Supports limit order entry at the best big trade POC price:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    GhostResistance strategy = (GhostResistance)Strategy.MZpackStrategy;
    SignalDirection direction = SignalDirection.None;

    ICandle candle = strategy.GetCandle(GetCurrentBarAgo(0));
    var trades = strategy.BigTradeIndicator.Trades.ToList();

    trades.Reverse();
    List<ITrade> barTrades = new List<ITrade>();
    foreach (var trade in trades)
    {
        if (trade.StartBarIdx == barIdx)
            barTrades.Add(trade);
        else if (trade.StartBarIdx < barIdx)
            break;
    }

    // Sell trades below body = potential long
    var sellTrades = barTrades.Where(
        x => x.Side == TradeSide.Bid && x.POC < candle.LowerBody);
    // Buy trades above body = potential short
    var buyTrades = barTrades.Where(
        x => x.Side == TradeSide.Ask && x.POC > candle.UpperBody);

    if (sellTrades.Count() > 0 && buyTrades.Count() > 0)
        direction = SignalDirection.Any;
    else if (buyTrades.Count() > 0)
        direction = Signal.ResolveDirection(SignalDirection.Short, allowed);
    else if (sellTrades.Count() > 0)
        direction = Signal.ResolveDirection(SignalDirection.Long, allowed);

    if (Signal.IsDetermined(direction))
    {
        var trds = direction == SignalDirection.Long ? sellTrades : buyTrades;

        Direction = direction;
        Time = e.Time;
        if (HasPrice)
        {
            if (strategy.Position_EnterByLimitOrder)
                EntryPrice = direction == SignalDirection.Long
                    ? trds.Min(x => x.POC)    // Best (lowest) big trade POC
                    : trds.Max(x => x.POC);   // Best (highest) big trade POC
            else
                EntryPrice = GetBestEntryPrice(direction);
        }
        ChartRange = new ChartRange()
        {
            MinBarIdx = barIdx, MaxBarIdx = barIdx,
            Low = EntryPrice, High = EntryPrice
        };
    }
}
```

### ApproachingToSessionLevelSignal

Checks if price is approaching prior session volume profile levels (overnight ETH and RTH). Uses the absorption signal's direction to determine which price side to check:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    GhostResistance strategy = Strategy.MZpackStrategy as GhostResistance;
    IVolumeProfile profile = strategy.VolumeProfileIndicator.Profiles.LastOrDefault()
        as IVolumeProfile;

    if (profile == null) return;

    profile = profile.Prior as IVolumeProfile;  // Prior session
    if (profile == null) return;

    IVolumeProfile profileRTH = profile.IsRTH() ? profile : null;
    IVolumeProfile profileETH = profile.IsETH() ? profile : null;

    profile = profile.Prior as IVolumeProfile;
    if (profile == null) return;

    profileRTH = profile.IsRTH() ? profile : null;
    profileETH = profile.IsETH() ? profile : null;

    // Direction comes from absorption signal
    allowed = strategy.AbsorptionSignal.Direction;
    SignalDirection direction = SignalDirection.None;

    ICandle candle = strategy.GetCandle(GetCurrentBarAgo(0));
    if (candle == null) return;

    List<string> levels = new List<string>();
    double current = allowed == SignalDirection.Long
        ? candle.Low : candle.High;

    // Check overnight levels (ETH High/Low, POC, VAH/VAL)
    if (profileETH != null)
    {
        if (strategy.Strategy_OvernightVP_HighLow)
        {
            if (strategy.IsPriceApproaching(current, profileETH.High,
                strategy.Strategy_SessionVP_Approaching))
            {
                direction = allowed;
                levels.Add("Overnight High");
            }
            // ... Low, POC, VAH, VAL checks
        }
    }

    // Check RTH levels
    if (profileRTH != null)
    {
        // ... same pattern for RTH High/Low, POC, VAH/VAL
    }

    if (IsDetermined(direction))
    {
        Direction = direction;
        Time = e.Time;
        if (HasPrice) EntryPrice = GetEntryPrice(e, direction);
        ChartRange = new ChartRange()
            { MinBarIdx = barIdx, MaxBarIdx = barIdx };
        Description = $" => {string.Join(", ", levels)}";
    }
}
```

### ApproachingToWeeklyLevelSignal

Same pattern as session levels but reads from the stacked weekly volume profile:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
{
    GhostResistance strategy = Strategy.MZpackStrategy as GhostResistance;
    IVolumeProfile profile = strategy.VolumeProfileIndicator.GetStackedProfile(0);

    if (profile == null) return;

    // Direction comes from absorption signal
    allowed = strategy.AbsorptionSignal.Direction;
    SignalDirection direction = SignalDirection.None;

    ICandle candle = strategy.GetCandle(GetCurrentBarAgo(0));
    if (candle == null) return;

    List<string> levels = new List<string>();
    double current = allowed == SignalDirection.Long
        ? candle.Low : candle.High;

    // Check weekly High/Low, POC, VAH/VAL
    if (strategy.Strategy_WeeklyVP_POC)
    {
        if (strategy.IsPriceApproaching(current, profile.High,
            strategy.Strategy_WeeklyVP_Approaching))
        {
            direction = allowed;
            levels.Add("Weekly High");
        }
        // ... Low check
    }
    // ... POC, VAH, VAL checks

    if (IsDetermined(direction))
    {
        Direction = direction;
        Time = e.Time;
        if (HasPrice) EntryPrice = GetEntryPrice(e, direction);
        ChartRange = new ChartRange()
            { MinBarIdx = barIdx, MaxBarIdx = barIdx };
        Description = $" => {string.Join(", ", levels)}";
    }
}
```

## Data Export Schema

Exports 3 signal features plus the combined pattern:

```csharp
public class ExportDataSchema : DataSchema
{
    GhostResistance strategy;

    public ExportDataSchema(DataSet dataSet, GhostResistance strategy) : base(dataSet)
    {
        this.strategy = strategy;

        if (strategy.Strategy_BarMetrics_Enable)
            Append("BarMetrics", ValueKind.Feature,
                new CalculateExportValueDelegate(GetOrdferflowBarMetrics));
        if (strategy.Strategy_Absorption_Enable)
            Append("Absorption", ValueKind.Feature,
                new CalculateExportValueDelegate(GetAbsorption));
        if (strategy.Strategy_BigTrade_Enable)
            Append("DeltaTail", ValueKind.Feature,
                new CalculateExportValueDelegate(GetBigTrade));

        Append("Pattern", ValueKind.Feature,
            new CalculateExportValueDelegate(GetPattern));
    }

    double directionToDouble(SignalDirection d)
    {
        if (d == SignalDirection.Long) return 1.0;
        else if (d == SignalDirection.Short) return -1.0;
        else return 0;
    }
}
```

## Indicator Configuration

During `State.Configure`, each indicator is configured with settings from the strategy properties. The footprint indicator always enables absorption:

```csharp
// Footprint — always enable absorption
FootprintIndicator.ShowAbsorption = true;
FootprintIndicator.ShowAbsorptionSRZones = true;
FootprintIndicator.AbsorptionPercentage = Strategy_Absorptions_Percent;
FootprintIndicator.AbsorptionDepth = Strategy_Absorptions_Depth;
FootprintIndicator.AbsorptionSRZonesConsecutiveLevels = Strategy_Absorptions_Consecutive;
FootprintIndicator.AbsorptionSRZonesVolumeFilter = Strategy_Absorptions_Volume;

// Volume profile — RTH/ETH sessions + weekly stacked
VolumeProfileIndicator.ProfileCreation = ProfileCreation.RTH_ETH;
VolumeProfileIndicator.ETH_Enable = true;
VolumeProfileIndicator.StackedShowProfileType1 = isWeeklyLevelEnabled()
    ? ProfileType.VP : ProfileType.None;
VolumeProfileIndicator.StackedProfileCreation1 = isWeeklyLevelEnabled()
    ? ProfileCreation.Weekly : ProfileCreation.None;
VolumeProfileIndicator.RTH_Begin = Strategy_RTH_Begin;
VolumeProfileIndicator.RTH_End = Strategy_RTH_End;
VolumeProfileIndicator.ETH_Begin = Strategy_ETH_Begin;
VolumeProfileIndicator.ETH_End = Strategy_ETH_End;

// Big trade — filter settings
BigTradeIndicator.FilterLogic = TradeFilterLogic.ALL;
BigTradeIndicator.TradeFilterMin = Strategy_BigTrade_TradeFilterMin;
BigTradeIndicator.IcebergFilterEnable = Strategy_BigTrade_IcebergFilterEnable;
BigTradeIndicator.IcebergFilterMin = Strategy_BigTrade_IcebergFilterMin;
BigTradeIndicator.AggressionFilterEnable = Strategy_BigTrade_AggressionEnable;
BigTradeIndicator.AggressionFilterMin = Strategy_BigTrade_AggressionTicks;
```

## Configurable Properties

### Strategy

| Property | Default | Description |
|---|---|---|
| `Strategy_Action` | `Trade` | Trade or Export mode |
| `OppositePatternAction` | `None` | None, Close, or Reverse on opposite signal |
| `Strategy_SuspendAfterTrade` | `false` | Pause after position opens |
| `Strategy_WaitForBarClose` | `false` | OnBarClose vs OnEachTick calculation |
| `Strategy_ShortCircuit` | `true` | Short-circuit pattern evaluation |

### Bar Metrics

| Property | Default | Description |
|---|---|---|
| `Strategy_BarMetrics_Enable` | `true` | Enable bar metrics signal group |
| `Strategy_MinBarVolume` | `100` | Minimum bar volume |
| `Strategy_MinBarDelta` | `100` | Minimum absolute bar delta |
| `Strategy_MinBarDeltaPercent` | `0` | Minimum bar delta percentage |
| `Strategy_MinWickPercent` | `30` | Minimum wick percentage |
| `Strategy_IsHammer` | `true` | Require hammer pattern |

### Absorption

| Property | Default | Description |
|---|---|---|
| `Strategy_Absorption_Enable` | `true` | Always enabled |
| `Strategy_Absorptions_Percent` | `200` | Absorption percentage threshold |
| `Strategy_Absorptions_Depth` | `2` | Price levels to check |
| `Strategy_Absorptions_Consecutive` | `2` | Consecutive levels required |
| `Strategy_Absorptions_Volume` | `50` | Zone volume minimum |

### Big Trade

| Property | Default | Description |
|---|---|---|
| `Strategy_BigTrade_Enable` | `true` | Always enabled |
| `Strategy_BigTrade_TradeFilterMin` | `200` | Minimum trade size |
| `Strategy_BigTrade_IcebergFilterEnable` | `true` | Detect iceberg orders |
| `Strategy_BigTrade_IcebergFilterMin` | `20` | Minimum iceberg volume |
| `Strategy_BigTrade_AggressionEnable` | `true` | Require sweep trades |
| `Strategy_BigTrade_AggressionTicks` | `3` | Minimum sweep ticks |

### Profile Levels

| Property | Default | Description |
|---|---|---|
| `Strategy_ProfileLevels_Enable` | `true` | Enable profile levels |
| `Strategy_SessionVP_Approaching` | `8` | Session approaching distance (ticks) |
| `Strategy_WeeklyVP_Approaching` | `20` | Weekly approaching distance (ticks) |
| Overnight POC/VAH-VAL/High-Low | `true` | Individual level toggles |
| RTH POC/VAH-VAL/High-Low | `true` | Individual level toggles |
| Weekly POC/VAH-VAL/High-Low | `true` | Individual level toggles |
| RTH/ETH session times | configurable | RTH 08:30-15:15, ETH 17:30-08:30 |

### Position

| Property | Default | Description |
|---|---|---|
| `Position_Direction` | `Any` | Allowed direction |
| `Position_Quantity1` | `1` | Entry 1 contracts |
| `Position_StopLoss1` | `20` | Entry 1 stop loss ticks |
| `Position_ProfitTarget1` | `40` | Entry 1 profit target ticks |
| `Position_Quantity2` | `2` | Entry 2 contracts |
| `Position_StopLoss2` | `20` | Entry 2 stop loss ticks |
| `Position_ProfitTarget2` | `60` | Entry 2 profit target ticks |
| `Position_Quantity3` | `0` | Entry 3 contracts (0 = disabled) |
| `Position_EnterByLimitOrder` | `false` | Use limit orders |
| `Position_IsBE` | `false` | Enable breakeven |
| `Position_IsTrail` | `false` | Enable trailing stop |

## See Also

- [Built-in Strategies](/docs/strategies/built-in-strategies#ghostresistance-strategy) — user-facing settings reference
- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Decision Tree](../strategies/decision-tree.md) — AND/OR logic
- [Pattern](../strategies/pattern.md) — pattern types and evaluation
- [Signal](../strategies/signals/custom-signal.md) — creating custom signals
- [Entry](../strategies/entry.md) — order submission with limit orders
- [Footprint Action](footprint-action.md) — related strategy with OR/mandatory signal grouping
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile
