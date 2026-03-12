---
sidebar_position: 2
title: "mzFootprint"
description: "Order flow footprint chart indicator with bid/ask clusters, imbalance, absorption, and S/R zones for NinjaTrader 8"
---

# mzFootprint

The mzFootprint indicator displays order flow data as a footprint (cluster) chart overlaid on NinjaTrader price bars. Each bar is broken down by price level, showing bid and ask volumes, delta, imbalances, absorption patterns, and more.

**Data required:** Level 1 (tick data)

## Key Features

- **Footprint ladder** with bid/ask volumes at every price level
- **8 footprint styles** — BidAsk, Volume, Delta, DeltaPercentage, TradesNumber, Bid, Ask, None
- **Imbalance detection** with configurable ratio threshold and S/R zones
- **Absorption patterns** with 5 concurrent detection levels
- **Unfinished Auction** highlighting
- **Bar Volume Profile** with POC and Value Area per bar
- **Session/Daily Volume Profile Levels** — developing POC and VA lines
- **Statistics Grid** — 16 real-time metrics per bar
- **Bar Statistics** — summary row with volume, delta, COT, ratio numbers
- **Cluster Zones** — horizontal zones projected from significant clusters
- **Delta Divergence signals** — built-in divergence detection
- **Alerts and notifications** — sound, email, per-metric thresholds

## Footprint Styles

The indicator supports two independent footprint columns (Left and Right), each with its own style and settings.

| Style | Description |
|---|---|
| **BidAsk** | Classical bid x ask footprint — shows volume on bid and ask sides |
| **Volume** | Total traded volume per cluster |
| **Delta** | Bid-Ask volume difference (positive = buying pressure) |
| **DeltaPercentage** | Delta as a percentage of total volume |
| **TradesNumber** | Number of individual trades per cluster |
| **Bid** | Only bid-side volume |
| **Ask** | Only ask-side volume |
| **None** | Column hidden |

## Cluster Visualization

Each footprint column supports three cluster rendering styles:

| Style | Description |
|---|---|
| **Brick** | Solid color fill of the entire cluster cell |
| **Histogram** | Partial fill proportional to the cell's value relative to the bar/chart maximum |
| **None** | No color fill — text values only |

### Cluster Scaling

Controls how the histogram fill is calculated:

| Scale | Description |
|---|---|
| **Bar** | Scaled relative to the current bar's maximum value |
| **Chart** | Scaled across all visible bars on the chart |
| **All** | Scaled across all loaded bars |

### Data Sources

Each column has three independent data source settings:

- **Scale source** — which data determines histogram fill size (Volume, Delta, or TradesNumber)
- **Color source** — which data determines cell coloring
- **Gradient source** — which data drives the gradient/heatmap intensity

Enable **Auto sources** to have these set automatically based on the selected footprint style.

### Color Modes

| Mode | Description |
|---|---|
| **Solid** | Uniform color for all clusters |
| **Saturation** | Color intensity scales with value — higher values are more saturated |
| **Heatmap** | Multi-color gradient from cool to hot |
| **GrayScale Heatmap** | Monochrome intensity gradient |
| **Custom** | 4-level color thresholds — define volume breakpoints and assign a color to each level |

#### Custom Color Thresholds

When using Custom mode, you define up to 4 color levels:

| Setting | Description |
|---|---|
| **Custom 'less' filter** | Values below this get the "less" color |
| **Custom '>=' filter #1** | First threshold |
| **Custom '>=' filter #2** | Second threshold |
| **Custom '>=' filter #3** | Third threshold (highest) |

Each threshold has a corresponding color brush.

## Settings Reference

### Filters

| Setting | Default | Description |
|---|---|---|
| **Ticks per level** | 1 | Price level aggregation — set to 2+ to merge adjacent levels |
| **Trade min** | 0 | Minimum trade size to include |
| **Trade max** | -1 | Maximum trade size (-1 = unlimited) |

### Presentation

| Setting | Default | Description |
|---|---|---|
| **Display volume filter** | 0 | Hide clusters below this value |
| **Bid** | — | Color for bid-side background |
| **Ask** | — | Color for ask-side background |
| **Bid/Ask relative scaling** | true | Scale bid and ask sides relative to each other |
| **Auto-scale values** | true | Automatically adjust font size to fit cells |
| **Bar border** | false | Show border around each footprint bar |
| **Bar marker** | false | Show bar markers instead of candles |
| **Bar space, px** | 100 | Vertical space between bars |
| **Bar width, px** | 3 | Width of the bar marker |
| **Bar outer margin, px** | 8 | Horizontal space between bars |
| **Control right margin** | false | Let the indicator control chart right margin |
| **Chart right margin, px** | 40 | Custom right margin value |

