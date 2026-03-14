---
title: "MZpack Indicators 3.18.31"
authors: [mzpack]
tags: [indicators]
---

Cluster Zones enhancements, Working time support for Volume Profiles, and DeltaDivergence visibility controls.

<!-- truncate -->

## What's New

### mzFootprint

- Cluster Zones received three new parameters: "on bar close," "ignore bar high/low," and "box"
- Added "Grid in front of Footprint" to the Statistics Grid category
- Background settings for Statistics Grid now apply to Legend as well

### mzVolumeProfile

- Implemented Working time support across all profile modes
- The "General -- Working time" option defines the working time interval for data processing
- Users can set start and stop times for processing market data, including overnight intervals where stop time falls on the next day
- Continuous mode with Working time enabled is recommended for optimal results

### mzDeltaDivergence

- Added complete visibility control through toolbar eye button functionality
- The "Show Divergence" parameter has been deprecated

## Bug Fixes

- **mzFootprint:** Fixed Cluster Zones issue when Reconstructed tape was enabled
- **mzVolumeDelta & mzDeltaDivergence:** Resolved scaling issues with additional plots on the indicator panel
