---
sidebar_position: 22
title: "Risk Management"
description: "RiskManagement class with daily loss, profit, and trade count limits."
---

# Risk Management

Demonstrates the `RiskManagement` class with daily loss, profit, and trade count limits. Trades up/down bars on bar close using a simple `UpDownBarSignal`.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/RiskManagement.cs`
**Class:** `RiskManagement : MZpackStrategyBase`

## What It Covers

- `RiskManagement` object with daily loss, profit, and trades limits
- `Algo.Strategy` with `OppositePatternAction.None`
- `UpDownBarSignal` (`OnBarClose`) -- Long for up-bars, Short for down-bars
- Single market entry with stop loss and profit target

## Strategy Setup

```csharp
protected MZpack.NT8.Algo.Strategy CreateAlgoStrategy()
{
    MZpack.NT8.Algo.Strategy strategy = new MZpack.NT8.Algo.Strategy(
        @"Risk Management", this)
    {
        OppositePatternAction = OppositePatternAction.None,
        LogLevel = LogLevel, LogTarget = LogTarget, LogTime = LogTime
    };

    strategy.RiskManagement = new MZpack.NT8.Algo.RiskManagement(strategy)
    {
        Currency = Currency.UsDollar,
        EntryName = ENTRY_NAME,
        DailyLossLimitEnable = Common_DailyLossLimit_Enable,
        DailyLossLimit = Common_DailyLossLimit,
        DailyProfitLimitEnable = Common_DailyProfitLimit_Enable,
        DailyProfitLimit = Common_DailyProfitLimit,
        DailyTradesLimitEnable = Common_DailyTradesLimit_Enable,
        DailyTradesLimit = Common_DailyTradesLimit
    };

    return strategy;
}
```

## Signal

The `UpDownBarSignal` generates Long entries for up-bars and Short entries for down-bars:

```csharp
class UpDownBarSignal : Signal
{
    public UpDownBarSignal(MZpack.NT8.Algo.Strategy strategy)
        : base(strategy, MarketDataSource.Level1, SignalCalculate.OnBarClose, true) { }

    public override void OnCalculate(MarketDataEventArgs e, int barIdx,
        SignalDirection allowed)
    {
        SignalDirection direction = SignalDirection.None;

        if (Signal.IsLongAllowed(allowed)
            && Strategy.MZpackStrategy.Open[1] > Strategy.MZpackStrategy.Close[1])
            direction = Signal.ResolveDirection(SignalDirection.Short, allowed);
        else if (Signal.IsLongAllowed(allowed)
            && Strategy.MZpackStrategy.Open[1] < Strategy.MZpackStrategy.Close[1])
            direction = Signal.ResolveDirection(SignalDirection.Long, allowed);

        if (Signal.IsDetermined(direction))
        {
            Direction = direction;
            ChartRange = new ChartRange() { MinBarIdx = barIdx, MaxBarIdx = barIdx };
            Time = e.Time;
            EntryPrice = e.Price;
        }
    }
}
```

## Configurable Properties

### Risk Management

| Property | Default | Description |
|---|---|---|
| `Common_DailyLossLimit_Enable` | `true` | Enable daily loss limit |
| `Common_DailyLossLimit` | `300` | Daily loss limit (USD) |
| `Common_DailyProfitLimit_Enable` | `false` | Enable daily profit limit |
| `Common_DailyProfitLimit` | `3000` | Daily profit limit (USD) |
| `Common_DailyTradesLimit_Enable` | `false` | Enable daily trades limit |
| `Common_DailyTradesLimit` | `5` | Max trades per day |

### Position

| Property | Default | Description |
|---|---|---|
| `Position_Direction` | `Any` | Allowed direction |
| `Position_Quantity` | `2` | Contracts |
| `Position_StopLoss` | `6` | Stop loss ticks |
| `Position_ProfitTarget` | `12` | Profit target ticks |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Risk Management](../strategies/risk-management.md) — RiskManagement class reference
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