### Bar Volume Profile

Per-bar volume distribution analysis.

| Setting | Default | Description |
|---|---|---|
| **POCs** | true | Show Point of Control |
| **POCs count** | 1 | Number of POC levels to display (1–10) |
| **Primary POC border** | Yellow, 2px | Style of the primary POC marker |
| **Other POCs border** | DarkOrange, 2px | Style of secondary POC markers |
| **Min width, px** | 0 | Minimum pixel width for POC marker |
| **VA** | true | Show Value Area |
| **VA, %** | 68 | Value Area percentage |
| **VA color** | White | Value Area fill color |
| **VA opacity, %** | 70 | Value Area transparency |

### Volume Profile Levels

Session or daily developing POC and Value Area lines.

| Setting | Default | Description |
|---|---|---|
| **Mode** | Session | Session or Daily profile calculation |
| **POC: enable** | false | Show session/daily POC line |
| **POC: developing** | true | Show developing POC (updates on each bar) |
| **POC: line** | Orange, 8px | POC line style |
| **VA: enable** | false | Show session/daily Value Area lines |
| **VA: developing** | true | Show developing VA |
| **VA: %** | 68 | Value Area percentage |
| **VA: line** | RoyalBlue, dotted, 6px | VA line style |

## Imbalance

Imbalance detection highlights clusters where the bid/ask volume ratio is disproportionate, indicating aggressive buying or selling.

| Setting | Default | Description |
|---|---|---|
| **Show** | true | Enable imbalance detection |
| **Only Imbalance** | false | Show only imbalanced cells (hide everything else) |
| **Imbalance, %** | 200 | Ratio threshold — e.g., 200% means one side must be 2x the other |
| **Filter** | 0 | Minimum volume on the imbalance side |
| **Sell/Resistance zone** | Red | Color for sell-side (bid) imbalance |
| **Buy/Support zone** | MediumSeaGreen | Color for buy-side (ask) imbalance |
| **Highlight values** | true | Color the text values of imbalanced cells |

### How Imbalance Works

mzFootprint calculates **diagonal imbalance**. A diagonal imbalance at the Ask side means the volume of filled Buy orders is greater by a given percentage than the volume of filled Sell orders at the price level just below:

**Formula:** `(AskVolume / BidVolume_below - 1) × 100`

**Example:** 71-lot Ask at 2384.50 vs 19-lot Bid at 2384.25:

`(71 / 19 - 1) × 100 = 274%`

With the default 200% threshold, this cluster is flagged as an imbalance.

**Absorption** is a diagonal imbalance combined with level rejection. The **Depth** parameter (in ticks) defines how far the price must bounce from the absorption level to qualify.

**S/R zone logic:**
- Imbalance levels on the **Ask side** create a **support zone**
- Imbalance levels on the **Bid side** create a **resistance zone**
- For **absorption**, the logic is reversed: Ask-side absorption creates resistance, Bid-side absorption creates support
- The more volume traded and the more consecutive levels in a zone, the stronger that zone is
- Zones can be canceled at session end (Break on session) or when price crosses and stays beyond the zone

### Imbalance Markers

When footprint values are not visible (zoomed out), markers indicate where imbalances occur:

| Setting | Default | Description |
|---|---|---|
| **Marker: visibility** | NoValues | When to show: None, NoValues, or Always |
| **Marker: type** | Dot | Shape: Dot or Cluster |
| **Marker: position** | Outer | Placement: Inner, Center, or Outer |

### Imbalance S/R Zones

Project horizontal support/resistance zones from consecutive imbalance levels:

| Setting | Default | Description |
|---|---|---|
| **S/R zones: enable** | false | Enable S/R zone projection |
| **S/R zones: consecutive levels** | 2 | Minimum stacked imbalance levels to form a zone |
| **S/R zones: volume filter** | 0 | Minimum volume for qualifying levels |
| **S/R zones: ended by** | ByBarHighLow | Zone termination rule: ByBarHighLow, ByBarClose, ByBarPOC, or ByBarTouch |
| **S/R zones: break on session** | true | End zones at session boundaries |
| **S/R zones: opacity, %** | 25 | Zone fill transparency |
| **S/R zones: alert** | false | Sound alert when price approaches a zone |

## Absorption

