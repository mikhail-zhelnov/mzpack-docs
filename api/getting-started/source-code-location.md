---
sidebar_position: 4
title: "Source Code Location"
description: "Where MZpack sample and strategy source code is installed on disk, and what the [INSTALL PATH] placeholder in the API reference refers to."
---

# Source Code Location

MZpack ships the complete C# source for all API samples, built-in strategies, signals, and framework classes alongside the compiled library. This page explains where those files live on disk and what the `[INSTALL PATH]` placeholder used throughout the API reference refers to.

## What `[INSTALL PATH]` Means

Every **Source:** line in the API reference points to a `.cs` file with a path like:

```
[INSTALL PATH]/API/Strategies/FootprintAction/FootprintAction.cs
```

`[INSTALL PATH]` is the **MZpack for NinjaTrader 8 installation folder** you chose when running the setup wizard. Every `[INSTALL PATH]/API/...` path in the docs is relative to that folder — replace the placeholder with your own installation path to locate the file.

## Installation Folder Layout

All source code lives under the `\API\` subfolder of the installation directory:

| Folder | Contents |
|---|---|
| `\API\samples\` | API samples — data access and strategy samples (the [Samples](../samples/advanced-template.md) walkthroughs) |
| `\API\Strategies\<Name>\` | Built-in strategy source — the [Source Code](../source-code/overview.md) walkthroughs (FootprintAction, GhostResistance, Data_Export, DrawingObjects_Export) |
| `\API\Signals\` | Signal framework base classes (`Node.cs`, `Signal.cs`, `LogicalNode.cs`, `RangeNode.cs`) and the built-in signal files |
| `\API\Indicators\` | Strategy indicator classes (`StrategyFootprintIndicator.cs`, `StrategyVolumeDeltaIndicator.cs`, …) |
| `\API\Extensions\Entries` / `Exits` / `Trails` | Entry, Exit, and Trail extensions |
| `\API\Actions\`, `\API\Filters\` | Action and Filter classes |
| `\API\ML\` | Machine learning source |
| `\API\` (root) | Core framework: `Strategy.cs`, `MZpackStrategyBase.cs`, `Position.cs`, `Positions.cs`, `RiskManagement.cs`, `TradingTime.cs`, `Pattern.cs`, `Range.cs` |

## Samples vs. the Zip Download

The samples are **precompiled** and ready to run in NinjaTrader — you can use them without touching the source. The `\API\samples\` folder holds the source so you can read, modify, and recompile them.

A zip archive of the samples is also available on [mzpack.pro](https://mzpack.pro), but the version on the site may lag behind your installed version — prefer the files in the installation folder. **Do not import the zip into NinjaTrader.** Unzip it to a folder and use it only to study the API.

## Compiling a Sample

The samples are wrapped in `#if APISAMPLE` blocks so they don't compile as-is. To build one, copy its `.cs` file into `Documents\NinjaTrader 8\bin\Custom\Strategies\`, remove the directives, and add a reference to `MZpack.NT8.Pro.dll`. See [Project Setup → Working with Samples](project-setup.md#working-with-samples) for the full steps.

## Related

- [API Overview](overview.md) — architecture and available interfaces
- [Source Code Walkthroughs](../source-code/overview.md) — developer-level walkthroughs of the built-in strategy source files
