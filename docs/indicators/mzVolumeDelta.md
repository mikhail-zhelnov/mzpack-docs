---
sidebar_position: 4
title: "mzVolumeDelta"
description: "Volume delta indicator with histograms, candles, cumulative delta, iceberg detection, and trade filtering for NinjaTrader 8"
---

# mzVolumeDelta

The mzVolumeDelta indicator combines a Buy/Sell Volume indicator and a Delta indicator with iceberg search algorithms. It displays volume and delta data in a separate chart panel below the price chart.

**Data required:** Level 1 (tick data)

## Key Features

- **2 primary modes** — Volume and Delta
- **Volume mode** with buy/sell breakdown and iceberg detection
- **Delta mode** with histogram, candles, and cumulative delta
- **3 volume alignment styles** — Total, Stacked, Opposite
- **5 color modes** — Solid, Saturation, Heatmap, GrayScaleHeatmap, Custom
- **2 color coding schemes** — UpDown and Delta
- **Trade size filters** — min/max trade size filtering
- **Iceberg order detection** with Hard/Soft algorithms
- **Alerts** for volume, delta, and iceberg thresholds with custom sounds
- **5 NinjaScript plots** — Volume, Buy Volume, Sell Volume, Delta, Cumulative Delta

## Indicator Modes

| Mode | Description |
|---|---|
| **Volume** | Display buy/sell volume histograms per bar |
| **Delta** | Display delta histograms, delta candles, or cumulative delta |

## Volume Mode

When Mode is set to **Volume**, the indicator shows volume bars with optional iceberg detection.

### Volume Display

| Show | Description |
|---|---|
| **Volume** | Total volume bars only |
| **Icebergs** | Iceberg volume only (requires Reconstruct tape) |
| **Both** | Volume and icebergs together (requires Reconstruct tape) |

### Volume Alignment

Controls how buy and sell volumes are arranged within each bar:

| Align | Description |
|---|---|
| **Total** | Single bar showing total volume |
| **Stacked** | Buy and sell volumes stacked in one bar |
| **Opposite** | Buy and sell volumes as separate bars on opposite sides of the zero line |

### Iceberg Detection

Iceberg orders are large hidden orders that are executed in smaller visible portions. The indicator detects iceberg activity using two algorithms:

| Algorithm | Description |
|---|---|
| **Hard** | Strict detection — requires strong evidence of iceberg behavior |
| **Soft** | Relaxed detection — flags more potential iceberg activity |

**Note:** The **Reconstruct tape** option (under General settings) must be enabled for iceberg features to work. When Reconstruct tape is off, the Show setting must be set to **Volume** (icebergs are unavailable).

## Delta Mode

When Mode is set to **Delta**, the indicator shows the difference between buy and sell volume (delta).

### Delta Display

| Show | Description |
|---|---|
| **Histogram** | Delta per bar rendered as vertical bars |
| **Candles** | Delta displayed as OHLC-style candles |
| **Cumulative** | Running cumulative delta across the session |

### Cumulate Session Only

When enabled (default: true), cumulative delta resets at the beginning of each new trading session. When disabled, cumulative delta accumulates continuously across sessions.

## Color Modes

Controls how bars are colored based on their values:

| Mode | Description |
|---|---|
| **Solid** | Uniform selected color for all bars |
| **Saturation** | Color intensity scales with volume/delta values — higher values are more saturated |
| **Heatmap** | Multi-color gradient from cool to hot based on values |
| **GrayScaleHeatmap** | Monochrome intensity gradient |
| **Custom** | 4-level color thresholds with separate buy/sell colors |

### Color Coding

| Code | Description |
|---|---|
| **UpDown** | Color by chart bar direction — up bars use buy color, down bars use sell color |
| **Delta** | Color by delta value sign — highlights volume bars where delta is significant |

### Bar Color Scale

| Scale | Description |
|---|---|
| **Chart** | Maximum value for color coding is calculated from visible bars on the chart |
| **All** | Maximum value is calculated from all loaded bars |

### Custom Color Thresholds

When Color mode is set to **Custom**, bars are colored based on 4 value thresholds with separate colors for buy/positive and sell/negative sides:

