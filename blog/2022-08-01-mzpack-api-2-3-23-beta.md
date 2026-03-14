---
title: "MZpack API 2.3.23 beta"
authors: [mzpack]
tags: [api, beta]
---

New Hammer with Absorption signal, 3rd part of position feature, and optimization for all main parameters.

<!-- truncate -->

## What's New

- Added "Hammer with Absorption" signal
- Absorption settings integrated into "Footprint" category
- Added 3rd part of position feature
- Added "Suspend after trade" option
- Optimization capability extended to all main parameters

### Hammer with Absorption Signal

This new signal executes trades when absorption occurs within a hammer candle pattern, indicating trapped sellers or buyers. The Point of Control (POC) filter allows traders to require absorption at, above, or below the POC level.

- **Long Entry:** Bullish hammer candle with buy absorption (trapped sellers) in the wick
- **Short Entry:** Bearish hammer candle with sell absorption (trapped buyers) in the wick
