---
sidebar_position: 14
title: "Algo Strategy — Patterns + ATM"
description: "Patterns with ATM, BigTradeSignal, EMASignal, and DOMImbalanceFilter (Level 2, live/replay)"
---

# Algo Strategy — Patterns + ATM

Demonstrates a pattern-based Algo.Strategy that combines custom `BigTradeSignal`, `EMASignal`, and `DOMImbalanceFilter`. Requires Level 2 data (live or replay only). Uses dual entries with independent stop/target settings and limit order support with cancel-after-bars logic.

**Source:** `[INSTALL PATH]/API/Samples/Built-in/MZpackAlgoStrategy1.cs` (uses `AlgoStrategy1.cs`)
**Class:** `MZpackAlgoStrategy1 : MZpackStrategyBase`

## What It Covers

- Custom `AlgoStrategy1` subclass with `OnPositionOpenFilter` (no entries on stop-loss bar)
- Three indicators: `StrategyBigTradeIndicator`, EMA, `StrategyMarketDepthIndicator`
- Two custom signals: `BigTradeSignal` (Level 1, OnEachTick) and `EMASignal` (Level 1, OnEachTick)
- Custom `DOMImbalanceFilter` (Level 2, OnEachTick)
- Pattern with AND root, `Range {Bars=1}` for signals, `Range {Bars=5}` for filters
- Dual entries with independent stop/target, trail on entry 2
- Limit order support with cancel-after-bars logic
- `OnEachTickHandler` for pending limit order cancellation

## Architecture

```
MZpackAlgoStrategy1 : MZpackStrategyBase
 ├── StrategyBigTradeIndicator "Big Trade"
 ├── EMA indicator
 ├── StrategyMarketDepthIndicator "Market Depth"
 └── AlgoStrategy1 : Algo.Strategy
      └── Entry Pattern (AND root, short-circuit)
           ├── SignalsTree (AND, range: 1 bar)
           │    ├── BigTradeSignal "Big Trade"
           │    └── EMASignal "EMA"
           └── FiltersTree (AND, range: 5 bars)
                └── DOMImbalanceFilter (optional)
```

## Custom Strategy Subclass

`AlgoStrategy1` prevents entries on the same bar as a stop loss and tracks stop-loss bar index:

```csharp
public class AlgoStrategy1 : MZpack.NT8.Algo.Strategy
{
    int stopLossBarIdx = -1;

    public override bool OnPositionOpenFilter(DateTime time)
    {
        if ((Pattern.Direction == ((MZpackAlgoStrategy1)MZpackStrategy).Position_Direction
            || ((MZpackAlgoStrategy1)MZpackStrategy).Position_Direction == SignalDirection.Any)
            && MZpackStrategy.CurrentBar > stopLossBarIdx)
        {
            stopLossBarIdx = -1;
            return true;
        }
        return false;
    }

    public override void OnOrderUpdate(Order order, OrderState orderState)
    {
        base.OnOrderUpdate(order, orderState);
        Entry e;
        if (orderState == OrderState.Filled && Positions.IsStoplossOrder(order, out e))
            stopLossBarIdx = MZpackStrategy.CurrentBar;
    }
}
```

## BigTradeSignal

Custom signal based on `ReconstructedTrades`. Fires when a trade meets volume, iceberg, and DOM pressure thresholds. Calculates entry price with a configurable shift from the trade price:

```csharp
class BigTradeSignal : Signal
{
    ITrade lastTrade;

    public BigTradeSignal(MZpack.NT8.Algo.Strategy strategy)
        : base(strategy, MarketDataSource.Level1, SignalCalculate.OnEachTick, false) { }

    public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
    {
        MZpackAlgoStrategy1 __strategy = ((MZpackAlgoStrategy1)Strategy.MZpackStrategy);
        if (__strategy.BigTradeIndicator.ReconstructedTrades.Count > 0)
        {
            ITrade trade = __strategy.BigTradeIndicator.ReconstructedTrades[
                __strategy.BigTradeIndicator.ReconstructedTrades.Count - 1];

            if (lastTrade == null || lastTrade.Id != trade.Id)
            {
                if (trade.Volume >= __strategy.BigTrade_TradeVolume
                    && trade.IcebergVolume >= __strategy.BigTrade_IcebergVolume
                    && trade.DomPressureVolume >= __strategy.BigTrade_DomPressureVolume)
                {
                    Direction = trade.Side == TradeSide.Bid
                        ? SignalDirection.Long : SignalDirection.Short;
                    ChartRange = new ChartRange()
                    { MinBarIdx = trade.StartBarIdx, MaxBarIdx = trade.StopBarIdx };
                    EntryPrice = __strategy.Instrument.MasterInstrument.RoundToTickSize(
                        Direction == SignalDirection.Long
                            ? trade.StopPrice + Math.Min(
                                __strategy.Signals_EntryShiftTicks * __strategy.TickSize,
                                __strategy.GetCurrentBid())
                            : trade.StopPrice - Math.Min(
                                __strategy.Signals_EntryShiftTicks * __strategy.TickSize,
                                __strategy.GetCurrentAsk()));
                }
                lastTrade = trade;
            }
        }
    }
}
```

## EMASignal

Fires when price is above or below the EMA, matching the allowed direction:

