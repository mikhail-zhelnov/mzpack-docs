---
title: "MZpack Indicators 3.19.0"
authors: [mzpack]
tags: [indicators]
---

Introduces dividing, merging, and unmerging of volume profiles, plus auto sources and Cluster Zones improvements for Footprint.

<!-- truncate -->

## What's New

### mzVolumeProfile

- Introduced functionality for dividing, merging, and unmerging of volume profiles
- Added support for dividing and merging custom profiles
- Implemented a "Buttons" option for enhanced user interface
- Added a profile divider line feature

### mzFootprint

- Introduced "Auto sources" feature that applies recommended sources automatically for Left and Right Footprints based on the chosen footprint style
- Added Cluster Zones capability that terminate when bars make contact
- Cluster Zones now work compatibly with rows aggregation
- Enhanced synthetic (non-orderflow) bars to populate with zero values when necessary

## Bug Fixes

- **mzVolumeProfile:** Fixed composite and continuous profiles not functioning as expected
- **mzFootprint:** Fixed a bug preventing Cluster Zone addition in certain scenarios when "Ignore high/low" was enabled
