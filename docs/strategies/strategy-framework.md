---
sidebar_position: 2
title: "Strategy Framework"
description: "Architecture and usage of the MZpack strategy framework with patterns, decision trees, signals, entries, and risk management"
---

# Strategy Framework

The MZpack strategy framework organizes trading logic into a structured pipeline: **patterns** define trading conditions through **decision trees** of **signals** and **filters**, which trigger **entries** with protective orders, managed by **position management** and **risk management** rules. This page covers each component in detail.

:::note
Every MZpack strategy inherits the settings documented on this page. In the NinjaTrader strategy properties they all appear under the **MZpack** category; the tables below are grouped by topic and follow the order of that category. Settings specific to an individual strategy are documented in [Built-in Strategies](./built-in-strategies.md).
:::

## Strategy Settings

| Setting | Default | Description |
|---|---|---|
| **Settings preset** | *(empty)* | Name that gives this strategy instance its own indicator and pattern template files. Empty means all instances share one set of templates in `Documents\NinjaTrader 8\mzpack\strategy\<namespace>\<strategy>\templates`; entering a name appends it to each file (`VP.ES.xml` instead of `VP.xml`) |
| **Backtesting** | false | Run the strategy in the historical state for the Strategy Analyzer. Increases loading time — do not enable it for chart trading. See [Backtesting](#backtesting) |
| **Operating** | Auto | Operating mode — Auto or Manual. See [Operating Modes](#operating-modes) |
| **Handle order errors** | true | Ignore real-time order errors instead of stopping the strategy, and handle protective orders moved on the chart. Resolves a Rithmic execution issue. Read-only |
| **Trace orders** | false | Write NinjaScript order tracing to the Output window (sets NinjaTrader's `TraceOrders`). Useful for diagnosing order submission |

### Operating Modes

| Mode | Description |
|---|---|
| **Auto** | Entries are submitted automatically when a pattern validates |
| **Manual** | Entries are not submitted — patterns and signals are only displayed on the chart, and positions are opened by hand from Chart Trader |

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

| Setting | Default | Description |
|---|---|---|
| **Position management** | MZpack | Which layer manages the position — MZpack (built-in Entry, Trail, and Break-even classes) or NinjaTraderATM (a NinjaTrader ATM strategy template) |
| **NinjaTrader ATM: template** | *(none)* | Name of the NinjaTrader ATM template to apply. The drop-down lists the ATM templates installed in NinjaTrader. Applies when Position management = NinjaTraderATM |
| **NinjaTrader ATM: entry method** | Market | Order type used to open the ATM position — Market, Limit, or StopLimit. Applies when Position management = NinjaTraderATM |

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

MZpack strategies can be backtested in the NinjaTrader **Strategy Analyzer** (order flow strategies, using Tick Replay) or against a **Market Replay** connection (strategies that need bid/ask volumes or the order book). Enable the **Backtesting** parameter — or set `EnableBacktesting = true` in code — so the strategy runs in the historical state.

See **[Backtesting](./backtesting.md)** for the full workflow, Tick Replay prerequisites, and how to choose between the two paths.

## Visualization

The strategy framework provides several visualization options, configured in the **Visual** category of the strategy properties.

### Pattern on Chart

Enable **Pattern on chart: show** to display a colored area on the chart when a pattern validates. The area is drawn over the bar/price range in which the pattern was found, with separate strokes for the signals portion and the filters portion, and for Long and Short directions.

| Setting | Default | Description |
|---|---|---|
| **Pattern on chart: show** | true | Draw the validated pattern's area on the chart |
| **Pattern on chart: Buy signal(s)** | Green, solid, 3 px, 25 % opacity | Stroke of the area covering the signals of a Long pattern |
| **Pattern on chart: Sell signal(s)** | Red, solid, 3 px, 25 % opacity | Stroke of the area covering the signals of a Short pattern |
| **Pattern on chart: Buy filter(s)** | Green, solid, 3 px, 10 % opacity | Stroke of the area covering the filters of a Long pattern |
| **Pattern on chart: Sell filter(s)** | Red, solid, 3 px, 10 % opacity | Stroke of the area covering the filters of a Short pattern |

### Entry/Exit Markup

Enable **Entry/Exit: markup** to display entry and exit markers on the chart. This is most useful in **Manual** operating mode, where it shows where the strategy would have entered and exited.

| Setting | Default | Description |
|---|---|---|
| **Entry/Exit: markup** | None | Marker style drawn at the entry and exit price — None, Marker (triangle only), or MarkerAndText (triangle plus the entry/exit label) |
| **Entry/Exit: Buy marker** | Lime | Marker color for Long entries and exits |
| **Entry/Exit: Sell marker** | Red | Marker color for Short entries and exits |

### Pattern Dashboard

Enable **Pattern dashboard: show** to display a real-time view of the decision tree on the chart, showing the current state (direction) of each signal and filter on every bar. This is particularly useful in Manual mode for discretionary trading.

The dashboard is a grid: one row per signal or filter node, one column per bar. Each cell is stroked with the color of the direction that node returned on that bar.

| Setting | Default | Description |
|---|---|---|
| **Pattern dashboard: show** | false | Show the decision-tree dashboard on the chart |
| **Pattern dashboard: LONG** | Green | Cell stroke when the node returned Long |
| **Pattern dashboard: SHORT** | Red | Cell stroke when the node returned Short |
| **Pattern dashboard: ANY** | RoyalBlue | Cell stroke when the node returned Any (both directions) |
| **Pattern dashboard: NONE** | DimGray | Cell stroke when the node returned None (no direction) |
| **Pattern dashboard: legend** | false | Show the legend that names the signal or filter in each row |
| **Pattern dashboard: position** | Bottom | Edge of the chart panel the grid is anchored to — Top or Bottom |
| **Pattern dashboard: offset, px** | 0 | Vertical offset from the anchor edge in pixels; positive values move the grid up, negative values move it down |
| **Pattern dashboard: row height, px** | 28 | Height of one dashboard row in pixels, range: 10–100 |
| **Pattern dashboard: font** | Arial 12 | Font of the dashboard cell and legend text |

### Partially Visible Mode

When a strategy uses multiple indicators, the chart can become cluttered. **Partially Visible** mode shows only the indicator plots that are relevant to validated signals. Three strategy indicator classes support this mode:

| Strategy Indicator | Partially Visible Property |
|---|---|
| StrategyBigTradeIndicator | ITrade.View.PartiallyVisible |
| StrategyFootprintIndicator | IFootprintBar.PartiallyVisible |
| StrategyMarketDepthIndicator | IMarketDepthBlock.PartiallyVisible |

Toggle Partially Visible mode by clicking the "eye" button next to the indicator name in the chart. See [Algo Strategy — Partially Visible](/api/samples/algo-strategy-partially-visible) for a full code sample.

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
| **None** | Logging disabled |
| **NinjaScriptOutput** | NinjaTrader Output window |
| **File** | Text file in `Documents\NinjaTrader 8\mzpacklog\` |
| **All** | Both Output window and file |

### Logging Settings

Each **Log:** toggle sets one bit of the log level bitmask described above.

| Setting | Default | Description |
|---|---|---|
| **Log: target** | NinjaScriptOutput | Where log records are written — None, File, NinjaScriptOutput, or All |
| **Log: Validated PATTERN** | true | Log each pattern when it validates (`V_PATTERN`) |
| **Log: not Validated PATTERN on Bar Close** | false | Log the state of patterns that did *not* validate, on each bar close (`NV_PATTERN_OBC`). Verbose — intended for debugging a pattern that never fires |
| **Log: ORDER** | false | Log order events: submitted, working, filled, partially filled, cancelled, rejected (`ORDER`) |
| **Log: ENTRY** | true | Log entry details (`ENTRY`) |
| **Log: POSITION** | true | Log position state changes (`POSITION`) |
| **Log: PROPERTIES** | true | Log the strategy properties on initialization (`PROPERTIES`) |
| **Log: time** | true | Prefix each log record with a timestamp |

:::note
Logging is disabled automatically in the Strategy Analyzer — the log target and level are forced to None while the strategy runs there.
:::

## Alerts

The strategy can play a sound when a signal or a pattern validates. Alerts fire in real time only.

| Setting | Default | Description |
|---|---|---|
| **Signal alert: enable** | false | Play a sound whenever an individual signal validates |
| **Signal alert: sound** | mzpack_alert1.wav | Sound file for the signal alert |
| **Entry pattern alert: enable** | false | Play a sound when an Entry pattern validates |
| **Entry pattern alert: sound** | mzpack_alert5.wav | Sound file for the entry pattern alert |
| **Exit pattern alert: enable** | false | Play a sound when an Exit pattern validates |
| **Exit pattern alert: sound** | mzpack_alert6.wav | Sound file for the exit pattern alert |

:::tip
See [Sound Files](/docs/getting-started/sound-files) for the full list of pre-installed sounds and how to add custom WAV files.
:::

## Control Panel

The optional **Control Panel** is a panel on the right side of the chart that provides runtime controls for the strategy. It has two tabs: **Properties**, a property grid for the strategy's settings, and a tab named after the strategy holding its custom controls — operating mode switches, direction selectors, and any control the strategy adds. The panel is disabled while historical data is loading.

| Setting | Default | Description |
|---|---|---|
| **Control Panel: show** | false | Show the control panel on the right side of the chart |
| **Control Panel: width** | 300 | Panel width in pixels |
| **Control Panel: show properties** | true | Include the **Properties** tab with the strategy property grid. Disable to show only the strategy's own controls |

## Multi-Data Series

Strategies can use multiple timeframes or instruments by adding additional data series. Each MZpack indicator and signal can be attached to a specific data series by index, enabling multi-timeframe analysis within a single strategy.
