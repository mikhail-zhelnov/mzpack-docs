---
title: "MZpack API 2.3.10 beta"
authors: [mzpack]
tags: [api, beta]
---

Rithmic connection fix, Chart Trader protection order adjustments, and order rejection retry functionality.

<!-- truncate -->

## What's New

- MZpack 3.18.5 core
- Protection orders are now adjustable in Chart Trader
- Introduction of MZpackStrategyBase.OrderErrorRetry feature ("Retry" parameter in UI) enabling order rejection retry functionality
- Rejected stop loss orders (tight stops) are resubmitted up to OrderErrorRetry times, with position closure occurring if the stop loss order remains unaccepted

## Bug Fixes

- Fixed execution issues with Rithmic connection
- Fixed mzVolumeProfile incorrect behavior in Minute accuracy mode
