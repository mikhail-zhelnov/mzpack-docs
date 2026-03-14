---
title: "MZpack Indicators 3.18.2"
authors: [mzpack]
tags: [indicators]
---

Footprint S/R zone improvements, Volume per second metric, and crypto instrument force option.

<!-- truncate -->

## What's New

### mzVolumeProfile

- Sigma 1/2 values are now in decimal format

### mzFootprint

- Added "Statistics Grid -- Volume per second" metric
- Introduced "S/R zones: ended by BarTouch" option
- Added "S/R zones: approaching, ticks" parameter for zone termination based on price proximity

### General

- Added "General -- Crypto force instrument" option for data connections that don't properly identify crypto pairs
- Relocated "Non-Crypto volumes divider" setting to the General category

## Bug Fixes

- **mzFootprint:** Fixed support/resistance zones ending unexpectedly with Reconstruct tape enabled
