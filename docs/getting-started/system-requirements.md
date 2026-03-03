---
sidebar_position: 1
title: "System Requirements"
description: "Hardware, software, and data feed requirements for running MZpack with NinjaTrader 8"
---

# System Requirements

## Platform

| Requirement | Specification |
|---|---|
| **Operating System** | Windows 10 / 11 (64-bit) |
| **Runtime** | .NET Framework 4.8 |
| **Trading Platform** | NinjaTrader 8.0.27 or later |

MZpack runs exclusively on Windows as a NinjaTrader 8 add-on. macOS and Linux are not supported.

## Hardware

MZpack processes real-time market data and renders order flow visualizations using Direct2D. Recommended specs:

| Component | Minimum | Recommended |
|---|---|---|
| **CPU** | Dual-core 2.0 GHz | Quad-core 3.0 GHz+ |
| **RAM** | 4 GB | 8 GB+ |
| **GPU** | DirectX 11 compatible | Dedicated GPU with 1 GB+ VRAM |
| **Display** | 1280x720 | 1920x1080 or higher |
| **Storage** | 500 MB free | SSD recommended |

Higher-resolution charts, multiple indicators, and tick-level data feeds increase CPU and memory usage.

## Data Feed

MZpack order flow indicators require **tick-level market data** (Level 1). The `mzMarketDepth` indicator additionally requires **Level 2 (market depth)** data.

Compatible data feeds include any provider supported by NinjaTrader 8 that delivers tick data — for example, Rithmic, CQG, Interactive Brokers, or Kinetick.

:::tip
For the most accurate order flow analysis, use a data feed that provides individual tick updates rather than aggregated snapshots. Rithmic and CQG are commonly used for futures order flow.
:::

## NinjaTrader 8 Installation

If you don't have NinjaTrader 8 installed:

1. Download NinjaTrader 8 from [ninjatrader.com](https://ninjatrader.com)
2. Run the installer and follow the setup wizard
3. Launch NinjaTrader 8 and connect to a data feed (live or simulated)

MZpack supports both **live** and **simulated (Sim101/Playback)** accounts.

## Development Requirements

If you plan to build custom indicators or strategies using the MZpack API, you will also need:

| Requirement | Specification |
|---|---|
| **IDE** | Visual Studio 2022 |
| **SDK** | .NET Framework 4.8 SDK |
| **Language** | C# 7.3 (maximum version supported) |

See the [API Reference — Project Setup](/api/getting-started/project-setup) for development environment configuration.
