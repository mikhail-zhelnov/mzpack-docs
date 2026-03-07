---
sidebar_position: 6
title: "mzMarketDepth"
description: "Market depth and order book visualization indicator for NinjaTrader 8"
---

# mzMarketDepth

The mzMarketDepth indicator visualizes limit orders resting in the order book (Depth Of Market). It displays DOM data on the chart as a historical heatmap and as a real-time histogram on the right chart margin. The indicator includes liquidity analysis, liquidity migration tracking, order book imbalance detection, quantitative depth metrics, and alert levels.

**Data required:** Level 2 (DOM data)

## Key Features

- **Real-time DOM histogram** on the right chart margin with bid/ask ladders
- **Historical DOM heatmap** on past chart bars with 4 filtering modes
- **4 color modes** — Solid, Saturation, Heatmap, GrayScaleHeatmap
- **Hold levels** — extend significant DOM levels beyond their original scope
- **Hold higher volume** — track maximum liquidity spikes per price level per bar
- **Liquidity plots** — overall bid/ask liquidity as lines or candles (OfferBid, OfferBidDelta, BidOfferDelta)
- **Liquidity Migration** — track adding and removing of limit orders in the DOM
- **Order book Imbalance** — percentage-based bid/ask imbalance detection with threshold
- **Quantitative Depth** — HQA, UQ, AC metrics for high-frequency order book analysis
- **Alert Levels** — interactive support/resistance levels with cross/touch alerts
- **Cumulative depth lines** — running totals on each DOM side
- **Pop-up info** — detailed level information on mouse hover

## Real-time DOM

The real-time DOM displays a colored histogram (ladders) of current bid and ask limit orders on the right chart margin. The number of visible levels is controlled by the **Depth of market** setting — this reflects the visible portion of the order book provided by the exchange (e.g., ES provides 10 levels nearest to the current price).

### Color Modes

| Mode | Description |
|---|---|
| **Solid** | Uniform selected color for all levels |
| **Saturation** | Color intensity scales with volume — larger orders are more saturated. 4 presets available |
| **Heatmap** | Multi-color gradient from cool to hot based on volume |
| **GrayScaleHeatmap** | Monochrome intensity gradient |

### Imbalance Detection

When **Imbalance: show** is enabled, individual DOM levels where volume is disproportionate relative to the average volume on that side are highlighted. The **Imbalance: ratio** controls the threshold — for example, a ratio of 2 means all volumes that are two times greater than the average volume of the given DOM side will be marked as imbalanced.

### Extreme Volume Coding

When **Code extremal** is enabled, DOM levels with volumes in the extreme range are rendered using the Extremal Bid / Extremal Offer colors and text colors, making large resting orders stand out visually.

### Cumulative Lines

When **Cumulative: show** is enabled, two lines display the running cumulative volume level by level on each DOM side. This shows how total depth builds up from the best bid/ask outward.

## Historical DOM

The historical DOM renders order book snapshots on past chart bars as a colored heatmap. Each price level shows the resting limit order volume at the time the bar was forming.

### Filtering Modes

| Mode | Description |
|---|---|
| **Percentage** | Display only limit orders with volume above a given percentage of the maximum order size. For example, 60% with a 100-lot maximum displays only 41-lot orders or greater. If the maximum grows to 200-lot, the threshold adjusts to 81-lot |
| **Absolute** | Display only limit orders with volume greater than or equal to a fixed contract value |
| **AdaptiveLess** | Uses the initial percentage as a starting point and slightly adjusts the minimum display threshold over time. Produces a moderately filtered view that adapts to changing order sizes |
| **AdaptiveMore** | Calculates the minimal DOM order size to display starting from DOM initialization and maintains it. Produces a strictly filtered view. Both adaptive modes provide a clear historical DOM picture that automatically adapts to future orders' sizes |

### Hold Levels

