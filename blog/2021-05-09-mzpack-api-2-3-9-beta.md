---
title: "MZpack API 2.3.9 beta"
authors: [mzpack]
tags: [api, beta]
---

Virtual OnEntryPatternValidated method and one-pattern-per-bar validation example.

<!-- truncate -->

## What's New

- Made MZpackStrategyBase.OnEntryPatternValidated() virtual (requires calling base method when overriding)
- Added implementation example demonstrating "one pattern validation per bar" for OnEachTick signals tree
- Sample code shows how to track the validated bar index and use it within OnValidateEntryPatternFilter() to prevent duplicate pattern validations within the same bar cycle
