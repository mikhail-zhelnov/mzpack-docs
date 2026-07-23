---
title: "MZpack Indicators w/ Divergence 4.4.0"
authors: [mzpack]
tags: [indicators]
---

This release rebuilds mzBigTrade DOM pressure detection around a refill-signature engine, adds color scaling to mzMarketDepth, and fixes several rendering issues across mzFootprint and mzVolumeProfile.

<!-- truncate -->

## DOM pressure (mzBigTrade)

DOM pressure detection is rebuilt around a refill signature. Instead of measuring the liquidity change at the best bid/ask at the moment a single trade executes, the indicator now follows a price level across trades: a price sitting at the best bid/ask that is repeatedly consumed by same-side aggressors and replenished within a short window is flagged as a defended level. Positive DOM pressure means net liquidity was refilled (absorption / resistance); negative means net liquidity was pulled. Detection still runs on the Level-1 quote stream (best bid/ask sizes), is feed-time based, and works on live data and Market Replay only. Not available in the free version.

### New

- **Refill-signature detection** — tune it with **DOM pressure: refill window (ms)**, **refill idle timeout (s)**, **refill min refills**, **refill min volume**, and **track pulling** (default on — counts liquidity pulled from the level as negative).
- **"Move right"** — a qualifying signature writes its pressure as soon as it qualifies and then re-anchors onto newer trades as the level keeps being defended, so the marker rides forward to the trade where the defense finally broke instead of appearing late.
- **Display filters** — applied on the fly: **min abs volume** (existing), **min hold duration (s)** (how long the level survived), and **min** / **max intensity (Σ/s)** (replenish rate). A trade shown only because of its DOM pressure disappears when it no longer passes; a trade that also passes the trade-volume filter keeps its marker without the triangle.
- **Show DOM pressure span** — draws a 1-tick band at the level price spanning the signature's extent, from its first refill to the anchor trade, plus a proportion bar comparing volume traded by the refill episodes against all volume traded at the level. Hovering the band shows the trade's pop-up. The DOM pressure value is also printed inside its triangle (auto-scaled), and the pop-up gains a `DOM pressure: N-Lot (refills) @price … traded sig/level` line.
- **Strategy API (StrategyBigTradeIndicator)** — new `DomPressureSignaturePassesFilter(ITrade)` method and `IndValue.DomPressurePassesFilter` property report whether a trade's DOM pressure signature passes the current DOM pressure filters (enable + min/max abs volume + min hold + min/max intensity), for gating strategy logic on filter-passing signals.

### Improvements

- **Triangle styling** — DOM pressure and DOM support triangles are now drawn in the Buy / Sell shape-border color, the DOM pressure span band opacity follows the Saturation preset, and the triangle-thickness setting is renamed **DOM pressure/support triangle thickness** and hidden unless a triangle is shown.
- **Reload prompt on detection change** — changing a detection parameter (refill window, idle timeout, min refills, min volume, track pulling) on a running chart now prompts to reload, since detection only re-runs on freshly processed data. The display filters (abs volume, hold, intensity) still apply on the fly.

### Bug Fixes

- DOM pressure / support triangles no longer keep growing after the largest one reaches the size cap — the whole set is rescaled proportionally, so the largest sits at the cap and smaller ones stay in proportion.
- A DOM pressure / support triangle (and a single marker) no longer renders dim when only one trade is on screen.

## New Features

- **Color scale for mzMarketDepth** — a new **Color scale** setting (Linear / Sqrt / Log) for both Historical DOM and Realtime DOM. It applies to the Saturation, Custom, Heatmap, and GrayScaleHeatmap color modes.

## Improvements

- **mzMarketDepth defaults retuned** — Historical DOM: **Display volume, %** 100 → 80 and **Extreme volume, %** 20 → 10. Realtime DOM: **Imbalance: Bid color** default changed from DarkGreen to `#FF00B300`, and **Depth of market** raised from 10 to 100 levels per side.

Retuned defaults apply to newly added indicator instances. Saved templates and workspaces keep their stored values — re-add the indicator to pick up the new defaults.

## Bug Fixes

- **mzMarketDepth:** small DOM sizes no longer wash out when large sizes are present — the volume-to-color curve now defaults to Sqrt in both the Saturation and Heatmap color modes.
- **mzMarketDepth:** changing the Realtime DOM **Color mode** now refreshes the property grid, so its dependent properties appear and disappear immediately.
- **mzFootprint:** Histogram clusters on the current bar no longer momentarily overflow past the footprint area in realtime. The histogram scale for the developing bar is now taken from the rows actually drawn, and cluster width is clamped to the footprint side.
- **mzVolumeProfile:** profile level lines (TPO POC/VAH/VAL, OPEN/CLOSE/HI/LO/MID, IB) were drawn one bar to the left on charts with a bar period of 1 day and more. Both ends are now resolved by bar index instead of by timestamp, so "End of day" ends the line at the bar next to the profile on 1 day, 1 week, and 1 month bars, and naked levels end at the bar that crossed them.

## Compatibility

- NinjaTrader 8.0.27+
- Requires MZpack API 2.4.13+ for strategy use
- MZpack API / Strategies 2.4.18 — adds `DomPressureSignaturePassesFilter` and `IndValue.DomPressurePassesFilter`
