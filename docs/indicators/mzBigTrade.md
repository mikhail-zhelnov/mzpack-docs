---
sidebar_position: 5
title: "mzBigTrade"
description: "Big trade detection indicator with iceberg orders, DOM pressure/support, aggression, and smart trade filtering for NinjaTrader 8"
---

import Image from '@theme/IdealImage';

# mzBigTrade

The mzBigTrade indicator detects and visualizes significant trades in the order flow. It aggregates tick data into trades, applies configurable volume and order flow filters, and renders the results as markers on the price chart. The indicator includes iceberg order detection, DOM pressure/support analysis, aggression (sweep) detection, and smart/predatory trade identification.

**Data required:** Level 1 (tick data)

## Key Features

- **2 presentation modes** — Default (markers on bars) and Tape (visual tape)
- **4 marker types** — Line, Bubble, Box, Bar
- **7 marker positions** — First, Last, Hi, Lo, POC, Stacked, StackedByTime
- **2 filter types** — Auto (statistical) and Manual (fine-grained)
- **Iceberg order detection** — Hard/Soft algorithms (real-time only) and the Tape algorithm, which also works on historical bars
- **Click to stack trades by time** — lay a bar's trades out as a time-ordered column
- **DOM pressure analysis** — refill-signature detection of defended (absorption) and pulled levels
- **DOM support detection** — Market-Limit order identification
- **Aggression (sweep) filter** — trades spanning multiple price levels
- **Smart/Predatory trade filter** — trades consuming all available liquidity
- **Selection filter** — percentage-based trade filtering
- **Volume-is-multiple-of filter** — detect rounded institutional sizes
- **Trades Volume Profile** — volume profile built from visible trades
- **4 color modes** — Solid, Saturation, Heatmap, GrayScaleHeatmap
- **Pop-up info** — detailed trade parameters on mouse hover
- **Alerts** — sound and email notifications for filtered trades

## Presentation Modes

| Mode | Description |
|---|---|
| **Default** | Trade markers are attached to chart bars at the price level where the trade occurred |
| **Tape** | Trade-by-trade visual tape scrolling across the chart. Trades that pass filters are rendered with configurable marker size; trades below filters appear as small dots |

In Tape mode, the tape can be placed over the chart, on the right margin, or on both. Use **Tape: position offset, px** to shift the tape left or right.

## Marker Types

| Marker | Description |
|---|---|
| **Line** | Horizontal line at the trade price level. Line length is proportional to trade volume. Configurable thickness scaling |
| **Bubble** | Circle marker. Size is proportional to trade volume. Shows volume text inside |
| **Box** | Rectangle marker. Size is proportional to trade volume. Shows volume text inside |
| **Bar** | Vertical bar spanning the full price range of the trade. Clearly shows the sweep range of aggressive trades |

## Marker Position

Controls where the marker is placed relative to the trade's price range:

| Position | Description |
|---|---|
| **First** | First tick of the trade |
| **Last** | Last tick of the trade |
| **Hi** | Highest price of the trade |
| **Lo** | Lowest price of the trade |
| **POC** | Point of Control — price level with the most volume in the trade |
| **Stacked** | Trades organized vertically as a chain within each bar (see Stacked Tape below) |
| **StackedByTime** | Trades of each bar laid out as a single time-ordered column (see Stacked by Time below) |

**Note:** Stacked and StackedByTime positions are available for Bubble and Box markers only.

### Stacked Tape

When Marker position is set to **Stacked**, trades are organized vertically by bar like a chain, in the order they arrive from the order flow. New buy trades are added at the top, and new sell trades at the bottom of each chain.

Stacked tape is useful when working with non-reconstructed tape or when there are many small trades for the instrument. Recommended for use on tick-based timeframes (e.g., 20 Ticks).

### Stacked by Time

When Marker position is set to **StackedByTime**, all trades of a bar are laid out as a single column ordered by trade time, earliest first. Buy and sell trades share the same column — unlike **Stacked**, where buys grow upward and sells grow downward from the trade price. This makes the sequence of the bar's order flow easy to read.

**Stacked by time: from bar edge** (default: true) anchors the column at the bar edge it grows from — the high for an up bar, the low for a down bar — instead of at the trade price.

