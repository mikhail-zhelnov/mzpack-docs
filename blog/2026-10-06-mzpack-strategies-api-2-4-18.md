---
title: "MZpack Strategies API w Divergence 2.4.18"
authors: [mzpack]
tags: [strategies, api]
---

This release adds streaming Data Export, a controllable Pattern dashboard, and Footprint Action signal probes for measuring setups without placing trades.

<!-- truncate -->

## Data Export in real time

- **Stream each indicator export to CSV while the strategy runs** — the `Footprint`, `VolumeProfile`, `BigTrade` and `MarketDepth` export groups each gain **Export real-time**. It is off by default, so saved configurations retain their previous write-on-disable behaviour. Streaming applies only when that group’s **Temporality** is `Realtime`; a Historical export is produced during the historical load and the strategy reports this in the Output window.
- **Built-in `Data_Export` strategy verified for live append** — set an exported group’s **Temporality** to `Realtime` and enable **Export real-time** to append its rows during a live run.
- **Export API streams correctly** — `ExportArgs.IsExportWhileCollecting` now writes to the target file as rows arrive. The file is truncated on its first row, then appended to; use `IsBatch` to retain previous runs. The writer remains open with `FileShare.ReadWrite`, so the CSV can be opened in Excel while it is written. `ExportArgs.FlushIntervalMs` controls batched flushing (0, the default, flushes every row).

## Built-in signals and Pattern dashboard

- **Built-in signals ship in the Strategies assembly** — `FootprintImbalanceSignal`, `FootprintAbsoprtionSignal`, `BigTradeSignal`, `RelativeToProfileSignal` and `DOMImbalanceSignal`. `FootprintAbsoprtionSignal` keeps its existing public spelling.
- **Collapse the Pattern dashboard** — click a legend node or its `[+]` / `[−]` connector control to hide or show its subtree in both the legend and the grid. The node’s own cell remains visible, preserving the aggregate direction. This works for `Pattern`, `Signals`, `Filters`, `And`, `Or`, `Conj`, and signals with children.
- **Dashboard state persists** — collapsed nodes survive strategy reinitialization, instrument changes and template application through the hidden `DashboardCollapsedNodes` property.
- **New dashboard controls** — a left-edge strip can collapse or expand the panel, show or hide the legend, dock it to the top or bottom, move it vertically and change row height. The collapsed panel leaves the control strip on the chart so it can be restored; placement and row height persist with the dashboard state.
- **Every pattern node has a grid cell** — logical nodes no longer share a row with their first child, so the grid shows each node’s own direction.

## Footprint Action: Signal Probe

- **New `Probe` and `TradeProbe` Action modes** — evaluate every signal independently for observation and statistics, outside the pattern tree and without trading. `Probe` collects historical data without orders; `TradeProbe` observes while the strategy trades. Probe instances include signals disabled for trading, and continue evaluating while a position is open. `Probe` and `Export` replay history themselves; use **MZpack > Backtesting** manually when a `TradeProbe` backtest must also submit historical orders.
- **First-touch outcome ladder** — each probe event records, at tick resolution, the first time and bar at which price reaches every configured favourable and adverse level. It also records `TicksAtHorizon`, MFE, MAE, `BarsToMFE` and `FirstTickPrice`, letting stop/target combinations be resolved later without replaying the data.
- **Bar-based observation horizon** — **Probe: horizon bars** defaults to 40. Observation never crosses a session boundary and records whether it ended normally, at session end or at end of data. **Probe: ladder ticks** defaults to ten bar ranges on Range charts and 100 ticks otherwise; the level spacing keeps each side to no more than 100 levels.
- **Export probe journals** — **Probe: export** writes one row per event to `mzpack\strategy\...\probe` when the strategy is removed. The self-describing file records settings, market context, warnings and first-touch columns such as `Fav0100_Time` and `Adv0100_Bar`; it never overwrites an existing file.
- **Signal report on removal** — diagnostics now include per-signal firings, long/short counts, median MFE and MAE, and expectation under the strategy’s first-leg stop and target. Rows below 50 events are marked unreliable; the report keeps signal-name ordering rather than ranking signals.

