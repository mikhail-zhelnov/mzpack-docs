---
sidebar_position: 1
title: "IDeltaDivergenceIndicator"
description: "Reference for the IDeltaDivergenceIndicator interface — access to ZigZag breakpoints, divergence signals, and deviation filters."
---

# IDeltaDivergenceIndicator

`IDeltaDivergenceIndicator` provides programmatic access to the [mzDeltaDivergence](/docs/indicators/mzDeltaDivergence) chart indicator. It extends [IVolumeDeltaIndicator](../volume-delta/ivolume-delta-indicator.md) and adds divergence detection between price swings and cumulative delta.

**Namespace:** `MZpack`
**Inheritance:** `IDeltaDivergenceIndicator : IVolumeDeltaIndicator : IOrderFlowIndicator : ITickIndicator : IIndicator`
**Conditional:** `#if !FREE`
**Source:** `MZpackBase/mzDeltaDivergence/IDeltaDivergenceIndicator.cs`

## Key Data Properties

| Property | Type | Description |
|---|---|---|
| `Divergences` | `Divergences` | Collection of detected divergences (`#if DATA`) |

## ZigZag Configuration

| Property | Type | Description |
|---|---|---|
| `ZigzagDeviationType` | `DeviationType` | Value or Percentage |
| `ZigzagDeviationThreshold` | `double` | Minimum deviation to form a new swing point |
| `ZigzagUseHighLow` | `bool` | Use High/Low instead of Close for swing detection |

## Price Deviation Filter

| Property | Type | Description |
|---|---|---|
| `PriceDeviationType` | `DeviationType` | Value or Percentage |
| `PriceDeviationMin` | `double` | Minimum price change between swing points |
| `PriceDeviationMax` | `double` | Maximum price change between swing points |

## Delta Deviation Filter

| Property | Type | Description |
|---|---|---|
| `DeltaDeviationType` | `DeviationType` | Value or Percentage |
| `DeltaDeviationMin` | `double` | Minimum delta change between swing points |
| `DeltaDeviationMax` | `double` | Maximum delta change between swing points |

## Filter Logic and Display

| Property | Type | Description |
|---|---|---|
| `DivergenceFiltersLogic` | `DivergenceFiltersLogic` | How filters are combined |
| `DeviationStatisticsShow` | `bool` | Show deviation statistics on chart |
| `BreakPointShow` | `bool` | Show ZigZag breakpoints |
| `BuySellAreasShow` | `bool` | Show buy/sell divergence areas |
| `UseDivergenceAlert` | `bool` | Enable divergence alert |
| `DivergenceAlertSound` | `string` | Alert sound file |

## IDivergence

Each detected divergence is represented by the `IDivergence` interface:

| Property/Method | Type | Description |
|---|---|---|
| `a` | `BreakPoint` | First swing point |
| `b` | `BreakPoint` | Second swing point |
| `Indicator` | `IDeltaDivergenceIndicator` | Parent indicator |
| `IsBuy()` | `bool` | Bullish divergence (lower price, higher delta) |
| `IsSell()` | `bool` | Bearish divergence (higher price, lower delta) |
| `GetDeltaChange(DeviationType)` | `double` | Delta change between points |
| `GetPriceChange(DeviationType)` | `double` | Price change between points |
| `GetStatisticsText()` | `string` | Formatted statistics string |

## Example: Read Divergences

```csharp
IDeltaDivergenceIndicator ddIndicator = ...;

Divergences divergences = ddIndicator.Divergences;
if (divergences == null) return;

// Iterate detected divergences
foreach (IDivergence div in divergences)
{
    if (div.IsBuy())
    {
        // Bullish divergence: price made lower low, delta made higher low
        double priceChange = div.GetPriceChange(DeviationType.Value);
        double deltaChange = div.GetDeltaChange(DeviationType.Value);
    }
    else if (div.IsSell())
    {
        // Bearish divergence: price made higher high, delta made lower high
    }
}
```

## See Also

- [IVolumeDeltaIndicator](../volume-delta/ivolume-delta-indicator.md) — parent interface
- [StrategyDeltaDivergenceIndicator](strategy-dd-indicator.md) — strategy wrapper class
