---
title: "MZpack API 2.3.5 beta"
authors: [mzpack]
tags: [api, beta]
---

Ninja ATM support, Conjunction logical node, Dashboard improvements, and Range session validation.

<!-- truncate -->

## What's New

- Added support for Ninja ATM with `MZpackStrategyBase.PositionManagement` and `MZpackStrategyBase.NinjaTraderATM_TemplateName` properties
- Introduced Conjunction logical node functionality
- Added "Not Calculated" state option for Dashboard cells
- Implemented pop-up hint feature for Dashboard cells
- Added `Strategy.IsOpeningPositionEnabled` property
- Introduced `Range.IsInSession` property to validate patterns within the current session only
- Actions can now return `SignalDirection.None` to terminate signal/filter validation
- ControlPanel is now disabled while loading market data
- Enhanced custom item addition to MZpack ControlPanel

## Bug Fixes

- Resolved issue affecting custom items addition to MZpack ControlPanel
