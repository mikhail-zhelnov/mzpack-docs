---
sidebar_position: 2
title: "mzFootprint"
description: "Order flow footprint chart indicator with bid/ask clusters, imbalance, absorption, and S/R zones for NinjaTrader 8"
---

import Image from '@theme/IdealImage';

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

<Image img={require('./img/footprint-styles-three-comparison.png')} alt="Footprint styles: BidAsk, Volume, Delta" />

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

When Color mode is set to **Custom**, cluster color is chosen from four value bands. Each band has a threshold and a color. These settings exist separately for the Left and Right columns.

| Setting | Default | Description |
|---|---|---|
| **Custom 'less' filter** | 1500 | Clusters below this value use the "less" color, range: 0–∞ |
| **Custom '&gt;=' filter #1** | 1500 | Clusters at or above this value use color #1, range: 0–∞ |
| **Custom '&gt;=' filter #2** | 2500 | Clusters at or above this value use color #2, range: 0–∞ |
| **Custom '&gt;=' filter #3** | 3000 | Clusters at or above this value use color #3, range: 0–∞ |
| **Custom color 'less'** | Teal | Color for clusters below the 'less' filter |
| **Custom color #1** | DarkGray | Color for clusters at or above filter #1 |
| **Custom color #2** | RoyalBlue | Color for clusters at or above filter #2 |
| **Custom color #3** | Red | Color for clusters at or above filter #3 |

The value compared against the thresholds is the one selected by **Color source**.

## Settings Reference

:::note
**General**, **Orderflow**, and **Levels** settings are shared by all MZpack indicators and are documented in [Common Settings](./common-settings.md).
:::

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

### General

