---
sidebar_position: 7
title: "mzDeltaDivergence"
description: "Delta divergence indicator for detecting price and volume delta discrepancies in NinjaTrader 8"
---

# mzDeltaDivergence

The mzDeltaDivergence indicator detects Price/Delta divergences on the chart. It uses a ZigZag algorithm to identify trend breakpoints and compares price changes against cumulative delta changes between those breakpoints. When price and delta move in opposite directions, a divergence signal is generated — indicating a potential trend reversal. The indicator inherits all functionality from [mzVolumeDelta](mzVolumeDelta.md), including volume histograms, delta candles, cumulative delta, and iceberg detection.

**Data required:** Level 1 (tick data)

## Key Features

- **Price/Delta divergence detection** using ZigZag breakpoint analysis
- **LONG and SHORT divergence signals** with colored buy/sell areas on chart
- **ZigZag algorithm** with configurable deviation type (Value or Percent) and threshold
- **Price deviation filter** — minimum and maximum price change between breakpoints (ticks or percent)
- **Delta deviation filter** — minimum and maximum cumulative delta change between breakpoints (contracts or percent)
- **Filter logic** — PriceAndDelta (both must meet threshold) or PriceOrDelta (either suffices)
- **Breakpoint arrows** marking ZigZag swing points on the chart
- **Statistics labels** showing price and delta change values near each divergence
- **Divergence alerts** with configurable sound
- **All mzVolumeDelta features** — volume/delta histograms, cumulative delta, iceberg detection, trade filters

## How Divergence Detection Works

The indicator uses a ZigZag algorithm to find swing highs and swing lows (breakpoints) in the price action. For each pair of consecutive breakpoints, it compares:

1. **Price change** — the direction and magnitude of the price move between breakpoint A and breakpoint B
2. **Cumulative delta change** — the difference in cumulative delta (by session) between the same two breakpoints

A divergence is detected when price and cumulative delta move in **opposite directions** — that is, when their product is negative (`priceChange × deltaChange < 0`).

### LONG Divergence (Buy)

Price makes a **new low** (breakpoint B is below breakpoint A), but cumulative delta between those breakpoints is **positive** — meaning buyers are present despite the lower price. This suggests the downtrend may be losing momentum.

### SHORT Divergence (Sell)

Price makes a **new high** (breakpoint B is above breakpoint A), but cumulative delta between those breakpoints is **negative** — meaning sellers are present despite the higher price. This suggests the uptrend may be losing momentum.

## ZigZag Settings

The ZigZag algorithm identifies swing highs and swing lows based on price deviation. A new breakpoint is confirmed when:

