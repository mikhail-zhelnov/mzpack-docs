---
title: "MZpack Indicators 3.18.9"
authors: [mzpack]
tags: [indicators]
---

Reduced minimal font size, Duration metric for Footprint, and new tape reconstruction parameter.

<!-- truncate -->

## What's New

### mzFootprint

- Minimal font size has been reduced
- Added Duration (duration of the bar) metric to the Statistics Grid

### Common

- Introduced "Orderflow -- Reconstruct tape: timestamps only" parameter enabling Level 1 event (best bid/ask) exclusion
- When enabled, trades with equal timestamps merge for streamlined reconstruction
- Note: Icebergs and DOM pressure/support metrics become unavailable when this feature is active

## Bug Fixes

- **mzFootprint:** Fixed Cluster zones always being broken on session end regardless of settings