Two settings are hidden in the shared [General](./common-settings.md#general) category and re-exposed by mzFootprint.

| Setting | Default | Description |
|---|---|---|
| **Optimize render performance** | false | Skip rendering detail when a frame would exceed **Maximal render time, ms**, keeping the chart responsive on heavy footprints |
| **Maximal render time, ms** | 100 | Render time budget per frame for this indicator instance. 20–50 ms is a good starting point, range: 1–200 |

### Footprint Columns

The Left and Right columns are configured independently — every setting below appears twice in the properties grid, once under **Left Footprint** and once under **Right Footprint**. Defaults are identical for both columns except **Footprint style**: the Left column defaults to Bid, the Right column to Ask.

| Setting | Default | Description |
|---|---|---|
| **Footprint style** | Bid (left) / Ask (right) | What the column shows — BidAsk, Volume, Delta, DeltaPercentage, TradesNumber, Bid, Ask, or None |
| **Cluster style** | Brick | Cluster fill style — Brick, Histogram, or None |
| **Cluster scale** | Bar | What the histogram fill is scaled against — Bar, Chart, or All |
| **Auto sources** | true | Set Scale, Color, and Gradient source automatically from the chosen footprint style |
| **Scale source** | Volume | Data that determines histogram fill size — Volume, Delta, or TradesNumber |
| **Color source** | Volume | Data that determines cluster color |
| **Gradient source** | Volume | Data that drives gradient and heatmap intensity |
| **Cluster** | SteelBlue | Base cluster color, used in Solid and Saturation color modes |
| **Negative Delta** | Red | Cluster color when the delta-driven color source is negative |
| **Positive Delta** | DarkGreen | Cluster color when the delta-driven color source is positive |
| **Cluster border** | DimGray | Stroke drawn around each cluster cell |
| **Color mode** | Saturation | How color is applied — Solid, Saturation, Heatmap, GrayScaleHeatmap, or Custom. See [Custom Color Thresholds](#custom-color-thresholds) |
| **Values: show** | true | Print the numeric value inside each cluster |
| **Values: align** | Center | Value placement inside the cell — Inner or Center |
| **Values: divider** | 1 | Divide displayed values by this number to fit them into narrow cells, range: 1–∞ |
| **Values: decimal places** | 1 | Decimal places shown after dividing |
| **Values: abs Delta/DeltaPercentage** | true | Print Delta and Delta % without a sign. Disable to see signed values when Color source is Delta |
| **Values: color** | DimGray | Color of the value text |
| **Values: font** | Montserrat, 12pt | Font of the value text |

### Bar Volume Profile

Per-bar volume distribution analysis.

| Setting | Default | Description |
|---|---|---|
| **POCs** | true | Show Point of Control |
| **POCs count** | 1 | Number of POC levels to display (1–10) |
| **Primary POC border** | Yellow, 2px | Style of the primary POC marker |
| **Other POCs border** | DarkOrange, 2px | Style of secondary POC markers |
| **Min width, px** | 0 | Minimum pixel width for POC marker |
| **VA** | true | Show the Value Area |
| **VA, %** | 68 | Percentage of bar volume the Value Area covers, range: 1–100 |
| **VA** | LightSkyBlue | Value Area fill color. A second setting with the same label, listed after **VA, %** |
| **VA opacity, %** | 70 | Value Area fill transparency, range: 1–100 |

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

<Image img={require('./img/footprint-imbalance-diagonal-chart.png')} alt="Diagonal imbalance calculation on footprint" />

### Imbalance Markers

When footprint values are not visible (zoomed out), markers indicate where imbalances occur:

| Setting | Default | Description |
|---|---|---|
| **Marker: visibility** | NoValues | When to show: None, NoValues, or Always |
| **Marker: type** | Dot | Shape: Dot or Cluster |
| **Marker: position** | Outer | Placement: Inner, Center, or Outer |
| **Marker: min width, px** | 0 | Minimum marker width in pixels; a value above 0 keeps imbalance markers visible on compressed charts, range: 0–20 |

### Imbalance S/R Zones

Project horizontal support/resistance zones from consecutive imbalance levels:

| Setting | Default | Description |
|---|---|---|
| **S/R zones: enable** | false | Enable S/R zone projection |
| **S/R zones: consecutive levels** | 2 | Minimum stacked imbalance levels to form a zone |
| **S/R zones: volume filter** | 0 | Minimum volume for qualifying levels |
| **S/R zones: ended by** | ByBarHighLow | Zone termination rule: ByBarHighLow, ByBarClose, ByBarPOC, or ByBarTouch |
| **S/R zones: approaching, ticks** | 0 | Price may terminate a zone from this distance in ticks instead of having to reach it; 0 requires price to reach the zone |
| **S/R zones: break on session** | true | End zones at session boundaries |
| **S/R zones: opacity, %** | 25 | Zone fill transparency, range: 1–100 |
| **S/R zones: alert** | false | Sound alert when price reaches a zone |
| **S/R zones: alert on bar close** | false | Fire the alert only on bar close instead of on each tick |
| **S/R zones: support zone sound** | imbalance_support_zone.wav | Sound played when price reaches a support zone |
| **S/R zones: resistance zone sound** | imbalance_resistance_zone.wav | Sound played when price reaches a resistance zone |

<Image img={require('./img/footprint-sr-zones-chart.png')} alt="Imbalance S/R zones on chart" />

## Absorption

Absorption detects levels where aggressive orders are being absorbed by passive limit orders. The indicator supports **5 independent absorption levels**, each with its own threshold, depth, and colors.

Per-level settings (repeated for #1 through #5):

| Setting | Default (#1) | Description |
|---|---|---|
| **Show** | false | Enable this absorption level |
| **Absorption, %** | 68 | Ratio threshold for absorption detection |
| **Depth** | 1 | How far price must bounce from the absorption level to qualify, in ticks |
| **Filter** | 0 | Minimum volume filter |
| **S/R zones: consecutive levels** | 2 | Stacked levels required for a zone |
| **S/R zones: volume filter** | 0 | Volume filter for zone qualification |
| **Sell/Support zone** | Cyan, 3px | Sell-side absorption zone color |
| **Buy/Resistance zone** | Orange, 3px | Buy-side absorption zone color |

Global absorption settings:

| Setting | Default | Description |
|---|---|---|
| **Only Absorption** | false | Show only absorption cells |
| **Min width, px** | 0 | Minimum on-screen width of the absorption marker; a value above 0 keeps absorption visible on compressed charts, range: 0–20 |
| **S/R zones: enable** | false | Enable absorption S/R zones |
| **S/R zones: ended by** | ByBarHighLow | Zone termination rule |
| **S/R zones: approaching, ticks** | 0 | Price may terminate a zone from this distance in ticks instead of having to reach it; 0 requires price to reach the zone |
| **S/R zones: break on session** | true | End zones at session boundaries |
| **S/R zones: opacity, %** | 25 | Zone fill transparency, range: 1–100 |
| **S/R zones: alert** | false | Sound alert when price reaches a zone |
| **S/R zones: alert on bar close** | false | Fire the alert only on bar close instead of on each tick |
| **S/R zones: support zone sound** | absorption_support_zone.wav | Sound played when price reaches a support zone |
| **S/R zones: resistance zone sound** | absorption_resistance_zone.wav | Sound played when price reaches a resistance zone |

<Image img={require('./img/footprint-absorption-zones-chart.png')} alt="Absorption zones at bar extremes" />

## Unfinished Auction

An unfinished auction occurs when a bar closes with non-zero volume at the high or low — indicating the market did not fully auction that price level.

| Setting | Default | Description |
|---|---|---|
| **Show** | false | Enable unfinished auction highlighting |
| **Color** | Indigo | Cell background color |
| **Opacity, %** | 30 | Background transparency |
| **Border** | Indigo | Cell border style |
| **Min width, px** | 0 | Minimum on-screen width of the unfinished auction marker; a value above 0 keeps it visible on compressed charts, range: 0–20 |

## Bar Statistics

Summary statistics displayed below each footprint bar. Each metric is a separate toggle.

| Setting | Default | Description |
|---|---|---|
| **Volume** | true | Show total bar volume |
| **Delta** | true | Show bar delta — ask volume minus bid volume |
| **Absolute Delta Average** | false | Show the average absolute delta across the bar's price levels |
| **Min/Max Delta** | true | Show the lowest and highest intra-bar delta readings |
| **Delta %** | true | Show delta as a percentage of bar volume |
| **COT** | true | Show COT High and COT Low |
| **Ratio Numbers: enable** | false | Show the NEUTRAL / REJECTED / DEFENDED ratio |
| **Ratio Numbers: bounds low** | 0.71 | Lower boundary of the NEUTRAL band, range: 0–∞ |
| **Ratio Numbers: bounds high** | 29.0 | Upper boundary of the NEUTRAL band, range: 0–∞ |
| **Ratio Numbers: NEUTRAL** | Gray | Color when the ratio is inside the bounds |
| **Ratio Numbers: REJECTED/DEFENDED** | RoyalBlue | Color when the ratio is outside the bounds |
| **Values are x1000** | true | Display values divided by 1000 |
| **Values divider** | 1 | Additional custom divider applied to displayed values, range: 1–∞ |
| **Negative Delta** | Red | Text color for negative delta |
| **Positive Delta** | Green | Text color for positive delta |
| **Font** | Montserrat, 12pt | Font of the statistics row |

### COT (Commitment Of Traders)

COT High and COT Low measure the cumulative delta from key price events:

- **COT High** — cumulative bid/ask delta starting from the moment the price makes a new high (or repeats the previous one). It reveals the buy/sell balance after a new high is reached.
- **COT Low** — the same logic applied at new lows.

**Trading interpretation:** A new high acts as a market test, and COT High is the reaction. If the price stays at highs while COT High is negative and growing in absolute value, this indicates strong support by buy limit orders.

### Ratio Numbers

Ratio Numbers classify bar activity into three states based on the **Ratio Numbers: bounds low** and **bounds high** settings above.

**Calculation:** For an up-bar, the ratio is bid volume above bar low divided by the bid volume at the bar low. For a down-bar, the ratio is ask volume below bar high divided by the ask volume at the bar high.

**Interpretation:**

| Ratio | State | Meaning |
|---|---|---|
| 0.71–29.0 | **NEUTRAL** | Market is facilitating trade at this level |
| > 29.0 | **REJECTED** | Price is being rejected — below an up-bar means lower prices rejected; above a down-bar means higher prices rejected |
| < 0.71 | **DEFENDED** | Price level is being defended by limit orders — below an up-bar means buyers supporting; above a down-bar means sellers defending |

## Statistics Grid

A detailed grid displaying up to 16 real-time metrics per bar, rendered alongside the footprint.

<Image img={require('./img/footprint-statistics-grid-chart.png')} alt="Statistics grid with 6 metrics per bar" />

### Metrics

Each metric is one row of the grid. Most metrics have three settings: `show` adds the row, `project` draws qualifying cells onto the price chart, and `project threshold` is the value a cell must exceed to be projected (see [Projecting Values on Chart](#projecting-values-on-chart)). All project thresholds accept a range of 0–∞ and default to 0.

| Setting | Default | Description |
|---|---|---|
| **Trades: show** | false | Number of trades in the bar |
| **Trades: project** | false | Project the Trades cell onto the chart |
| **Trades: project threshold** | 0 | Trades value above which the cell is projected |
| **Volume: show** | true | Bar volume |
| **Volume: project** | false | Project the Volume cell onto the chart |
| **Volume: project threshold** | 0 | Volume above which the cell is projected |
| **Buy volume: show** | false | Bar ask-side volume |
| **Sell volume: show** | false | Bar bid-side volume |
| **Delta: show** | true | Bar delta |
| **Delta: project** | false | Project the Delta cell onto the chart |
| **Delta: project threshold** | 0 | Absolute delta above which the cell is projected |
| **Delta %: show** | true | Delta as a percentage of bar volume |
| **Delta %: project** | false | Project the Delta % cell onto the chart |
| **Delta %: project threshold** | 0 | Delta percentage above which the cell is projected |
| **Absolute Delta Average: show** | false | Average absolute delta across the bar's price levels |
| **Absolute Delta Average: project** | false | Project the Abs Delta avr cell onto the chart |
| **Absolute Delta Average: project threshold** | 0 | Value above which the cell is projected |
| **Delta Cumulative: show** | true | Session cumulative delta |
| **Delta Cumulative: project** | false | Project the Cum Delta cell onto the chart |
| **Delta Cumulative: project threshold** | 0 | Value above which the cell is projected |
| **Min Delta: show** | false | Lowest intra-bar delta reading |
| **Min Delta: project** | false | Project the Min Delta cell onto the chart |
| **Min Delta: project threshold** | 0 | Value above which the cell is projected |
| **Max Delta: show** | false | Highest intra-bar delta reading |
| **Max Delta: project** | false | Project the Max Delta cell onto the chart |
| **Max Delta: project threshold** | 0 | Value above which the cell is projected |
| **Delta change: show** | false | Delta change from the previous bar |
| **Delta change: project** | false | Project the Delta chng cell onto the chart |
| **Delta change: project threshold** | 0 | Value above which the cell is projected |
| **Delta rate: show** | false | Maximal delta rate in the bar. See [Delta Rate](#delta-rate) |
| **Delta rate: type** | Tick | Interval the rate is measured over — Tick or Millisecond |
| **Delta rate: type value** | 100 | Size of that interval, in ticks or milliseconds. Changing it reloads historical data |
| **Delta rate: show in bar** | false | Draw a vertical line on the bar at the price range where the maximal delta rate occurred |
| **Delta rate: project** | false | Project the Delta rate cell onto the chart |
| **Delta rate: project threshold** | 0 | Value above which the cell is projected |
| **COT High: show** | false | COT High value |
| **COT High: project** | false | Project the COT High cell onto the chart |
| **COT High: project threshold** | 0 | Value above which the cell is projected |
| **COT Low: show** | false | COT Low value |
| **COT Low: project** | false | Project the COT Low cell onto the chart |
| **COT Low: project threshold** | 0 | Value above which the cell is projected |
| **Volume per second: show** | false | Volume arrival rate |
| **Volume per second: project** | false | Project the Vol/sec cell onto the chart |
| **Volume per second: project threshold** | 0 | Value above which the cell is projected |
| **Bar duration: show** | false | Elapsed time of the bar |

### Grid Appearance

| Setting | Default | Description |
|---|---|---|
| **Show** | false | Enable the statistics grid |
| **Show legend** | true | Display the row labels column |
| **Legend position** | Left | Label placement — Left or Right |
| **Grid in front of Footprint** | true | Render the grid above the footprint instead of behind it |
| **Predicted values: show** | false | Show extrapolated values for the bar in progress. See [Predicted Values](#predicted-values) |
| **Predicted values: gauge** | false | Show the bar-progress gauge with a countdown to bar close |
| **Values are x1000** | true | Display values divided by 1000 |
| **Values divider** | 1 | Additional custom divider applied to displayed values, range: 1–∞ |
| **Cell height, px** | 24 | Height of one grid row |
| **Cell color scale** | Chart | What cell color intensity is scaled against — Chart or All |
| **Cell border** | true | Draw a border around each cell |
| **Cell border** | Black | Stroke of the cell border. A second setting with the same label, listed after the toggle |
| **Auto-scale values** | true | Shrink the text to fit the cell |
| **Auto-scale bars** | true | Scale in-cell bars to fit the cell |
| **Font** | Montserrat, 12pt | Grid font |
| **Align** | Center | Horizontal alignment of the cell text |
| **Values color** | DimGray | Text color of the cell values |
| **Background** | WhiteSmoke | Grid background color |

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
| **Cluster Zones: on bar close** | false | Only create zones after the bar closes |
| **Cluster Zones: filter min** | 0 | Minimum absolute cluster value to qualify, range: 0–∞ |
| **Cluster Zones: filter max** | 2 | Maximum absolute cluster value; -1 means unlimited. The default of 2 selects low volume nodes, range: -1–∞ |
| **Cluster Zones: ignore bar high/low** | false | Exclude clusters sitting at the bar high or low |
| **Cluster Zones: ended by** | ByBarHighLow | Termination rule: ByBarHighLow or ByBarTouch |
| **Cluster Zones: break on session** | true | End zones at session boundaries |
| **Cluster Zones: style** | Line | Display: Zone, Line, or None |
| **Cluster Zones: box** | false | Draw a box around the zone |
| **Cluster Zones: color** | RoyalBlue, solid, 4 px, 50 % opacity | Stroke of the projected zone or line |

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
| **Delta Divergence: sound** | mzpack_alert4.wav | Sound file for the divergence alert |

**Delta Divergence** is a trend reversal signal triggered on bar close:

- **LONG signal:** Price makes a new low with a bullish candle and positive delta
- **SHORT signal:** Price makes a new high with a bearish candle and negative delta

**Example:** A bearish bar making a new high with -135 delta. When the next bullish bar closes, the signal fires for a short trade.

For full divergence analysis, see the dedicated [mzDeltaDivergence](mzDeltaDivergence.md) indicator.

## Reconstruct Tape Mode

The MZpack order flow core reconstructs individual tick trades into aggregated trades. The settings below (group **Orderflow**) control reconstruction behavior.

| Setting | Default | Description |
|---|---|---|
| **Reconstruct tape** | true | Reconstruct tape using timestamps and Level 1 (best bid/ask) events. Required for Iceberg detection, DOM pressure, and DOM support |
| **Reconstruct tape: timestamps only** | false | Use only timestamps for reconstruction — Level 1 (best bid/ask) events are ignored, including for live data, and trades with equal timestamps are merged. Enable to get an exact match between reconstructed historical and reconstructed live data. Iceberg detection, DOM pressure, and DOM support are unavailable when enabled |

**Note:** Iceberg detection, DOM pressure, and DOM support require Reconstruct tape to be enabled **with timestamps-only mode disabled**.

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

Each bar metric can raise a sound alert when it crosses a threshold. Thresholds are compared against the absolute value, so one threshold covers both directions. Alerts fire once per bar and reset on each new bar.

| Setting | Default | Description |
|---|---|---|
| **On bar close** | false | Evaluate all alerts below only on bar close instead of on each tick |
| **Trades number: alert** | false | Alert on the number of trades in the bar |
| **Trades number: threshold** | 0 | Trades count that triggers the alert |
| **Trades number: sound** | beep.wav | Sound file for the trades alert |
| **Volume: alert** | false | Alert on bar volume |
| **Volume: threshold** | 0 | Volume that triggers the alert |
| **Volume: sound** | beep.wav | Sound file for the volume alert |
| **Buy volume: alert** | false | Alert on bar ask-side volume |
| **Buy volume: threshold** | 0 | Buy volume that triggers the alert |
| **Buy volume: sound** | beep.wav | Sound file for the buy volume alert |
| **Sell volume: alert** | false | Alert on bar bid-side volume |
| **Sell volume: threshold** | 0 | Sell volume that triggers the alert |
| **Sell volume: sound** | beep.wav | Sound file for the sell volume alert |
| **Delta: alert** | false | Alert on bar delta |
| **Delta: threshold** | 0 | Absolute delta that triggers the alert |
| **Delta: sound** | beep.wav | Sound file for the delta alert |
| **Delta %: alert** | false | Alert on bar delta percentage |
| **Delta %: threshold** | 0 | Absolute delta percentage that triggers the alert |
| **Delta %: sound** | beep.wav | Sound file for the delta % alert |
| **Abs Delta avr: alert** | false | Alert on the average absolute delta of the bar |
| **Abs Delta avr: threshold** | 0 | Value that triggers the alert |
| **Abs Delta avr: sound** | beep.wav | Sound file for the absolute delta average alert |
| **Cumulative Delta: alert** | false | Alert on session cumulative delta. This alert is not reset on a new bar |
| **Cumulative Delta: threshold** | 0 | Absolute cumulative delta that triggers the alert |
| **Cumulative Delta: sound** | beep.wav | Sound file for the cumulative delta alert |
| **Delta chng: alert** | false | Alert on the delta change from the previous bar |
| **Delta chng: threshold** | 0 | Absolute delta change that triggers the alert |
| **Delta chng: sound** | beep.wav | Sound file for the delta change alert |
| **Delta rate: alert** | false | Alert on the maximal delta rate in the bar |
| **Delta rate: threshold** | 0 | Absolute delta rate that triggers the alert |
| **Delta rate: sound** | beep.wav | Sound file for the delta rate alert |
| **COT High: alert** | false | Alert on the COT High value |
| **COT High: threshold** | 0 | Absolute COT High that triggers the alert |
| **COT High: sound** | beep.wav | Sound file for the COT High alert |
| **COT Low: alert** | false | Alert on the COT Low value |
| **COT Low: threshold** | 0 | Absolute COT Low that triggers the alert |
| **COT Low: sound** | beep.wav | Sound file for the COT Low alert |
| **Left cluster: alert** | false | Alert on a cluster value in the Left footprint column |
| **Left cluster: threshold** | 0 | Cluster value that triggers the alert |
| **Left cluster: sound** | beep.wav | Sound file for the left cluster alert |
| **Right cluster: alert** | false | Alert on a cluster value in the Right footprint column |
| **Right cluster: threshold** | 0 | Cluster value that triggers the alert |
| **Right cluster: sound** | beep.wav | Sound file for the right cluster alert |
| **Imbalance: alert** | false | Alert when an imbalance is detected |
| **Imbalance: sound** | beep.wav | Sound file for the imbalance alert |
| **Absorption: alert** | false | Alert when an absorption is detected |
| **Absorption: sound** | beep.wav | Sound file for the absorption alert |
| **Imbalance/Absorption: send email** | false | Also send an email when an imbalance or absorption alert fires |
| **Imbalance/Absorption: email address** | *(empty)* | Recipient address for those emails |

:::note
The cluster, imbalance, and absorption alerts carry the price at which they triggered; the bar-metric alerts do not.
:::

:::tip
See [Sound Files](/docs/getting-started/sound-files) for the full list of pre-installed sounds and how to add custom WAV files. S/R zone alerts have their own sounds, configured in the [Imbalance](#imbalance-sr-zones) and [Absorption](#absorption) sections.
:::
