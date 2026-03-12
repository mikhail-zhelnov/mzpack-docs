---
sidebar_position: 23
title: "Trading Times"
description: "TradingTimes feature with configurable time windows and session break control (OnBarClose)."
---

# Trading Times

Demonstrates the `TradingTimes` feature with two configurable time windows. Trades up/down bars on bar close using a simple `UpDownBarSignal`.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/TradingTimes.cs`
**Class:** `TradingTimes : MZpackStrategyBase`

## What It Covers

- `TradingTime` objects with Begin/End time windows
- `Strategy.TradingTimes` list for restricting when the strategy can trade
- `SessionBreak` control — disabled when time schedule is active
- `UpDownBarSignal` (OnBarClose) — Long for up-bars, Short for down-bars
- Time string parsing with error handling via `NTMessageBox`

## Strategy Setup

```csharp
protected MZpack.NT8.Algo.Strategy CreateAlgoStrategy()
{
    MZpack.NT8.Algo.Strategy strategy = new MZpack.NT8.Algo.Strategy(
        @"Trading Times", this)
    {
        OppositePatternAction = OppositePatternAction.None,
        LogLevel = LogLevel, LogTarget = LogTarget, LogTime = LogTime
    };

    // Trading times
    if (Time1_Enable)
        strategy.TradingTimes.Add(new TradingTime()
        { Begin = TryParseDateTime(Time1_Begin), End = TryParseDateTime(Time1_End) });
    if (Time2_Enable)
        strategy.TradingTimes.Add(new TradingTime()
        { Begin = TryParseDateTime(Time2_Begin), End = TryParseDateTime(Time2_End) });

    // No session break when time schedule is enabled
    strategy.SessionBreak = !(Time1_Enable || Time2_Enable);

    return strategy;
}
```

Time parsing helper:

```csharp
DateTime TryParseDateTime(string s)
{
    if (!DateTime.TryParse(s, out DateTime time))
        NTMessageBox.Show("Error in date/time format: '" + s + "'",
            Name, System.Windows.MessageBoxImage.None);
    return time;
}
```

## Entry and Signal

```csharp
Entry[] entries = new Entry[EntriesPerDirection];
entries[0] = new Entry(Strategy)
{
    EntryMethod = EntryMethod.Market,
    Quantity = Position_Quantity,
    SignalName = ENTRY_NAME,
    StopLossTicks = Position_StopLoss,
    ProfitTargetTicks = Position_ProfitTarget,
};

Pattern pattern = new Pattern(Strategy, Logic.And, null, true);
pattern.Signals.Root.AddChild(new UpDownBarSignal(Strategy));
Strategy.Initialize(pattern, entries, 3);
```

The `UpDownBarSignal` evaluates on bar close — Long for up-bars, Short for down-bars:

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

### Trading Time

| Property | Default | Description |
|---|---|---|
| `Time1_Enable` | `true` | Enable first time window |
| `Time1_Begin` | `"08:30:00"` | First window start |
| `Time1_End` | `"15:15:00"` | First window end |
| `Time2_Enable` | `false` | Enable second time window |
| `Time2_Begin` | `"15:30:00"` | Second window start |
| `Time2_End` | `"17:00:00"` | Second window end |

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
- [TradingTime](../strategies/trading-time.md) — time windows reference
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
