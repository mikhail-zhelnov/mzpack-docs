---
title: "MZpack Indicators 3.19.3"
authors: [mzpack]
tags: [indicators]
---

Major mzVolumeProfile update with ETH/RTH profile mode, TPO enhancements, and multiple bug fixes across indicators.

<!-- truncate -->

## What's New

### mzVolumeProfile

- Added ETH_RTH profile mode
- Added OnEachTick calculation for Minute accuracy (default)
- Added open/close letters for split mode
- Added open/close markers (triangle) for block split mode
- Adjusted price of period/profile closing letter
- Added calculation of TPO VA to split profiles
- TPO level ended by entire profile but not particular bar
- Added End of Day for TPO levels
- More condensed TPO letters

## Bug Fixes

- **mzBigTrade:** Fixed manually added levels not being manageable
- **mzFootprint:** Fixed unexpected normalization of bars when Calculate = OnBarClose
- **mzFootprint:** Fixed UA not working as expected since 3.19.0
- **Common:** Price line is not available when Calculate = OnBarClose