When **Hold levels** is enabled, DOM levels that move out of the visible depth-of-market scope continue to be displayed. The actual liquidity may no longer be there, but the last known quantities are kept for analysis. Use **Extend levels, px** to project held levels onto the right chart margin.

### Hold Higher Volume

When **Hold higher volume** is enabled, only the maximum limit order volume observed within the current bar at each price level is displayed. This lets you spot liquidity spikes — moments when large orders briefly appeared at a level.

### Display Options

- **Show volumes** — display volume numbers on historical DOM levels
- **Show max volumes** — show maximum volume in brackets next to the real-time volume
- **Show pop-up info** — detailed level information on mouse hover
- **History depth, bars** — maximum number of chart bars for which historical DOM is rendered (range: 10–10000). Use smaller values if you have performance issues

## Liquidity

Liquidity plots show overall (total) DOM liquidity at the bottom or top of the chart. These plots aggregate all visible bid and ask levels into a summary view.

### Plot Types

| Type | Description |
|---|---|
| **OfferBid** | Two lines — total volume on Offer side and total volume on Bid side |
| **OfferBidDelta** | One line or candles — total Offer volume minus total Bid volume |
| **BidOfferDelta** | One line or candles — total Bid volume minus total Offer volume |

### Plot Styles

| Style | Description |
|---|---|
| **Line** | Continuous line for all plot types |
| **Candle** | Candle representation for OfferBidDelta and BidOfferDelta types |

**Liquidity Cross pattern:** On OfferBid plots, a symmetrical cross can form where bid and ask liquidity lines intersect. An entry can be made after the right parts of the cross break its low and high bound.

## Liquidity Migration

Liquidity Migration tracks the process of adding and removing limit orders in the DOM. Individual migration events are shown as colored markers at the price level where they occur.

### Migration Markers

| Marker | Default Color | Description |
|---|---|---|
| **Added Offer** | Fuchsia | Limit orders added to the ask side |
| **Added Bid** | Aqua | Limit orders added to the bid side |
| **Removed Offer** | Yellow | Limit orders removed from the ask side |
| **Removed Bid** | Green | Limit orders removed from the bid side |

Only events exceeding the **Added volume filter** or **Removed volume filter** thresholds are displayed.

### Overall Migration Plots

Overall migration plots aggregate migration activity into summary lines or candles at the bottom/top of the chart.

- **Overall method** — **Discrete** calculates migration per each price level and then sums on each Level 2 update. **Totals** sums liquidity on each price level on each Level 2 update and then calculates migration
- **Overall type** — OfferBid, OfferBidDelta, or BidOfferDelta (same as Liquidity plot types)
- **Cumulate** — when enabled, migration accumulates from bar to bar. Migration for a new bar starts from the migration value of the previous bar

### Interpreting Liquidity Migration

- **Added Bid clusters** at a price level suggest passive buy interest building — potential support
- **Removed Offer clusters** above the price suggest sellers pulling back — potential for upside
- **Added Offer clusters** above the price suggest passive sell interest — potential resistance
- **Removed Bid clusters** below the price suggest buyers pulling back — potential for downside
- Combine with the overall migration plots to see the net direction of order book changes

## Imbalance

Order book imbalance is calculated as the percentage ratio of buy and sell limit order total quantities. When the imbalance exceeds the threshold, it is plotted as a line on the chart.

- **Imbalance, %** — threshold to display imbalance (default: 20%). Changing this value does not affect historical bars
- **Bid imbalance** — line style when bid side dominates
- **Offer imbalance** — line style when offer side dominates
- **No imbalance** — line style when bid and offer are balanced

**Note:** When Imbalance: Show is enabled, mzMarketDepth auto-scales the chart to fit the DOM. To disable this, uncheck the Auto scale option in the Visual section of NinjaTrader's built-in settings.

## Quantitative Depth

Quantitative Depth provides three metrics that analyze high-frequency order book behavior at configurable intervals.