- A swing high or swing low is detected (the bar's high/low is greater/less than both adjacent bars)
- The price deviation from the last swing exceeds the configured threshold
- The trend direction changes (from up to down or vice versa)

| Setting | Default | Description |
|---|---|---|
| **Zigzag: deviation type** | Value | **Value** — deviation measured in ticks. **Percent** — deviation measured as percentage of the price range within the current session |
| **Zigzag: deviation threshold** | 1 | Minimum price deviation required to confirm a new breakpoint. In Value mode, this is measured in ticks (not points). In Percent mode, calculated within the current session range |
| **Zigzag: use High-Low** | true | When enabled, uses bar High/Low prices for ZigZag calculation. When disabled, uses Close prices |

**Breakpoints lookback** (default: 2) controls how many breakpoints the indicator keeps in its queue. Each new breakpoint is compared against all existing breakpoints in the queue to check for divergences.

## Deviation Filters

Deviation filters control the minimum (and optionally maximum) price and delta changes required for a divergence to qualify.

### Price Deviation

| Setting | Default | Description |
|---|---|---|
| **Price deviation: type** | Value | **Value** — deviation measured in ticks. **Percent** — deviation measured as percentage of the price range within the current session |
| **Price deviation: min** | 2 | Minimum price deviation between breakpoints to qualify as a divergence |
| **Price deviation: max** | -1 | Maximum price deviation between breakpoints. Set to -1 for unlimited |

### Delta Deviation

| Setting | Default | Description |
|---|---|---|
| **Delta deviation: type** | Value | **Value** — deviation measured in contracts. **Percent** — deviation measured as percentage change relative to the starting cumulative delta |
| **Delta deviation: min** | 100 | Minimum cumulative delta deviation between breakpoints to qualify |
| **Delta deviation: max** | -1 | Maximum cumulative delta deviation. Set to -1 for unlimited |

### Deviation Logic

| Setting | Default | Description |
|---|---|---|
| **Divergence: deviation logic** | PriceAndDelta | **PriceAndDelta** — both price and delta deviations must meet their thresholds. **PriceOrDelta** — at least one deviation must meet its threshold |

## Visualization

### Breakpoint Arrows

When **Breakpoint: show** is enabled, arrows are drawn near ZigZag breakpoints — arrow up at swing lows and arrow down at swing highs.

| Setting | Default | Description |
|---|---|---|
| **Breakpoint: show** | true | Show arrows near ZigZag breakpoints |
| **Breakpoint: arrow offset, ticks** | 1 | Arrow offset from the breakpoint price in ticks |
| **Breakpoint: color** | DeepSkyBlue | Arrow color |

### Statistics Labels

When **Statistics: show** is enabled, text labels near each divergence display the price change and delta change values (e.g., "4 / 250" meaning 4 ticks of price deviation and 250 contracts of delta deviation).

| Setting | Default | Description |
|---|---|---|
| **Statistics: show** | true | Show price/delta change values near each divergence |
| **Statistics: offset, px** | 60 | Vertical offset of the statistics text in pixels |
| **Statistics: font** | Montserrat, 12pt | Font for statistics text |

### Buy/Sell Areas

Colored regions highlight divergence zones between breakpoint A and breakpoint B:

| Setting | Default | Description |
|---|---|---|
| **Buy/Sell areas: show** | true | Show colored divergence zones on the chart |
| **Buy area: color** | Green | Color for buy (LONG) divergence zones |
| **Sell area: color** | Red | Color for sell (SHORT) divergence zones |

### Alerts

| Setting | Default | Description |
|---|---|---|
| **Divergence alert: enable** | false | Enable alert on divergence detection (real-time only) |
| **Divergence alert: sound** | mzpack_alert2.wav | Alert sound file |

## Use Cases for ES

The following presets demonstrate common mzDeltaDivergence configurations for E-mini S&P 500 (ES). Each use case lists only settings that differ from defaults. Recommended chart type: 1000 Tick.

### Trend Reversal Detection

Default-like setup for catching trend reversals on a 1000 Tick chart.

| Setting | Value |
|---|---|
| **Zigzag: deviation type** | Value |
| **Zigzag: deviation threshold** | 2 |
| **Price deviation: min** | 4 |
| **Delta deviation: min** | 150 |
| **Divergence: deviation logic** | PriceAndDelta |

A zigzag deviation of 2 ticks (0.50 pts on ES) filters out minor noise while catching meaningful swings. Price deviation min of 4 ticks (1.00 pt) ensures the price move is significant. Delta deviation min of 150 contracts filters out weak delta disagreements. PriceAndDelta logic requires both conditions to be met — producing higher-quality reversal signals. Look for LONG divergences near support levels and SHORT divergences near resistance.

### Wide Swing Divergences

Larger zigzag and price deviations for swing-style trading on higher timeframes.

| Setting | Value |
|---|---|
| **Zigzag: deviation type** | Value |
| **Zigzag: deviation threshold** | 8 |
| **Price deviation: min** | 12 |
| **Delta deviation: min** | 500 |
| **Divergence: deviation logic** | PriceAndDelta |
| **Statistics: show** | true |

Zigzag deviation of 8 ticks (2.00 pts on ES) captures only larger swings. Price deviation min of 12 ticks (3.00 pts) and delta deviation min of 500 contracts ensure only significant divergences are flagged. This produces fewer but higher-conviction signals suited for swing entries. Use on a 2000+ Tick chart or 5-minute chart. Statistics labels help verify that the price/delta disagreement is substantial.

### High-Delta Divergences Only

Focus on divergences with strong cumulative delta disagreement.

| Setting | Value |
|---|---|
| **Zigzag: deviation threshold** | 2 |
| **Price deviation: min** | 2 |
| **Delta deviation: min** | 500 |
| **Delta deviation: max** | -1 |
| **Divergence: deviation logic** | PriceAndDelta |
| **Buy area: color** | Lime |
| **Sell area: color** | OrangeRed |

Low price deviation min keeps the price filter relaxed, while delta deviation min of 500 contracts is high — only divergences with very strong delta disagreement are shown. These signals indicate that a large number of contracts are accumulating against the price direction, which can precede sharp reversals. Distinct colors (Lime/OrangeRed) make the high-conviction signals easy to spot.

### Cumulative Delta Candles with Divergence

Combine cumulative delta candle display with divergence overlay for full context.

| Setting | Value |
|---|---|
| **Volume/Delta mode** | Delta |
| **Delta mode** | Cumulative |
| **Zigzag: deviation threshold** | 3 |
| **Price deviation: min** | 4 |
| **Delta deviation: min** | 200 |
| **Divergence: deviation logic** | PriceAndDelta |
| **Buy/Sell areas: show** | true |
| **Statistics: show** | true |

Delta mode set to Cumulative shows cumulative delta candles in the lower panel, providing visual context for how delta evolves across the session. Divergence zones on the price chart highlight where price and cumulative delta disagree. Compare the divergence arrows with the cumulative delta plot — a LONG divergence should align with a rising or flat cumulative delta line despite falling price. This combined view helps confirm divergence signals before entry.

### Filtered Divergences (PriceOrDelta)

Relaxed deviation logic to catch more divergences for screening.

| Setting | Value |
|---|---|
| **Zigzag: deviation threshold** | 2 |
| **Price deviation: min** | 6 |
| **Delta deviation: min** | 300 |
| **Divergence: deviation logic** | PriceOrDelta |
| **Breakpoint: show** | true |
| **Statistics: show** | true |

PriceOrDelta logic means a divergence qualifies if **either** the price deviation or the delta deviation meets its threshold. This produces more signals than PriceAndDelta mode. Higher individual thresholds (6 ticks price, 300 contracts delta) compensate for the relaxed logic by ensuring at least one dimension is significant. Useful as a screening tool — scan for clusters of divergences at a price level to identify potential reversal zones, then confirm with other MZpack indicators.

## Settings Reference

### Divergence

| Setting | Default | Description |
|---|---|---|
| **Zigzag: deviation type** | Value | Value (ticks) or Percent (within session) |
| **Zigzag: deviation threshold** | 1 | Minimum deviation to confirm a ZigZag breakpoint (range: 1–∞) |
| **Zigzag: use High-Low** | true | Use High/Low prices for ZigZag. When false, uses Close |
| **Breakpoints lookback** | 2 | Number of breakpoints kept in queue for comparison (range: 2–∞) |
| **Price deviation: type** | Value | Value (ticks) or Percent (within session) |
| **Price deviation: min** | 2 | Minimum price deviation to qualify |
| **Price deviation: max** | -1 | Maximum price deviation, -1 = unlimited |
| **Delta deviation: type** | Value | Value (contracts) or Percent |
| **Delta deviation: min** | 100 | Minimum cumulative delta deviation to qualify |
| **Delta deviation: max** | -1 | Maximum cumulative delta deviation, -1 = unlimited |
| **Divergence: deviation logic** | PriceAndDelta | PriceAndDelta or PriceOrDelta |
| **Breakpoint: show** | true | Show arrows near ZigZag breakpoints |
| **Breakpoint: arrow offset, ticks** | 1 | Arrow offset from breakpoint price |
| **Breakpoint: color** | DeepSkyBlue | Breakpoint arrow color |
| **Statistics: show** | true | Show price/delta change values near divergences |
| **Statistics: offset, px** | 60 | Statistics text vertical offset |
| **Statistics: font** | Montserrat, 12pt | Statistics text font |
| **Buy/Sell areas: show** | true | Show colored divergence zones |
| **Buy area: color** | Green | Buy divergence zone color |
| **Sell area: color** | Red | Sell divergence zone color |
| **Divergence alert: enable** | false | Alert on divergence detection |
| **Divergence alert: sound** | mzpack_alert2.wav | Alert sound file |

### Inherited from mzVolumeDelta

All Volume/Delta settings (Volume/Delta mode, delta mode, color mode, trade size filters, iceberg detection, alerts, and other settings) are inherited from mzVolumeDelta. See [mzVolumeDelta](mzVolumeDelta.md) for the full reference.

**Note:** mzDeltaDivergence sets Delta mode to **Cumulative** by default (mzVolumeDelta defaults to Delta).

## Non-Bid/Ask Data Support

Some markets (Forex, cryptocurrencies, NSE/Indian stock market) do not provide historical bid/ask data. Without it, all historical trades appear on the Bid side only.

**Solution:** Set `Orderflow > Calculation mode` to **UpDownTick** for these instruments.

**Hybrid mode (NSE):** NSE data providers do not transmit historical bid/ask data. Use **Hybrid** mode, which applies UpDownTick calculation for historical data and BidAsk for real-time data.

**Recommendation:** For Forex pairs, use the relevant futures contract (e.g., 6E for EURUSD) to get accurate bid/ask data and full order flow features.
