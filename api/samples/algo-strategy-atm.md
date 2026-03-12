---
sidebar_position: 13
title: "Algo Strategy — ATM + TradesClusterSignal"
description: "Algo.Strategy with proprietary ATM and TradesClusterSignal"
---

# Algo Strategy — ATM + TradesClusterSignal

Demonstrates an Algo.Strategy that uses `TradesClusterSignal` to detect trade clusters on both Ask and Bid sides, then enters with market orders using breakeven and trailing stop management.

**Source:** `[INSTALL PATH]/API/Samples/Built-in/MZpackAlgoStrategy0.cs`
**Class:** `MZpackAlgoStrategy0 : MZpackStrategyBase`

## What It Covers

- `StrategyBigTradeIndicator` for trade cluster detection
- `Algo.Strategy` with `OppositePatternAction.Reverse`
- Pattern with OR logic root and two `TradesClusterSignal` instances (Ask/Bid)
- Single `Entry` with market orders, breakeven, and trailing stop
- `TradesClusterSignal` configured with `Range` (bars + ticks), `MinVolume`, `MinCount`
- `PartiallyVisibleMode = OnPatternValidated`

## Architecture

```
MZpackAlgoStrategy0 : MZpackStrategyBase
 ├── StrategyBigTradeIndicator "Clusters"
 └── Algo.Strategy
      └── Entry Pattern (OR root)
           ├── TradesClusterSignal "Ask Clusters" → Short
           └── TradesClusterSignal "Bid Clusters" → Long
```

## Constructor

The constructor wires up delegate callbacks for indicator and strategy creation:

```csharp
public MZpackAlgoStrategy0() : base()
{
    OnCreateAlgoStrategy = new OnCreateAlgoStrategyDelegate(CreateAlgoStrategy);
    OnCreateIndicators = new OnCreateIndicatorsDelegate(CreateIndicators);
}
```

## Creating the Algo.Strategy

```csharp
protected MZpack.NT8.Algo.Strategy CreateAlgoStrategy()
{
    return new MZpack.NT8.Algo.Strategy(@"MZpack Algo Strategy #0", this)
    {
        OppositePatternAction = OppositePatternAction.Reverse,
        LogLevel = LogLevel,
        LogTarget = LogTarget,
        LogTime = LogTime
    };
}
```

## Indicator Setup

```csharp
bigTradeIndicator = new StrategyBigTradeIndicator(this, @"Clusters")
{
    FilterLogic = TradeFilterLogic.ALL,
    TradeFilterEnable = true,
    DomPressureFilterEnable = true,
    AggressionFilterEnable = false,
    MarkerType = TradeMarkerType.Box,
    MaxShapeExtent = 10,
    ColorMode = ColorMode.Saturation,
    ShowTradePOC = true,
    VolumesPosition = VolumesPosition.OutsideRight,
    UseBigTradeAlert = false
};
```

## Pattern Setup

Two `TradesClusterSignal` instances are added to an OR root — Ask clusters trigger Short entries, Bid clusters trigger Long entries:

```csharp
Pattern pattern = new Pattern(Strategy,
    Logic.Or,
    null,
    true);

pattern.Signals.Root.AddChild(
    new TradesClusterSignal(Strategy, bigTradeIndicator, SignalDirection.Short)
    {
        Name = "Ask Clusters",
        Side = TradeSide.Ask,
        Range = new Range() { Bars = BigTrade_ClusterBarRange, Ticks = BigTrade_ClusterPriceRangeTicks, Logic = Logic.And },
        MinVolume = BigTrade_MinTotalVolume,
        MinCount = BigTrade_MinTotalCount,
        VolumeCountLogic = Logic.And,
        PartiallyVisibleMode = SignalPartiallyVisibleMode.OnPatternValidated
    });
pattern.Signals.Root.AddChild(
    new TradesClusterSignal(Strategy, bigTradeIndicator, SignalDirection.Long)
    {
        Name = "Bid Clusters",
        Side = TradeSide.Bid,
        Range = new Range() { Bars = BigTrade_ClusterBarRange, Ticks = BigTrade_ClusterPriceRangeTicks, Logic = Logic.And },
        MinVolume = BigTrade_MinTotalVolume,
        MinCount = BigTrade_MinTotalCount,
        VolumeCountLogic = Logic.And,
        PartiallyVisibleMode = SignalPartiallyVisibleMode.OnPatternValidated
    });

Strategy.Initialize(pattern, entries, 3);
```

## Entry Setup

A single entry with market order, optional breakeven, and optional trailing stop:

```csharp
Entry[] entries = new Entry[EntriesPerDirection];
Trail trail = Position_IsTrail ? new Trail(Position_TrailAfter, Position_TrailDistance, Position_TrailStep) : null;
entries[0] = new Entry(Strategy)
{
    EntryMethod = EntryMethod.Market,
    Quantity = Position_Quantity,
    SignalName = SIGNAL_NAME,
    StopLossTicks = Position_StopLoss,
    ProfitTargetTicks = Position_ProfitTarget,
    IsBreakEven = Position_IsBE,
    BreakEvenAfterTicks = Position_BEAfterTicks,
    BreakEvenShiftTicks = Position_BEShiftTicks,
    Trail = trail
};
```

## Configurable Properties

### Signals

| Property | Default | Description |
|---|---|---|
| `BigTrade_TradeMin` | `20` | Min trade volume filter |
| `BigTrade_TradeMax` | `500` | Max trade volume filter |
| `BigTrade_DomPressureMin` | `5` | Min DOM pressure |
| `BigTrade_ClusterBarRange` | `4` | Cluster bar range |
| `BigTrade_ClusterPriceRangeTicks` | `4` | Cluster price range in ticks |
| `BigTrade_MinTotalVolume` | `50` | Min total cluster volume |
| `BigTrade_MinTotalCount` | `3` | Min trades in cluster |

### Position

| Property | Default | Description |
|---|---|---|
| `Position_Direction` | `Any` | Allowed direction |
| `Position_Quantity` | `2` | Contracts |
| `Position_StopLoss` | `18` | Stop loss ticks |
| `Position_ProfitTarget` | `35` | Profit target ticks |
| `Position_IsBE` | `false` | Enable breakeven |
| `Position_BEAfterTicks` | `14` | Ticks before breakeven |
| `Position_BEShiftTicks` | `4` | Breakeven shift ticks |
| `Position_IsTrail` | `true` | Enable trailing |
| `Position_TrailAfter` | `20` | Trail activation ticks |
| `Position_TrailDistance` | `10` | Trail distance ticks |
| `Position_TrailStep` | `2` | Trail step ticks |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Entry](../strategies/entry.md) — entry configuration
- [Trail](../strategies/trail.md) — trailing stop
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
