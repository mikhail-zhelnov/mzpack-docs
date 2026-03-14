---
title: "MZpack API 2.3.7 beta"
authors: [mzpack]
tags: [api, beta]
---

New Position.CancelClose() method for manual position management and GetCandle() accuracy fix.

<!-- truncate -->

## What's New

- `Position.CancelClose()` method enables cancellation of manually placed limit orders or manual entries
- Users can manage positions through the MZpack Control Panel UI without disabling the strategy

### Changes

- `MZpackStrategyBase.WorkingDataSeriesIdx` now defaults to 0, indicating a non-multi-timeframe strategy

## Bug Fixes

- Fixed issue with cancelling pending/working orders
- Fixed `MZpackStrategyBase.GetCandle()` returning inaccurate candle metrics when the ago value exceeded 1
