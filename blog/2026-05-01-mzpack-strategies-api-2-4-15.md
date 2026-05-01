---
title: "MZpack Strategies API w Divergence 2.4.15"
authors: [mzpack]
tags: [strategies, api]
---

This release updates to the new 4.2.2 Indicators core and fixes two strategy issues.

<!-- truncate -->

## What's New

New 4.2.2 Indicators core.

## Fixes

- **Calculate=OnBarClose:** strategies with `BarsRequiredToTrade=1` no longer skip bar 0 in OnBarClose signal validation. Signal `GetEffectiveCurrentBarIndex()` now returns the right index for OnBarClose mode, and `isFirstTickOfBars` is properly reset.
- **IsExportWhileCollecting** re-enabled — it had been disabled to speed up research/backtest runs; streaming export to file now works again.
