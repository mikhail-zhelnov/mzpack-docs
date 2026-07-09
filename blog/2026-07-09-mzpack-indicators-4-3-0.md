---
title: "MZpack Indicators w/ Divergence 4.3.0"
authors: [mzpack]
tags: [indicators]
---

This release brings iceberg detection to historical data, adds a time-ordered stacked layout for mzBigTrade, and refreshes marker defaults.

<!-- truncate -->

## New Features

- **Tape iceberg algorithm (mzBigTrade)** — a third iceberg detection method that estimates hidden refilling-iceberg volume from a trade's fill composition (a run of identical-size fills) instead of the order book. Unlike the Hard and Soft algorithms, it works on historical bars, where NinjaTrader provides no Level 2 data. Enable it with **Iceberg: tape** and tune it with **Iceberg: tape min clip** and **Iceberg: tape min refills**. Its result feeds the existing iceberg filter, marker sizing, Iceberg Volume Profile, and pop-up, and changing a parameter recalculates the chart without a reload. The pop-up now shows the detected clip, e.g. `Clip: 5 x 57 @7510.5` (#54).
- **Stacked by time (mzBigTrade)** — a new **StackedByTime** marker position that lays a bar's trades out as a single time-ordered column, buys and sells together. **Stacked by time: from bar edge** anchors the column at the bar's high or low instead of the trade price (#56).
- **Click to stack (mzBigTrade)** — left-click a bar holding two or more trades to lay it out as a time-ordered column on demand, without changing Marker position; click any of its trades again to revert. Controlled by **Click: stack trades by time** (#56).

## Improvements

- **Refreshed mzBigTrade defaults** — volume text inside markers is now ForestGreen for buys and Red for sells (was White for both), and the Trades Volume Profile is shown by default. The internal ceiling on auto-scaled marker size was lowered so large trades no longer dominate the chart (#58).

Defaults apply to newly added indicator instances. Saved templates and workspaces keep their stored values — re-add the indicator to pick up the new defaults.

## Bug Fixes

- **Strategies were not persisted to NinjaTrader's database** — the MZpack assembly could not be resolved by name during XmlSerializer operations, so NinjaTrader logged "Error on executing DB command" on every database write while a strategy was running. The assembly now resolves correctly and strategies persist across restarts (#55).
- **mzBigTrade:** the pop-up stayed pinned to its pre-click position after a bar was toggled with click-to-stack, describing a marker that had moved. It is now hidden on toggle and rebuilt on the next mouse move (#58).

## Compatibility

- NinjaTrader 8.0.27+
- Requires MZpack API 2.4.13+ for strategy use