## Footprint Action: calibration and offline analysis

- **Probe respects auto-calibration warm-up** — when **Filters: auto** is on, it records no events until calibration is ready, keeping manual-threshold warm-up events out of the calibrated sample. Diagnostics and journal metadata state the skipped count and first recorded session; no journal is written if every event was skipped.
- **Per-signal skipped-fire counts** — diagnostics and the Signal Report distinguish a signal that never fired from one whose firings all fell in warm-up.
- **Auto-calibrated bar filters** — **Filters: auto** calibrates global **Min bar Volume** and **Min bar Delta** from completed prior sessions, using percentile thresholds per intraday bucket. It drops incomplete, poorly covered and volume-outlier sessions; diagnostics and **Filters: dump baseline** expose the input, decisions and resulting thresholds.
- **Protect the baseline from bar-count-dominant sessions** — a session that contributes over twice its expected share of bars is now excluded, preventing an unusually long, light session from setting the calibration percentile.
- **Record `VolumeRank` and `DeltaRank`** — the probe journal records 0–100 percentile ranks against the same baseline distribution used by its filter. A run collected at a low percentile can therefore be filtered offline to higher percentiles. `n/a` denotes unavailable calibration, rather than a rank of zero.

## Changes

- **Probe ranks now describe the whole event** — `VolumeRank` and `DeltaRank` are the binding ranks across every bar a signal needs, not merely the firing bar. AND conditions use the minimum rank and OR conditions the maximum. Signal authors can declare alternatives and unbounded conditions; undeclared alternatives are reported in the journal and Output window.
- **Breaking journal format change** — the rank columns keep their names but change meaning. New journals include `unmarkedAlternatives` in `[params]`; reject a journal without it rather than interpreting older event-bar ranks as current values.
- **Pattern dashboard reads more clearly** — legend columns size to their measured text, with measurements cached across scrolling and zooming. `None` is now an empty coloured cell (while an uncalculated signal remains `-`); the default row height is 24 px instead of 28 px. Borders are omitted below 8 px column width, and the row pointer now reaches the final cell of every row.

## Bug Fixes

- **Data Export live-write failures no longer stop a strategy** — a read-only file, full disk or missing path is reported once, collection continues and the data is written when the strategy is disabled. A routing error stops and reports only its own export, leaving others running.
- **Drawing-object streaming now resolves its output file** — `DrawingObjectsExport` now creates the destination, file name and header when exporting while collecting.
- **Batch suffix is applied once** — a repeated export initialization no longer turns `data_001.csv` into `data_001_002.csv`.
- **Pattern dashboard small-row rendering is stable** — legend margins shrink with row height, and `Range` nodes and indicator templates are excluded from the legend instead of throwing `NotImplementedException`.
- **`Hammer w Absorption` can fire without a manually configured footprint template** — signals now declare their required indicator calculations, enabling absorptions when the signal needs them.
- **`Stacked Imbalances` can be probed while disabled for trading** — its imbalance S/R zones no longer depend on the trading enable switch, so probe statistics are collected.
- **`Delta Trap` uses the right delta threshold** — all three bars now use the signal’s own **Min bar Delta** when **Override filters** is on, otherwise the global threshold (including its per-bucket auto-calibrated value). A fresh signal defaults to 100, preserving prior default behaviour; auto-calibrated and manually overridden configurations may become stricter or change according to their configured threshold.
- **Zero is an explicit no-filter setting** — a signal with **Override filters** on and **Min bar Delta** set to 0 applies no delta threshold. The strategy now reports that configuration at startup for every affected signal.

## Indicators Core

- Includes MZpack Indicators Core 4.4.3.
