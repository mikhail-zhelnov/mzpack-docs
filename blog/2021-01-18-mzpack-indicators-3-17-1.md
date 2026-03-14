---
title: "MZpack Indicators 3.17.1"
authors: [mzpack]
tags: [indicators]
---

Bug fixes for Volume Delta licensing, Footprint stat readability, and Volume Profile rendering.

<!-- truncate -->

## What's New

### mzFootprint

- Readability of stat values has been improved

## Bug Fixes

- **mzVolumeDelta:** Fixed indicator terminating if license checking was not completed before market data arrival
- **mzVolumeProfile:** Fixed last profile on the chart not rendering as expected if Position is RightOnChartMargin and Calculate is OnBarClose
