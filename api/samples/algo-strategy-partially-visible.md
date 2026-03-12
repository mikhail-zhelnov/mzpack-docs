---
sidebar_position: 15
title: "Algo Strategy — Partially Visible"
description: "Algo.Strategy with TradesClusterSignal, DOMImbalanceSignal, absorption SR zones, and Partially Visible mode for indicators."
---

# Algo Strategy — Partially Visible

Demonstrates **Partially Visible** mode — when enabled, strategy indicators only render plots related to validated signals, keeping the chart uncluttered. The strategy combines `TradesClusterSignal` for trade clusters, a custom `AbsorptionSRZonesSignal` for absorption zones, and `DOMImbalanceSignal` as a filter.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/MZpackAlgoStrategy2.cs`
**Class:** `MZpackAlgoStrategy2 : MZpackStrategyBase`

## What It Covers

- Partially Visible mode on three indicator types
- `SignalPartiallyVisibleMode` enum usage
- Manual `PartiallyVisible` control on `IFootprintBar`
- `TradesClusterSignal` with cluster range and volume filters
- `DOMImbalanceSignal` as a filter in `FiltersTree`
- Custom signal with `Reset(resetView)` override
- Visibility state persistence to XML

## Architecture

```
MZpackAlgoStrategy2 : MZpackStrategyBase
 ├── StrategyBigTradeIndicator "Clusters"
 │    └── IsPartiallyVisible = true (default)
 ├── StrategyFootprintIndicator "Absorptions"
 │    └── IsPartiallyVisible = true (default)
 ├── StrategyMarketDepthIndicator "DOM Imbalance"
 │    └── Visible = true (always shown)
 └── Algo.Strategy
      └── Entry Pattern (AND root, short-circuit)
           ├── SignalsTree
           │    ├── OR LogicalNode
           │    │    ├── TradesClusterSignal "Ask Clusters" → Short
           │    │    └── TradesClusterSignal "Bid Clusters" → Long
           │    └── AbsorptionSRZonesSignal "Absorption" (optional)
           └── FiltersTree
                └── DOMImbalanceSignal (optional)
```

## Partially Visible Mode

### How It Works

Each strategy indicator has two visibility properties:

| Property | Description |
|---|---|
| `Visible` | Show/hide the indicator entirely |
| `IsPartiallyVisible` | When `true`, only show plots related to validated signals |

Toggle Partially Visible mode by clicking the "eye" button next to the indicator name on the chart.

### SignalPartiallyVisibleMode Enum

Signals control when their indicator plots become visible via the `PartiallyVisibleMode` property:

| Value | Description |
|---|---|
| `None` | Plots are not shown in Partially Visible mode |
| `OnSignalValidated` | Plots appear as soon as the signal validates |
| `OnPatternValidated` | Plots appear only after the entire pattern validates |

### Automatic Mode (TradesClusterSignal)

Built-in signals like `TradesClusterSignal` support `PartiallyVisibleMode` directly. Set it on the signal and the framework handles the rest:

```csharp
new TradesClusterSignal(Strategy, bigTradeIndicator, SignalDirection.Short)
{
    Name = "Ask Clusters",
    Side = TradeSide.Ask,
    Range = new Range()
    {
        Bars = BigTrade_ClusterBarRange,
        Ticks = BigTrade_ClusterPriceRangeTicks,
        Logic = Logic.And
    },
    MinVolume = BigTrade_MinTotalVolume,
    MinCount = BigTrade_MinTotalCount,
    VolumeCountLogic = Logic.And,
    PartiallyVisibleMode = SignalPartiallyVisibleMode.OnSignalValidated
}
```

### Manual Mode (AbsorptionSRZonesSignal)

For custom signals, control `PartiallyVisible` on individual data objects manually:

```csharp
class AbsorptionSRZonesSignal : Signal
{
    StrategyFootprintIndicator indicator;
    IFootprintBar bar;

    public AbsorptionSRZonesSignal(Strategy strategy,
        StrategyFootprintIndicator indicator)
        : base(strategy, MarketDataSource.Level1,
               SignalCalculate.OnBarClose, false)
    {
        this.indicator = indicator;
    }

    public override void OnCalculate(MarketDataEventArgs e, int barIdx,
        SignalDirection allowed)
    {
        IFootprintBar _bar;
        if (indicator.FootprintBars.TryGetValue(barIdx, out _bar))
        {
            int buyAbsCnt = _bar.AbsorptionSRZones.Zones[(int)TradeSide.Ask].Count;
            int sellAbsCnt = _bar.AbsorptionSRZones.Zones[(int)TradeSide.Bid].Count;

            SignalDirection dir;
            if (buyAbsCnt > 0 && sellAbsCnt == 0)
                dir = SignalDirection.Short;
            else if (sellAbsCnt > 0 && buyAbsCnt == 0)
                dir = SignalDirection.Long;
            else
                dir = SignalDirection.None;

            dir = Signal.ResolveDirection(dir, allowed);

            if (Signal.IsDetermined(dir))
            {
                Direction = dir;
                Time = e.Time;
                EntryPrice = e.Price;
                ChartRange = new ChartRange()
                {
                    MinBarIdx = barIdx, MaxBarIdx = barIdx,
                    Low = e.Price, High = e.Price
                };

                bar = _bar;
                // Show this footprint bar in Partially Visible mode
                bar.PartiallyVisible = true;
            }
        }
    }

