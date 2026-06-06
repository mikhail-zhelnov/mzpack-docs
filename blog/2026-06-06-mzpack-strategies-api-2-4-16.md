---
title: "MZpack Strategies API w Divergence 2.4.16"
authors: [mzpack]
tags: [strategies, api]
---

This release fixes obfuscated indicators failing to load on newer NinjaTrader 8 builds and a Footprint rendering issue.

<!-- truncate -->

## Bug Fixes

- **Indicators not loading on newer NinjaTrader 8 builds** — the Release build now restores the mscorlib assembly reference version that .NET Reactor corrupted to `65535.65535.65535.65535`, which prevented the obfuscated indicators from loading.
- **mzFootprint:** fixed the chart freezing on small zoom levels when `MaximalRenderMs` is greater than 100.
