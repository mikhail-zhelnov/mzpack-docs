---
title: "MZpack Indicators 3.18.13"
authors: [mzpack]
tags: [indicators]
---

Developing Tick POC, Trades Volume Profile positioning, and multiple bug fixes across indicators.

<!-- truncate -->

## What's New

### mzVolumeProfile

- Added Developing Tick POC

### mzBigTrade

- Added Trades Volume Profile -- Position option
- Added Trades Volume Profile -- Margin parameter

### mzFootprint

- Added Statistics Grid -- Background option

## Bug Fixes

- **mzVolumeProfile:** Fixed new profile being created starting from live market data when mode = Session and Working time is enabled
- **mzVolumeDelta:** Fixed Cumulated Delta starting not from zero at the beginning of the session
- **mzMarketDepth:** Fixed multiple market maker value not being saved in template