#### Click to Stack

Instead of switching Marker position permanently, you can stack a single bar on demand. With **Click: stack trades by time** enabled (default), left-click a bar holding two or more trades to temporarily lay its trades out as a time-ordered column. Click any of its trades again to revert.

Click-to-stack is available in Default presentation mode, with Bubble, Box, or Bar markers, and with Marker position set to First, Last, Hi, Lo, or POC. The stacked state is temporary — it is not saved and resets when the chart or script reloads.

## Filtering

### Filter Type

| Type | Description |
|---|---|
| **Auto** | Automatic statistical filtering. The number of displayed trades is calculated as **Days x Trades per day**. The largest trades within that range are shown. Iceberg size, DOM pressure, and DOM support are also considered in the selection. This filter is calculated when historical data is loaded and does not change live |
| **Manual** | Fine-grained filtering with individual controls for trade volume, iceberg, DOM pressure, DOM support, and selection. Use **Logic** to combine filters |

**Note:** In Auto mode, the actual number of trades on the chart may exceed the calculated number if the loaded data spans more days than the Days value.

### Filter Logic

When using Manual filter type, the Logic setting controls how multiple enabled filters are combined:

| Logic | Description |
|---|---|
| **ANY** | A trade passes if **any** enabled filter condition is met |
| **ALL** | A trade passes only if **all** enabled filter conditions are met |

## Trade Volume Filter

The primary filter for selecting trades by volume:

- **Trade: min volume** — minimum trade size (default: 50)
- **Trade: max volume** — maximum trade size; set to -1 for unlimited (default: -1)

### Volume-is-Multiple-of

This filter identifies market participants trading with significant rounded sizes. When enabled, only trades whose volume is evenly divisible by the specified value are shown.

**Example:** With value set to 100, trades with volumes of 100, 200, 300, 400, etc. will be displayed.

## Iceberg Detection

Iceberg orders are large hidden orders executed in smaller visible portions. The indicator detects iceberg activity using three algorithms.

| Algorithm | Data required | Description |
|---|---|---|
| **Hard** | Live or Market Replay | Uses volumes on best bid/ask price levels to calculate the size of the hidden liquidity. Strict detection requiring strong evidence of iceberg behavior |
| **Soft** | Live or Market Replay | Adds positive DOM pressure (if any) to the iceberg size calculated by the Hard algorithm. Relaxed detection that flags more potential iceberg activity |
| **Tape** | Any, including historical | Estimates hidden refilling-iceberg volume from the trade's fill composition rather than from the order book |

Hard and Soft read the order book, so they work on **live or Market Replay data only** — NinjaTrader 8 does not provide the Level 2 data needed to reconstruct the book on historical bars. The Tape algorithm has no such limitation.

When iceberg volume is detected, the trade marker is rendered with a special border (Iceberg color). The iceberg border is shown if the iceberg value is greater than or equal to the iceberg filter threshold, even if the Iceberg filter is disabled.

### Tape Algorithm

The Tape algorithm looks at how a trade was filled. A refilling iceberg leaves a distinctive trace: a run of consecutive fills of identical size at the same price, as the hidden order is replenished after each hit. That run is called a **clip**.

Two thresholds define what counts as a clip:

- **Iceberg: tape min clip** (default: 20) — the minimum identical-fill size to consider.
- **Iceberg: tape min refills** (default: 3) — the minimum number of consecutive identical fills that qualify as a refilling iceberg.

For a confirmed clip of `N` fills of size `C`, the hidden volume is estimated as `(N − 1) × C`, plus the trailing partial fill when it does not exceed the clip size. The result is deduplicated against the order-book estimate at the trade's start price, so enabling Tape alongside Hard or Soft does not double-count the same liquidity.

