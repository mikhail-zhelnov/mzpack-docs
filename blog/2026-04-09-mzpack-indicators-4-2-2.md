---
title: "MZpack Indicators w/ Divergence 4.2.2"
authors: [mzpack]
tags: [indicators]
---

Version 4.2.2 improves license verification robustness and network resilience.

<!-- truncate -->

## Bug Fixes

- Fixed `MachineLimitReached` (HTTP 403) being lost during the activation dialog flow
- Fixed lifetime keys being incorrectly blocked by clock manipulation checks in Release builds
- Fixed `MachineLimitReached` (HTTP 403) misreported as "Activation required"
- Fixed license validation MessageBox appearing repeatedly instead of once
- License result dialog is now triggered in `State.Configure`, before realtime, so users see it earlier
- Native verification session is now reinitialized on indicator reload after a network failure
- Managed fallback is now allowed in Release when native verification fails due to network
- `MachineLimitReached` is now always propagated over native crypto failure
