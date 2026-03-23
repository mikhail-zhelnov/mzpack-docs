---
title: "MZpack Indicators w/ Divergence 4.2.0"
authors: [mzpack]
tags: [indicators]
---

Version 4.2.0 introduces LVN/HVN (Low/High Volume Nodes) detection and display in mzVolumeProfile along with rendering and export fixes.

<!-- truncate -->

## What's New

- **mzVolumeProfile: LVN/HVN detection and display** — automatic identification of Low Volume Nodes and High Volume Nodes on volume profiles with configurable highlight brushes, separate LevelsValuesMode, and EndOfSession naked line extension
- **mzVolumeProfile: ContourStroke property** for Contour profile view customization

## Bug Fixes

- Fixed S/R and cluster zones not rendering when start bar is off-screen
- Fixed realtime export file not updating when IsExportWhileCollecting is enabled
- Fixed activation key not being requested from user
