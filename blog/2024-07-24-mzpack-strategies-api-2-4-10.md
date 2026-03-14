---
title: "MZpack Strategies/API 2.4.10"
authors: [mzpack]
tags: [strategies, api]
---

New drawing objects export functionality for third-party indicator integration.

<!-- truncate -->

## What's New

### API

- New ChartObjectDescriptor and DrawingObjectsExport classes for exporting drawing objects created by third-party indicators
- Supported drawing tools: ArrowDown, ArrowUp, Diamond, Dot, Region, Square, Text, TextFixed, TriangleDown, and TriangleUp
- Additional drawing tools are accessible by tag, display text property, and color attributes

### Strategies

- New DrawingObjects_Export strategy added
- Export configuration is defined within an XML file, with a sample schema available for download
