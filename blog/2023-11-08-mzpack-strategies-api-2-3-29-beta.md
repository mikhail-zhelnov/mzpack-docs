---
title: "MZpack Strategies/API 2.3.29 beta"
authors: [mzpack]
tags: [strategies, api, beta]
---

FootprintAction v1.3 with cross-instrument trading and deferred trading activation.

<!-- truncate -->

## What's New

### FootprintAction v1.3

- "Trading Instrument" option added within the Position category, enabling users to operate the strategy on one futures contract (such as ES) while executing trades on another (like MES)
- A new "Strategy -- Trading: ON" parameter allows traders to defer trading initiation until manually activating the "Trading" button on the control panel

### API

- MZpackStrategyBase.TradingDataSeriesIndex property added for multi-data-series strategies. Reference the MultiDataSeriesAdvancedStrategy sample for implementation guidance.
- "MZpack -- Trace orders" parameter introduced
