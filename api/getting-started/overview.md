---
sidebar_position: 1
title: "API Overview"
description: "Overview of the MZpack API for building custom indicators and automated trading strategies on NinjaTrader 8."
---

# API Overview

The MZpack API is a C# framework for building custom indicators and automated trading strategies on NinjaTrader 8. It exposes all public classes of the MZpack library, including data types guarded by the `#if DATA` compilation symbol. This gives you programmatic access to the same order flow data, volume profiling, and trade detection that power the MZpack chart indicators — letting you create your own analysis tools and trading algorithms.

## What You Can Build

| Use Case | Description |
|---|---|
| **Custom indicators** | Process order flow data (footprint, delta, volume profile, big trades, DOM) and render custom visualizations on NinjaTrader charts using SharpDX/Direct2D |
| **Automated strategies** | Build rule-based trading systems using the strategy pipeline — combine signals, filters, and decision trees with built-in position and risk management |
| **Data export** | Extract indicator data (footprint clusters, volume profiles, trade records, DOM snapshots) to CSV for external analysis or machine learning |

## Architecture

The API is organized into three layers:

**Core Types** — data structures that represent market data at every granularity:

| Type | What It Represents |
|---|---|
| [Candle / ICandle](../core-types/candle.md) | OHLCV bar data |
| [Tick, Trade, AggregatedTrade](../core-types/tick-and-trade.md) | Individual ticks, reconstructed trades, and aggregated trade records |
| [OrderFlowColumn / OrderFlowRow](../core-types/orderflow-column-row.md) | Footprint bar structure — columns of price levels with bid/ask volumes, delta, and trade counts |
| [VolumeProfile](../core-types/volume-profile.md) | Horizontal volume distribution with POC, Value Area, VWAP, and TPO data |

**Indicators API** — each chart indicator is accessible through a typed interface:

| Interface | Chart Indicator | Key Data |
|---|---|---|
| IFootprintIndicator | [mzFootprint](/docs/indicators/mzFootprint) | Footprint bars, clusters, imbalance, absorption, S/R zones |
| IVolumeProfileIndicator | [mzVolumeProfile](/docs/indicators/mzVolumeProfile) | Volume profiles, POC, Value Area, VWAP, TPO |
| IVolumeDeltaIndicator | [mzVolumeDelta](/docs/indicators/mzVolumeDelta) | Volume/delta histograms, cumulative delta, icebergs |
| IBigTradeIndicator | [mzBigTrade](/docs/indicators/mzBigTrade) | Filtered trades, iceberg detection, DOM pressure |
| IMarketDepthIndicator | [mzMarketDepth](/docs/indicators/mzMarketDepth) | DOM snapshots, liquidity, migration, imbalance |
| IDeltaDivergenceIndicator | [mzDeltaDivergence](/docs/indicators/mzDeltaDivergence) | ZigZag breakpoints, divergence signals |

**Strategy Pipeline** — components for building trading algorithms:

| Component | Role |
|---|---|
| [Action](../strategy-pipeline/action.md) | Signal generation — processes market data and outputs a trading direction |
| [Filter](../strategy-pipeline/filter.md) | Trade filtering — confirms or rejects signals based on additional conditions |
| [Decision Tree](../strategy-pipeline/decision-tree.md) | Combines signals and filters using AND/OR/CONJUNCTION logic |
| [Entry](../strategy-pipeline/entry.md) | Order submission — market, limit, or stop-limit with protective orders |
| [Exit](../strategy-pipeline/exit.md) | Position closing — stop loss, profit target, and exit signals |
| [Trail](../strategy-pipeline/trail.md) | Trailing stop — follows price at a configurable distance after activation |
| [Risk Management](../strategy-pipeline/risk-management.md) | Daily limits — loss, drawdown, profit, and trade count caps |

For a detailed walkthrough of how these components connect, see [Pipeline Overview](../strategy-pipeline/overview.md).

## Strategy Indicator Classes

Strategies use their own internal indicator instances rather than chart indicators. Each strategy indicator class wraps the corresponding chart indicator:

