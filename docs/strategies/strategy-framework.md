---
sidebar_position: 2
title: "Strategy Framework"
description: "Architecture and usage of the MZpack strategy framework with patterns, decision trees, signals, entries, and risk management"
---

# Strategy Framework

The MZpack strategy framework organizes trading logic into a structured pipeline: **patterns** define trading conditions through **decision trees** of **signals** and **filters**, which trigger **entries** with protective orders, managed by **position management** and **risk management** rules. This page covers each component in detail.

## Patterns

A pattern is a set of conditions that, when satisfied, produce a determined trading direction (Long or Short). Patterns are the central organizing unit of any MZpack strategy.

### Pattern Types

| Type | Purpose |
|---|---|
| **Entry** | Opens a new position when validated |
| **Exit** | Closes an existing position when validated (optional) |
| **Reversal** | Closes the current position and opens one in the opposite direction |
| **ScaleIn** | Adds to an existing position |
| **ScaleOut** | Reduces an existing position |

### How a Pattern Works

When a pattern is evaluated, three steps occur in sequence:

1. **Signals tree** — the signals decision tree is evaluated. If a determined direction (Long or Short) results, proceed to step 2. Otherwise the pattern is not validated.
2. **Filters tree** — the filters decision tree is evaluated starting from the bar at which signals validated. If the direction is confirmed, proceed to step 3.
3. **Entry** — a position is opened according to the entry configuration and the determined direction.

The signals tree must contain at least one signal. The filters tree is optional — if no filters are present, the pattern proceeds directly from signals to entry.

### Pattern Localization

A pattern can be localized to constrain where its signals and filters must occur:

- **Price range** — signals/filters must occur within a specified number of ticks
- **Bar range** — signals/filters must occur within a specified number of bars
- **Session** — signals/filters must occur within the current trading session

Price and bar ranges can be set independently for the signals tree and the filters tree.

### Allowed Direction

Each pattern has an **AllowedDirection** property that restricts which directions the pattern can validate: Long, Short, or Any (both). The resulting direction from the decision trees must be consistent with the allowed direction.

## Decision Trees

Signals and filters are organized into logical decision trees. Each tree has a root logical node, and supports three types of nodes:

- **Logical node** — performs AND, OR, or CONJUNCTION operations on its child nodes
- **Signal/Filter node** — a terminal node that evaluates market data and returns a direction (Long, Short, Any, or None)
- **Action node** — performs auxiliary calculations without affecting the resulting direction, but can return None to terminate tree evaluation

### Logic Operations

Each logical node combines the directions of its children using one of three operations:

| Operation | Input | Result |
|---|---|---|
| **AND** | None, None | None |
| **AND** | Long, None | None |
| **AND** | Long, Short | None |
| **AND** | Long, Long | Long |
| **AND** | Long, Any | Long |
| **OR** | None, None | None |
| **OR** | Long, None | Long |
| **OR** | Long, Short | None |
| **OR** | Long, Any | Long |
| **CONJUNCTION** | None, None | None |
| **CONJUNCTION** | Long, None | Long |
| **CONJUNCTION** | Short, Long | Any |
| **CONJUNCTION** | Long, Any | Any |

**AND** requires all children to agree on direction. **OR** accepts any single valid direction. **CONJUNCTION** combines differing directions into Any — useful when you want coherent signals in a range without requiring a specific order.

### Short-Circuit Evaluation

By default, AND nodes use short-circuit evaluation: if the first child returns None, the remaining children are skipped. This improves performance but makes the result dependent on the order of signals in the tree. For ranged patterns where signal order matters, consider using a CONJUNCTION root node with separate Long and Short branches.

### Tree Structure Rules

- The root node is always a logical node
- Logical nodes cannot be terminal (leaf) nodes — they must have children
- Signal/filter nodes must be terminal nodes
- The signals tree must have at least one signal node
- The filters tree root can be terminal (empty), meaning no filters are used

Invalid tree structures raise an error on strategy initialization.

## Signals

A signal processes incoming market data and determines a trading direction based on indicator values. Each signal has:

- **Direction** — the current output: Long, Short, Any, or None
- **Entry price** — an optional price for opening the position
- **Chart range** — the bar/price range where the signal was validated (for pattern localization)

### Calculation Modes

| Mode | Description |
|---|---|
| **OnEachTick** | Signal is recalculated on every incoming tick |
| **OnBarClose** | Signal is recalculated only when a bar closes |
| **NotApplicable** | Used for Level 2 (DOM) signals that process market depth events independently |

### Market Data Sources

| Source | Description |
|---|---|
| **Level1** | Order flow data (tick data) — used by most signals |
| **Level2** | Market depth / DOM data — used by DOM-based signals |
| **Custom** | Custom event source |

