---
title: "MZpack Indicators 3.18.4"
authors: [mzpack]
tags: [indicators]
---

New rounded-size trade filtering, expanded Extra filters, and improved saturation calculations for BigTrade.

<!-- truncate -->

## What's New

### mzBigTrade

- New filter for identifying market participants trading with significant rounded sizes by filtering trades where volume represents a multiple of a specified value
- Selection filtering expanded through Extra filters, enabling users to choose between percent of volumes or percent of numbers of trades criteria
- Solid color mode now permits customizable saturation levels
- Saturation and heatmap calculations for trade markers refined to operate within the current chart frame, improving visual contrast

### General

- Version number display disabled by default