| Strategy Class | Chart Indicator | Data |
|---|---|---|
| StrategyFootprintIndicator | [mzFootprint](/docs/indicators/mzFootprint) | Level 1 |
| StrategyVolumeProfileIndicator | [mzVolumeProfile](/docs/indicators/mzVolumeProfile) | Level 1 |
| StrategyVolumeDeltaIndicator | [mzVolumeDelta](/docs/indicators/mzVolumeDelta) | Level 1 |
| StrategyBigTradeIndicator | [mzBigTrade](/docs/indicators/mzBigTrade) | Level 1 |
| StrategyMarketDepthIndicator | [mzMarketDepth](/docs/indicators/mzMarketDepth) | Level 2 |
| StrategyDeltaDivergenceIndicator | [mzDeltaDivergence](/docs/indicators/mzDeltaDivergence) | Level 1 |

Strategy indicators are not visible on the chart by default. Use **Partially Visible** mode to show only the data relevant to validated signals.

## Built-in Signals

The API ships with 20+ ready-to-use signals that you can combine in decision trees. A few examples:

| Signal | Source Indicator | Description |
|---|---|---|
| DeltaDivergenceSignal | mzDeltaDivergence | Price/delta divergence at swing points |
| FootprintImbalanceSignal | mzFootprint | Stacked imbalances indicating aggressive one-sided activity |
| FootprintAbsorptionSignal | mzFootprint | Passive absorption at price extremes |
| BigTradeSignal | mzBigTrade | Large trade detection with optional iceberg and sweep filters |
| RelativeToProfileSignal | mzVolumeProfile | Price position relative to VWAP, VAH, or VAL |
| DOMImbalanceSignal | mzMarketDepth | Order book bid/ask imbalance |

Custom signals are created by extending the `Signal` base class. See [Built-in Strategies](/docs/strategies/built-in-strategies) for examples of how these signals are combined.

## Requirements

| Requirement | Specification |
|---|---|
| **Platform** | NinjaTrader 8.0.27 or later |
| **Runtime** | .NET Framework 4.8 |
| **Language** | C# 13 (NinjaTrader v8.1.6 required) |
| **IDE** | Visual Studio 2022 or NinjaTrader 8 built-in editor |
| **License** | MZpack Strategies or MZpack Indicators w/ Divergence |

See [Prerequisites](prerequisites.md) for the full development environment setup, and [Project Setup](project-setup.md) for creating your first project.

## Samples

All samples are included in the MZpack source code wrapped in `#if APISAMPLE` blocks with XML summary comments.

| Sample | What It Demonstrates |
|---|---|
| [Basic Strategy](../samples/basic-strategy.md) | Building an automated strategy using the pipeline with signals, entry, and risk management |
| [Custom Indicators](../samples/custom-indicators.md) | Creating a custom indicator with SharpDX rendering on NinjaTrader charts |
| [Data Export](../samples/data-export.md) | Exporting order flow and volume profile data to CSV for external analysis |
| [Footprint Data Access](../samples/footprint-data-access.md) | Reading footprint clusters, delta, imbalances, and absorption levels via IFootprintIndicator |
| [Volume Profile Levels](../samples/volume-profile-levels.md) | Reading POC, Value Area, VWAP, and naked levels from IVolumeProfileIndicator |
| [Big Trade Filter](../samples/big-trade-filter.md) | Filtering trades by volume, iceberg size, and DOM pressure via IBigTradeIndicator |
| [DOM Liquidity Analysis](../samples/dom-liquidity.md) | Reading order book snapshots, liquidity migration, and imbalance data via IMarketDepthIndicator |
| [Custom Signal](../samples/custom-signal.md) | Creating a custom Signal subclass for the strategy decision tree |
| [Multi-Timeframe Strategy](../samples/multi-timeframe-strategy.md) | Strategy using multiple data series to combine signals from different timeframes |
| [Delta Divergence Strategy](../samples/delta-divergence-strategy.md) | Trading delta-price divergences using IDeltaDivergenceIndicator and the decision tree |