### Built-in Signals

The framework includes these ready-to-use signals:

| Signal | Indicator | Description |
|---|---|---|
| TradesClusterSignal | mzBigTrade | Detects a cluster of trades at a given side within a bar/price range |
| BigTradeSignal | mzBigTrade | LONG for sell trades, SHORT for buy trades |
| FootprintImbalanceSignal | mzFootprint | LONG for buy imbalances, SHORT for sell imbalances |
| FootprintAbsorptionSignal | mzFootprint | LONG for sell absorptions, SHORT for buy absorptions |
| FootprintSRZonesSignal | mzFootprint | Searches for S/R zones (imbalance or absorption type) |
| ClusterZonesSignal | mzFootprint | Searches for consecutive cluster zones in the current bar |
| BarJoinedPOCsSignal | mzFootprint | Validates if the bar has a given number of joined POCs |
| BarDeltaSignal | mzFootprint | LONG for positive delta, SHORT for negative delta |
| CumulativeDeltaSignal | mzFootprint | LONG for positive session cumulative delta, SHORT for negative |
| DeltaRateSignal | mzFootprint | LONG for positive delta rate, SHORT for negative delta rate |
| OrderflowBarMetricsSignal | mzFootprint | Signal based on orderflow metrics of the bar |
| DeltaDivergenceSignal | mzDeltaDivergence | Detects delta-price divergence patterns |
| RelativeToProfileSignal | mzVolumeProfile | SHORT if price above VWAP/VAH, LONG if below VWAP/VAL |
| VolumeProfileDeltaSignal | mzVolumeProfile | LONG for negative profile delta, SHORT for positive |
| DOMImbalanceSignal | mzMarketDepth | Detects DOM imbalance; entry at best bid (LONG) or best offer (SHORT) |
| DOMBlockSignal | mzMarketDepth | Detects large limit orders in the DOM |
| BarIcebergsSignal | mzVolumeDelta | LONG for icebergs on bid side, SHORT for icebergs on ask side |
| BarVolumeSignal | Volume | Validates if bar volume meets a minimum threshold |
| BarMetricsSignal | Price Action | Signal based on price action patterns inside the bar |
| BarWickSignal | OHLC | LONG for bars with low wick only, SHORT for bars with high wick only |
| UpDownBarSignal | OHLC | LONG for bullish bars, SHORT for bearish bars |

Custom signals can be created by extending the Signal base class.

## Filters

Filters are structurally identical to signals — they process market data and return a direction. The distinction is organizational: filters are placed in the **filters tree**, which is evaluated after the signals tree validates. This separation lets you define primary trading conditions as signals and confirmations as filters.

For example, a strategy might use big-trade clusters and absorption zones as signals, and DOM imbalance as a filter to confirm the entry direction before opening a position.

## Entry Configuration

When a pattern validates, a position is opened according to the entry configuration.

### Order Methods

| Method | Description |
|---|---|
| **Market** | Submits a market order for immediate execution |
| **Limit** | Submits a limit order at the price generated by the pattern, with optional shift in ticks |
| **StopLimit** | Submits a stop-limit order |

For limit orders, additional options include:

- **Limit entry shift** — offset in ticks added to the pattern-generated price
- **Limit entry price chase** — moves the pending limit order tick-by-tick as price moves away
- **Cancel limit order** — cancels unfilled limit orders after a specified number of ticks, bars, or milliseconds

### Protective Orders

| Order Type | Description |
|---|---|
| **Stop Loss** | Closes the position at a specified number of ticks or a fixed price from entry |
| **Profit Target** | Takes profit at a specified number of ticks or a fixed price from entry |
| **Break-even** | Moves the stop loss to the entry price (plus an optional shift) after price moves a specified number of ticks in your favor |
| **Trail** | A trailing stop that activates after a specified profit threshold, then follows price at a defined distance and step size |

Each entry also specifies a **Quantity** (number of contracts) and a **Signal name** for order identification.

## Position Management

### ATM Modes

MZpack strategies support two ATM (Advanced Trade Management) approaches:

| Mode | Description |
|---|---|
| **MZpack ATM** | Uses MZpack's built-in order management with Entry, Trail, and Break-even classes |
| **NinjaTrader ATM** | Delegates order management to a NinjaTrader ATM strategy template |

The ATM mode is configured via the strategy's PositionManagement property.

### Opposite Pattern Action

When a position is open and the pattern validates in the opposite direction, the strategy's behavior is controlled by the OppositePatternAction setting:

| Action | Description |
|---|---|
| **None** | Keep the current position, ignore the opposite signal |
| **Close** | Close the current position |
| **Reverse** | Close the current position and open a new one in the opposite direction |
| **Unmanaged** | Signals continue to be calculated after entering a position — can be used for scaling in |

