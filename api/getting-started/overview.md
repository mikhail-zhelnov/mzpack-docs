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
| [ICandle](../core-types/candle.md) | OHLCV bar data |
| [Tick & ITrade](../core-types/tick-and-trade.md) | Individual ticks and trade data |

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

| Sample | Class | What It Demonstrates |
|---|---|---|
| [Advanced Template](../samples/advanced-template.md) | AdvancedTemplate | Advanced MZpack strategy template with full indicator setup |
| [Algo.Strategy Abstract Class](../samples/algo-strategy-abstract.md) | AlgoStrategy1 | Algo.Strategy abstract class with custom "no entries on stop loss bar" filter |
| [Biggest Trade Indicator](../samples/biggest-trade-indicator.md) | BiggestTradeIndicator | Custom indicator marking the biggest trade with a rectangle |
| [Control Panel](../samples/control-panel.md) | ControlPanel | Control Panel with [ControlPanel] attribute and CreateControlPanelElements() |
| [Custom Plots](../samples/custom-plots.md) | CustomPlots | Access mzFootprint data, custom plots via StrategyPlotIndicator |
| [Data Access — mzFootprint](../samples/data-access-footprint.md) | DataAccess_mzFootprint | Access StrategyFootprintIndicator data |
| [Data Access — mzVolumeDelta](../samples/data-access-volume-delta.md) | DataAccess_mzVolumeDelta | Access StrategyVolumeDeltaIndicator data |
| [Data Access — mzVolumeProfile](../samples/data-access-volume-profile.md) | DataAccess_mzVolumeProfile_MinuteAccuracy | Access StrategyVolumeProfileIndicator with Minute accuracy |
| [Export Indicator Values](../samples/export-indicators-values.md) | ExportIndicatorsValues | Export indicator values with Historical/Realtime temporality |
| [Fibonacci Retracement Entry](../samples/fibonacci-retracement-entry.md) | FiboRetracementEntryStrategy | Fibonacci retracement entry strategy |
| [Multi-DataSeries Advanced](../samples/multi-dataseries-advanced.md) | MultiDataSeriesAdvancedStrategy | Trading on a second data series |
| [Multi-DataSeries Strategy](../samples/multi-dataseries-strategy.md) | MultiDataSeriesStrategy | Using indicators on different data series |
| [Algo Strategy — ATM + TradesCluster](../samples/algo-strategy-atm.md) | MZpackAlgoStrategy0 | Algo.Strategy with proprietary ATM and TradesClusterSignal |
| [Algo Strategy — Patterns + ATM](../samples/algo-strategy-patterns.md) | MZpackAlgoStrategy1 | Patterns with ATM, BigTradeSignal, EMASignal, and DOMImbalanceFilter (Level 2, live/replay) |
| [Algo Strategy — Partially Visible](../samples/algo-strategy-partially-visible.md) | MZpackAlgoStrategy2 | Algo.Strategy with TradesClusterSignal, DOMImbalanceSignal, and Partially Visible mode |
| [Algo Strategy — Footprint Imbalance](../samples/algo-strategy-imbalance.md) | MZpackAlgoStrategy_Imbalance | Algo.Strategy with FootprintImbalanceSignal |
| [Custom Strategy — VWAP/POC](../samples/custom-strategy-vwap-poc.md) | MZpackCustomStrategy0 | StrategyVolumeProfileIndicator with VWAP/POC rules for backtesting (OnBarClose) |
| [Custom Strategy — BigTrade + VolumeProfile](../samples/custom-strategy-bigtrade-profile.md) | MZpackCustomStrategy1 | StrategyBigTradeIndicator with StrategyVolumeProfileIndicator in Custom mode for backtesting |
| [Custom Strategy — DOM + Footprint](../samples/custom-strategy-dom-footprint.md) | MZpackCustomStrategy4 | StrategyMarketDepthIndicator with StrategyFootprintIndicator, DOM imbalance/block/pace rules (Level 2, live/replay) |
| [Custom Strategy — Liquidity Migration](../samples/custom-strategy-liquidity-migration.md) | MZpackCustomStrategy6 | Liquidity migration from StrategyMarketDepthIndicator (1 Tick, live/replay) |
| [Technical Indicators](../samples/technical-indicators.md) | MZpackTechnicalSample0 | Using well-known technical indicators in MZpack strategies |
| [Risk Management](../samples/risk-management.md) | RiskManagement | RiskManagement class demo (OnBarClose) |
| [Trading Times](../samples/trading-times.md) | TradingTimes | TradingTimes feature (OnBarClose) |
