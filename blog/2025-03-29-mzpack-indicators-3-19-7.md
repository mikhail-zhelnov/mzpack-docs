---
title: "MZpack Indicators 3.19.7"
authors: [mzpack]
tags: [indicators]
---

Added TPO POC letters coloring, Order Book Imbalance for Market Depth, and Historical DOM optimization.

<!-- truncate -->

## What's New

### mzVolumeProfile

- Added TPO POC letters coloring
- Added independent switches for open and close letter/marker

### mzMarketDepth

- Added OBI (Order Book Imbalance) as Overall Type in the Liquidity Migration category. OBI = Delta Bids / Sign(Delta BestBid) + Delta Offers / Sign(Delta BestOffer). OBI requires more observations.
- Added optional grid lines for Liquidity sub-charts
- Optimization of Historical DOM building
