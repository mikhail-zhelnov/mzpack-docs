---
sidebar_position: 0
title: "Source Code Walkthroughs"
description: "Developer-level walkthroughs of the built-in MZpack strategy source files, and where to find them on disk."
---

# Source Code Walkthroughs

This section provides developer-level walkthroughs of the built-in strategy source files — class structure, indicator wiring, signal implementations, decision tree construction, and data export schemas. Use them as reference implementations when building your own strategies.

:::info Where these files live
Each walkthrough lists its source file as `[INSTALL PATH]/API/Strategies/<Name>/…`. `[INSTALL PATH]` is your MZpack for NinjaTrader 8 installation folder — see [Source Code Location](../getting-started/source-code-location.md) for the full installation folder layout and how to compile a sample.
:::

## Built-in Strategies

| Strategy | What It Demonstrates |
|---|---|
| [Footprint Action](footprint-action.md) | 10 signals, AND/OR tree with mandatory grouping, runtime signal toggle, EMA indicator, per-signal bar filters |
| [Ghost Resistance](ghost-resistance.md) | 3 indicators, AND tree with OR sub-node, signal dependency, limit orders, one-entry-per-bar filter |
| [Data Export](data-export.md) | Non-trading utility, conditional indicators, per-indicator export schemas, 100+ export fields |
| [Drawing Objects Export](drawing-objects-export.md) | Minimal strategy, XML schema loading, ChartObjectDescriptor mappings |
