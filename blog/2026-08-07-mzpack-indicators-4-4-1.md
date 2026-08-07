---
title: "MZpack Indicators w/ Divergence 4.4.1"
authors: [mzpack]
tags: [indicators]
---

This release fixes licensing and activation: NinjaTrader no longer crashes minutes after a successful activation, an unreachable time server no longer freezes the start of the indicators, and a refused activation now says what actually went wrong.

<!-- truncate -->

## Bug Fixes

- **Crash a few minutes after start** — on machines where activation had succeeded, so nothing pointed at licensing (#73).
- **Slow start** — an unreachable time server could freeze the indicators for minutes. With no internet connection the "Internet connection required" message now arrives in about 10 seconds (#74).
- **Activation errors said the wrong thing** — every refusal was reported as "License cannot be verified for this machine". An invalid key, a deactivated license, an exhausted machine limit and an expired subscription now each get their own message. A request blocked by a WAF, proxy, antivirus or VPN is recognized as such, retried, and no longer blamed on the license.
- **Activation rejected by security software** on some machines, and could fail outright where no proxy was configured.
- **The stored license key is no longer lost** when NinjaTrader is killed at the wrong moment — activation is no longer asked for on every start.

## Improvements

- **license.log now explains a failed activation** and can be sent to support as is — the license key in it is masked.

## Compatibility

- NinjaTrader 8.0.27+
- Requires MZpack API 2.4.13+ for strategy use
- MZpack API / Strategies remains at 2.4.18 — unchanged in this release