### Position Lifecycle

The position progresses through these states:

| State | Description |
|---|---|
| **Flat** | No position open |
| **EntrySubmitting** | Entry order has been submitted |
| **LongLimitPending** / **ShortLimitPending** | Limit order is pending, not yet filled |
| **LongMarketPending** / **ShortMarketPending** | Market order is pending |
| **Long** / **Short** | Position is filled |

## Trading Times

The strategy can be restricted to specific trading hours using the Trading Times setting:

- In **Auto** mode, no entries are made outside trading times. Open positions are closed and pending orders are cancelled when trading times end.
- In **Manual** mode, trading times do not affect the strategy — signals continue to display regardless of the time.

## Risk Management

Risk management enforces daily limits that apply at the **account level** (not per instrument). All limits reset overnight if the strategy is not in a position.

| Limit | Description |
|---|---|
| **DailyLossLimit** | Maximum loss allowed in a single day. The strategy stops trading when realized + unrealized PnL reaches this negative threshold. |
| **DailyMaxDrawdown** | A trailing daily loss limit. Tracks the peak account value for the day and stops trading if the account drops by this amount from the peak. |
| **DailyProfitLimit** | Maximum profit target for the day. The strategy stops trading when realized + unrealized PnL reaches this positive threshold. |
| **DailyTradesLimit** | Maximum number of trades (filled entries) allowed per day. |

When a risk limit is reached, the current position is closed automatically and no further entries are made for the rest of the day.

:::note
Risk management tracks both realized and unrealized PnL. An open position's floating profit or loss counts toward daily limits.
:::

## Backtesting

MZpack strategies can be backtested in the NinjaTrader Strategy Analyzer:

1. Enable the **MZpack: backtesting** option in the strategy settings
2. Open NinjaTrader **Strategy Analyzer**
3. Select your strategy and configure the backtest parameters
4. Run the backtest

:::note
Enabling backtesting increases historical data loading time for mzFootprint and mzVolumeProfile indicators, as load-time optimizations must be disabled to calculate all values on historical bars.
:::

## Visualization

The strategy framework provides several visualization options, configured in the **Visual** category of the strategy properties.

### Pattern Background

Enable **Pattern: background** to display a colored vertical area on the chart when an Entry pattern validates. Separate colors can be assigned for Long and Short directions, and for the signals and filters portions of the pattern.

### Entry/Exit Markup

In **Manual** operating mode, enable **Entry/Exit: markup** to display entry and exit markers on the chart. Options include Marker only, or Marker and Text.

### Pattern Dashboard

Enable **Pattern dashboard: show** to display a real-time view of the decision tree on the chart, showing the current state (direction) of each signal and filter on every bar. This is particularly useful in Manual mode for discretionary trading.

### Partially Visible Mode

When a strategy uses multiple indicators, the chart can become cluttered. **Partially Visible** mode shows only the indicator plots that are relevant to validated signals. Three strategy indicator classes support this mode:

| Strategy Indicator | Partially Visible Property |
|---|---|
| StrategyBigTradeIndicator | ITrade.View.PartiallyVisible |
| StrategyFootprintIndicator | IFootprintBar.PartiallyVisible |
| StrategyMarketDepthIndicator | IMarketDepthBlock.PartiallyVisible |

Toggle Partially Visible mode by clicking the "eye" button next to the indicator name in the chart.

## Logging

MZpack strategies include a built-in logging system for debugging and monitoring.

### Log Levels

Log level is a bitmask — multiple levels can be combined:

| Level | Description |
|---|---|
| **NONE** | No logging |
| **NV_PATTERN_OBC** | Log not-validated pattern state on each bar close (for debugging) |
| **V_PATTERN** | Log pattern when validated |
| **ORDER** | Log order events: submitted, working, filled, partially filled, cancelled, rejected |
| **ENTRY** | Log entry details |
| **POSITION** | Log position state changes |
| **PROPERTIES** | Log strategy properties on initialization |
| **ALL** | All of the above |

### Log Targets

| Target | Description |
|---|---|
| **NinjaScriptOutput** | NinjaTrader Output window |
| **File** | Text file in `Documents\NinjaTrader 8\mzpacklog\` |
| **All** | Both Output window and file |

## Control Panel

The optional **Control Panel** is a panel on the right side of the chart that provides runtime controls for the strategy. It can display operating mode switches, direction selectors, and other configurable properties. Enable it with the **ControlPanelShow** option. The panel is disabled while historical data is loading.

## Multi-Data Series

Strategies can use multiple timeframes or instruments by adding additional data series. Each MZpack indicator and signal can be attached to a specific data series by index, enabling multi-timeframe analysis within a single strategy.
