---
sidebar_position: 18
title: "Custom Strategy — BigTrade + VolumeProfile"
description: "StrategyBigTradeIndicator with StrategyVolumeProfileIndicator in Custom mode for backtesting"
---

# Custom Strategy — BigTrade + VolumeProfile

Demonstrates `StrategyBigTradeIndicator` with `StrategyVolumeProfileIndicator` in Custom mode for backtesting (OnBarClose). This is a custom strategy without Algo.Strategy — it uses NinjaTrader `EnterLong`/`EnterShort` directly.

**Source:** `[INSTALL PATH]/API/Samples/MZpackCustomStrategy1.cs`
**Class:** `MZpackCustomStrategy1 : MZpackStrategyBase`

## What It Covers

- `StrategyVolumeProfileIndicator` with `ProfileCreation.Custom` (manual profiles)
- `StrategyBigTradeIndicator` with aggression filter
- Strategy logic: create developing profile when bar range >= threshold, close profile and enter when bar range drops below min or exceeds max
- Entry direction based on profile delta vs big trade delta divergence
- `EnableBacktesting = true`

## Indicator Setup

```csharp
volumeProfileIndicator = new StrategyVolumeProfileIndicator(this, @"Custom VP")
{
    ProfileCreation = ProfileCreation.Custom,
    ProfileMode = ProfileMode.BuySell,
    StackedProfileCreation1 = ProfileCreation.Sessions,
    StackedProfileCreation2 = ProfileCreation.None,
    StackedProfileCreation3 = ProfileCreation.None
};

bigTradeIndicator = new StrategyBigTradeIndicator(this, @"Aggressive Trades")
{
    FilterLogic = TradeFilterLogic.ANY,
    MarkerType = TradeMarkerType.Bar,
    UseBigTradeAlert = false
};
```

## Strategy Logic

The `OnBarCloseHandler` creates a developing volume profile when bar range is large enough, then closes the profile and enters a position when the bar range drops or the profile grows too wide. Entry direction is determined by divergence between profile delta and big trade delta.

```csharp
protected void StrategyOnBarCloseHandler(MarketDataEventArgs e, int currentBarIdx)
{
    int barRange = 0;
    if (Bars.Count > 1)
        barRange = (int)((High[1] - Low[1]) / TickSize);

    // Create new profile when bar range is large enough
    if (profile == null && barRange >= Strategy_StartProfileMinBarRange)
    {
        // Exit existing positions...
        profile = volumeProfileIndicator.AddProfile();
        profile.AssignRange(currentBarIdx, currentBarIdx + 1);
        profile.IsDeveloping = true;
    }
    else
    // Close profile and enter position
    if (profile != null && (barRange <= Strategy_KeepProfileMinBarRange
        || profile.RangeTicks >= Strategy_KeepProfileMaxBarRange))
    {
        // Calculate big trades delta inside profile
        long bigTradeDelta = 0;
        List<ITrade> trades = bigTradeIndicator.Trades
            .Where(t => t.StartBarIdx >= profile.BeginBarIdx
                && t.StartBarIdx <= profile.EndBarIdx).ToList();

        foreach (ITrade trade in trades)
        {
            if (trade.Side == TradeSide.Bid)
                bigTradeDelta -= trade.Volume;
            else if (trade.Side == TradeSide.Ask)
                bigTradeDelta += trade.Volume;
        }

        // SHORT if profile Delta < 0 and bigTradeDelta > 0
        if (profile.Delta < 0 && bigTradeDelta > 0)
        {
            signalShort = string.Format("VP delta:{0}, T delta:{1}",
                profile.Delta, bigTradeDelta);
            SetProfitTarget(signalShort, CalculationMode.Ticks, Strategy_TakeProfitTicks);
            SetStopLoss(signalShort, CalculationMode.Ticks, Strategy_StopLossTicks, false);
            EnterShort(signalShort);
        }
        // LONG if profile Delta > 0 and bigTradeDelta < 0
        else if (profile.Delta > 0 && bigTradeDelta < 0)
        {
            signalLong = string.Format("VP delta:{0}, T delta:{1}",
                profile.Delta, bigTradeDelta);
            SetProfitTarget(signalLong, CalculationMode.Ticks, Strategy_TakeProfitTicks);
            SetStopLoss(signalLong, CalculationMode.Ticks, Strategy_StopLossTicks, false);
            EnterLong(signalLong);
        }

        profile.IsDeveloping = false;
        profile = null;
    }
}
```

## Configurable Properties

### Strategy

| Property | Default | Description |
|---|---|---|
| `Strategy_TakeProfitTicks` | `96` | Take profit ticks |
| `Strategy_StopLossTicks` | `32` | Stop loss ticks |

### Filtering

| Property | Default | Description |
|---|---|---|
| `Strategy_StackedProfileType` | `VP` | Stacked profile type |
| `Strategy_StartProfileMinBarRange` | `12` | Min bar range to create profile |
| `Strategy_KeepProfileMinBarRange` | `5` | Min bar range to keep profile |
| `Strategy_KeepProfileMaxBarRange` | `30` | Max profile range in ticks |
| `Strategy_TradeVolume` | `100` | Trade volume filter |
| `Strategy_AggressionFilter` | `2` | Aggression/sweep filter in ticks |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzVolumeProfile](data-access-volume-profile.md) — volume profile data
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
