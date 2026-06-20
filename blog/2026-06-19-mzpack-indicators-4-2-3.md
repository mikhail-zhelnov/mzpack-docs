---
title: "MZpack Indicators w/ Divergence 4.2.3"
authors: [mzpack]
tags: [indicators]
---

This release fixes a startup license error for activated users and a Levels workspace-reload issue.

<!-- truncate -->

## Bug Fixes

- **License validation error on startup for already-activated users** — the stored-credential activation path built a WPF window on NinjaTrader's non-STA worker thread, throwing "The calling thread must be STA" even though the key was valid. The activation window is now created on the UI dispatcher thread.
- Show a distinct message when an indicator feature is not included in the license.
- **Levels:** an indicator with Levels (e.g. mzVolumeProfile) was removed from the chart when reopening a workspace that had Levels saved. Level data is now serialized in a NinjaTrader-safe form (stroke as primitives, price as an invariant string) so the indicator and its levels reload correctly (#37). Note: levels saved by an earlier version reload with the default color until the workspace is re-saved.

## Compatibility

- NinjaTrader 8.0.27+
- Requires MZpack API 2.4.13+ for strategy use
