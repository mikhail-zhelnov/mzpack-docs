---
title: "MZpack API 2.3.13 beta"
authors: [mzpack]
tags: [api, beta]
---

New StopLimit entry method, unmanaged position support, and signal-based position management.

<!-- truncate -->

## What's New

- MZpack 3.18.12 core
- Added StopLimit method for the entry
- Added Strategy.IsUnmanaged property
- Added Strategy.RejectedToMarketOrder property
- Added OppositePatternAction.Unmanaged method when positions are managed by signals but not API
- Added Position.IsActive property
- Added Signal.Positions property to manage strategy positions from signals' code

## Bug Fixes

- Fixed MZpack strategies not being present in Strategy Analyzer
