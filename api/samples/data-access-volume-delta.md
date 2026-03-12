---
sidebar_position: 7
title: "Data Access — mzVolumeDelta"
description: "Access StrategyVolumeDeltaIndicator data — volume, delta, cumulative delta, iceberg volume, and trade side breakdown."
---

# Data Access — mzVolumeDelta

Demonstrates how to access volume delta bar data from `StrategyVolumeDeltaIndicator`. The `OnBarCloseHandler` prints volume, delta, cumulative delta, and iceberg volume for each bar.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/DataAccess_mzVolumeDelta.cs`
**Class:** `DataAccess_mzVolumeDelta : MZpackStrategyBase`

## Indicator Setup

```csharp
volumeDeltaIndicator = new StrategyVolumeDeltaIndicator(this, @"Volume Delta")
{
    VolumeDeltaMode = VolumeDeltaMode.Delta,
    DeltaMode = DeltaMode.Cumulative,
    TradeFilterMin = 0,
    TradeFilterMax = 10,
    ZeroLine = true
};
```

Apply UI property overrides in `State.Configure`:

```csharp
else if (State == State.Configure)
{
    volumeDeltaIndicator.TradeFilterMin = TradeFilterMin;
    volumeDeltaIndicator.TradeFilterMax = TradeFilterMax;
}
```

## Accessing IVolumeDeltaBar

```csharp
void StrategyOnBarCloseHandler(MarketDataEventArgs e, int currentBarIdx)
{
    if (volumeDeltaIndicator.VolumeDeltaBars.ContainsKey(currentBarIdx))
    {
        IVolumeDeltaBar bar = volumeDeltaIndicator.VolumeDeltaBars[currentBarIdx];
        // ...
    }
}
```

### Available Data

```csharp
// Volume (use FromInternalVolume() for crypto)
volumeDeltaIndicator.FromInternalVolume(bar.Volume)  // Total volume
bar.VolumeBySide(TradeSide.Bid)     // Sell volume
bar.VolumeBySide(TradeSide.Ask)     // Buy volume

// Iceberg volume
bar.IcebergVolume                          // Total iceberg volume
bar.IcebergVolumeBySide(TradeSide.Bid)     // Iceberg on bid
bar.IcebergVolumeBySide(TradeSide.Ask)     // Iceberg on ask

// Delta
bar.Delta               // Bar delta
bar.OpenDelta           // Open delta (cumulative delta of previous bar)
bar.CumulativeDelta     // Cumulative delta of this bar
bar.DeltaHi             // Max delta within bar
bar.DeltaLo             // Min delta within bar

// Cumulative extremes
bar.DeltaHi + bar.OpenDelta    // Max cumulative delta in bar
bar.DeltaLo + bar.OpenDelta    // Min cumulative delta in bar
```

## Properties

| Property | Default | Description |
|---|---|---|
| `TradeFilterMin` | `0` | Minimum trade size filter |
| `TradeFilterMax` | `-1` | Maximum trade size filter (-1 = no limit) |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzFootprint](data-access-footprint.md) — footprint data
- [Data Access — mzVolumeProfile](data-access-volume-profile.md) — volume profile data
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
