---
title: "MZpack Indicators 3.18.25"
authors: [mzpack]
tags: [indicators]
---

Introduces the Visual Tape presentation mode for mzBigTrade and statistics grid projection for mzFootprint.

<!-- truncate -->

## What's New

### mzBigTrade

A new presentation mode called "Tape" has been introduced as an alternative to the default trade presentation. Switch to this mode by setting Presentation -- Type = Tape.

The Tape view displays trades sequentially as they appear in the order flow. Key configuration options include:
- Marker size adjustment via "Tape: marker size, px"
- Marker style options: Bubble or Box formats
- Trades not meeting filter criteria display as small dots
- Positioning flexibility with "Presentation -- Tape: position offset, px" to shift the tape display left or right
- Tape can overlay the chart, appear on the right margin, or display in both locations

### mzFootprint

- The statistics grid now projects onto the chart itself. The Volume highlight feature displays a vertical area on the chart marking bars that meet or exceed the specified threshold.
