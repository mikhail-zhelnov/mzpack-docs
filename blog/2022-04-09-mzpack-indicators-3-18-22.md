---
title: "MZpack Indicators 3.18.22"
authors: [mzpack]
tags: [indicators]
---

Bid/Ask relative scaling for Footprint, extended bar type support for Volume Profile, and TPO gap fix.

<!-- truncate -->

## What's New

### mzFootprint

- Implemented a "Bid/Ask relative scaling" feature that adjusts histogram widths proportionally to each other

### mzVolumeProfile

- Extended support to include Day, Week, and Month bar types when using Minute accuracy settings

## Bug Fixes

- **mzFootprint:** Fixed developing Naked levels within Volume Profile not displaying when positioned outside the visible chart area
- **mzFootprint:** Fixed behavior requiring Accuracy setting change to Tick to also update the indicator's Calculate mode to OnEachTick
- **mzVolumeProfile:** Corrected gaps appearing in TPO mode letters when price movements contain gaps
