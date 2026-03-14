---
title: "MZpack Strategies/API 2.3.15 beta"
authors: [mzpack]
tags: [strategies, api, beta]
---

Introduces the Footprint Action strategy, enhanced SignalsTree validation, and daily max drawdown risk management.

<!-- truncate -->

## What's New

- Added Footprint Action strategy for order flow analysis
- SignalsTree: Added MinValidatedCount property to specify the minimum number of validated signals required for OR tree operations. All logical nodes must be configured as OR operators for this feature to function properly.
- Added RiskManagement.DailyMaxDrawdown property for enhanced position management
