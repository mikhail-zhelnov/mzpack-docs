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

Each signal has its own category in the strategy properties, named after the signal. The first setting in that category is the toggle that enables it and carries the signal's name.

| Setting | Default | Description |
|---|---|---|
| **Delta Divergence** | true | Trend reversal signal — price makes a new extreme while delta moves in the opposite direction |
| **Delta Tail** | true | Bar has negative delta across all levels except the bottom (or vice versa), indicating absorption at the extreme |
| **Delta Surge/Drop** | true | 4-bar signal tracking consecutive increasing or decreasing delta, indicating momentum buildup |
| **Delta Flip** | true | 2-bar reversal signal showing a sudden delta shift from positive to negative (or vice versa) |
| **Delta Trap** | false | 3-bar signal identifying a delta reversal followed by renewed strength in the original direction |
| **Delta Slingshot** | false | Trend reversal when an extreme delta reading gets overrun by the opposite extreme delta within a lookback range |
| **Above/Below POC** | false | Trade when a bar opens and closes on the same side of its Point of Control |
| **Stacked Imbalances** | false | Multiple imbalances stacked at consecutive price levels (configurable number and direction) |
| **Volume Sequencing** | false | Multiple price levels with increasing volume, indicating large trader activity |
| **Hammer with Absorption** | false | Absorption (trapped sellers/buyers) detected in the wick of a hammer candle pattern |

### Common Signal Controls

Every signal category repeats the same filter and routing settings below the enable toggle. They are documented once here.

| Setting | Default | Description |
|---|---|---|
| **Mandatory** | false | The signal must validate for the pattern to validate, regardless of the tree logic. In OR mode a mandatory signal is still always required |
| **Filters: mode** | Global | Choose the bar-filter source: Global uses the Strategy filters, Percentile uses this signal's percentile, and Absolute uses the per-signal values below |
| **Filters: percentile** | 70 | Percentile used when Filters: mode is Percentile, range: 0–100 |
| **Override filters (deprecated)** | false | Legacy alias for Filters: mode = Absolute. Existing templates continue to work; use Filters: mode for new configurations |
| **Min bar Volume** | 0 | Per-signal minimum bar volume. Applied in Absolute mode |
| **Min bar Delta** | 0 | Per-signal minimum absolute bar delta. Applied in Absolute mode; 0 intentionally disables the delta threshold |
| **Min bar Delta %** | 0 | Per-signal minimum bar delta as a percentage of bar volume. Applied in Absolute mode |

### Signal-specific Parameters

Delta Divergence, Delta Tail, Delta Surge/Drop, Delta Trap, and Above/Below POC have no extra settings — they are configured entirely with the common controls above.

#### Delta Flip

| Setting | Default | Description |
|---|---|---|
| **Precision** | 40 | Sensitivity of the delta-flip detection — higher values require a sharper flip, range: 1–100 |

#### Delta Slingshot

| Setting | Default | Description |
|---|---|---|
| **Lookback bars** | 3 | Number of prior bars compared with the closed bar; the closed bar itself is not included. Example: value = 2 compares the two bars before the closed bar with the closed bar, range: 1–100 |

#### Stacked Imbalances

| Setting | Default | Description |
|---|---|---|
| **Stacked Imbalances: reverse** | false | Reverse the direction the signal returns |
| **Imbalances: %** | 68 | Imbalance percentage threshold — the diagonal bid/ask ratio a level must exceed to count as an imbalance, range: 0.01–∞ |
| **Number** | 3 | Minimum number of imbalances in the stack. Set 1 to accept a single imbalance, range: 1–∞ |
| **Volume filter** | 0 | Minimum total volume in the imbalance S/R zone; 0 disables the filter, range: 0–∞ |
| **Above/below POC** | true | Require the stack to be on the correct side of the bar POC — buy stacks below it, sell stacks above it |

#### Volume Sequencing

| Setting | Default | Description |
|---|---|---|
| **Levels** | 4 | Number of consecutive price levels with increasing volume required, range: 2–5 |

