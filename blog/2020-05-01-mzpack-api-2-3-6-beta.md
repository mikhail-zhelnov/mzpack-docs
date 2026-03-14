---
title: "MZpack API 2.3.6 beta"
authors: [mzpack]
tags: [api, beta]
---

Signal.GetDisplayName() method for signal name display in Log and Pattern Dashboard.

<!-- truncate -->

## What's New

- MZpack 3.18.3 core
- Added `Signal.GetDisplayName()` method to display signal names in the Log and Pattern Dashboard legend
- Custom signals can override this method to display relevant information
- The base implementation returns either a custom name or the class type name if no custom name exists
