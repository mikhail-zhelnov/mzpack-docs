---
sidebar_position: 4
title: "Indicator Capabilities"
description: "Declare the indicator data a custom signal needs so MZpack enables its calculation automatically."
---

# Indicator Capabilities

Some indicator values are calculated only when their corresponding feature is enabled. A custom `Signal` declares the data it reads with `Require()`; when `Algo.Strategy.Initialize()` finishes, MZpack collects requirements from all tree and probe signals and enables the required indicator calculations.

Requirements are per indicator instance, not per indicator type. A strategy with two footprint instances can therefore request absorptions from one without changing the other. Capability application is monotonic: MZpack enables what the signal needs but never turns off a setting enabled in the indicator template.

## Declaring a Requirement

Override `DeclareRequirements()` in the signal. It runs after the framework has resolved the signal's indicator references.

```csharp
public class MyAbsorptionSignal : Signal
{
    readonly StrategyFootprintIndicator footprint;

    public MyAbsorptionSignal(Strategy strategy, StrategyFootprintIndicator footprint)
        : base(strategy, MarketDataSource.Level1, SignalCalculate.OnBarClose, true)
    {
        this.footprint = footprint;
    }

    public override void DeclareRequirements()
    {
        Require(footprint, FootprintCapabilities.Absorptions);
    }
}
```

Declare the data that the signal reads, not a UI setting. Do not declare a capability for data calculated unconditionally, such as footprint bar delta, volume, POC, min/max delta, per-level rows, or session POCs.

## Capability Enums

### `FootprintCapabilities`

| Value | Makes available |
|---|---|
| `Imbalances` | Per-level imbalance rows |
| `ImbalanceSRZones` | Imbalance support/resistance zones |
| `Absorptions` | Bar absorption data |
| `AbsorptionSRZones` | Absorption support/resistance zones; also enables `Absorptions` |
| `BarValueArea` | Bar VAH and VAL |
| `BarMultiplePOC` | Multiple POC data; raises the POC-count setting to at least 2 |
| `UnfinishedAuction` | Unfinished auction high and low |
| `RatioNumbers` | Ratio-number data |
| `AbsoluteDeltaAverage` | Absolute-delta average |
| `DeltaRate` | Delta rate, high and low |
| `DeltaDivergence` | Buy and sell delta-divergence flags |
| `SessionValueArea` | Session VAH and VAL |

### `VolumeProfileCapabilities`

| Value | Makes available |
|---|---|
| `ProfileVWAP` | Profile VWAP |
| `ProfileVWAPDeviation` | VWAP standard-deviation bands; also enables `ProfileVWAP` |

If a signal requires deviation and the indicator's VWAP mode is `None` or `Dynamic`, MZpack selects a dynamic standard-deviation mode. A `Last` VWAP mode is left unchanged because it has different semantics; MZpack reports that the required deviation is unavailable.

### `MarketDepthCapabilities`

| Value | Makes available |
|---|---|
| `OverallLiquidity` | Per-bar overall liquidity |
| `LiquidityMigration` | Per-bar liquidity migration |

The realtime order book itself is always maintained and needs no capability.

### `BigTradeCapabilities`

| Value | Makes available |
|---|---|
| `Icebergs` | Iceberg detection |
| `Aggression` | Aggression detection |

`VolumeDeltaCapabilities` currently contains only `None`: its public signal data is not gated by an indicator setting. The same applies to data exposed through the derived Delta Divergence indicator.

## Built-in Signal Requirements

Built-in signals declare their own requirements. For example, `Hammer w Absorption` requests footprint absorptions, `Stacked Imbalances` requests imbalance S/R zones, and `Delta Trap` requests bar value-area data. No separate footprint-template switch is needed for those signals to calculate their required data.

## See Also

- [Signal Base Classes](signals/signal-base.md) — implementing a custom signal
- [Algo.Strategy](algo-strategy.md) — initialization and probe signal factories
- [Signal Probe](signal-probe.md) — probes also contribute requirements
