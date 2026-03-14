---
title: "MZpack Indicators 3.17.0"
authors: [mzpack]
tags: [indicators]
---

Introduces Auto-filtering and Stacked Tape for mzBigTrade, providing smarter trade visualization.

<!-- truncate -->

## What's New

### mzBigTrade

#### Auto-filtering

This functionality helps traders identify significant trades on charts by operating in the background. Users can regulate order flow intensity through the "Presentation -- Max number of trades in chart frame" parameter. The algorithm accounts for iceberg order portions, DOM pressure, and DOM support when selecting which trades to display. As chart zoom levels increase, progressively smaller trades become visible, allowing deeper order flow analysis.

#### Stacked Tape

Accessible by selecting "Stacked" in the "Presentation -- Marker position" parameter. This feature organizes trades vertically by bar in sequential order. Buy trades accumulate at the top of chains while sell trades accumulate at the bottom. This arrangement is particularly useful with non-reconstructed tape or instruments with numerous small trades. It is recommended to use stacked positioning with tick-based timeframes, such as 20 Ticks. This feature is limited to Bubble and Box marker types only.
