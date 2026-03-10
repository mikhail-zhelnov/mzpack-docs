---
sidebar_position: 3
title: "Custom Signal"
description: "Step-by-step guide to creating a custom Signal subclass for the MZpack strategy decision tree."
---

# Custom Signal

Create your own signal by extending the `Signal` base class. Custom signals plug into the decision tree alongside built-in signals.

**Namespace:** `MZpack.NT8.Algo`

## Steps

### 1. Inherit from Signal

```csharp
public class DeltaThresholdSignal : Signal
{
    public DeltaThresholdSignal() { }

    public DeltaThresholdSignal(Strategy strategy,
        MarketDataSource source, SignalCalculate calculate)
        : base(strategy, source, calculate, isReset: true)
    {
    }
}
```

### 2. Override Name

```csharp
public override string Name => "Delta Threshold";
```

### 3. Declare Parameters

Use public properties for configurable parameters. Decorate with `[Display]` for the property grid:

```csharp
[Display(Name = "Delta Threshold", GroupName = "Custom", Order = 1)]
public double DeltaThreshold { get; set; } = 500;

[Display(Name = "Reverse", GroupName = "Custom", Order = 2)]
public bool IsReverse { get; set; } = false;
```

### 4. Reference Indicators

Override `GetIndicatorsTemplates()` to declare which strategy indicators your signal needs:

```csharp
StrategyFootprintIndicator footprint;

public override List<IndicatorTemplate> GetIndicatorsTemplates()
{
    return new List<IndicatorTemplate>
    {
        new IndicatorTemplate(typeof(StrategyFootprintIndicator), (i) => footprint = (StrategyFootprintIndicator)i)
    };
}
```

The framework calls `ReferIndicators()` during initialization to resolve the indicator reference from the strategy's indicator collection.

### 5. Implement Calculate

Override `OnCalculate` for your data source. Return the direction by setting `Direction`:

```csharp
public override void OnCalculate(MarketDataEventArgs e, int barIdx,
    SignalDirection allowed)
{
    if (footprint == null) return;
    if (!footprint.FootprintBars.ContainsKey(barIdx)) return;

    IFootprintBar bar = footprint.FootprintBars[barIdx];
    long delta = bar.Delta;

    if (delta > DeltaThreshold)
        Direction = Node.ReverseDirection(SignalDirection.Long, IsReverse);
    else if (delta < -DeltaThreshold)
        Direction = Node.ReverseDirection(SignalDirection.Short, IsReverse);
    else
        Direction = SignalDirection.None;

    if (Node.IsDetermined(Direction))
    {
        ChartRange = new ChartRange
        {
            MinBarIdx = barIdx,
            MaxBarIdx = barIdx,
            High = bar.Hi,
            Low = bar.Lo
        };
        EntryPrice = GetBestEntryPrice(Direction);
    }
}
```

### 6. Add to Decision Tree

```csharp
OnCreateAlgoStrategy = () =>
{
    var strategy = new Strategy("DeltaStrategy", this);

    var signal = new DeltaThresholdSignal(strategy,
        MarketDataSource.Level1,
        SignalCalculate.OnBarClose);
    signal.DeltaThreshold = 1000;

    var pattern = new Pattern(strategy, Logic.And, new Range(),
        isShortCircuitANDEvaluation: true);
    pattern.Signals.Root.Add(signal);

    strategy.Initialize(pattern);
    return strategy;
};
```

:::tip
Use `SignalCalculate.OnBarClose` for backtesting performance. `OnEachTick` requires Tick Replay or live data and is significantly slower.
:::

## Complete Example

```csharp
public class DeltaThresholdSignal : Signal
{
    StrategyFootprintIndicator footprint;

    [Display(Name = "Delta Threshold", GroupName = "Custom", Order = 1)]
    public double DeltaThreshold { get; set; } = 500;

    [Display(Name = "Reverse", GroupName = "Custom", Order = 2)]
    public bool IsReverse { get; set; } = false;

    public override string Name => "Delta Threshold";

    public DeltaThresholdSignal() { }

    public DeltaThresholdSignal(Strategy strategy,
        MarketDataSource source, SignalCalculate calculate)
        : base(strategy, source, calculate, isReset: true) { }

    public override List<IndicatorTemplate> GetIndicatorsTemplates()
    {
        return new List<IndicatorTemplate>
        {
            new IndicatorTemplate(typeof(StrategyFootprintIndicator),
                (i) => footprint = (StrategyFootprintIndicator)i)
        };
    }

    public override void OnCalculate(MarketDataEventArgs e, int barIdx,
        SignalDirection allowed)
    {
        if (footprint == null) return;
        if (!footprint.FootprintBars.ContainsKey(barIdx)) return;

        IFootprintBar bar = footprint.FootprintBars[barIdx];
        long delta = bar.Delta;

        if (delta > DeltaThreshold)
            Direction = Node.ReverseDirection(SignalDirection.Long, IsReverse);
        else if (delta < -DeltaThreshold)
            Direction = Node.ReverseDirection(SignalDirection.Short, IsReverse);
        else
            Direction = SignalDirection.None;

        if (Node.IsDetermined(Direction))
        {
            ChartRange = new ChartRange
            {
                MinBarIdx = barIdx,
                MaxBarIdx = barIdx,
                High = bar.Hi,
                Low = bar.Lo
            };
            EntryPrice = GetBestEntryPrice(Direction);
        }
    }
}
```

## See Also

- [Signal Base Classes](signal-base.md) — Node, Signal, LogicalNode reference
- [Signals Overview](overview.md) — all built-in signals
- Custom Signal sample — sample code (not yet available)
