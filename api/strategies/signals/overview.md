---
sidebar_position: 1
title: "Signals Overview"
description: "Overview of the MZpack signal system — built-in signals, decision tree nodes, and how signals drive strategy patterns."
---

# Signals Overview

Signals are the building blocks of MZpack strategy patterns. Each signal evaluates a market condition and returns a direction (`Long`, `Short`, or `None`). Signals are organized into decision trees where `AND`, `OR`, and `CONJUNCTION` logic combines them into pattern validation rules.

## Node Hierarchy

```
Node (abstract)
├── Signal                          ← market condition evaluator
│   ├── Action                      ← simplified signal (no range constraints)
│   │   └── RollingProfileAction    ← rolling volume profile generation
│   └── [21 built-in signals]
├── LogicalNode                     ← AND / OR / CONJUNCTION logic
└── RangeNode                       ← bar/tick range constraint
    └── Range                       ← concrete range implementation
```

## Two Ways to Use Signals

### 1. In a Decision Tree (Pattern Condition)

Signals are added to a pattern's `SignalsTree` or `FiltersTree`. The tree evaluates all signals on each market event and validates the pattern when the tree resolves to a determined direction.

```csharp
var pattern = new Pattern(strategy, Logic.And, new Range(), true);
pattern.Signals.Root.Add(new FootprintImbalanceSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnEachTick));
pattern.Signals.Root.Add(new BarDeltaSignal(strategy,
    MarketDataSource.Level1, SignalCalculate.OnBarClose));
```

### 2. As an Action

`Action` is a simplified `Signal` subclass used for preparatory operations (like generating a rolling volume profile) before other signals evaluate. Actions have no range constraints and don't expire.

## Built-in Signals by Data Source

### Footprint Signals

| Signal | Condition | Calculate |
|---|---|---|
| [FootprintImbalanceSignal](footprint/footprint-imbalance-signal.md) | Stacked buy/sell imbalances in footprint bar | OnEachTick |
| [FootprintAbsorptionSignal](footprint/footprint-absorption-signal.md) | Passive absorption at price extremes | OnEachTick |
| [FootprintSRZonesSignal](footprint/footprint-sr-zones-signal.md) | Active imbalance/absorption S/R zones | OnEachTick |
| [ClusterZonesSignal](footprint/cluster-zones-signal.md) | Consecutive cluster zones in footprint | OnBarClose |

### Volume Profile Signals

| Signal | Condition | Calculate |
|---|---|---|
| [RelativeToProfileSignal](volume-profile/relative-to-profile-signal.md) | Price position relative to VWAP, VAH/VAL, or StdDev | OnBarClose |
| [VolumeProfileDeltaSignal](volume-profile/volume-profile-delta-signal.md) | Profile delta direction with volume/range filters | OnBarClose |
| [BarJoinedPOCsSignal](volume-profile/bar-joined-pocs-signal.md) | Consecutive joined POCs within a bar | OnEachTick |

### Volume Delta Signals

| Signal | Condition | Calculate |
|---|---|---|
| [BarDeltaSignal](volume-delta/bar-delta-signal.md) | Bar delta direction with minimum threshold | OnBarClose |
| [CumulativeDeltaSignal](volume-delta/cumulative-delta-signal.md) | Session cumulative delta direction | OnBarClose |
| [DeltaRateSignal](volume-delta/delta-rate-signal.md) | Delta rate of change with threshold | OnBarClose |
| [BarIcebergsSignal](volume-delta/bar-icebergs-signal.md) | Iceberg detection by volume threshold | OnEachTick |

### Big Trade Signals

| Signal | Condition | Calculate |
|---|---|---|
| [BigTradeSignal](big-trade/big-trade-signal.md) | Large trade detection (opposite side = signal) | OnEachTick |
| [TradesClusterSignal](big-trade/trades-cluster-signal.md) | Cluster of trades by volume, count, and range | OnEachTick |

### Market Depth Signals (Level 2)

| Signal | Condition | Calculate |
|---|---|---|
| [DOMImbalanceSignal](market-depth/dom-imbalance-signal.md) | Bid/ask ratio imbalance in order book | NotApplicable |
| [DOMBlockSignal](market-depth/dom-block-signal.md) | Persistent large order in DOM | NotApplicable |

### Delta Divergence Signals

| Signal | Condition | Calculate |
|---|---|---|
| [DeltaDivergenceSignal](delta-divergence/delta-divergence-signal.md) | Price/delta divergence at swing points | OnBarClose |

### Bar-Based Signals

| Signal | Condition | Calculate |
|---|---|---|
| [BarVolumeSignal](bar/bar-volume-signal.md) | Bar volume exceeds threshold (filter) | OnBarClose |
| [BarWickSignal](bar/bar-wicks-signal.md) | Wick size at bar extreme | OnBarClose |
| [BarMetricsSignal](bar/bar-metrics-signal.md) | Bar body/size/wick metrics | OnBarClose |
| [OrderflowBarMetricsSignal](bar/orderflow-bar-metrics-signal.md) | Orderflow bar metrics (volume, delta, delta%) | OnBarClose |
| [UpDownBarSignal](bar/up-down-bar-signal.md) | Bullish or bearish bar direction | OnBarClose |
| [TradesClusterSignal](big-trade/trades-cluster-signal.md) | Cluster of trades matching criteria | OnEachTick |

## Creating Custom Signals

Extend the `Signal` base class to create your own signal. See [Custom Signal](custom-signal.md) for a step-by-step guide.

## See Also

- [Signal Base Classes](signal-base.md) — Node, Signal, LogicalNode, RangeNode
- [Decision Tree](../decision-tree.md) — how signals combine in patterns
