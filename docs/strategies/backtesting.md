---
sidebar_position: 4
title: "Backtesting"
description: "Backtest MZpack strategies in NinjaTrader 8 — Strategy Analyzer with Tick Replay for order flow, and Market Replay for Level 2 / DOM strategies."
---

# Backtesting

MZpack strategies process the market **tick by tick** — their logic runs off NinjaTrader's tick stream (`OnMarketData`), not off finished bars. Even a strategy whose logic runs on bar close is driven by the first tick of the next bar. Because of this, a meaningful historical backtest needs tick-level data, and the way you supply that data depends on what the strategy consumes.

There are two paths:

- **Strategy Analyzer + Tick Replay** — for order flow strategies that need only Level 1 (historical Bid/Ask) data.
- **Market Replay (Playback)** — for strategies that need Level 2 (the order book / DOM), which NinjaTrader does not store historically.

## Choosing your path

| Strategy uses… | Data needed | Backtest path |
|---|---|---|
| Footprint, delta, volume profile, big trades (Level 1) | Historical Bid/Ask | **Strategy Analyzer + Tick Replay** |
| mzMarketDepth, iceberg (Hard/Soft), DOM pressure/support, Smart/Predatory trades (Level 2) | Order book (DOM) | **Market Replay (Playback)** or live |

The dividing line is Level 1 vs Level 2. NinjaTrader can *replay* historical Level 1 (trades and best bid/ask) through Tick Replay, but it keeps **no** historical order book — so any Level 2 feature can only be exercised against Market Replay or live data. See [Order Flow — Data Levels](../concepts/order-flow.md#data-levels) for the distinction.

:::note
mzBigTrade's [Tape iceberg algorithm](../indicators/mzBigTrade.md#tape-algorithm) is the exception on the Level 2 side: it derives hidden volume from each trade's fill composition instead of the order book, so it also works on historical bars under Tick Replay.
:::

## Prerequisites: Tick Replay

Both paths that use historical data depend on **Tick Replay**, which reconstructs the tick-by-tick record (including historical Bid/Ask) that order flow calculations require. Enabling it is a two-step switch — both are required:

1. **Global** — turn on `Tools ▸ Options ▸ Market Data ▸ Show Tick Replay`. This only makes the Tick Replay option *available*.
2. **Per data series** — turn on **Tick Replay** in the chart's `Data Series` properties (and, for a backtest, on the Strategy Analyzer's data series). This actually enables historical Bid/Ask processing for that series.

:::warning Tick Replay is required
Without Tick Replay, order flow indicators cannot reconstruct historical data — they display an on-chart warning (*"Enable 'Tick Replay' option from DataSeries properties…"*) and produce no historical plots, which in a backtest means no signals and no trades. Tick Replay is resource-intensive, so keep **Days to load** as small as your test allows (typically 1–14).
:::

## Path 1 — Strategy Analyzer + Tick Replay

This is the primary path for order flow strategies.

### 1. Make the strategy backtest-ready

MZpack strategies are **not active in the historical state by default**, but the Strategy Analyzer runs in the historical state only. You must therefore tell the strategy to work on historical bars:

- **From the UI** — enable the **MZpack: backtesting** option in the strategy settings window.
- **From code** — set `EnableBacktesting = true` in `State.SetDefaults`:

```csharp
protected override void OnStateChange()
{
    if (State == State.SetDefaults)
    {
        // Required for backtesting in Strategy Analyzer
        EnableBacktesting = true;
    }
}
```

Either way, MZpack switches its indicator models to `ModelIncrementRefresh.HistoricalRealtime` and sets `WorkingStateHistorical = true` so the order flow models compute on historical bars. You don't set those properties manually.

:::note
Enabling backtesting increases historical loading time for mzFootprint and mzVolumeProfile, because their load-time optimizations must be disabled to calculate all values on historical bars. Don't enable it for normal chart trading.
:::

### 2. Run the backtest

1. Open the NinjaTrader **Strategy Analyzer**.
2. Add your strategy and select the instrument and date range. Keep the range short at first — Tick Replay backtests are heavy.
3. Make sure **Tick Replay** is enabled on the Analyzer's data series (see [Prerequisites](#prerequisites-tick-replay) above).
4. Confirm the **Calculation mode** matches your data feed, then run.

### 3. Match the calculation mode to your data

The calculation mode decides how each trade is classified as buy or sell — and how accurate your historical delta will be:

| Mode | When to use |
|---|---|
| **BidAsk** | Futures with Tick Replay enabled — most accurate |
| **UpDownTick** | Forex, crypto, stocks, or any feed without historical Bid/Ask |
| **Hybrid** | Markets where historical Bid/Ask is unavailable but live is (UpDownTick for history, BidAsk live) |

See [Order Flow — Trade Classification](../concepts/order-flow.md#trade-classification) and [Indicators Overview — Calculation Modes](../indicators/overview.md#order-flow-calculation-modes) for full details.

:::tip Profile accuracy vs Tick Replay
For volume profile / footprint work, the two must agree: **Tick** accuracy requires Tick Replay **on**; **Minute** accuracy (used to speed up very long ranges) requires Tick Replay **off**. A mismatch triggers a warning and suppresses historical output.
:::

## Path 2 — Market Replay (Playback)

Use Market Replay when the strategy relies on Level 2 data — **mzMarketDepth**, the **Hard/Soft iceberg** algorithms, **DOM pressure/support**, or **Smart/Predatory** trade detection. These work only on live or Market Replay data, because NinjaTrader provides no historical order book. (The one Level-2-flavored exception is mzBigTrade's [Tape algorithm](../indicators/mzBigTrade.md#tape-algorithm), which works historically under Tick Replay.)

At a high level, backtesting against Market Replay means:

1. **Download** Market Replay data for the instrument and dates via `Tools ▸ Historical Data ▸ Load` (Market Replay).
2. **Connect** the built-in **Playback** connection (`Connections ▸ Playback Connection`).
3. **Load** the strategy on a chart and drive the session forward with the Playback controller. Fills run against NinjaTrader's `Playback101` simulation account.

For the full mechanics of downloading replay data and using the Playback connection, see NinjaTrader's own documentation: [Playback Connection](https://ninjatrader.com/support/helpguides/nt8/playback_connection.htm).

:::note
The Strategy Analyzer runs on historical data only, so Level 2 strategies **cannot** be backtested there — Market Replay (or live) is the only way to exercise their order-book logic.
:::

## Troubleshooting

If a backtest returns no trades or the order flow looks empty, the cause is almost always the data underneath it:

- **Footprint shows no data or all zeros** — usually Tick Replay off, no tick data for the instrument, or a calculation-mode mismatch. See [Troubleshooting — Footprint shows no data](../troubleshooting.md#footprint-shows-no-data-or-all-zeros).
- **Missing or corrupted `.ncd` tick data (OneDrive / cloud folders)** — a synced NinjaTrader data folder can leave tick files incomplete, so backtests return no trades or unreliable results. See [Troubleshooting — File access errors](../troubleshooting.md#file-access-errors-or-missing-tick-data-onedrive--cloud-synced-folders).