Absorption detects levels where aggressive orders are being absorbed by passive limit orders. The indicator supports **5 independent absorption levels**, each with its own threshold, depth, and colors.

Per-level settings (repeated for #1 through #5):

| Setting | Default (#1) | Description |
|---|---|---|
| **Show** | false | Enable this absorption level |
| **Absorption, %** | 68 | Ratio threshold for absorption detection |
| **Depth** | 1 | Number of adjacent price levels to consider |
| **Filter** | 0 | Minimum volume filter |
| **S/R zones: consecutive levels** | 2 | Stacked levels required for a zone |
| **S/R zones: volume filter** | 0 | Volume filter for zone qualification |
| **Sell/Support zone** | Cyan, 3px | Sell-side absorption zone color |
| **Buy/Resistance zone** | Orange, 3px | Buy-side absorption zone color |

Global absorption settings:

| Setting | Default | Description |
|---|---|---|
| **Only Absorption** | false | Show only absorption cells |
| **S/R zones: enable** | false | Enable absorption S/R zones |
| **S/R zones: ended by** | ByBarHighLow | Zone termination rule |
| **S/R zones: break on session** | true | End zones at session boundaries |
| **S/R zones: opacity, %** | 25 | Zone fill transparency |

## Unfinished Auction

An unfinished auction occurs when a bar closes with non-zero volume at the high or low — indicating the market did not fully auction that price level.

| Setting | Default | Description |
|---|---|---|
| **Show** | false | Enable unfinished auction highlighting |
| **Color** | Indigo | Cell background color |
| **Opacity, %** | 30 | Background transparency |
| **Border** | Indigo | Cell border style |

## Bar Statistics

Summary statistics displayed below or beside each footprint bar.

| Metric | Description |
|---|---|
| **Volume** | Total bar volume |
| **Delta** | Net delta (ask volume minus bid volume) |
| **Absolute Delta Average** | Average absolute delta across clusters |
| **Min/Max Delta** | Minimum and maximum delta within the bar |
| **Delta %** | Delta as a percentage of total volume |
| **COT** | COT High and Low values |
| **Ratio Numbers** | NEUTRAL / REJECTED / DEFENDED classification based on configurable bounds |

| Setting | Default | Description |
|---|---|---|
| **Values are x1000** | true | Divide displayed values by 1000 |
| **Values divider** | 1 | Additional custom divider for values |
| **Negative Delta** | Red | Color for negative delta |
| **Positive Delta** | Green | Color for positive delta |
| **Font** | Montserrat, 12pt | Statistics font |

### COT (Commitment Of Traders)

COT High and COT Low measure the cumulative delta from key price events:

- **COT High** — cumulative bid/ask delta starting from the moment the price makes a new high (or repeats the previous one). It reveals the buy/sell balance after a new high is reached.
- **COT Low** — the same logic applied at new lows.

**Trading interpretation:** A new high acts as a market test, and COT High is the reaction. If the price stays at highs while COT High is negative and growing in absolute value, this indicates strong support by buy limit orders.

### Ratio Numbers

Ratio Numbers classify bar activity into three states based on configurable bounds:

| Setting | Default | Description |
|---|---|---|
| **Ratio Numbers: bounds low** | 0.71 | Lower boundary for NEUTRAL |
| **Ratio Numbers: bounds high** | 29.0 | Upper boundary for NEUTRAL |
| **NEUTRAL** | Gray | Color when ratio is within bounds |
| **REJECTED/DEFENDED** | RoyalBlue | Color when ratio is outside bounds |

**Calculation:** For an up-bar, the ratio is bid volume above bar low divided by the bid volume at the bar low. For a down-bar, the ratio is ask volume below bar high divided by the ask volume at the bar high.

**Interpretation:**

| Ratio | State | Meaning |
|---|---|---|
| 0.71–29.0 | **NEUTRAL** | Market is facilitating trade at this level |
| > 29.0 | **REJECTED** | Price is being rejected — below an up-bar means lower prices rejected; above a down-bar means higher prices rejected |
| < 0.71 | **DEFENDED** | Price level is being defended by limit orders — below an up-bar means buyers supporting; above a down-bar means sellers defending |

## Statistics Grid

A detailed grid displaying up to 16 real-time metrics per bar, rendered alongside the footprint.

### Available Metrics

| Metric | Description |
|---|---|
| Trades | Number of trades |
| Volume | Total volume |
| Buy Volume | Buy-side volume |
| Sell Volume | Sell-side volume |
| Delta | Net delta |
| Delta % | Delta percentage |
| Absolute Delta Average | Average absolute delta |
| Delta Cumulative | Running cumulative delta |
| Min Delta | Minimum delta in bar |
| Max Delta | Maximum delta in bar |
| Delta Change | Delta change from previous bar |
| COT High | COT high value |
| COT Low | COT low value |
| Delta Rate | Rate of delta change (per tick or per millisecond) |
| Volume per Second | Volume arrival rate |
| Bar Duration | Time duration of the bar |

Each metric can be individually shown/hidden and has a configurable highlight threshold for visual emphasis.

| Setting | Default | Description |
|---|---|---|
| **Show** | false | Enable the statistics grid |
| **Show legend** | true | Display row labels |
| **Legend position** | Left | Label placement: Left or Right |
| **Grid in front of Footprint** | true | Render grid above the footprint |
| **Predicted values: show** | false | Show predicted values for incomplete bars |
| **Values are x1000** | true | Divide values by 1000 |
| **Cell height, px** | 24 | Height of each grid row |
| **Cell color scale** | Chart | Scale color intensity: Chart or All |
| **Auto-scale values** | true | Auto-fit text to cell size |
| **Auto-scale bars** | true | Scale bars to fit cell |
| **Font** | Montserrat, 12pt | Grid font |

### Delta Rate

Delta Rate measures the rate of delta change over a chosen time interval (milliseconds) or tick interval. When delta changes, the price also changes — the indicator shows the price range at which the delta rate occurred.

Only the **maximal** (by absolute value) Delta Rate is recorded and displayed per bar in the Statistics Grid and optionally on the chart as a vertical line.

**High Delta Rate indicates:**
- Stop-loss triggers cascading
- Price reversals
- Breakouts

### Predicted Values

Statistics values are **extrapolated proportionally to bar time**. A gauge shows the progress of the bar with a countdown to bar close. This feature is available for **time-based intraday bar types only**.

### Projecting Values on Chart

Each Statistics Grid metric has a `project` toggle and a `project threshold` setting. When enabled, cells exceeding the threshold are projected directly onto the chart, highlighting bars where that metric is significant.

**Example:** Enable `Volume: project` and set `Volume: project threshold` to highlight bars with notable volume directly on the price chart.

## Cluster Zones

Cluster zones project horizontal zones from significant volume clusters into the future, acting as potential support/resistance levels.

Each footprint column (Left/Right) has independent cluster zone settings:

| Setting | Default | Description |
|---|---|---|
| **Cluster Zones: enable** | false | Enable zone projection |
| **Cluster Zones: on bar close** | false | Only create zones after bar closes |
| **Cluster Zones: filter min** | 0 | Minimum cluster value to qualify |
| **Cluster Zones: filter max** | -1 | Maximum cluster value (-1 = unlimited) |
| **Cluster Zones: ignore bar high/low** | false | Exclude clusters at bar extremes |
| **Cluster Zones: ended by** | ByBarHighLow | Termination rule: ByBarHighLow or ByBarTouch |
| **Cluster Zones: break on session** | false | End zones at session boundaries |
| **Cluster Zones: style** | Zone | Display: Zone, Line, or None |
| **Cluster Zones: box** | false | Draw a box around the zone |

### Use Cases

Cluster Zones can identify different types of significant price levels depending on filter settings:

- **Low Volume Nodes (LVN):** Set a small `filter min` and `filter max` range to isolate low-volume clusters — areas where price moved quickly and may act as future breakout/breakdown levels
- **High Volume Nodes (HVN):** Set a large `filter min` threshold to capture high-volume clusters — areas of price acceptance that often act as magnets or support/resistance
- **Delta/Delta Percentage ranges:** Filter by delta values to find clusters with strong directional bias
- **Trades ranges:** Filter by number of trades to spot institutional or retail activity clusters

## Signals

Built-in delta divergence signal detection (licensed builds only).

| Setting | Default | Description |
|---|---|---|
| **Delta Divergence: enable** | false | Enable divergence signals |
| **Delta Divergence: volume threshold** | -1 | Minimum volume (-1 = any) |
| **Delta Divergence: delta threshold** | 100 | Minimum delta for signal |
| **Delta Divergence: alert** | false | Play sound on signal |

**Delta Divergence** is a trend reversal signal triggered on bar close:

- **LONG signal:** Price makes a new low with a bullish candle and positive delta
- **SHORT signal:** Price makes a new high with a bearish candle and negative delta

**Example:** A bearish bar making a new high with -135 delta. When the next bullish bar closes, the signal fires for a short trade.

For full divergence analysis, see the dedicated [mzDeltaDivergence](mzDeltaDivergence.md) indicator.

## Use Cases for ES

The following presets demonstrate common mzFootprint configurations for E-mini S&P 500 (ES). Each use case lists only settings that differ from defaults.

### Classic Bid/Ask Footprint

Standard order flow reading — see bid/ask volumes at every price level with visual emphasis on delta.

| Setting | Value |
|---|---|
| **Left: Footprint style** | BidAsk |
| **Left: Cluster style** | Brick |
| **Left: Color mode** | Saturation |
| **Left: Color source** | Delta |
| **POCs** | true |
| **POCs count** | 1 |
| **VA** | true |
| **VA, %** | 68 |

The default starting point for footprint analysis. Saturation mode highlights clusters where delta is strongest. POC and Value Area show where the most volume traded within each bar. Look for price rejection at Value Area boundaries.

### Delta Heatmap

Instantly spot aggressive buying and selling clusters across the chart.

| Setting | Value |
|---|---|
| **Left: Footprint style** | Delta |
| **Left: Cluster style** | Brick |
| **Left: Color mode** | Heatmap |
| **Left: Scale source** | Delta |
| **Left: Color source** | Delta |
| **Left: Gradient source** | Delta |
| **Display volume filter** | 50 |

Delta-only view with heatmap coloring turns each cell into a heat signature. Hot cells = aggressive activity. Filter out noise below 50 contracts. Useful on 5–15 min charts to find bars with hidden aggression that candlesticks don't reveal.

### Volume Clusters with Custom Thresholds

Highlight institutional volume levels on ES using fixed thresholds.

| Setting | Value |
|---|---|
| **Left: Footprint style** | Volume |
| **Left: Cluster style** | Brick |
| **Left: Color mode** | Custom |
| **Custom 'less' filter** | 500 |
| **Custom '>=' filter #1** | 500 |
| **Custom '>=' filter #2** | 1000 |
| **Custom '>=' filter #3** | 2000 |

Four color tiers make institutional activity stand out: cells under 500 get a muted color, 500+ first highlight, 1000+ second, 2000+ brightest. Adjust thresholds based on current ES average volume — these values work for regular trading hours.

### Imbalance Detection

Find price levels with aggressive one-sided order flow.

| Setting | Value |
|---|---|
| **Imbalance: Show** | true |
| **Imbalance, %** | 300 |
| **Imbalance: Filter** | 10 |
| **Imbalance: Highlight values** | true |
| **Imbalance: Marker: visibility** | Always |
| **Imbalance: Marker: type** | Dot |

A 300% threshold (3:1 ratio) ensures only strong imbalances are flagged. Filter of 10 removes noise from thin price levels. Dot markers visible at any zoom level. Stacked buy imbalances at bar lows indicate support; stacked sell imbalances at bar highs indicate resistance.

### Imbalance S/R Zones

Project support and resistance zones from consecutive imbalance levels.

| Setting | Value |
|---|---|
| **Imbalance: Show** | true |
| **Imbalance, %** | 200 |
| **Imbalance: Filter** | 10 |
| **S/R zones: enable** | true |
| **S/R zones: consecutive levels** | 3 |
| **S/R zones: volume filter** | 10 |
| **S/R zones: ended by** | ByBarClose |

Three consecutive imbalance levels required — produces fewer but higher-quality zones. ByBarClose termination is more conservative than ByBarHighLow: a zone survives wicks and only ends on a decisive close through it. Green zones = support, red zones = resistance.

### Absorption Pattern Detection

Detect where passive limit orders absorb aggressive market orders — exhaustion and reversal points.

| Setting | Value |
|---|---|
| **Absorption #1: Show** | true |
| **Absorption #1: Absorption, %** | 100 |
| **Absorption #1: Depth** | 2 |
| **Absorption #1: Filter** | 20 |
| **Absorption #2: Show** | true |
| **Absorption #2: Absorption, %** | 200 |
| **Absorption #2: Depth** | 1 |
| **Absorption #2: Filter** | 50 |
| **Absorption: S/R zones: enable** | true |
| **Absorption: S/R zones: ended by** | ByBarHighLow |

Two absorption levels work together: Level #1 (100%, depth 2) casts a wider net for moderate absorption, Level #2 (200%, depth 1) catches only strong absorption events with 50+ contracts. Absorption at bar extremes often precedes reversals. S/R zones project these levels forward.

### Unfinished Auction

Find bars with incomplete price auction — potential continuation or revisit levels.

| Setting | Value |
|---|---|
| **Unfinished Auction: Show** | true |
| **POCs** | true |
| **POCs count** | 1 |
| **POC: enable** | true |
| **POC: developing** | true |

An unfinished auction means the bar closed with volume still at the high or low — the market did not fully reject that price. These levels often get revisited. Combine with developing session POC to see whether unfinished levels align with the session's value center.

### Cluster Zones — High Volume Nodes

Project horizontal S/R zones from high-volume clusters.

| Setting | Value |
|---|---|
| **Left: Footprint style** | Volume |
| **Left: Cluster style** | Histogram |
| **Cluster Zones: enable** | true |
| **Cluster Zones: filter min** | 500 |
| **Cluster Zones: ignore bar high/low** | true |
| **Cluster Zones: on bar close** | true |
| **Cluster Zones: ended by** | ByBarHighLow |
| **Cluster Zones: style** | Zone |

Zones project from clusters with 500+ contracts, excluding bar highs/lows (which are often just wicks, not genuine support/resistance). "On bar close" prevents false zones from forming mid-bar. High-volume clusters act as magnets — price tends to revisit them.

### Delta Divergence Signals

Detect potential trend reversals using delta divergence.

| Setting | Value |
|---|---|
| **Delta Divergence: enable** | true |
| **Delta Divergence: volume threshold** | 5000 |
| **Delta Divergence: delta threshold** | 200 |
| **Delta Divergence: alert** | true |

A LONG signal fires when price makes a new low but the bar closes bullish with positive delta above 200 contracts — sellers failed to drive the close lower. Volume threshold of 5000 ensures the signal occurs on bars with enough participation to be meaningful. Works best on 5–15 min timeframes.

### Statistics Grid for Scalping

Real-time metrics dashboard for ES scalping — monitor volume, delta, and pace at a glance.

| Setting | Value |
|---|---|
| **Show** | true |
| **Show legend** | true |
| **Grid in front of Footprint** | false |
| **Cell color scale** | Chart |
| **Values are x1000** | true |

Enable these metrics: **Volume**, **Delta**, **Delta %**, **Delta Cumulative**, **Delta Rate**, **Volume per Second**.

Six key metrics per bar: Volume and Delta for size, Delta % for context, Cumulative Delta for session trend, Delta Rate for speed of flow, Volume per Second for tempo. Grid behind footprint keeps clusters readable. Color scale per chart view — hot cells show where the action is relative to visible bars.

## Performance Tips

mzFootprint is a tick-level indicator processing market data on every tick. To keep charts responsive:

**Reduce loading time:**
- Use **Tick Replay** for maximum historical precision (requires additional PC resources)
- Set **Days to load** to the minimum value you need
- Remove unused indicators from the chart — use the visibility toggle (eye button) to temporarily hide indicators you need only periodically
- Close unused shadow workspaces

**Optimize live rendering:**
- Set `MaximalRenderMs` to **20–50 ms** (under General > Optimize render performance). The chart may flash briefly but will remain responsive
- Set **Ticks per level** to 2 or more for instruments with many price levels
- This indicator supports **OnBarClose mode** for further optimization of system resources

## Non-Bid/Ask Data Support

Some markets (Forex, cryptocurrencies, NSE/Indian stock market) do not provide historical bid/ask data. Without it, all historical trades appear on the Bid side only.

**Solution:** Set `Orderflow > Calculation mode` to **UpDownTick** for these instruments.

**Hybrid mode (NSE):** NSE market data providers do not transmit historical bid/ask data. Use **Hybrid** mode, which applies UpDownTick calculation for historical data and BidAsk calculation for real-time data (100% accurate attribution for live trades).

**Recommendation:** For Forex pairs, use the relevant futures contract (e.g., 6E for EURUSD) to enable all order flow features including DOM analysis.

## Notifications

Configurable alerts for any metric crossing a threshold. Each alert supports:

- **Enable** — turn the alert on/off
- **Threshold** — trigger value
- **Sound** — alert sound file (see [Sound Files](/docs/getting-started/sound-files))
- **On bar close** — fire alerts only on completed bars
- **Email** — send email notifications (for imbalance/absorption alerts)

Available alert metrics: Trades, Volume, Buy Volume, Sell Volume, Delta, Delta %, Absolute Delta Average, Cumulative Delta, Delta Change, Delta Rate, COT High, COT Low, Left/Right Cluster, Imbalance, Absorption.
