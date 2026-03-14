---
title: "MZpack API 2.3.11 beta"
authors: [mzpack]
tags: [api, beta]
---

Signal-specific stop loss and profit target levels via new Node properties.

<!-- truncate -->

## What's New

- MZpack 3.18.6 core
- Added Node.StopLossPrice and Node.ProfitTargetPrice properties
- Assign them when the signal is validated inside OnCalculate() if you need signal-specific stop loss/profit target levels