```csharp
class EMASignal : Signal
{
    public EMASignal(MZpack.NT8.Algo.Strategy strategy)
        : base(strategy, MarketDataSource.Level1, SignalCalculate.OnEachTick, false) { }

    public override void OnCalculate(MarketDataEventArgs e, int barIdx, SignalDirection allowed)
    {
        double ema = ((MZpackAlgoStrategy1)Strategy.MZpackStrategy).EMAIndicator.Values[0][barIdx];
        if ((e.Price > ema && Signal.IsShortAllowed(allowed)) ||
            (e.Price < ema && Signal.IsLongAllowed(allowed)))
        {
            Direction = allowed;
            ChartRange = new ChartRange() { MinBarIdx = barIdx, MaxBarIdx = barIdx };
            Time = e.Time;
        }
    }
}
```

## DOMImbalanceFilter

Level 2 filter that compares total offer vs. total bid volume in the order book:

```csharp
class DOMImbalanceFilter : Signal
{
    double ratio;

    public DOMImbalanceFilter(MZpack.NT8.Algo.Strategy strategy, double ratio)
        : base(strategy, MarketDataSource.Level2, SignalCalculate.OnEachTick, false)
    {
        this.ratio = ratio;
    }

    public override void OnCalculate(MarketDepthEventArgs e, int barIdx, SignalDirection allowed)
    {
        MZpackAlgoStrategy1 __strategy = ((MZpackAlgoStrategy1)Strategy.MZpackStrategy);
        if (barIdx > -1 && Signal.IsDetermined(allowed))
        {
            long totalOffer = __strategy.DOMImbalanceIndicator
                .RealtimeOrderBook.GetVolume(TradeSide.Ask);
            long totalBid = __strategy.DOMImbalanceIndicator
                .RealtimeOrderBook.GetVolume(TradeSide.Bid);
            double offerBidRatio = (double)totalOffer / totalBid;
            double bidOfferRatio = (double)totalBid / totalOffer;

            if ((Signal.IsShortAllowed(allowed) && offerBidRatio >= ratio) ||
                (Signal.IsLongAllowed(allowed) && bidOfferRatio >= ratio))
            {
                Direction = allowed;
                ChartRange = new ChartRange() { MinBarIdx = barIdx, MaxBarIdx = barIdx };
                Time = e.Time;
            }
        }
    }
}
```

## Pending Limit Cancellation

`OnEachTickHandler` cancels pending limit orders after a configurable number of bars:

```csharp
protected void StrategyOnEachTickHandler(MarketDataEventArgs e, int currentBarIdx)
{
    lock (Sync)
    {
        if (pendingLimitBarIdx > 0
            && currentBarIdx - pendingLimitBarIdx > Common_CancelLimitAfterBars
            && Strategy.Positions.HasPendingLimitOrders())
        {
            Strategy.Patterns.Reset(SignalsTree.MARKETDATASOURCES_LEVEL1);
            Strategy.Positions.CancelPendingEntries(
                "Cancelled by overpassed bars count", e.Time);
            pendingLimitBarIdx = -1;
        }
    }
}
```

## Configurable Properties

### Common

| Property | Default | Description |
|---|---|---|
| `Common_EntryMethod` | `Limit` | Order type (Market/Limit) |
| `Common_CancelLimitAfterBars` | `10` | Cancel pending limit after N bars |
| `Common_OppositePatternAction` | `Reverse` | Action on opposite signal |

### Position

| Property | Default | Description |
|---|---|---|
| `Position_Direction` | `Any` | Allowed direction |
| `Position_Quantity1` | `2` | Entry 1 contracts |
| `Position_Quantity2` | `1` | Entry 2 contracts (0 = disabled) |
| `Position_StopLoss1` | `18` | Entry 1 stop loss ticks |
| `Position_StopLoss2` | `20` | Entry 2 stop loss ticks |
| `Position_ProfitTarget1` | `35` | Entry 1 profit target ticks |
| `Position_ProfitTarget2` | `70` | Entry 2 profit target ticks |
| `Position_IsBE` | `false` | Enable breakeven |
| `Position_BEAfterTicks` | `20` | Ticks before breakeven |
| `Position_BEShiftTicks` | `5` | Breakeven shift ticks |
| `Position_IsTrail` | `true` | Enable trailing on entry 2 |
| `Position_TrailAfter` | `15` | Trail activation ticks |
| `Position_TrailDistance` | `10` | Trail distance ticks |
| `Position_TrailStep` | `2` | Trail step ticks |

### Signals

| Property | Default | Description |
|---|---|---|
| `BigTrade_TradeVolume` | `300` | Trade volume filter |
| `BigTrade_IcebergVolume` | `0` | Iceberg volume filter |
| `BigTrade_IcebergAlgo` | `Soft` | Iceberg detection algorithm |
| `BigTrade_DomPressureVolume` | `20` | DOM pressure filter |
| `EMA_Period` | `14` | EMA period |
| `Signals_EntryShiftTicks` | `-2` | Entry price shift from trade price |

### Filters

| Property | Default | Description |
|---|---|---|
| `Filters_DOMImbalance` | `true` | Enable DOM imbalance filter |
| `Filters_DOMImbalance_Ratio` | `1.4` | DOM bid/ask imbalance ratio |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Algo.Strategy](../strategies/algo-strategy.md) — strategy framework
- [Pattern](../strategies/pattern.md) — pattern configuration
- [Entry](../strategies/entry.md) — entry configuration
- [Custom Signal](../strategies/signals/custom-signal.md) — creating your own signal
- [Filter](../strategies/filter.md) — filter in decision tree
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
