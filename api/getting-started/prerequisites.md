---
sidebar_position: 2
title: "Prerequisites"
description: "Required software, tools, and knowledge for developing with the MZpack API on .NET Framework 4.8 and NinjaTrader 8."
---

# Prerequisites

Everything you need before writing your first MZpack indicator or strategy.

## Software

| Requirement | Version | Notes |
|---|---|---|
| **NinjaTrader 8** | 8.0.27 or later | v8.1.6 required for C# 13 |
| **.NET Framework** | 4.8 | Included with Windows 10/11 |
| **Visual Studio** | 2022 (any edition) | Community edition is free; optional if you use the NinjaTrader built-in editor |

### IDE Choice

You can write NinjaScript code in two ways:

| IDE | Best For |
|---|---|
| **NinjaTrader built-in editor** | Quick edits, single-file strategies, no project setup needed |
| **Visual Studio 2022** | Multi-file projects, IntelliSense, debugging, refactoring |

The built-in editor compiles code automatically when you save. Visual Studio gives you full IDE features but requires a project referencing NinjaTrader and MZpack assemblies — see [Project Setup](project-setup.md).

## MZpack License

The API requires one of the following license editions:

| Edition | API Access |
|---|---|
| **MZpack Strategies w/ Divergence** | Full strategy pipeline + all indicator interfaces |
| **MZpack Indicators & Strategies w/ Divergence** | Full strategy pipeline + all indicator interfaces |

The FREE and Indicators-only editions do not include strategy API access.

## Required Knowledge

| Topic | Why |
|---|---|
| **C#** | All MZpack code is C#. Familiarity with classes, interfaces, generics, and events is expected |
| **NinjaScript** | MZpack strategies extend `NinjaTrader.NinjaScript.Strategies.Strategy`. Understanding [State lifecycle](https://ninjatrader.com/support/helpGuides/nt8/state.htm), `OnStateChange`, `OnBarUpdate`, data series, and order methods is essential |
| **Order flow concepts** | Footprint, volume profile, delta, DOM — the data the API exposes. See the [MZpack Indicators](/docs/indicators/mzFootprint) documentation |

:::tip
If you are new to NinjaScript, start with the [NinjaTrader 8 Help Guide](https://ninjatrader.com/support/helpGuides/nt8/) — particularly the Strategy and Indicator development sections.
:::

## Verify Your Environment

Before proceeding to [Project Setup](project-setup.md), confirm:

1. **NinjaTrader 8 launches** and connects to a data feed (live or Sim101)
2. **MZpack is installed** — type `mz` in the Indicators dialog and verify all six indicators appear (see [Installation](/docs/getting-started/installation))
3. **Your license is active** — open any MZpack indicator properties and confirm it loads without a license error
4. **Visual Studio 2022 is installed** (if you plan to use it instead of the built-in editor)