#### Hammer with Absorption

| Setting | Default | Description |
|---|---|---|
| **Wick %** | 35 | Minimum wick size as a percentage of the bar range, range: 1–100 |
| **POC** | true | Require the absorption to be below the POC for a long signal and above it for a short signal |

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

Each signal can select global, percentile, or absolute per-signal bar filters with **Filters: mode**. The deprecated **Override filters** option remains available for old templates and maps to Absolute mode.

### Strategy Settings

| Setting | Default | Description |
|---|---|---|
| **Action** | Trade | What the strategy does — Trade submits orders; Export writes validated patterns to CSV without trading; Probe observes every signal over history without trading; TradeProbe trades and observes signals at the same time |
| **Trading: ON** | true | Master switch for opening positions. Turn it off to keep signals calculating and drawing without entering the market |
| **Opposite Pattern Action** | None | What to do when the pattern validates in the opposite direction while a position is open — None, Close, Reverse, or Unmanaged. See [Opposite Pattern Action](strategy-framework.md#opposite-pattern-action) |
| **Suspend after trade** | false | Stop opening new positions once the current trade closes, until trading is switched back on from the Control Panel |
| **Logic of signals** | Or | How enabled signals are combined — And (all must agree on direction), Or (any one is enough), or Conjunction |
| **Min bar Volume** | 100 | Global minimum bar volume; bars below it are ignored by all signals that do not override filters |
| **Min bar Delta** | 100 | Global minimum absolute bar delta |
| **Min bar Delta %** | 0 | Global minimum bar delta as a percentage of bar volume |
| **Min # validated signals** | 0 | Minimum number of validated signals for an OR tree; 0 means a single signal is enough, range: 0–∞ |
| **Filters: auto** | false | Calibrate Min bar Volume and Min bar Delta from completed prior sessions. Min bar Delta % remains manual |
| **Filters: percentile** | 70 | Percentile of the calibration baseline used as the global volume and delta threshold, range: 1–99 |
| **Filters: baseline sessions** | 10 | Number of completed sessions in the calibration baseline and required warm-up, range: 3–60 |
| **Filters: intraday buckets** | 60 minutes | Time-of-day bucket size for calibration; the grid is anchored to local midnight |
| **Filters: session outlier, %** | 50 | Exclude a session whose median bar volume differs from the baseline median by more than this percentage, range: 10–100 |
| **Filters: diagnostics** | true | Report calibration decisions and resulting thresholds whenever the baseline is rebuilt |
| **Filters: dump baseline** | false | Write calibration input and results to `mzpack\strategy\...\calibration` for support analysis |
| **Probe: horizon bars** | 40 | Number of bars after a signal over which its outcome is observed, range: 1–1000 |
| **Probe: ladder ticks** | 0 | First-touch range recorded on each side of the entry price. 0 derives ten bar ranges on a Range chart, otherwise 100 ticks; the step is widened so that each side has no more than 100 levels |
| **Probe: export** | false | Write the probe journal to `mzpack\strategy\...\probe` when the strategy is removed |

### Signal Probe

**Probe** measures individual signals without allowing them to submit orders. It does not use the pattern tree: every one of the ten signals is evaluated independently, including signals disabled for trading. Use it to establish which setups occur and how price behaves after them before choosing a trading combination.

Set **Action** to one of these modes:

| Mode | Trading | Probe collection | Historical behavior |
|---|---|---|---|
| **Trade** | Yes | No | Normal trading behavior |
| **Export** | No | No | Replays history to export validated patterns |
| **Probe** | No | Yes | Replays history and collects probe events |
| **TradeProbe** | Yes | Yes | Observes live trading; does not automatically enable historical collection |

`TradeProbe` deliberately does not enable historical collection. On a live chart, automatically replaying history while trading is enabled could submit historical entries. To backtest trading and collect probe events together, enable **MZpack > Backtesting** yourself. Historical probe data also needs Tick Replay; without it, the strategy reports that it can observe only realtime ticks.

For each signal event, the probe records the first tick and bar that reach each favourable and adverse price level in its ladder. It also records MFE, MAE, `BarsToMFE`, `FirstTickPrice`, and the price at the observation horizon. This first-touch sequence lets you evaluate different stop and target pairs later without replaying the strategy. Observation ends at the configured horizon, at the session boundary, or at the end of available data; the event identifies which condition ended it.

When **Probe: export** is on, the strategy writes a self-describing journal when it is removed. It contains one event per row, signal and market context, probe settings, warnings, calibration data, and columns such as `Fav0100_Time` and `Adv0100_Bar`. Existing files are not overwritten. The Output window also prints a Signal Report with each signal's long/short count, median MFE and MAE, and expectation using the first position's stop loss and profit target. Rows with fewer than 50 events are marked unreliable.

### Auto-calibrated Filters

With **Filters: auto** enabled, the strategy builds volume and absolute-delta thresholds from completed sessions before the current session. Until the configured number of baseline sessions has been collected, the manual **Min bar Volume** and **Min bar Delta** values still filter signals, but probe events are deliberately not recorded. This prevents warm-up events, admitted under a different filter, from being mixed with the calibrated sample.

The calibration can use 60- or 30-minute intraday buckets, so each time of day receives its own threshold. Sessions with too little data, poor trading-window coverage, abnormal median volume, or more than twice their expected share of bar-count data are excluded. A thin or one-sided bucket falls back to the common pool. Use **Filters: diagnostics** to inspect every decision and **Filters: dump baseline** to write the baseline to disk for support.

Probe journals record `VolumeRank` and `DeltaRank` for the event against the calibration distribution. A run collected at a lower percentile can be filtered offline to any higher percentile; it cannot recover events rejected by a higher percentile during collection. The ranks describe the complete signal event — the binding bar for AND conditions and the best valid alternative for OR conditions — rather than only the firing bar. The journal format changed with this behavior: reject older files that do not contain `unmarkedAlternatives` in `[params]`.

### Position Settings

Up to three entries can be configured for position scaling, each with its own quantity, profit target, and stop loss. Set a quantity to 0 to disable that entry.

| Setting | Default | Description |
|---|---|---|
| **Direction** | Any | Allowed trading direction — Long, Short, or Any |
| **Trading Instrument: enable** | false | Submit orders on a data series other than the chart series. Patterns are still evaluated on the chart series |
| **Trading Instrument: name** | MES 12-24 | Instrument of the trading data series |
| **Trading Instrument: period** | Minute | Bars period type of the trading data series |
| **Trading Instrument: value** | 1 | Bars period value of the trading data series, range: 1–∞ |
| **Quantity 1** | 1 | Contracts for the first entry, range: 1–∞ |
| **Profit target 1, ticks** | 20 | Profit target of the first entry in ticks, range: 1–∞ |
| **Stop loss 1, ticks** | 10 | Stop loss of the first entry in ticks, range: 1–∞ |
| **Quantity 2** | 2 | Contracts for the second entry; 0 disables it, range: 0–∞ |
| **Profit target 2, ticks** | 30 | Profit target of the second entry in ticks, range: 1–∞ |
| **Stop loss 2, ticks** | 10 | Stop loss of the second entry in ticks, range: 1–∞ |
| **Quantity 3** | 0 | Contracts for the third entry; 0 disables it, range: 0–∞ |
| **Profit target 3, ticks** | 40 | Profit target of the third entry in ticks, range: 1–∞ |
| **Stop loss 3, ticks** | 10 | Stop loss of the third entry in ticks, range: 1–∞ |
| **Breakeven** | false | Move the stop loss to the entry price once the position gains **Breakeven after, ticks** |
| **Breakeven after, ticks** | 10 | Profit in ticks that triggers the break-even move, range: 1–∞ |
| **Breakeven shift, ticks** | 1 | Ticks added to the break-even stop beyond the entry price; a positive value locks in that many ticks of profit |
| **Trail** | false | Enable the trailing stop |
| **Trail after, ticks** | 15 | Profit in ticks that activates the trail, range: 1–∞ |
| **Trail distance, ticks** | 10 | Distance the trailing stop keeps behind price, in ticks, range: 1–∞ |
| **Trail step, ticks** | 1 | Minimum price movement in ticks before the trailing stop is moved again, range: 1–∞ |

### Trading Time Settings

Two independent intraday windows can be defined. Times use the chart's time zone. Leave both disabled to trade the whole session.

| Setting | Default | Description |
|---|---|---|
| **Trading time #1: enable** | false | Enable the first trading window |
| **Trading time #1: begin** | 08:30:00 | Start of the first window |
| **Trading time #1: end** | 15:15:00 | End of the first window |
| **Trading time #2: enable** | false | Enable the second trading window |
| **Trading time #2: begin** | 15:30:00 | Start of the second window |
| **Trading time #2: end** | 17:00:00 | End of the second window |

### Risk Management Settings

Limits apply at the account level and reset overnight. See [Risk Management](strategy-framework.md#risk-management) for how they are evaluated.

| Setting | Default | Description |
|---|---|---|
| **Daily loss limit: enable** | false | Enable the daily loss limit |
| **Daily loss limit** | 500 | Maximum loss for the day in account currency |
| **Daily profit limit: enable** | false | Enable the daily profit limit |
| **Daily profit limit** | 2500 | Profit target for the day in account currency |
| **Daily max drawdown: enable** | false | Enable the trailing daily drawdown limit |
| **Daily max drawdown** | 1500 | Maximum drop from the day's peak account value, in account currency |
| **Daily trades limit: enable** | false | Enable the daily trades limit |
| **Daily trades limit** | 5 | Maximum number of filled entries per day |

### Export Settings

When **Action** is set to Export, the strategy writes each validated pattern to a CSV file instead of trading.

| Setting | Default | Description |
|---|---|---|
| **Header** | true | Write the column header row at the top of the file |
| **Batch** | false | Accumulate records in memory and write them in one pass instead of after each pattern |
| **File** | footprint_action.csv | Output file name |
| **NinjaScript Output** | false | Mirror each exported record to the NinjaTrader Output window |

### Control Panel and Dashboard Defaults

Footprint Action re-exposes four inherited [strategy framework](strategy-framework.md) settings on the MZpack [Control Panel](strategy-framework.md#control-panel) so they can be changed at runtime, and ships different defaults for them.

| Setting | Default | Description |
|---|---|---|
| **Entry/Exit: markup** | MarkerAndText | Marker style drawn at the entry and exit price — None, Marker, or MarkerAndText |
| **Pattern dashboard: show** | true | Show the decision-tree dashboard on the chart |
| **Pattern dashboard: legend** | true | Show the legend that names the signal in each dashboard row |
| **Pattern dashboard: position** | Top | Edge of the chart panel the dashboard is anchored to — Top or Bottom |

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

### Strategy Settings

| Setting | Default | Description |
|---|---|---|
| **Action** | Trade | What the strategy does — Trade (evaluate patterns and submit orders) or Export (write validated patterns to CSV without trading) |
| **Trading: ON** | true | Master switch for opening positions. Turn it off to keep signals calculating and drawing without entering the market |
| **Opposite Pattern Action** | None | What to do when the pattern validates in the opposite direction while a position is open — None, Close, Reverse, or Unmanaged. See [Opposite Pattern Action](strategy-framework.md#opposite-pattern-action) |
| **Suspend after trade** | false | Stop opening new positions once the current trade closes, until trading is switched back on from the Control Panel |
| **Wait for bar close** | false | Validate the pattern only on bar close instead of on each tick. Fewer, later, but more reliable entries |
| **Short circuit** | true | Stop evaluating the signal tree as soon as a signal returns None. Read-only |

### Bar Metrics Settings

| Setting | Default | Description |
|---|---|---|
| **Enable** | true | Include the bar metrics signal in the pattern |
| **Min bar Volume** | 100 | Minimum bar volume |
| **Min bar Delta** | 100 | Minimum absolute bar delta |
| **Min bar Delta %** | 10 | Minimum bar delta as a percentage of bar volume |
| **Min wick %** | 30 | Minimum wick size as a percentage of the bar range, range: 0–100 |
| **Hammer** | true | Require a hammer candle — the wick must be on the side the reversal is expected from |

### Absorption Settings

| Setting | Default | Description |
|---|---|---|
| **Enable** | true | Include the absorption signal in the pattern. Read-only — absorption is always required |
| **Absorption %** | 200 | Minimum absorption percentage — how far the absorbing side's volume must exceed the aggressing side's |
| **Absorption depth** | 2 | How far price must bounce from the absorption level to qualify, in ticks |
| **Consecutive** | 2 | Minimum number of consecutive absorption levels forming the S/R zone |
| **Zone volume** | 50 | Minimum total volume in the absorption S/R zone |

### Big Trade Settings

| Setting | Default | Description |
|---|---|---|
| **Enable** | true | Include the big trade signal in the pattern. Read-only — a big trade is always required |
| **Trade filter** | 200 | Minimum trade size in contracts for a trade to count |
| **Iceberg filter: enable** | true | Require iceberg volume in the trade |
| **Iceberg filter** | 20 | Minimum iceberg volume, applied when the iceberg filter is enabled |
| **Aggression filter: enable** | true | Require the trade to be aggressive — a sweep across several price levels |
| **Aggression filter, ticks** | 3 | Minimum sweep range in ticks, applied when the aggression filter is enabled |

### Profile Levels Settings

When enabled, the strategy only takes trades near selected volume profile levels. The bar high or low must come within the approaching distance (in ticks) of a selected level.

| Setting | Default | Description |
|---|---|---|
| **Enable** | true | Require price to be approaching a selected profile level. Disable for pure order flow mode |
| **RTH begin** | 08:30:00 | Start of the regular trading hours session used to build the RTH profile |
| **RTH end** | 15:15:00 | End of the regular trading hours session |
| **ETH begin** | 17:30:00 | Start of the overnight (extended hours) session. Clamped to be no earlier than RTH end |
| **ETH end** | 08:30:00 | End of the overnight session. Clamped to be no later than ETH begin |
| **Overnight POC** | true | Use the overnight session Point of Control as a level |
| **Overnight VAH/VAL** | true | Use the overnight session value area high and low as levels |
| **Overnight High/Low** | true | Use the overnight session high and low as levels |
| **RTH POC** | true | Use the RTH session Point of Control as a level |
| **RTH VAH/VAL** | true | Use the RTH session value area high and low as levels |
| **RTH High/Low** | true | Use the RTH session high and low as levels |
| **Overnight/RTH level approaching, ticks** | 8 | How close the bar high/low must come to an overnight or RTH level, in ticks |
| **Weekly POC** | true | Use the weekly Point of Control as a level |
| **Weekly VAH/VAL** | true | Use the weekly value area high and low as levels |
| **Weekly High/Low** | true | Use the weekly high and low as levels |
| **Weekly level approaching, ticks** | 20 | How close the bar high/low must come to a weekly level, in ticks |

### Operating Modes

GhostResistance can be configured for different trading styles:

- **Level-based trap trading** — profile levels enabled with stricter absorption and big trade thresholds for selective setups near key levels
- **Pure order flow reversals** — profile levels disabled, relying only on absorption and big trade activity to identify turning points
- **Conservative mode** — enable **Wait for bar close** for bar-close confirmation with higher thresholds for fewer, higher-quality trades

### Position Settings

GhostResistance supports up to 3 entries for position scaling, each with independent quantity, stop loss, and profit target. The same break-even and trail settings apply to all entries. Set a quantity to 0 to disable that entry.

| Setting | Default | Description |
|---|---|---|
| **Direction** | Any | Allowed trading direction — Long, Short, or Any |
| **Trading Instrument: enable** | false | Submit orders on a data series other than the chart series. Patterns are still evaluated on the chart series |
| **Trading Instrument: name** | MES 12-24 | Instrument of the trading data series |
| **Trading Instrument: period** | Minute | Bars period type of the trading data series |
| **Trading Instrument: value** | 1 | Bars period value of the trading data series, range: 1–∞ |
| **Enter by limit order** | false | Enter with a limit order at the big trade POC instead of a market order |
| **Cancel limit order type** | Bars | What measures the life of an unfilled limit order — None, Ticks, Bars, or Milliseconds |
| **Cancel limit order value** | 3 | How many ticks, bars, or milliseconds an unfilled limit order is left working before it is cancelled |
| **Quantity 1** | 1 | Contracts for the first entry, range: 1–∞ |
| **Profit target 1, ticks** | 40 | Profit target of the first entry in ticks, range: 1–∞ |
| **Stop loss 1, ticks** | 20 | Stop loss of the first entry in ticks, range: 1–∞ |
| **Quantity 2** | 2 | Contracts for the second entry; 0 disables it, range: 0–∞ |
| **Profit target 2, ticks** | 60 | Profit target of the second entry in ticks, range: 1–∞ |
| **Stop loss 2, ticks** | 20 | Stop loss of the second entry in ticks, range: 1–∞ |
| **Quantity 3** | 0 | Contracts for the third entry; 0 disables it, range: 0–∞ |
| **Profit target 3, ticks** | 80 | Profit target of the third entry in ticks, range: 1–∞ |
| **Stop loss 3, ticks** | 20 | Stop loss of the third entry in ticks, range: 1–∞ |
| **Breakeven** | false | Move the stop loss to the entry price once the position gains **Breakeven after, ticks** |
| **Breakeven after, ticks** | 10 | Profit in ticks that triggers the break-even move, range: 1–∞ |
| **Breakeven shift, ticks** | 1 | Ticks added to the break-even stop beyond the entry price; a positive value locks in that many ticks of profit |
| **Trail** | false | Enable the trailing stop |
| **Trail after, ticks** | 15 | Profit in ticks that activates the trail, range: 1–∞ |
| **Trail distance, ticks** | 10 | Distance the trailing stop keeps behind price, in ticks, range: 1–∞ |
| **Trail step, ticks** | 1 | Minimum price movement in ticks before the trailing stop is moved again, range: 1–∞ |

GhostResistance uses the same [trading time](#trading-time-settings) and [risk management](#risk-management-settings) settings as Footprint Action, and re-exposes the same four [Control Panel and dashboard](#control-panel-and-dashboard-defaults) settings with the same defaults.

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

### Common Export Settings

The **Export** category applies to all four exports.

| Setting | Default | Description |
|---|---|---|
| **Header** | true | Write the column header row at the top of each file |
| **Time** | true | Write a timestamp column as the first column |
| **Batch** | false | Accumulate records in memory and write them in one pass instead of after each record |
| **Signed volume** | false | Give volumes a sign — `+` for buy, `-` for sell |
| **Delimiter** | `;` | Column separator character |

Every setting in the four sections below is a column toggle unless noted otherwise: enabling it adds that column to the file, in the order the settings appear. All columns are off by default except the ones listed with default `true`.

### Footprint Export

Exported once per closed bar. Values not calculated by mzFootprint are written as empty strings or zeros — enable the corresponding indicator feature first.

| Setting | Default | Description |
|---|---|---|
| **Export** | true | Enable the footprint export |
| **Temporality** | Historical | When data is collected — Historical or Realtime. See [Temporality](#temporality) |
| **File** | `footprint\` | Output folder, relative to the strategy data folder |
| **Open** | true | Bar open price |
| **Close** | true | Bar close price |
| **High** | false | Bar high price |
| **Low** | false | Bar low price |
| **RangeTicks** | false | Bar range in ticks |
| **RangeLevels** | false | Bar range in price levels (clusters) |
| **Direction** | false | Bar direction — up or down |
| **DurationMs** | false | Bar duration in milliseconds |
| **Volumes** | false | Per-level total volume ladder |
| **Bids** | false | Per-level bid (sell) volume ladder |
| **Asks** | false | Per-level ask (buy) volume ladder |
| **Deltas** | false | Per-level delta ladder |
| **TradesNumbers** | false | Per-level trades count ladder |
| **TradesNumber** | false | Total number of trades in the bar |
| **Volume** | true | Bar total volume |
| **BuyVolume** | false | Bar ask-side volume |
| **SellVolume** | false | Bar bid-side volume |
| **Delta** | true | Bar delta — buy volume minus sell volume |
| **VAH** | false | Bar value area high price |
| **VAL** | false | Bar value area low price |
| **POC** | false | Bar Point of Control price |
| **POCVolume** | false | Volume at the bar POC |
| **BuyPercentage** | false | Buy volume as a percentage of bar volume |
| **SellPercentage** | false | Sell volume as a percentage of bar volume |
| **DeltaPercentage** | false | Delta as a percentage of bar volume |
| **MinDelta** | false | Lowest intra-bar cumulative delta reading |
| **MaxDelta** | false | Highest intra-bar cumulative delta reading |
| **DeltaChange** | false | Change in delta from the previous bar |
| **DeltaCumulative** | false | Session cumulative delta at bar close |
| **DeltaRate** | false | Delta rate — delta per unit of time |
| **DeltaRateHigh** | false | Highest intra-bar delta rate |
| **DeltaRateLow** | false | Lowest intra-bar delta rate |
| **AbsoluteDeltaAverage** | false | Average absolute per-level delta in the bar |
| **AbsoluteDeltaTotal** | false | Sum of absolute per-level deltas in the bar |
| **COTHigh** | false | Commitment of Traders high |
| **COTLow** | false | Commitment of Traders low |
| **RatioNumbers** | false | Ratio Numbers metric — volume of the level adjacent to the highest-volume level divided by that level's volume, an exhaustion measure |
| **VolumePerSecond** | false | Bar volume divided by bar duration in seconds |
| **UnfinishedAuctionHigh** | false | Price of an unfinished auction at the bar high, 0 if none |
| **UnfinishedAuctionLow** | false | Price of an unfinished auction at the bar low, 0 if none |
| **BuyImbalanceCount** | false | Number of buy imbalances in the bar |
| **SellImbalanceCount** | false | Number of sell imbalances in the bar |
| **BuyAbsorptionCount** | false | Number of buy absorptions in the bar |
| **SellAbsorptionCount** | false | Number of sell absorptions in the bar |
| **BuyStackedImbalanceCount** | false | Number of buy imbalances that belong to a stack |
| **SellStackedImbalanceCount** | false | Number of sell imbalances that belong to a stack |
| **BuyStackedAbsorptionCount** | false | Number of buy absorptions that belong to a stack |
| **SellStackedAbsorptionCount** | false | Number of sell absorptions that belong to a stack |
| **BuyStackedImbalanceMaxConsec** | false | Longest run of consecutive buy imbalances in the bar |
| **SellStackedImbalanceMaxConsec** | false | Longest run of consecutive sell imbalances in the bar |
| **BuyStackedAbsorptionMaxConsec** | false | Longest run of consecutive buy absorptions in the bar |
| **SellStackedAbsorptionMaxConsec** | false | Longest run of consecutive sell absorptions in the bar |
| **DeltaDivergence** | false | Delta divergence on the bar — 1 for buy divergence, -1 for sell divergence, 0 for none |
| **SessionOpen** | false | Session open price |
| **SessionClose** | false | Session close price |
| **SessionHigh** | false | Session high price |
| **SessionLow** | false | Session low price |
| **SeesionVAH** | false | Session value area high price |
| **SeesionVAL** | false | Session value area low price |
| **SessionPOC** | false | Session Point of Control price |

:::note
**SeesionVAH** and **SeesionVAL** are spelled that way in the NinjaTrader property grid.
:::

### Volume Profile Export

| Setting | Default | Description |
|---|---|---|
| **Export** | false | Enable the volume profile export |
| **Granularity** | Bar | One record per Bar or per Tick |
| **Temporality** | Historical | When data is collected — Historical or Realtime |
| **File** | `volumeprofile\` | Output folder, relative to the strategy data folder |
| **Open** | false | Profile open price |
| **Close** | false | Profile close price |
| **High** | false | Profile high price |
| **Low** | false | Profile low price |
| **RangeTicks** | false | Profile range in ticks |
| **MID** | false | Midpoint between the profile high and low |
| **DurationMs** | false | Profile duration in milliseconds |
| **TradesNumber** | false | Total number of trades in the profile |
| **Volume** | false | Profile total volume |
| **BuyVolume** | false | Profile ask-side volume |
| **SellVolume** | false | Profile bid-side volume |
| **Delta** | false | Profile delta |
| **VAH** | false | Value area high price |
| **VAL** | false | Value area low price |
| **POC** | false | Point of Control price |
| **POCVolume** | false | Volume at the POC |
| **TickPOC** | false | Tick POC price — the POC computed at single-tick resolution |
| **TickPOCVolume** | false | Volume at the tick POC |
| **VWAP** | false | Volume weighted average price |
| **_1StdDeviationPos** | false | VWAP plus one standard deviation |
| **_1StdDeviationNeg** | false | VWAP minus one standard deviation |
| **_2StdDeviationPos** | false | VWAP plus two standard deviations |
| **_2StdDeviationNeg** | false | VWAP minus two standard deviations |
| **DeltaPercentage** | false | Delta as a percentage of profile volume |
| **BuyPOCVolume** | false | Ask-side volume at the POC |
| **SellPOCVolume** | false | Bid-side volume at the POC |
| **VAVolume** | false | Total volume inside the value area |
| **TPO_POC** | false | TPO Point of Control price |
| **TPO_VAH** | false | TPO value area high price |
| **TPO_VAL** | false | TPO value area low price |
| **TPOLettersCount** | false | Number of TPO letters in the profile |

### Big Trade Export

Exported once per detected trade.

| Setting | Default | Description |
|---|---|---|
| **Export** | false | Enable the big trade export |
| **Temporality** | Historical | When data is collected — Historical or Realtime |
| **File** | `bigtrade\` | Output folder, relative to the strategy data folder |
| **High** | false | Highest price of the trade |
| **Low** | false | Lowest price of the trade |
| **Volume** | false | Trade volume |
| **IcebergVolume** | false | Iceberg volume within the trade |
| **Direction** | false | Trade side — 1 for buy, -1 for sell |
| **RangeTicks** | false | Price range swept by the trade, in ticks |
| **POC** | false | Price level of the trade that took the most volume |
| **POCVolume** | false | Volume at the trade POC |
| **DomPressureVolume** | false | DOM pressure volume associated with the trade |
| **DomSupportVolume** | false | DOM support volume associated with the trade |
| **Smart/Predatory** | false | Whether the trade was classified as smart/predatory — 1 or 0 |
| **TicksNumber** | false | Number of ticks the trade consists of; greater than 1 for a reconstructed trade |
| **Ticks** | false | The individual ticks of the trade |

### Market Depth Export

Exported on each order book update. Market depth has no Temporality setting — it is real time only.

| Setting | Default | Description |
|---|---|---|
| **Export** | false | Enable the market depth export |
| **File** | `orderbook\` | Output folder, relative to the strategy data folder |
| **MarketDepth** | false | Configured depth of the order book |
| **RealMarketDepth** | false | Actual number of levels the data feed delivered |
| **BestBid** | false | Best bid price |
| **BestOffer** | false | Best offer price |
| **RealtimeBids** | false | Bid sizes per level |
| **RealtimeOffers** | false | Offer sizes per level |
| **RealtimeBidsWithPrices** | false | Bid sizes paired with their price levels |
| **RealtimeOffersWithPrices** | false | Offer sizes paired with their price levels |
| **RealtimeBidVolume** | false | Total bid volume across the book |
| **RealtimeOfferVolume** | false | Total offer volume across the book |

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
