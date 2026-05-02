---
sidebar_position: 3
title: "Built-in Strategies"
description: "Reference guide for MZpack built-in automated trading strategies"
---

# Built-in Strategies

MZpack includes three built-in strategies for NinjaTrader 8: two trading strategies and one data export utility. All built-in strategies support Auto and Manual [operating modes](overview.md#operating-modes), the [Control Panel](strategy-framework.md#control-panel), [trading times](strategy-framework.md#trading-times), and [logging](strategy-framework.md#logging).

## Footprint Action Strategy

Footprint Action is an order flow strategy built entirely on the [mzFootprint](../indicators/mzFootprint.md) indicator. It provides 10 delta and order flow signals that can be combined using AND or OR logic to form trading patterns.

### Signals

Each signal can be individually enabled or disabled. Every signal has its own bar filter overrides (Min bar Volume, Min bar Delta, Min bar Delta %) and can be marked as **Mandatory** (always required regardless of the tree logic).

| Signal | Description |
|---|---|
| **Delta Divergence** | Trend reversal signal — price makes a new extreme while delta moves in the opposite direction |
| **Delta Tail** | Bar has negative delta across all levels except the bottom (or vice versa), indicating absorption at the extreme |
| **Delta Surge/Drop** | 4-bar signal tracking consecutive increasing or decreasing delta, indicating momentum buildup |
| **Delta Flip** | 2-bar reversal signal showing a sudden delta shift from positive to negative (or vice versa) |
| **Delta Trap** | 3-bar signal identifying a delta reversal followed by renewed strength in the original direction |
| **Delta Slingshot** | Trend reversal when an extreme delta reading gets overrun by the opposite extreme delta within a lookback range |
| **Above/Below POC** | Trade when a bar opens and closes on the same side of its Point of Control |
| **Stacked Imbalances** | Multiple imbalances stacked at consecutive price levels (configurable number and direction) |
| **Volume Sequencing** | Multiple price levels with increasing volume, indicating large trader activity |
| **Hammer with Absorption** | Absorption (trapped sellers/buyers) detected in the wick of a hammer candle pattern |

### Signal-specific parameters

Every signal exposes the same **common controls** — Enable, Mandatory, Override filters, Min bar Volume, Min bar Delta, Min bar Delta % — so the tables below list only the extras specific to each signal. Delta Divergence, Delta Tail, Delta Surge/Drop, Delta Trap, and Above/Below POC have no extras and are configured entirely with the common controls.

#### Delta Flip

| Setting | Description | Range | Default |
|---|---|---|---|
| Precision | Sensitivity of the delta-flip detection | 1–100 | 40 |

#### Delta Slingshot

| Setting | Description | Range | Default |
|---|---|---|---|
| Lookback bars | Number of prior bars compared to the closed bar (closed bar excluded) | 1–100 | 3 |

#### Stacked Imbalances

| Setting | Description | Range | Default |
|---|---|---|---|
| Stacked Imbalances: reverse | Reverse the direction of the signal | bool | Off |
| Imbalances: % | Imbalance percentage threshold | ≥ 0.01 | 68 |
| Number | Minimum number of imbalances in the stack (1 = single imbalance) | ≥ 1 | 3 |
| Volume filter | Minimum total volume in the imbalance S/R zone | ≥ 0 | 0 |
| Above/below POC | Require the stack to be on the correct side of the POC | bool | On |

#### Volume Sequencing

| Setting | Description | Range | Default |
|---|---|---|---|
| Levels | Number of consecutive price levels with increasing volume required | 2–5 | 4 |

#### Hammer with Absorption

| Setting | Description | Range | Default |
|---|---|---|---|
| Wick % | Minimum wick size as percentage of bar range | 1–100 | 35 |
| POC | Require absorption to be at/above/below the POC accordingly | bool | On |

### Bar Filters

Each signal applies bar-level filters to the bars it analyzes. The bars that filters apply to depend on the signal:

| Signal | Min bar Volume | Min bar Delta | Min bar Delta % |
|---|---|---|---|
| Delta Divergence | Closed | Closed | Closed |
| Delta Tail | Closed | Closed | Closed |
| Delta Surge/Drop | Closed | Closed | Closed |
| Delta Flip | Closed, Closed-1 | Closed, Closed-1 | Closed, Closed-1 |
| Delta Trap | Closed | Closed, Closed-1, Closed-2 | Closed |
| Delta Slingshot | Lookback | Lookback | Lookback |
| Above/Below POC | Closed | Closed | Closed |
| Stacked Imbalances | Closed | Closed | Closed |
| Volume Sequencing | Closed | Closed | Closed |
| Hammer with Absorption | Closed | Closed | Closed |

"Closed" = the just-closed bar. "Closed-1" = one bar before. "Lookback" = all bars in the lookback range.

### Signal Logic

- **AND** — all enabled signals must validate in the same direction
- **OR** — at least one signal must validate. Use **Min # validated signals** to require a minimum number (e.g., 2 of 5 enabled signals)

Each signal also has an **Override filters** option that lets it bypass the global bar filters when its own per-signal filters are configured.

### Strategy Settings

| Setting | Description | Default |
|---|---|---|
| Logic of signals | AND or OR combination of enabled signals | OR |
| Min bar Volume | Global minimum bar volume filter | 100 |
| Min bar Delta | Global minimum absolute bar delta filter | 100 |
| Min bar Delta % | Global minimum bar delta percentage filter | 0 |
| Min # validated signals | Minimum signals that must validate (OR mode only) | 0 |
| Opposite Pattern Action | What to do when an opposite signal occurs while in a position: None, Close, or Reverse | None |
| Suspend after trade | Pause trading after a position is closed until manually re-enabled | Off |

### Position Settings

| Setting | Description | Default |
|---|---|---|
| Direction | Allowed trading direction: Long, Short, or Any | Any |
| Quantity (entries 1-3) | Number of contracts per entry (up to 3 entries for scaling) | 1 |
| Stop Loss (entries 1-3) | Stop loss in ticks per entry | 20 |
| Profit Target (entries 1-3) | Profit target in ticks per entry | 40 |
| Break-even after | Move stop to entry price after this many ticks of profit | 10 |
| Break-even shift | Ticks added to break-even stop (positive = additional profit) | 1 |
| Trail | Enable trailing stop | Off |
| Trail after / distance / step | Trail activation threshold, trailing distance, and step size in ticks | 15 / 10 / 1 |
| Enter by limit order | Use limit orders instead of market orders for entries | Off |

### Source Code

See [Footprint Action Source Code](/api/source-code/footprint-action) for a developer-level walkthrough of the class structure, decision tree construction, all 10 signal implementations, and data export schema.

---

## GhostResistance Strategy

GhostResistance is a reversal strategy that targets **liquidity traps** — situations where price pushes beyond support or resistance levels, triggering stop orders and breakout entries from trapped traders, then reverses sharply back into the prior value area.

The strategy combines absorption zones, big trade detection, bar metrics, and volume profile levels to identify these reversal setups.

### How It Works

**Short setup:** Price spikes above resistance with aggressive buying. Absorption builds at the extreme as sellers absorb the buying pressure. Price reverses downward as trapped longs exit.

**Long setup:** Price drops below support with aggressive selling. Absorption builds at the extreme as buyers absorb the selling pressure. Price reverses upward as trapped shorts cover.

### Confirmation Signals

GhostResistance uses AND logic — all enabled signal groups must confirm before a trade is taken. One entry per bar maximum.

| Signal Group | Description |
|---|---|
| **Bar Metrics** | Bar must meet minimum volume, delta, delta %, wick %, and optionally be a hammer pattern |
| **Absorption** | Absorption S/R zones from [mzFootprint](../indicators/mzFootprint.md) — configurable percentage, depth, consecutive levels, and zone volume |
| **Big Trade** | Significant trades detected by [mzBigTrade](../indicators/mzBigTrade.md) — configurable minimum size, iceberg detection, and aggression (sweep) filter |
| **Profile Levels** | Price must be approaching a volume profile level (session or weekly) from [mzVolumeProfile](../indicators/mzVolumeProfile.md) — optional, can be disabled for pure order flow mode |

### Bar Metrics Settings

| Setting | Description | Default |
|---|---|---|
| Min bar Volume | Minimum bar volume | 500 |
| Min bar Delta | Minimum absolute bar delta | 20 |
| Min bar Delta % | Minimum bar delta percentage | 10 |
| Min wick % | Minimum wick size as percentage of bar range | 30 |
| Hammer | Require hammer candle pattern | On |

### Absorption Settings

| Setting | Description | Default |
|---|---|---|
| Absorption % | Minimum absorption percentage threshold | 200 |
| Absorption depth | Number of price levels to check for absorption | 2 |
| Consecutive | Minimum consecutive absorption levels required | 2 |
| Zone volume | Minimum volume in the absorption S/R zone | 50 |

### Big Trade Settings

| Setting | Description | Default |
|---|---|---|
| Trade filter | Minimum trade size (contracts) | 200 |
| Iceberg filter: enable | Detect iceberg orders | On |
| Iceberg filter | Minimum iceberg volume | 20 |
| Aggression filter: enable | Require aggressive (sweep) trades | On |
| Aggression filter, ticks | Minimum sweep range in ticks | 3 |

### Profile Levels Settings

When enabled, the strategy only takes trades near selected volume profile levels. Price must be within the **approaching distance** (in ticks) of a selected level.

**Session levels** (overnight and RTH):

| Setting | Default |
|---|---|
| Overnight POC | On |
| Overnight VAH/VAL | On |
| Overnight High/Low | On |
| RTH POC | On |
| RTH VAH/VAL | On |
| RTH High/Low | On |
| Approaching distance | 8 ticks |

**Weekly levels:**

| Setting | Default |
|---|---|
| Weekly POC | On |
| Weekly VAH/VAL | On |
| Weekly High/Low | On |
| Approaching distance | 20 ticks |

RTH/ETH session times are configurable (default RTH: 08:30–15:15, ETH: 17:30–08:30).

### Operating Modes

GhostResistance can be configured for different trading styles:

- **Level-based trap trading** — profile levels enabled with stricter absorption and big trade thresholds for selective setups near key levels
- **Pure order flow reversals** — profile levels disabled, relying only on absorption and big trade activity to identify turning points
- **Conservative mode** — enable **Wait for bar close** for bar-close confirmation with higher thresholds for fewer, higher-quality trades

### Position Settings

GhostResistance supports up to 3 entries for position scaling, each with independent quantity, stop loss, and profit target. The same break-even and trail settings apply to all entries.

| Setting | Entry 1 | Entry 2 | Entry 3 |
|---|---|---|---|
| Quantity | 1 | 2 | 0 (disabled) |
| Stop Loss | 20 ticks | 20 ticks | 20 ticks |
| Profit Target | 40 ticks | 60 ticks | 80 ticks |

### Control Panel

The GhostResistance Control Panel provides runtime buttons:

| Button | Action |
|---|---|
| **Trade** | Toggle trading on/off (green = active) |
| **Auto suspend** | Pause trading after the next completed trade |
| **Break Even** | Immediately move stop loss to break-even on the current position |
| **Trail** | Toggle trailing stop on/off for the current position |
| **Close** | Cancel pending orders and close the current position |

### Best Market Conditions

- Rotational or range-bound sessions with defined support/resistance
- Price action with frequent stop-runs and wicks beyond key levels
- Avoid strong trending days where reversals fail more frequently

### Source Code

See [GhostResistance Source Code](/api/source-code/ghost-resistance) for a developer-level walkthrough of the class structure, indicator wiring, signal implementations, and decision tree construction.

---

## Data Export Strategy

The Data Export strategy is a utility that exports indicator data to CSV files. It does not trade — it collects and writes data from up to four MZpack indicators for external analysis, backtesting research, or machine learning pipelines.

### Supported Indicators

| Indicator | Data Source | Export Granularity |
|---|---|---|
| [mzFootprint](../indicators/mzFootprint.md) | Level 1 | Bar |
| [mzVolumeProfile](../indicators/mzVolumeProfile.md) | Level 1 | Bar or Tick |
| [mzBigTrade](../indicators/mzBigTrade.md) | Level 1 | Tick |
| [mzMarketDepth](../indicators/mzMarketDepth.md) | Level 2 | Update |

Each indicator can be independently enabled or disabled for export.

### Footprint Export Values

| Value | Description |
|---|---|
| Open, Close, High, Low | Bar OHLC prices |
| RangeTicks, RangeLevels | Bar range in ticks and price levels |
| Direction | Bar direction (up/down) |
| DurationMs | Bar duration in milliseconds |
| Volumes, Bids, Asks, Deltas | Price ladders (per-level data) |
| TradesNumbers | Per-level trades count ladder |
| TradesNumber | Total trades count in the bar |
| Volume, BuyVolume, SellVolume | Bar total, buy, and sell volumes |
| Delta, DeltaPercentage | Bar delta and delta percentage |
| MinDelta, MaxDelta | Intra-bar delta extremes |
| DeltaChange, DeltaCumulative | Delta change and session cumulative delta |
| DeltaRate, DeltaRateHigh, DeltaRateLow | Delta rate and its extremes |
| AbsoluteDeltaAverage, AbsoluteDeltaTotal | Absolute delta statistics |
| VAH, VAL, POC, POCVolume | Bar value area high/low, POC price and volume |
| BuyPercentage, SellPercentage | Buy/sell volume percentages |
| COTHigh, COTLow | Commitment of Traders high/low |

### Export Settings

| Setting | Description | Default |
|---|---|---|
| Header | Include column headers in the CSV file | On |
| Time | Include timestamp column | On |
| Batch | Batch write mode (writes accumulated data at once) | Off |
| Signed volume | Prefix volumes with +/- for buy/sell direction | Off |
| Delimiter | Column separator character | `;` |
| File | Custom file path (optional) | Auto-generated |

### Output File Location

By default, exported files are saved to:

```
Documents\NinjaTrader 8\mzpack\strategy\...\Data_Export\data\<instrument>_<id>.csv
```

Indicator settings are saved to XML and restored automatically on the next run. Values that are not calculated or not supported by the indicator are exported as empty strings or zeros.

:::note
Enable the relevant indicator features before exporting. For example, enable volume profile POC in the mzVolumeProfile settings to export POC values.
:::

### Temporality

Each indicator export can run in one of two temporalities:

| Mode | Description |
|---|---|
| **Historical** | Exports data from loaded historical bars (requires backtesting mode) |
| **Realtime** | Exports data as it arrives during live trading |

### Source Code

See [Data Export Source Code](/api/source-code/data-export) and [Drawing Objects Export Source Code](/api/source-code/drawing-objects-export) for developer-level walkthroughs of the export strategy implementations.
