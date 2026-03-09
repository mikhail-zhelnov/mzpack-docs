---
sidebar_position: 1
title: "Strategies Overview"
description: "Overview of MZpack automated trading strategies and the strategy framework for NinjaTrader 8"
---

# Strategies Overview

MZpack strategies are automated and semi-automated trading systems for NinjaTrader 8 that use order flow signals derived from MZpack indicators. The strategy framework organizes trading logic into patterns, decision trees, entries, and risk management — letting you build rule-based trading algorithms without writing code from scratch.

## Operating Modes

Every MZpack strategy runs in one of two operating modes:

| Mode | Description |
|---|---|
| **Auto** | The strategy submits orders automatically via an ATM (MZpack ATM or NinjaTrader ATM) when a pattern is validated |
| **Manual** | The strategy evaluates patterns and displays signals on the chart, but does not submit orders — you trade discretionally based on the visual output |

The operating mode can be changed at any time from the strategy properties or the [Control Panel](strategy-framework.md#control-panel).

## Relationship to Indicators

Strategies use their own internal indicator classes rather than the chart indicators you add manually. Each strategy indicator class corresponds to a chart indicator:

| Strategy Indicator Class | Chart Indicator |
|---|---|
| StrategyFootprintIndicator | [mzFootprint](../indicators/mzFootprint.md) |
| StrategyVolumeProfileIndicator | [mzVolumeProfile](../indicators/mzVolumeProfile.md) |
| StrategyVolumeDeltaIndicator | [mzVolumeDelta](../indicators/mzVolumeDelta.md) |
| StrategyBigTradeIndicator | [mzBigTrade](../indicators/mzBigTrade.md) |
| StrategyMarketDepthIndicator | [mzMarketDepth](../indicators/mzMarketDepth.md) |
| StrategyDeltaDivergenceIndicator | [mzDeltaDivergence](../indicators/mzDeltaDivergence.md) |

Strategy indicators are not visible on the chart by default. Use **Partially Visible** mode to show only the indicator data relevant to validated signals — see [Visualization](strategy-framework.md#visualization).

## Strategy Framework at a Glance

The strategy framework provides building blocks for constructing trading algorithms:

- **Pattern** — a set of conditions (signals + filters) that, when satisfied, produce a trading direction (Long or Short). Pattern types include Entry, Exit, Reversal, Scale-in, and Scale-out.
- **Signal** — processes market data and outputs a direction. Signals are organized into a decision tree with AND/OR/CONJUNCTION logic.
- **Filter** — same as a signal but placed in a separate filters tree, evaluated after signals validate.
- **Entry** — defines how a position is opened: order method (Market, Limit, Stop-Limit), stop loss, profit target, break-even, and trail.
- **Risk Management** — daily loss limit, max drawdown, profit limit, and trades limit.
- **Visualization** — pattern background coloring, entry/exit markup, and a real-time pattern dashboard.

For a detailed walkthrough, see the [Strategy Framework](strategy-framework.md) page.

## Built-in Strategies

MZpack ships with three ready-to-use strategies:

| Strategy | Description |
|---|---|
| **Footprint Action** | An order flow strategy with 10 delta and footprint signals (delta divergence, delta trap, stacked imbalances, etc.) combined using AND/OR logic |
| **GhostResistance** | A reversal strategy targeting liquidity traps — detects absorption, big trades, and price action near volume profile levels to trade reversals |
| **Data Export** | A utility strategy that exports indicator data (footprint, volume profile, big trades, market depth) to CSV files for external analysis and machine learning |

For configuration details, see [Built-in Strategies](built-in-strategies.md).

## Adding a Strategy

1. Right-click on a NinjaTrader 8 chart
2. Select **Strategies**
3. Search for the strategy name (e.g., `FootprintAction`)
4. Click **Add**, configure the parameters, then click **OK**
5. Enable the strategy from the chart toolbar or **Strategies** tab in the Control Center

## Product Availability

Strategy features require specific license types:

| Feature | FREE | TRIAL | Indicators | API |
|---|---|---|---|---|
| Chart indicators | Limited | All 6 | All 6 | — |
| Built-in strategies | — | Yes | — | Yes |
| Strategy framework (custom strategies) | — | Yes | — | Yes |
| Data Export Strategy | — | Yes | — | Yes |
| Risk management | — | Yes | — | Yes |

See [Licensing](../getting-started/licensing.md) for details.
