---
sidebar_position: 16
title: "Algo Strategy — Footprint Imbalance"
description: "Algo.Strategy with FootprintImbalanceSignal"
---

# Algo Strategy — Footprint Imbalance

Demonstrates an Algo.Strategy that uses `FootprintImbalanceSignal` to detect footprint imbalances, with trading time windows, risk management, and a custom strategy subclass that tracks entry bar indices.

**Source:** `[INSTALL PATH]/API/Samples/MZpackAlgoStrategy_Imbalance.cs`
**Class:** `MZpackAlgoStrategy_Imbalance : MZpackStrategyBase`

## What It Covers

- Custom `AlgoStrategy_Imbalance` subclass with `OnPositionOpenFilter` override
- `OnOrderUpdate` tracking entry bar index
- `StrategyFootprintIndicator` configured for imbalance detection
- `FootprintImbalanceSignal` with `MinCount` and `PartiallyVisibleMode`
- `TradingTimes` with two configurable windows
- `RiskManagement` with daily loss, profit, and trades limits
- Footprint visual customization (values brush, font)

## Architecture

```
MZpackAlgoStrategy_Imbalance : MZpackStrategyBase
 ├── StrategyFootprintIndicator "Imbalance"
 │    └── IsPartiallyVisible (configurable)
 └── AlgoStrategy_Imbalance : Algo.Strategy
      ├── TradingTimes[] (two configurable windows)
      ├── RiskManagement (daily limits)
      └── Entry Pattern (AND root, short-circuit)
           └── FootprintImbalanceSignal "Imbalance"
```

## Custom Strategy Subclass

The `AlgoStrategy_Imbalance` subclass overrides `OnPositionOpenFilter` and tracks the entry bar index via `OnOrderUpdate`:

```csharp
class AlgoStrategy_Imbalance : MZpack.NT8.Algo.Strategy
{
    int entryBarIdx = -1;

    public AlgoStrategy_Imbalance(string name, MZpackAlgoStrategy_Imbalance strategy)
        : base(name, strategy) { }

    public override bool OnPositionOpenFilter(DateTime time)
    {
        return true;  // No double entries logic available (commented out)
    }

    public override void OnOrderUpdate(Order order, OrderState orderState)
    {
        base.OnOrderUpdate(order, orderState);
        if (orderState == OrderState.Filled && order.Name == ENTRY_NAME)
            entryBarIdx = MZpackStrategy.CurrentBar;
    }
}
```

## Creating the Algo.Strategy

Trading times and risk management are configured on the strategy instance:

```csharp
AlgoStrategy_Imbalance strategy = new AlgoStrategy_Imbalance(
    @"MZpack Algo Strategy - Imbalance", this)
{
    OppositePatternAction = OppositePatternAction.None,
    LogLevel = LogLevel, LogTarget = LogTarget, LogTime = LogTime
};

if (Time1_Enable)
    strategy.TradingTimes.Add(new TradingTime()
    { Begin = tryParseDateTime(Time1_Begin), End = tryParseDateTime(Time1_End) });

strategy.RiskManagement = new MZpack.NT8.Algo.RiskManagement(strategy)
{
    Currency = Currency.UsDollar,
    EntryName = ENTRY_NAME,
    DailyLossLimitEnable = Risk_DailyLossLimit_Enable,
    DailyLossLimit = Risk_DailyLossLimit,
    DailyProfitLimitEnable = Risk_DailyProfitLimit_Enable,
    DailyProfitLimit = Risk_DailyProfitLimit,
    DailyTradesLimitEnable = Risk_DailyTradesLimit_Enable,
    DailyTradesLimit = Risk_DailyTradesLimit
};
```

## Footprint Indicator Setup

```csharp
footprintIndicator = new StrategyFootprintIndicator(this, @"Imbalance")
{
    ShowBarVolume = false,
    ShowBarDelta = true,
    ShowImbalance = true,
    ImbalanceMarker = FootprintImbalanceMarker.Always,
    ImbalanceHighlightValues = true,
    ShowBarPOC = true,
    ShowVersionInfo = false
};
```

## Signal Setup

A single `FootprintImbalanceSignal` is added to an AND-root pattern:

```csharp
pattern.Signals.Root.AddChild(new FootprintImbalanceSignal(Strategy, footprintIndicator)
{
    Name = "Imbalance",
    IsReset = true,
    MinCount = Strategy_Footprint_BarImbalanceMinCount,
    PartiallyVisibleMode = SignalPartiallyVisibleMode.OnPatternValidated
});

Strategy.Initialize(pattern, null, entries);
```

## Configurable Properties

### Strategy

| Property | Default | Description |
|---|---|---|
| `Strategy_Footprint_TicksPerLevel` | `1` | Ticks per level |
| `Strategy_Footprint_ImbalancePercentage` | `100` | Imbalance percentage |
| `Strategy_Footprint_ImbalanceFilter` | `1` | Imbalance volume filter |
| `Strategy_Footprint_BarImbalanceMinCount` | `1` | Min imbalances in bar |

### Position

| Property | Default | Description |
|---|---|---|
| `Position_Direction` | `Any` | Allowed direction |
| `Position_Quantity` | `2` | Contracts |
| `Position_StopLoss` | `18` | Stop loss ticks |
| `Position_ProfitTarget` | `35` | Profit target ticks |
| `Position_IsBE` | `false` | Enable breakeven |
| `Position_IsTrail` | `true` | Enable trailing |
| `Position_TrailAfter` | `20` | Trail after ticks |
| `Position_TrailDistance` | `10` | Trail distance ticks |
| `Position_TrailStep` | `2` | Trail step ticks |

### Trading Time

| Property | Default | Description |
|---|---|---|
| `Time1_Enable` | `false` | Enable first window |
| `Time1_Begin` | `"08:30:00"` | Start time |
| `Time1_End` | `"15:15:00"` | End time |
| `Time2_Enable` | `false` | Enable second window |

### Risk Management

| Property | Default | Description |
|---|---|---|
| `Risk_DailyLossLimit_Enable` | `true` | Enable daily loss limit |
| `Risk_DailyLossLimit` | `500` | Daily loss limit (USD) |
| `Risk_DailyProfitLimit_Enable` | `true` | Enable daily profit limit |
| `Risk_DailyProfitLimit` | `2500` | Daily profit limit (USD) |
| `Risk_DailyTradesLimit_Enable` | `false` | Enable daily trades limit |
| `Risk_DailyTradesLimit` | `5` | Max trades per day |

### Footprint

| Property | Default | Description |
|---|---|---|
| `VisibleFootprintIndicator` | `true` | Show footprint indicator |
| `PartiallyVisibleFootprintIndicator` | `false` | Partially visible mode |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Risk Management](../strategies/risk-management.md) — daily limits
- [TradingTime](../strategies/trading-time.md) — trading time windows
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