| Threshold | Buy/Positive Default | Sell/Negative Default |
|---|---|---|
| Less than 1000 (#0) | Gray | Gray |
| 1000 or more (#1) | Green | DarkRed |
| 7000 or more (#2) | Lime | Red |
| 10000 or more (#3) | Cyan | DeepPink |

## Settings Reference

### Common

| Setting | Default | Description |
|---|---|---|
| **Mode** | Delta | Primary indicator mode — Volume or Delta |
| **Bar width** | Auto | Bar width mode — Auto (follows chart bar width) or Custom |
| **Bar width, px** | 10 | Custom bar width in pixels (when Bar width = Custom) |
| **Zero line** | true | Show horizontal zero line |

### Filters

| Setting | Default | Description |
|---|---|---|
| **Trade min** | 0 | Minimum trade size — trades smaller than this value are not counted |
| **Trade max** | -1 | Maximum trade size — trades larger than this value are not counted (-1 = unlimited) |
| **Display color** | 0 | Bars with values below this threshold are rendered with the "Below display color" |
| **Below display color** | Gray | Color for bars below the Display color threshold |

**Note:** Changing Trade min or Trade max requires reloading the indicator (press F5) to take effect.

### Presentation

| Setting | Default | Description |
|---|---|---|
| **Bar color scale** | Chart | Maximum value source for color coding — Chart or All |
| **Color code** | UpDown | Color coding scheme — UpDown or Delta |
| **Color mode** | Solid | Color rendering mode — Solid, Saturation, Heatmap, GrayScaleHeatmap, or Custom |
| **Buy volume/Positive delta** | Green | Color for buy volume or positive delta |
| **Sell volume/Negative delta** | Red | Color for sell volume or negative delta |
| **Custom 'less' filter #0** | 1000 | Upper bound for the lowest custom color tier |
| **Custom 'gte' filter #1** | 1000 | First custom threshold |
| **Custom 'gte' filter #2** | 7000 | Second custom threshold |
| **Custom 'gte' filter #3** | 10000 | Third custom threshold |
| **Buy/Positive color #0** | Gray | Buy/positive color for values below filter #0 |
| **Buy/Positive color #1** | Green | Buy/positive color for values at or above filter #1 |
| **Buy/Positive color #2** | Lime | Buy/positive color for values at or above filter #2 |
| **Buy/Positive color #3** | Cyan | Buy/positive color for values at or above filter #3 |
| **Sell/Negative color #0** | Gray | Sell/negative color for values below filter #0 |
| **Sell/Negative color #1** | DarkRed | Sell/negative color for values at or above filter #1 |
| **Sell/Negative color #2** | Red | Sell/negative color for values at or above filter #2 |
| **Sell/Negative color #3** | DeepPink | Sell/negative color for values at or above filter #3 |
| **Bar border** | DarkGray | Volume bar border stroke |
| **Buy Iceberg** | Fuchsia | Buy-side iceberg volume color |
| **Sell Iceberg** | Fuchsia | Sell-side iceberg volume color |
| **Candle/Bar border** | DarkGray | Delta candle border stroke |
| **Candle wick/Zero volume** | DarkGray | Delta candle wick stroke |
| **Scale plots: Volume** | false | Include Volume plot in chart scale calculation |
| **Scale plots: Buy Volume** | false | Include Buy Volume plot in chart scale calculation |
| **Scale plots: Sell Volume** | false | Include Sell Volume plot in chart scale calculation |
| **Scale plots: Delta** | false | Include Delta plot in chart scale calculation |
| **Scale plots: Cumulative Delta** | false | Include Cumulative Delta plot in chart scale calculation |

### Volume Mode

| Setting | Default | Description |
|---|---|---|
| **Show** | Both | What to display — Volume, Icebergs, or Both |
| **Align** | Opposite | Volume bar alignment — Total, Stacked, or Opposite |
| **Iceberg algorithm** | Hard | Iceberg detection algorithm — Hard or Soft |
| **Volume alert: enable** | false | Enable bar volume alert |
| **Volume alert: threshold** | 1000 | Volume value to trigger the alert |
| **Volume alert: sound** | mzpack_alert2.wav | Alert sound file |
| **Iceberg alert: enable** | false | Enable iceberg volume alert |
| **Iceberg alert: threshold** | 100 | Iceberg volume value to trigger the alert |
| **Iceberg alert: sound** | iceberg.wav | Alert sound file |

### Delta Mode

| Setting | Default | Description |
|---|---|---|
| **Show** | Candles | Delta display style — Histogram, Candles, or Cumulative |
| **Cumulate session only** | true | Reset cumulative delta on each new session |
| **Bar Delta alert: enable** | false | Enable bar delta alert |
| **Bar Delta alert: threshold** | 1000 | Absolute delta value to trigger the alert |
| **Bar Delta alert: sound** | mzpack_alert1.wav | Alert sound file |

## Plots

The indicator exposes 5 NinjaScript output plots that can be used by other indicators and strategies:

| Plot | Description |
|---|---|
| **Volume** | Total bar volume |
| **Buy Volume** | Buy-side (ask) volume |
| **Sell Volume** | Sell-side (bid) volume (displayed as negative) |
| **Delta** | Bar delta (buy volume minus sell volume) |
| **Cumulative Delta** | Running cumulative delta |

Set any non-transparent color for a plot to display the current value marker on the chart scale. Use the **Scale plots** toggles in Presentation settings to include specific plots in the chart scale calculation.

## Non-Bid/Ask Data Support

Some markets (Forex, cryptocurrencies, NSE/Indian stock market) do not provide historical bid/ask data. Without it, all historical trades appear on the Bid side only.

**Solution:** Set `Orderflow > Calculation mode` to **UpDownTick** for these instruments.

**Hybrid mode (NSE):** NSE data providers do not transmit historical bid/ask data. Use **Hybrid** mode, which applies UpDownTick calculation for historical data and BidAsk for real-time data.

**Recommendation:** For Forex pairs, use the relevant futures contract (e.g., 6E for EURUSD) to get accurate bid/ask data and full order flow features.
