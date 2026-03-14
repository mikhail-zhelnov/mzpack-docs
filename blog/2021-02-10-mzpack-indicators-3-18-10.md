---
title: "MZpack Indicators 3.18.10"
authors: [mzpack]
tags: [indicators]
---

New Auto/Manual filtering for BigTrade, Volume Delta plot options, and Market Depth Renko fix.

<!-- truncate -->

## What's New

### mzBigTrade

The "Filters -- Type" parameter was added with two filtering modes:
- **Auto** filtering displays prominent trades based on a calculation combining "Days" and "Trades per day" parameters
- **Manual** filtering provides granular control, allowing filtering by trade volume, iceberg properties, DOM pressure/support values, and selection logic (All/Any)
- Both modes support Aggression and Smart attributes

### mzVolumeDelta

- Added new plot visualization options: Volume, Buy/Sell Volume, Delta, and Cumulative Delta plots

## Bug Fixes

- **mzMarketDepth:** Fixed incorrect overall liquidity migration candles when using Renko bars
