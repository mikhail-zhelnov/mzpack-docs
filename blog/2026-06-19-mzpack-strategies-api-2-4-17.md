---
title: "MZpack Strategies API w Divergence 2.4.17"
authors: [mzpack]
tags: [strategies, api]
---

This release fixes a StrategyDeltaDivergenceIndicator type-cast error and restores obfuscated indicator loading on newer NinjaTrader 8 builds.

<!-- truncate -->

## Bug Fixes

- **StrategyDeltaDivergenceIndicator:** fixed an invalid type cast when accessing `VolumeDeltaBars` (#43).
- **Indicators not loading on newer NinjaTrader 8 builds** — the Release build now restores the mscorlib assembly reference version that .NET Reactor corrupted to `65535.65535.65535.65535`, which prevented the obfuscated indicators from loading.

## Compatibility

- Requires MZpack Indicators 4.2.3+
