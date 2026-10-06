---
sidebar_position: 5
title: "Signal Probe"
description: "API reference for SignalProbe — independently observe signal events and their first-touch outcomes."
---

# Signal Probe

`SignalProbe` evaluates its own signal instances independently of a pattern's decision tree. It records signal events and first-touch price outcomes, but never validates a pattern or opens a position. Use it when a strategy needs to measure signals that are disabled for trading, or to collect statistics without allowing probe evaluation to affect the trading path.

**Namespace:** `MZpack.NT8.Algo`  
**Source:** `[INSTALL PATH]/API/SignalProbe.cs`

## Creating a Probe

Pass signal factories to an `Algo.Strategy.Initialize()` overload. Factories are required because a probe must own fresh signal instances: tree signals have mutable evaluation state and cannot safely be evaluated by both paths.

```csharp
strategy.Initialize(
    entryPattern,
    exitPattern,
    new[] { entry },
    attempts: 1,
    entryProbeSignals: new Func<Signal>[]
    {
        () => new MySignal(strategy, footprint),
        () => new AnotherSignal(strategy, footprint)
    });
```

The resulting probes are available through `strategy.SignalProbes`. A probe marks each event with `IsInTree`, so the same journal can distinguish signals that trade from signals observed only for research.

## Configuration

Configure a new probe in `MZpackStrategyBase.OnConfigureSignalProbe()`:

```csharp
protected internal override void OnConfigureSignalProbe(SignalProbe probe)
{
    probe.HorizonBars = 40;
    probe.LadderTicks = 100;
}
```

| Property | Default | Description |
|---|---:|---|
| `HorizonBars` | 40 | Number of bars for which an event's outcome remains open. Observation closes at the session boundary or end of data if it comes first |
| `LadderTicks` | 0 | First-touch reach on each side of the entry price. `0` lets the host choose a derived reach |
| `BeforePass` | `null` | Optional callback immediately before all probe signals are evaluated |
| `CanRecord` | `null` | Optional per-event gate. A rejected firing increments `SkippedCount` but does not create an event |
| `VolumeRankOf` / `DeltaRankOf` | `null` | Optional host-provided percentile ranks written into each firing |

Use `OnBeforeSignalProbePass()` rather than a signal to refresh shared state that probe signals would otherwise update first. `SignalProbe` does not know a host's calibration or other strategy-specific state.

## Results

| Member | Description |
|---|---|
| `Events` | Captured `ProbeEvent` items in chronological order |
| `Outcomes` | First-touch outcomes corresponding to the events |
| `Diagnostics` | Human-readable capture summary |
| `SkippedCount` | Number of signal firings rejected by `CanRecord` |
| `FirstRecordedSession` | First session that produced a recorded event |
| `ResolvedLadderTicks` / `ResolvedLadderStep` / `ResolvedLadderLevels` | Effective first-touch ladder after the probe resolves the requested reach |
| `CloseOpenOutcomes()` | Close all events still open at end of data or strategy lifetime |

A `ProbeEvent` records signal name, direction, price, time, bar index, tree membership, market context, and optional `VolumeRank` / `DeltaRank`. Its `ProbeOutcome` records first-touch times and bars for favourable and adverse ladder levels, MFE, MAE, `BarsToMFE`, `FirstTickPrice`, and the price at the observation horizon.

## Capabilities

Probe signals participate in the same capability collection as tree signals. Their `DeclareRequirements()` calls are included when `Algo.Strategy.Initialize()` calls `ApplyRequiredCapabilities()`. This is important for observed-only signals: a signal disabled for trading can still request the indicator data it needs to be measured.

## See Also

- [Algo.Strategy](algo-strategy.md) — `Initialize()` overloads and `SignalProbes`
- [MZpackStrategyBase](mzpack-strategy-base.md) — probe configuration hooks
- [Indicator Capabilities](indicator-capabilities.md) — declaring indicator data requirements