    protected override void Reset(bool resetView)
    {
        base.Reset(resetView);

        if (bar != null)
        {
            // Hide on signal reset
            if (resetView)
                bar.PartiallyVisible = false;
            bar = null;
        }
    }
}
```

Key points:
- Set `bar.PartiallyVisible = true` in `OnCalculate` when the signal fires
- Set `bar.PartiallyVisible = false` in `Reset(resetView)` when `resetView` is `true`
- Alternatively, use `OnPatternValidated()` to show plots only after the full pattern validates

### Visibility Persistence

Save visibility state in `State.Terminated` so it persists across sessions:

```csharp
if (State == State.Terminated)
{
    if (bigTradeIndicator != null)
    {
        VisibleBigTradeIndicator = bigTradeIndicator.Visible;
        PartiallyVisibleBigTradeIndicator = bigTradeIndicator.IsPartiallyVisible;
    }
    // ... same for other indicators
}
```

## Indicator Configuration

### BigTrade (Clusters)

```csharp
bigTradeIndicator = new StrategyBigTradeIndicator(this, @"Clusters")
{
    FilterLogic = TradeFilterLogic.ALL,
    TradeFilterEnable = true,
    DomPressureFilterEnable = true,
    MarkerType = TradeMarkerType.Box,
    MarkerPosition = TradeMarkerPosition.POC,
    MaxShapeExtent = 10,
    ColorMode = ColorMode.Saturation,
    ShowTradePOC = true,
    VolumesPosition = VolumesPosition.OutsideRight
};
```

### Footprint (Absorptions Only)

```csharp
footPrintIndicator = new StrategyFootprintIndicator(this, @"Absorptions")
{
    LeftFootprintStyle = FootprintStyle.None,
    RightFootprintStyle = FootprintStyle.None,
    ShowAbsorptionSRZones = true,
    AbsorptionPercentage = 50,
    AbsorptionSRZonesConsecutiveLevels = 2,
    AbsorptionSRZonesVolumeFilter = 80,
    AbsoprtionSRZoneEnding = SRZoneEnding.ByBarClose,
    // Everything else disabled
};
```

### DOM Imbalance (Filter)

```csharp
domImbalanceIndicator = new StrategyMarketDepthIndicator(this, @"DOM Imbalance")
{
    ShowRealtimeOrderBook = false,
    ShowImbalance = true,
    ImbalancePercentage = Filters_DOMImbalance_Ratio * 100d - 100d
};
```

The `DOMImbalanceSignal` is added to `FiltersTree` with `IsReset = false` (holds state after validation):

```csharp
pattern.Filters.Root.AddChild(
    new DOMImbalanceSignal(Strategy, domImbalanceIndicator)
    {
        Name = "DOM Imbalance",
        IsReset = false,
        HasPrice = false,
        Ratio = Filters_DOMImbalance_Ratio
    });
```

## Configurable Properties

### Signals

| Property | Default | Description |
|---|---|---|
| `BigTrade_TradeMin` | `20` | Min trade volume |
| `BigTrade_TradeMax` | `200` | Max trade volume |
| `BigTrade_DomPressureMin` | `5` | Min DOM pressure |
| `BigTrade_ClusterBarRange` | `3` | Cluster bar range |
| `BigTrade_ClusterPriceRangeTicks` | `6` | Cluster price range in ticks |
| `BigTrade_MinTotalVolume` | `50` | Min total cluster volume |
| `BigTrade_MinTotalCount` | `3` | Min trades in cluster |
| `BigTrade_EnableAggression` | `false` | Enable aggression filter |
| `BigTrade_MinAggression` | `1` | Min aggression value |
| `Footprint_EnableAbsorption` | `false` | Enable absorption signal |

### Filters

| Property | Default | Description |
|---|---|---|
| `Filters_DOMImbalance` | `true` | Enable DOM imbalance filter |
| `Filters_DOMImbalance_Ratio` | `1.2` | DOM imbalance ratio (1.2 = 20%) |

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

### Visual

| Property | Default | Description |
|---|---|---|
| `VisibleBigTradeIndicator` | `false` | Show clusters indicator |
| `PartiallyVisibleBigTradeIndicator` | `true` | Partially visible for clusters |
| `VisibleFootPrintIndicator` | `false` | Show absorptions indicator |
| `PartiallyVisibleFootPrintIndicator` | `true` | Partially visible for absorptions |
| `VisibleDomImbalanceIndicator` | `true` | Show DOM imbalance indicator |
| `PartiallyVisibleDomImbalanceIndicator` | `false` | Partially visible for DOM |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Signal Base Classes](../strategies/signals/signal-base.md) — `PartiallyVisibleMode` property
- [Filter](../strategies/filter.md) — filter in decision tree
- [Custom Signal](../strategies/signals/custom-signal.md) — creating your own signal