Because it reads the stored fill composition of an already-reconstructed trade, the Tape algorithm works on cold historical data where the order book is unavailable. **Reconstruct tape** must be enabled — but unlike Hard and Soft, the Tape algorithm also works with **Reconstruct tape: timestamps only** enabled, which is what makes it the iceberg algorithm to use when [backtesting](../strategies/backtesting.md#4-tape-reconstruction-matching-historical-to-live).

**Tape** is an independent toggle, not a value of the **Iceberg: algorithm** setting — you can run it on its own or together with Hard/Soft. Its result is written into the same iceberg volume, so the iceberg filter threshold, **Marker size relative to = Iceberg**, the Iceberg Volume Profile, and the pop-up all use it unchanged. Changing a Tape parameter recalculates the chart on the fly, with no reload.

:::note
The Tape algorithm is not available in the free version.
:::

## DOM Pressure

DOM pressure measures how aggressively a price level at the best bid or ask is **defended** — repeatedly consumed by same-side market orders and replenished within a short window. It is derived from the Level 1 quote stream (the volumes resting at the best bid/ask). Rather than measuring the liquidity change at the moment a single trade executes, mzBigTrade now follows a price level across trades with a refill-signature engine.

A **signature** forms when a level is hit and refilled again and again. As long as the level keeps being replenished the signature stays open; it closes when refills stop (idle timeout) or price walks too far from the level. The net refilled volume becomes the trade's DOM pressure:

- **Positive DOM pressure** — the level was, on balance, **refilled** faster than it was consumed. Liquidity is being absorbed and the level acts as **resistance to the trend**
- **Negative DOM pressure** — the level was, on balance, **pulled**: more liquidity was withdrawn than replenished (requires **DOM pressure: track pulling**)

<Image img={require('./img/dom-pressure-example.png')} alt="DOM pressure example — a refill signature shown as a triangle with its span band" />
<!-- TODO(4.4.0): replace this placeholder with a real DOM pressure screenshot -->

DOM pressure detection is **feed-time based and available on live data and Market Replay only** — it does not run on cold historical bars. It is not available in the free version.

### Detection vs. Display Filters

The DOM pressure settings split into two groups:

- **Detection** (refill window, idle timeout, min refills, min volume, track pulling, max deviation from level) shape which signatures are recognized. They take effect only on freshly processed data, so changing one on a running chart prompts a chart reload.
- **Display filters** (min abs. volume, min traded sig volume, min hold duration, min/max intensity) decide which recognized signatures are shown. They apply **on the fly** with no reload. A trade shown only because of its DOM pressure disappears when it no longer passes; a trade that also passes the trade-volume filter keeps its marker but loses the triangle.

### Visualization

When **Show DOM pressure** is enabled, DOM pressure is drawn as a triangle in the Buy/Sell marker-border color, with the value printed inside it (auto-scaled). Negative DOM pressure (liquidity pulling) uses the **Liquidity pulling line** outline style.

As a level keeps being defended, its signature **re-anchors onto newer trades** ("moves right"), so the marker rides forward to the trade where the defense finally broke instead of appearing on the first hit.

Enable **Show DOM pressure span** to draw a 1-tick band at the level price spanning the signature's extent — from its first refill to the anchor trade — together with a proportion bar comparing the volume traded by the signature's refills against all volume traded at the level. Hovering the band shows that trade's pop-up.

The pop-up reports the signature on its own line, for example:

```
DOM pressure: 250-Lot (12) @7510.5 3.4s 74/s traded 180/240/75%
```

This reads as a net +250 contracts refilled across 12 refills at price 7510.5, held for 3.4 seconds at 74 contracts/s, with 180 of the 240 contracts traded at the level (75%) coming from the signature. The lead value is signed — a negative number means the level was net pulled.

**Note:** The DOM pressure filter uses the **absolute value** for comparison. For example, a trade with DOM pressure of -100 will pass a filter with min = 90 because abs(-100) > 90.

## DOM Support and Market-Limit Orders

DOM support describes liquidity added in the tail (same side) of an executed market order. For example, a buy trade with DOM support means contracts were added at the best Bid right after the order was executed.

Market-Limit orders are commonly used by institutional traders. A Market-Limit order executes at the best available price, and if only partially filled, the remaining quantity becomes a limit order at the specified price. The limit portion provides price support (for buys) or resistance (for sells).

To spot Market-Limit orders, enable the **DOM support** filter and also enable **Smart/Predatory** and **Aggression: min ticks** = 1 in Extra Filters.

When **Show DOM support** is enabled, DOM support is visualized with triangles in the same color as the trade marker.

## Aggression (Sweep) Filter

An aggressive trade consumes liquidity across two or more price levels to get filled. Aggressive trades can be:

- Initiative market orders sweeping through multiple levels
- Triggered stop-market orders causing a stop run
- Also called trades with a **sweep**

Aggressive trades are shown with a **dotted contour** on the marker.

The aggression filter measures the sweep range in ticks:

- **Aggression: min ticks** — minimum sweep range (default: 2)
- **Aggression: max ticks** — maximum sweep range; set to -1 for unlimited (default: -1)

**Tip:** Use the **Bar** marker type to clearly see the full price range of aggressive trades.

## Smart/Predatory Trades

A smart/predatory trade consumes **all available liquidity** on the best bid or ask. The frequency of smart/predatory trades depends on the instrument.

Enable the **Smart/Predatory: enable** filter to show only trades that fully sweep the top-of-book liquidity.

## Selection Filter

The Selection filter limits the number of visible trades based on percentage criteria. It is applied **on top of** the main filters.

| Type | Description |
|---|---|
| **PercentOfVolumes** | Only trades within the top N% of volumes are shown. The maximum trade volume is 100%. Example: with 68%, only trades with volume between 68–100% of the largest trade are displayed |
| **PercentOfNumber** | Only the top N% of all trades (by count) are shown. Use small values (1–0.01%) because there are typically thousands of trades on a chart |

## Marker Size Relative To

Controls what value determines the size of trade markers:

| Value | Description |
|---|---|
| **Volume** | Marker size is proportional to the trade's volume |
| **Iceberg** | Marker size is proportional to the detected iceberg volume |
| **DOMpressure** | Marker size is proportional to the DOM pressure value |
| **DOMsupport** | Marker size is proportional to the DOM support value |

When set to **Volume**, the **Max number of trades in chart frame** setting is available to limit marker density. This setting has priority over all filters.

## Trades Volume Profile

Displays a volume profile built from trades that are currently visible on the chart. The profile is linked to the **Marker size relative to** setting — for example, set it to **Iceberg** to build an Iceberg Volume Profile. In that case, icebergs at the offer side appear as sell volumes and icebergs at the bid side appear as buy volumes.

**Note:** The Iceberg filter must be enabled in the Filters category for the Iceberg VP to work.

## Color Modes

Controls how trade markers are colored:

| Mode | Description |
|---|---|
| **Solid** | Uniform selected color for all markers |
| **Saturation** | Color intensity scales with value — larger trades are more saturated. 4 saturation presets available |
| **Heatmap** | Multi-color gradient from cool to hot based on trade values |
| **GrayScaleHeatmap** | Monochrome intensity gradient |

## Pop-up Info

A floating window that shows all parameters of a trade when hovering over its marker. The pop-up displays trade volume, side, iceberg volume, DOM pressure, DOM support, aggression range, price levels, and timestamps.

Enable **Order ticks** to sort tick data by volume within the pop-up. When disabled, ticks are ordered by time as they arrive in the order flow.

When the Tape iceberg algorithm is enabled and a clip is detected, the pop-up adds a line describing it:

```
Clip: 5 x 57 @7510.5 (+14)
```

This reads as five refills of 57 contracts each at price 7510.5. The optional `(+14)` suffix is a trailing partial refill.

## Use Cases for ES

The following presets demonstrate common mzBigTrade configurations for E-mini S&P 500 (ES). Each use case lists only settings that differ from defaults.

### Institutional Block Trades

Spot large round-lot institutional orders.

| Setting | Value |
|---|---|
| **Type** | Manual |
| **Trade: min volume** | 200 |
| **Trade: volume is multiple of** | true |
| **Trade: volume is multiple of, value** | 100 |
| **Trade marker** | Bubble |
| **Color mode** | Saturation |

Large round-lot trades (200, 300, 500+ contracts) often originate from institutional algorithms. Saturation mode makes the biggest fills stand out visually. Hover over markers to inspect individual trade details.

### Iceberg Order Detection

Reveal hidden liquidity at key price levels. Requires real-time or Market Replay data.

| Setting | Value |
|---|---|
| **Type** | Manual |
| **Trade: min volume** | 50 |
| **Iceberg: enable** | true |
| **Iceberg: algorithm** | Hard |
| **Iceberg: min volume** | 50 |
| **Marker size relative to** | Iceberg |
| **Color mode** | Heatmap |
| **Trades Volume Profile: Show** | true |

Markers sized by iceberg volume reveal where hidden orders absorb price movement. Enable Trades Volume Profile to build an Iceberg VP — a volume profile based on detected iceberg sizes. Clusters of icebergs at a price level indicate strong hidden support/resistance.

### Historical Iceberg Detection (Tape)

Find refilling icebergs on historical bars, where the order book is unavailable.

| Setting | Value |
|---|---|
| **Type** | Manual |
| **Iceberg: enable** | true |
| **Iceberg: tape** | true |
| **Iceberg: tape min clip** | 20 |
| **Iceberg: tape min refills** | 3 |
| **Marker size relative to** | Iceberg |
| **Trades Volume Profile: Show** | true |

Unlike the Hard/Soft preset above, this configuration needs no real-time data — the Tape algorithm reconstructs hidden volume from each trade's fill composition. Lower **min refills** to 2 to catch shorter clips at the cost of more false positives; raise **min clip** on liquid instruments where small identical fills occur by chance. Hover a marker to see the detected clip.

### Aggressive Sweeps / Stop Runs

Identify trades sweeping multiple price levels — initiative orders or stop cascades.

| Setting | Value |
|---|---|
| **Type** | Manual |
| **Trade: min volume** | 100 |
| **Aggression: enable** | true |
| **Aggression: min ticks** | 3 |
| **Trade marker** | Bar |
| **Color mode** | Solid |

Bar marker shows the full price range swept. Dotted contour indicates aggression. Sweeps of 3+ ticks (0.75 pts on ES) often signal initiative activity or triggered stop-loss clusters. Combine with mzFootprint to see the footprint of the sweep.

### Smart Money / Market-Limit Orders

Detect institutional Market-Limit orders that leave a limit order residual in the book. Requires real-time or Market Replay data.

| Setting | Value |
|---|---|
| **Type** | Manual |
| **Logic** | ALL |
| **Trade: min volume** | 50 |
| **DOM support: enable** | true |
| **DOM support: min volume** | 20 |
| **Aggression: enable** | true |
| **Aggression: min ticks** | 1 |
| **Smart/Predatory: enable** | true |
| **Show DOM support** | true |
| **Trade marker** | Box |

Logic = ALL requires all conditions simultaneously — the trade must be smart/predatory (sweeps all top-of-book liquidity), have at least 1-tick aggression, and leave 20+ contracts of DOM support. Triangles in the marker color show the limit-order residual. Buy-side DOM support acts as price support; sell-side acts as resistance.

### Quick Overview (Auto Filter)

Fast setup with no manual tuning — see the most significant trades at any zoom level.

| Setting | Value |
|---|---|
| **Type** | Auto |
| **Days** | 5 |
| **Trades per day** | 15 |
| **Trade marker** | Bubble |
| **Color mode** | Heatmap |
| **Max number of trades in chart frame** | 150 |

Auto mode statistically selects the 75 largest trades (5 days × 15/day). Zoom in to see progressively smaller trades become visible. Heatmap coloring gives instant visual weight. Good starting point before switching to Manual for fine-tuning.

## Settings Reference

:::note
Default values apply to newly added indicator instances only. Saved templates and workspaces keep the values stored in them, so a setting whose default changed in a new release keeps its old value until you re-add the indicator or change the setting by hand.
:::

### Filters

| Setting | Default | Description |
|---|---|---|
| **Type** | Manual | Filter type — Auto or Manual |
| **Logic** | ANY | Filter logic — ANY or ALL (Manual mode only) |
| **Trade: enable** | true | Enable trade volume filtering (Manual mode only) |
| **Trade: min volume** | 50 | Minimum trade size (Manual mode only) |
| **Trade: max volume** | -1 | Maximum trade size, -1 = unlimited (Manual mode only) |
| **Trade: volume is multiple of** | false | Enable volume-is-multiple-of filter (Manual mode only) |
| **Trade: volume is multiple of, value** | 100 | Divisor value for the multiple-of filter (Manual mode only) |
| **Iceberg: enable** | false | Enable iceberg volume filtering (Manual mode only) |
| **Iceberg: algorithm** | Hard | Iceberg detection algorithm — Hard or Soft (Manual mode only) |
| **Iceberg: min volume** | 10 | Minimum iceberg volume (Manual mode only) |
| **Iceberg: tape** | false | Estimate hidden refilling-iceberg volume from the trade's fill composition. Complements the DOM-based Hard/Soft algorithm, including where the order book is unavailable (shown when Iceberg: enable is on) |
| **Iceberg: tape min clip** | 20 | Minimum identical-fill size to count as a clip (shown when Iceberg: tape is on) |
| **Iceberg: tape min refills** | 3 | Minimum number of consecutive identical fills to qualify as a refilling iceberg (shown when Iceberg: tape is on) |
| **DOM pressure: enable** | false | Enable DOM pressure filtering (Manual mode only) |
| **DOM pressure: min abs.volume** | 120 | Minimal DOM pressure size (absolute value) |
| **DOM pressure: max abs.volume** | -1 | Maximal DOM pressure size, -1 = unlimited |
| **DOM pressure: min traded sig volume** | 50 | Absorption: minimum volume traded at the level by the signature's committed refills (the "traded sig" value) for the DOM pressure to show. 1 disables. Applied on the fly |
| **DOM pressure: min hold duration (s)** | 10 | Level survivability: minimum time from the first to the last refill for the DOM pressure to show. 0 disables. Applied on the fly |
| **DOM pressure: min intensity (Σ/s)** | 3 | Replenisher reaction speed: minimum summed refill volume per second of hold for the DOM pressure to show. 0 disables. Applied on the fly |
| **DOM pressure: max intensity (Σ/s)** | 10 | Replenisher reaction speed: maximum summed refill volume per second of hold. -1 = no upper bound. Applied on the fly |
| **DOM pressure: refill window (ms)** | 150 | Detection: how long after a print a volume increase at that level still counts as a refill. Change prompts a chart reload |
| **DOM pressure: refill idle timeout (s)** | 10 | Detection: seconds without a new refill before the level is abandoned and the signature closes. Change prompts a chart reload |
| **DOM pressure: refill min refills** | 8 | Detection: minimum number of refills for a closed signature to count. 1 allows a single large refill. Change prompts a chart reload |
| **DOM pressure: refill min volume** | 2 | Detection: minimum summed refill volume of an episode to count. 1 disables the size test. Change prompts a chart reload |
| **DOM pressure: max deviation from level (ticks)** | 3 | Detection: close the signature once the near-side inside price is this many ticks from the level (a confirmed signature is kept, an in-process one discarded). OR'd with the idle timeout. -1 disables. Change prompts a chart reload |
| **DOM pressure: track pulling** | true | Detection: count liquidity pulled from the level (an L1 decrease inside the refill window) as negative volume, so a net-pulled level produces negative DOM pressure. Change prompts a chart reload |
| **DOM support: enable** | false | Enable DOM support filtering (Manual mode only) |
| **DOM support: min volume** | 5 | Minimum DOM support volume (Manual mode only) |
| **DOM support: max volume** | -1 | Maximum DOM support volume, -1 = unlimited (Manual mode only) |
| **Days** | 7 | Number of days for auto-filtering calculation (Auto mode only, range: 1–10) |
| **Trades per day** | 10 | Target trades per day for auto-filtering (Auto mode only, range: 1–100) |

### Extra Filters

Extra filters are applied on top of the main filters.

| Setting | Default | Description |
|---|---|---|
| **Aggression: enable** | false | Enable aggression (sweep range) filtering |
| **Aggression: min ticks** | 2 | Minimum sweep range in ticks |
| **Aggression: max, ticks** | -1 | Maximum sweep range in ticks, -1 = unlimited |
| **Smart/Predatory: enable** | false | Enable smart/predatory trade filtering |
| **Selection: enable** | false | Enable selection-based filtering (Manual mode only) |
| **Selection: type** | PercentOfVolumes | Selection criteria — PercentOfVolumes or PercentOfNumber (Manual mode only) |
| **Selection: percent of volumes, %** | 68 | Percentage of volumes to display (Manual mode only, PercentOfVolumes type) |
| **Selection: percent of number, %** | 68 | Percentage of trade count to display (Manual mode only, PercentOfNumber type) |

**Note:** The **Max number of trades in chart frame** setting (Presentation) has priority over all filters.

### Presentation

| Setting | Default | Description |
|---|---|---|
| **Type** | Default | Presentation mode — Default or Tape |
| **Tape: position** | ChartAndRightMargin | Tape placement — Chart, RightMargin, or ChartAndRightMargin (Tape mode only) |
| **Tape: position offset, px** | -20 | Tape horizontal offset in pixels; negative values shift left (Tape mode only) |
| **Tape: speed** | 10 | Tape visual scrolling speed, range: 10–50 (Tape mode only) |
| **Tape: refresh, ms** | 500 | Tape refresh interval in milliseconds, range: 200–500 (Tape mode only) |
| **Tape: min marker size, px** | 6 | Minimum marker size in Tape mode, range: 4–20 (Tape mode only) |
| **Tape: max marker size, px** | 80 | Maximum marker size in Tape mode, range: 20–150 (Tape mode only) |
| **Marker size relative to** | Volume | What value determines marker size — Volume, Iceberg, DOMpressure, or DOMsupport (Default mode only) |
| **Max number of trades in chart frame** | 100 | Maximum trades displayed in the visible chart frame, range: 1–800. Has priority over all filters (Default mode only, Volume marker base only) |
| **Trade marker** | Bubble | Marker shape — Line, Bubble, Box, or Bar |
| **Marker position** | Last | Marker placement — First, Last, Hi, Lo, POC, Stacked, or StackedByTime (Default mode only, non-Bar markers) |
| **Stacked by time: from bar edge** | true | Anchor the Stacked-by-time column at the bar edge it grows from (high for up bars, low for down bars) instead of the trade price. Shown when the StackedByTime position or click-to-stack is active |
| **Click: stack trades by time** | true | Left-click a bar with 2+ trades to temporarily lay its trades out as a time-ordered column. Not saved on reload (Default mode only, Bubble/Box/Bar markers at First/Last/Hi/Lo/POC) |
| **Buy line** | LimeGreen, 6px | Buy-side line style (Line marker only) |
| **Sell line** | Red, 6px | Sell-side line style (Line marker only) |
| **Max line length** | 300 | Maximum line length in chart bars (Line marker only) |
| **Scale line thickness** | true | Scale line thickness proportionally to trade volume (Line marker only) |
| **Max shape extent** | 5 | Maximum bubble/box extent in bar spaces (Default mode only, Bubble/Box markers) |
| **Buy shape color** | LimeGreen | Buy-side marker fill color (Bubble/Box/Bar markers) |
| **Buy shape border** | LimeGreen, 1px | Buy-side marker border style (Bubble/Box/Bar markers) |
| **Sell shape color** | Red | Sell-side marker fill color (Bubble/Box/Bar markers) |
| **Sell shape border** | Red, 1px | Sell-side marker border style (Bubble/Box/Bar markers) |
| **Iceberg color** | Fuchsia, dashed, 2px | Border style for trades with detected iceberg orders |
| **Color mode** | Saturation | Color rendering mode — Solid, Saturation, Heatmap, or GrayScaleHeatmap |
| **Saturation** | 2 | Saturation preset level, range: 1–4 |
| **Show DOM pressure** | true | Display DOM pressure with triangles |
| **Show DOM support** | false | Display DOM support with triangles |
| **DOM pressure/support triangle thickness** | 2 | Triangle line thickness (5 preset levels). Hidden unless a triangle is shown |
| **Liquidity pulling line** | Gray, dotted, 2px | Line style for negative DOM pressure (liquidity pulling) triangles |
| **Show DOM pressure span** | false | Draw the DOM pressure signature extent: a 1-tick band from the signature start to the anchor trade, plus a traded-sig/level proportion bar |
| **Trade POC: show** | false | Show Point of Control line for each trade (non-Line markers) |
| **Trade POC: line** | Orange, 3px | Trade POC line style |
| **Volume text: position** | Inside | Volume label placement — Inside, OutsideLeft, OutsideRight, or Off |
| **Volume text: auto-scale** | true | Automatically adjust volume text size based on chart zoom |
| **Volume text: font** | Montserrat, 12pt | Font for volume labels |
| **Buy volume in shape color** | ForestGreen | Volume text color inside buy markers (Bubble/Box/Bar markers) |
| **Sell volume in shape color** | Red | Volume text color inside sell markers (Bubble/Box/Bar markers) |

### Trades Volume Profile

| Setting | Default | Description |
|---|---|---|
| **Show** | true | Display the trades volume profile |
| **Width** | 200 | Profile width in pixels, range: 100–2000 |
| **Position** | Left | Profile placement — Left, Right, or RightOnChartMargin |
| **Margin** | 0 | Profile margin in pixels, range: 0–2000 |
| **Buy color** | LimeGreen | Buy-side profile bar color |
| **Sell color** | Red | Sell-side profile bar color |
| **Show volumes** | true | Display volume values on profile bars |
| **Volumes color** | White | Volume text color |
| **Background color** | Transparent | Profile background color (set to Transparent for no background) |

### Other

| Setting | Default | Description |
|---|---|---|
| **Draw lines on right margin** | true | Extend Line markers onto the chart right margin (Line marker mode) |
| **Show pop-up info** | true | Show detailed trade info on mouse hover |
| **Order ticks in pop-up** | true | Sort ticks by volume in pop-up. When disabled, ticks are shown in time order |
| **Pop-up info font** | Montserrat, 12pt | Font for the pop-up window |
| **Volumes font** | Montserrat, 12pt | Font for volume profile text |

### Notifications

| Setting | Default | Description |
|---|---|---|
| **Alert** | false | Enable alert on filtered trade or iceberg |
| **Buy sound** | bigtrade.wav | Sound file for buy trade alerts |
| **Sell sound** | bigtrade.wav | Sound file for sell trade alerts |
| **Send Email** | false | Send email notification on filtered trade |
| **Email address** | — | Destination email address |

:::tip
See [Sound Files](/docs/getting-started/sound-files) for the full list of pre-installed sounds and how to add custom WAV files.
:::

## Reconstruct Tape Mode

The MZpack order flow core reconstructs individual tick trades into aggregated trades. The settings below (group **Orderflow**) control reconstruction behavior.

| Setting | Default | Description |
|---|---|---|
| **Reconstruct tape** | true | Reconstruct tape using timestamps and Level 1 (best bid/ask) events. Required for Iceberg detection, DOM pressure, and DOM support |
| **Reconstruct tape: timestamps only** | false | Use only timestamps for reconstruction — Level 1 (best bid/ask) events are ignored, including for live data, and trades with equal timestamps are merged. Enable to get an exact match between reconstructed historical and reconstructed live data — recommended for [backtesting](../strategies/backtesting.md#4-tape-reconstruction-matching-historical-to-live). Hard/Soft iceberg detection, DOM pressure, and DOM support are unavailable when enabled; the **Tape** iceberg algorithm still works |
| **'Reconstruct tape' apply** | ChartReload | `ChartReload` — reload the chart to apply changes (minimizes memory). `OnTheFly` — apply changes without reloading (requires more memory). mzBigTrade only |

**Note:** Disabling Reconstruct tape or using the OnTheFly method significantly increases memory consumption. Hard/Soft iceberg detection, DOM pressure, and DOM support require Reconstruct tape to be enabled **with timestamps-only mode disabled**, because they all rely on the Level 1 events that this mode discards. DOM pressure and DOM support additionally need the **volumes** resting at the best bid/ask, which Tick Replay does not reconstruct, so they run on **live data and Market Replay only**. The [Tape iceberg algorithm](#tape-algorithm) only requires Reconstruct tape — it works in timestamps-only mode as well.

## Non-Bid/Ask Data Support

Some markets (Forex, cryptocurrencies, NSE/Indian stock market) do not provide historical bid/ask data. Without it, all historical trades appear on the Bid side only.

**Solution:** Set `Orderflow > Calculation mode` to **UpDownTick** for these instruments.

**Hybrid mode (NSE):** NSE data providers do not transmit historical bid/ask data. Use **Hybrid** mode, which applies UpDownTick calculation for historical data and BidAsk for real-time data.

**Recommendation:** For Forex pairs, use the relevant futures contract (e.g., 6E for EURUSD) to get accurate bid/ask data and full order flow features.
