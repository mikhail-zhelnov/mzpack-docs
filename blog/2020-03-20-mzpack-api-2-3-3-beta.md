---
title: "MZpack API 2.3.3 beta"
authors: [mzpack]
tags: [api, beta]
---

New ICandle interface and BarMetricsSignal class for intra-bar Price Action rules.

<!-- truncate -->

## What's New

- Added ICandle interface for easy handling of values like OCHL, Body, Size, Upper/LowerWick, IsBullish, IsBearish, IsDoji
- Added `MZpackStrategyBase.GetCandle(int ago)` method returning an ICandle object
- Added BarMetricsSignal class for implementing intra-bar rules based on Price Action