| Metric | Description |
|---|---|
| **HQA** (High Quoting Activity) | Detects price levels where limit orders are being placed and canceled at a high rate — indicates active algorithmic participation |
| **UQ** (Unbalanced Quoting) | Identifies asymmetric quoting behavior between bid and ask sides — may signal directional intent |
| **AC** (Abnormal Cancellation) | Flags levels where an unusually high proportion of placed orders are subsequently canceled — potential spoofing or order faking activity |

- **Interval, ms** — calculation interval in milliseconds (default: 1000)
- **Output** — enable data output for external analysis

## Levels

Alert levels let you place interactive horizontal lines on the chart at significant price levels. Each level acts as a support or resistance marker with configurable alerts.

### Adding and Removing Levels

| Action | Default Shortcut |
|---|---|
| **Add a level** | Left Mouse Click + Left Shift |
| **Remove a level** | Left Mouse Click + Left Shift on an existing level, or click the remove button |
| **Adjust level duration** | Left Mouse Click + Left Alt on a level |
| **Drag a level** | Click left mouse button on the level (don't hold), move the cursor, then click again |

Click inside a Footprint bar or Volume profile to set that visual as the starting point of the level.

### Level Settings

- **Support level** / **Resistance level** — default line styles (support is below price, resistance is above)
- **Value position** — Left, Right, AboveLeft, AboveRight, or None
- **Alert on** — LevelCross or LevelTouch
- **Rearm** — re-enable the alert after it fires. **Rearm interval, sec** controls the cooldown (0 = immediate rearm)

**Note:** Levels are saved in the workspace XML file when you click Save workspace. Levels not saved in the workspace file will not be restored after reloading the indicator or re-establishing the data connection. You can export levels or replicate them on another chart using Templates > Save as from the chart context menu.

## Use Cases for ES

The following presets demonstrate common mzMarketDepth configurations for E-mini S&P 500 (ES). Each use case lists only settings that differ from defaults.

### Real-time DOM Heatmap with Imbalance

Visualize current order book depth with imbalanced levels highlighted.

| Setting | Value |
|---|---|
| **Show histogram** | true |
| **Color mode** (Realtime DOM) | Heatmap |
| **Code extremal** | true |
| **Imbalance: show** | true |
| **Imbalance: ratio** | 2 |
| **Cumulative: show** | true |
| **Ladders: width, px** | 250 |

Heatmap coloring gives instant visual weight to the largest resting orders. Imbalance ratio of 2 highlights levels with twice the average volume on their side. Cumulative lines show how total depth builds up from the inside out. Extreme volume coding in a different color makes the biggest orders unmissable. Useful for scalping — watch for imbalanced levels that align with cumulative depth buildups.

### Historical Support/Resistance from DOM Levels

Identify significant historical liquidity levels that acted as support or resistance.

| Setting | Value |
|---|---|
| **Show** (Historical DOM) | true |
| **Filtering mode** | AdaptiveLess |
| **Display volume, %** | 70 |
| **Extreme volume, %** | 15 |
| **Code extremal** (Historical DOM) | true |
| **Color mode** (Historical DOM) | Saturation |
| **Hold levels** | true |
| **Extend levels, px** | 50 |
| **Hold higher volume** | true |

AdaptiveLess filtering adapts thresholds over time for a clean view. 70% display volume shows only the top 30% of orders. Hold levels extends significant levels forward — even after they leave the visible DOM depth, you can see where large orders were resting. Hold higher volume captures fleeting liquidity spikes. Extreme volume coding makes the largest historical levels stand out. Look for price reactions at held extreme levels.

### Liquidity Migration Tracking

Track where large limit orders are being added and removed in real time.

| Setting | Value |
|---|---|
| **Show** (Liquidity Migration) | true |
| **Added volume filter** | 50 |
| **Removed volume filter** | 50 |
| **Show Overall** (Liquidity Migration) | true |
| **Overall type** (Liquidity Migration) | OfferBidDelta |
| **Plot** (Liquidity Migration) | Candle |
| **Cumulate** | true |
| **Show Overall** (Liquidity) | true |
| **Overall type** (Liquidity) | OfferBid |
| **Plot** (Liquidity) | Line |

Migration markers on the chart show where 50+ contract orders are being placed and pulled. OfferBidDelta candles at the bottom summarize net migration direction — positive candles mean more offer-side migration (selling pressure building), negative means bid-side (buying pressure). Cumulate mode shows the running total across bars. Liquidity OfferBid lines at the top show absolute bid/ask depth. Look for migration divergence: price rising while bid migration is negative (buyers pulling) warns of potential reversal.

### DOM Imbalance Scalping

Use order book imbalance as a real-time directional bias for scalping entries.

| Setting | Value |
|---|---|
| **Show** (Imbalance) | true |
| **Imbalance, %** | 15 |
| **Show histogram** | true |
| **Color mode** (Realtime DOM) | Saturation |
| **Imbalance: show** (Realtime DOM) | true |
| **Imbalance: ratio** | 1.5 |
| **Cumulative: show** | true |

Two layers of imbalance detection work together: the Imbalance section plots the overall bid/ask ratio as a line, while the Realtime DOM imbalance highlights individual levels. A 15% imbalance threshold on the overall ratio catches moderate shifts. Ratio 1.5 on individual levels highlights any level 50% above average. When the imbalance line shows bid dominance and the DOM histogram shows bid-side imbalanced levels clustering, the market has upward pressure. Enter on pullbacks within that bias.

### Comprehensive Market Depth Analysis

Full-featured setup combining historical DOM, liquidity, migration, and imbalance for swing analysis on ES.

| Setting | Value |
|---|---|
| **Show** (Historical DOM) | true |
| **Filtering mode** | Percentage |
| **Display volume, %** | 60 |
| **Extreme volume, %** | 20 |
| **Code extremal** (Historical DOM) | true |
| **Color mode** (Historical DOM) | Heatmap |
| **Hold levels** | true |
| **Show Overall** (Liquidity) | true |
| **Overall type** (Liquidity) | BidOfferDelta |
| **Plot** (Liquidity) | Candle |
| **Plots position** (Liquidity) | Top |
| **Show** (Liquidity Migration) | true |
| **Added volume filter** | 30 |
| **Removed volume filter** | 30 |
| **Show Overall** (Liquidity Migration) | true |
| **Overall type** (Liquidity Migration) | OfferBidDelta |
| **Cumulate** | true |
| **Plots position** (Liquidity Migration) | Bottom |
| **Show** (Imbalance) | true |
| **Imbalance, %** | 20 |

Four views working together: historical DOM heatmap reveals where large orders rested, liquidity BidOfferDelta candles at the top show net depth bias, migration at the bottom tracks order flow changes, and the imbalance line captures ratio shifts. Look for convergence — when historical extreme levels, positive liquidity delta, and bid-side migration all align at a price, that level has strong support. Best on 5–15 min charts with several hours of data loaded.

## Settings Reference

### Common

| Setting | Default | Description |
|---|---|---|
| **Depth of market** | 10 | Number of DOM levels to display (range: 1–1000). Reflects the visible portion of the exchange order book |
| **Multiple Market Maker** | false | Enable for stock markets with multiple market makers. Do not enable for futures via IQFeed |
| **Bid** | DodgerBlue | Color for buy-side limit orders |
| **Offer** | SteelBlue | Color for sell-side limit orders |
| **Extremal Bid** | Lime | Color for extreme buy-side limit orders |
| **Extremal Offer** | Crimson | Color for extreme sell-side limit orders |
| **Bid text** | White | Text color for bid volume values |
| **Offer text** | White | Text color for offer volume values |
| **Extremal Bid text** | Black | Text color for extreme bid values |
| **Extremal Offer text** | Black | Text color for extreme offer values |
| **Level min height, px** | 4 | Minimum pixel height per DOM level (range: 0–100) |

### Real-time DOM

| Setting | Default | Description |
|---|---|---|
| **Show histogram** | true | Show DOM histogram ladders on the right margin |
| **Histogram border** | Black | Border style for histogram bars |
| **Show volumes** | true | Show volume numbers on DOM levels |
| **Side total as %** | false | Show each side's total as a percentage |
| **Volumes filter** | 0 | Hide levels with volume below this value |
| **Volume font** | Montserrat, 12pt | Font for volume text |
| **Code extremal** | false | Highlight extreme volumes with extreme colors |
| **Color mode** | Solid | Color rendering — Solid, Saturation, Heatmap, or GrayScaleHeatmap |
| **Saturation preset** | 3 | Saturation level (range: 1–4) |
| **Imbalance: show** | false | Show imbalanced DOM levels |
| **Imbalance: ratio** | 1.5 | Ratio threshold for imbalance detection (range: 0.01–100) |
| **Imbalance: Bid color** | DarkGreen | Color for bid-side imbalance |
| **Imbalance: Offer color** | Firebrick | Color for offer-side imbalance |
| **Cumulative: show** | true | Show cumulative bid/offer depth lines |
| **Cumulative: Bid color** | Green, 2px | Line style for cumulative bid depth |
| **Cumulative: Offer color** | Red, 2px | Line style for cumulative offer depth |
| **Ladders: width, px** | 200 | Maximum histogram width in pixels (range: 40–1900) |
| **Ladders: extend** | false | Extend all ladders to full width |
| **Margin: left, px** | 5 | Left margin in pixels (range: 0–1000) |
| **Margin: right, px** | 5 | Right margin in pixels (range: 0–1000) |
| **Margin: control right** | true | Control the minimum width of the chart right margin |

### Historical DOM

| Setting | Default | Description |
|---|---|---|
| **Show** | true | Show historical DOM on the chart |
| **History depth, bars** | 2000 | Maximum bars for historical DOM display (range: 10–10000) |
| **Filtering mode** | Percentage | Filtering mode — Percentage, Absolute, AdaptiveLess, or AdaptiveMore |
| **Display volume, %** | 100 | Display levels above this percentage of the maximum order size (Percentage/Adaptive modes) |
| **Extreme volume, %** | 20 | Top percentage of displayed volumes treated as extreme (Percentage/Adaptive modes) |
| **Display volume** | 50 | Minimum volume in contracts to display (Absolute mode) |
| **Extreme volume** | 500 | Volumes at or above this contract size are extreme (Absolute mode) |
| **Code extremal** | false | Highlight extreme volumes with extreme colors |
| **Color mode** | Saturation | Color rendering — Solid, Saturation, Heatmap, or GrayScaleHeatmap |
| **Saturation preset** | 4 | Saturation level (range: 1–4) |
| **Hold levels** | true | Continue displaying levels that move out of DOM scope |
| **Extend levels, px** | 0 | Extend held levels onto the right margin by this many pixels (range: 0–10000) |
| **Hold higher volume** | false | Display only the maximum volume observed per price level per bar |
| **Show pop-up info** | false | Show level details on mouse hover |
| **Pop-up info font** | — | Font for the pop-up window |
| **Show volumes** | false | Display volume numbers on historical DOM levels |
| **Show max volumes** | false | Show max volume in brackets next to real-time volume |
| **Volume font** | Montserrat, 10pt | Font for volume text |

### Liquidity

| Setting | Default | Description |
|---|---|---|
| **Show Overall** | false | Show overall liquidity plots |
| **Overall type** | BidOfferDelta | Plot type — OfferBid, OfferBidDelta, or BidOfferDelta |
| **Plot** | Line | Plot style — Line or Candle |
| **Plot Bid/Up-candle** | Cyan, 2px | Line style for bid liquidity / color for up-candles |
| **Plot Offer/Down-candle** | Red, 2px | Line style for offer liquidity / color for down-candles |
| **Plots position** | Top | Plots placement — Top or Bottom |
| **Plots height, px** | 140 | Height of plots area (range: 10–1000) |
| **Plots background** | true | Show background behind plots |
| **Plots background color** | Black | Background color |
| **Plots background opacity, %** | 60 | Background transparency (range: 0–100) |
| **Grid lines** | false | Show grid lines on plots |

### Liquidity Migration

| Setting | Default | Description |
|---|---|---|
| **Show** | false | Show liquidity migration markers |
| **Added volume filter** | 20 | Minimum added volume to display a marker |
| **Removed volume filter** | 20 | Minimum removed volume to display a marker |
| **Added offer** | Fuchsia | Color for added ask-side orders |
| **Added bid** | Aqua | Color for added bid-side orders |
| **Removed offer** | Yellow | Color for removed ask-side orders |
| **Removed bid** | Green | Color for removed bid-side orders |
| **Show Overall** | false | Show overall migration plots |
| **Overall method** | Totals | Calculation method — Discrete or Totals |
| **Overall type** | OfferBidDelta | Plot type — OfferBid, OfferBidDelta, or BidOfferDelta |
| **Cumulate** | false | Accumulate migration values from bar to bar |
| **Plot** | Candle | Plot style — Line or Candle |
| **Plot Bid/Up-candle** | Cyan, 2px | Line style for bid migration / color for up-candles |
| **Plot Offer/Down-candle** | Red, 2px | Line style for offer migration / color for down-candles |
| **Plots position** | Bottom | Plots placement — Top or Bottom |
| **Plots height, px** | 140 | Height of plots area (range: 10–1000) |
| **Plots background** | true | Show background behind plots |
| **Plots background color** | Black | Background color |
| **Plots background opacity, %** | 60 | Background transparency (range: 0–100) |
| **Grid lines** | false | Show grid lines on plots |

### Imbalance

| Setting | Default | Description |
|---|---|---|
| **Show** | true | Show order book imbalance line |
| **Imbalance, %** | 20 | Threshold percentage for imbalance display. Changing this value does not affect historical bars |
| **Bid imbalance** | Yellow | Line style for bid-side imbalance |
| **Offer imbalance** | Yellow | Line style for offer-side imbalance |
| **No imbalance** | Gray | Line style when bid/offer are balanced |

### Quantitative Depth

| Setting | Default | Description |
|---|---|---|
| **Enable** | false | Enable quantitative depth metrics |
| **Interval, ms** | 1000 | Calculation interval in milliseconds |
| **Output** | false | Enable data output for external analysis |

### Notifications

| Setting | Default | Description |
|---|---|---|
| **Extreme alert** | false | Alert when extreme limit order volume appears |
| **Extreme sound** | ding.wav | Sound file for extreme volume alerts |

### General

| Setting | Default | Description |
|---|---|---|
| **Optimize render performance** | true | Limit rendering time to free CPU/GPU resources |
| **Maximal render time, ms** | 100 | Maximum rendering time before frame skip. Chart may flash — adjust for balance between performance and visual comfort |
| **Refresh delay** | 250 | Refresh delay in milliseconds |

## Performance Tips

mzMarketDepth processes Level 2 market data on every DOM update, which is significantly more data than Level 1 tick-based indicators. To keep charts responsive:

- Set **History depth, bars** to the minimum you need — 2000 bars of historical DOM data can consume significant memory
- Use **Optimize render performance** (enabled by default) and adjust **Maximal render time, ms** to 20–50 ms if the chart lags
- Use **AdaptiveLess** or **AdaptiveMore** filtering modes instead of Percentage — adaptive modes automatically manage the display threshold and reduce the number of rendered levels
- Reduce **Depth of market** if you don't need all 10 levels
- Disable **Hold levels** and **Hold higher volume** when not needed — they increase the number of rendered elements
- Remove unused indicators from the chart or use the visibility toggle (eye button) to temporarily hide indicators you need only periodically
- For multi-session analysis, use two mzMarketDepth instances with different Start/Stop time settings instead of one instance covering the full day
