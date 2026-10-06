---
title: "MZpack Indicators w/ Divergence 4.4.3"
authors: [mzpack]
tags: [indicators]
---

This release adds two stronger saturation presets to mzMarketDepth and mzBigTrade, and restores contrast in the Historical DOM after the display-volume filter is tightened.

<!-- truncate -->

## New Features

- **mzMarketDepth and mzBigTrade: Saturation presets 5 and 6** — two stronger options beyond preset 4. Presets 1–4 are unchanged, so existing charts retain their appearance. Since preset 4 already makes the strongest level fully opaque, the new presets increase saturation from the low end: the weakest level rises from an opacity of 40 (of 255) in preset 4 to 70 in preset 5 and 110 in preset 6, while the strongest level stays fully opaque. In mzBigTrade, where the preset also controls shape and line opacity, presets 5 and 6 correspond to 85% and 100%.

## Bug Fixes

- **mzMarketDepth: Historical DOM retains its contrast after lowering "Display volume, %"** — in the Saturation and Custom colour modes, the colour ramp now begins at the visibility threshold instead of zero. Tightening the filter therefore still spreads the remaining levels across the full saturation range, rather than making them appear in nearly the same colour. Heatmap and GrayScaleHeatmap already behaved this way; the modes now agree. If every visible level is extremal, it is drawn fully saturated. Realtime DOM is unchanged.
