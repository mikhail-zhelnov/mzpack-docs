---
sidebar_position: 1
title: "Enums Reference"
description: "Complete reference of all public enumerations in the MZpack API, grouped by topic."
---

# Enums Reference

All public enumerations in the MZpack API, grouped by topic.

## Profile Creation

### ProfileCreation

**Namespace:** `MZpack`

How a volume profile is created.

| Value | Description |
|---|---|
| `Bar` | Single bar profile |
| `Bars` | Fixed number of bars |
| `Volume` | Fixed volume threshold |
| `Delta` | Fixed delta threshold |
| `Tick` | Fixed tick count |
| `Session` | Single trading session |
| `Sessions` | Fixed number of sessions |
| `Daily` | Single day |
| `Days` | Fixed number of days |
| `Weekly` | Single week |
| `Weeks` | Fixed number of weeks |
| `Monthly` | Single month |
| `Months` | Fixed number of months |
| `Quarterly` | Single quarter |
| `Yearly` | Single year |
| `RTH_ETH` | Regular / Extended trading hours split |
| `Composite` | Composite profile (merged from multiple) |
| `Continuous` | Continuous rolling profile |
| `Custom` | Custom-defined creation |
| `None` | No creation type |

### ProfileType

**Namespace:** `MZpack`

| Value | Description |
|---|---|
| `TPO` | Time Price Opportunity (Market Profile) |
| `VP` | Volume Profile |
| `VP_TPO` | Combined Volume Profile and TPO |
| `None` | No type |

### ProfileMode

**Namespace:** `MZpack`

Volume display mode for profile bars.

| Value | Description |
|---|---|
| `Volume` | Total volume |
| `BuySell` | Separate buy/sell volume |
| `Delta` | Delta (buy − sell) |
| `VolumeDelta` | Volume with delta overlay |
| `None` | No mode |

### ProfileAccuracy

**Namespace:** `MZpack`

Data accuracy for volume profile calculations.

| Value | Description |
|---|---|
| `Tick` | Tick-level accuracy (requires Tick Replay) |
| `Minute` | Minute-level accuracy |

### ProfilePresentation

**Namespace:** `MZpack`

Visual presentation style for profiles.

| Value | Description |
|---|---|
| `Ladders` | Horizontal ladder bars |
| `Area` | Filled area |
| `Contour` | Contour outline |

### LevelMode

**Namespace:** `MZpack`

Display mode for profile levels (POC, VAH, VAL).

| Value | Description |
|---|---|
| `Off` | Levels hidden |
| `On` | Levels visible |
| `Naked` | Only naked (untouched) levels |
| `Extended` | Levels extended to the right edge |
| `Developing` | Developing levels shown over time |
| `DevelopingNaked` | Developing naked levels |

### NodeLevelMode

**Namespace:** `MZpack`

Display mode for LVN/HVN volume nodes.

| Value | Description |
|---|---|
| `Off` | Node detection disabled |
| `Highlight` | Highlight node price levels on the profile |
| `Extended` | Draw level lines extending to the chart right edge |
| `Naked` | Draw level lines that extend until price touches them |
| `HighlightAndExtended` | Highlight + extended level lines |
| `HighlightAndNaked` | Highlight + naked level lines |

### LVNHVNDetection

**Namespace:** `MZpack`

Detection method for Low/High Volume Nodes.

| Value | Description |
|---|---|
| `PercentOfPOC` | Detect nodes by volume threshold as percent of POC volume |
| `LocalExtrema` | Detect nodes as local minima/maxima among N neighbors |

### ProfileLevelType

**Namespace:** `MZpack`

| Value | Description |
|---|---|
| `POC` | Point of Control |
| `VAH` | Value Area High |
| `VAL` | Value Area Low |
| `TickPOC` | Tick-based Point of Control |

### ValuesMode

**Namespace:** `MZpack`

What values to display on profile bars.

| Value | Description |
|---|---|
| `Volume` | Total volume |
| `Delta` | Delta value |
| `BidAsk` | Bid and ask volumes |
| `None` | No values |

### TotalDeltaMode

**Namespace:** `MZpack`

How total delta is displayed on a profile.

| Value | Description |
|---|---|
| `Delta` | Total delta value |
| `BidAsk` | Separate bid/ask totals |
| `None` | No total delta |

### VWAPMode

**Namespace:** `MZpack`

VWAP display mode.

| Value | Description |
|---|---|
| `Last` | VWAP for the last profile only |
| `Dynamic` | Dynamic VWAP line |
| `DynamicStdDev1` | Dynamic VWAP with ±1 standard deviation |
| `DynamicStdDev2` | Dynamic VWAP with ±2 standard deviations |
| `None` | VWAP hidden |

---

## Order Flow

### OrderflowCalculationMode

**Namespace:** `MZpack`

How order flow (bid/ask) volumes are assigned to trades.

| Value | Description |
|---|---|
| `BidAsk` | Bid/Ask calculation. Use for futures and stock markets. Requires Tick Replay for historical data |
| `UpDownTick` | Up/Down tick calculation. Use for Forex and crypto |
| `Hybrid` | UpDownTick for historical data, BidAsk for live data. Use for NSE and similar markets |

### OrderflowApplyMode

**Namespace:** `MZpack`

When order flow calculation mode changes take effect.

| Value | Description |
|---|---|
| `ChartReload` | Applied on chart reload |
| `OnTheFly` | Applied immediately |

### TradeSide

**Namespace:** `MZpack`

| Value | Description |
|---|---|
| `Ask` | Ask side (buy trade) |
| `Bid` | Bid side (sell trade) |
| `NA` | Not applicable |

### SpreadTradesProcessing

**Namespace:** `MZpack`

How trades at the spread (between bid and ask) are handled.

| Value | Description |
|---|---|
| `Split` | Split volume equally between bid and ask |
| `LastKnownSide` | Assign to the last known trade side |
| `Ignore` | Ignore spread trades |

### ColorMode

**Namespace:** `MZpack`

Coloring mode for footprint cells and profile bars.

| Value | Description |
|---|---|
| `Solid` | Single solid color |
| `Saturation` | Color saturation varies with volume |
| `Heatmap` | Heat map coloring |
| `GrayScaleHeatmap` | Grayscale heat map |
| `Custom` | Custom coloring logic |

---

## Signals & Strategy

### SignalDirection

**Namespace:** `MZpack.NT8.Algo`

| Value | Description |
|---|---|
| `None` | Signal has not been found |
| `Long` | Long direction |
| `Short` | Short direction |
| `Any` | Both directions — resulting direction determined by other signals/filters |

### SignalCalculate

**Namespace:** `MZpack.NT8.Algo`

| Value | Description |
|---|---|
| `OnEachTick` | Calculate signal on each tick |
| `OnBarClose` | Calculate signal on bar close |
| `NotApplicable` | Not applicable (e.g., Level 2 signals) |

### Logic

**Namespace:** `MZpack.NT8.Algo`

Logical operator for combining nodes in a decision tree.

| Value | Description |
|---|---|
| `And` | All child nodes must be satisfied |
| `Or` | At least one child node must be satisfied |
| `Conjunction` | Logical conjunction |

### MarketDataSource

**Namespace:** `MZpack.NT8.Algo`

| Value | Description |
|---|---|
| `None` | No data source |
| `Level1` | Level 1 event (trade/tick data) |
| `Level2` | Market depth event |
| `Custom` | Custom event |

### PatternType

**Namespace:** `MZpack.NT8.Algo`

| Value | Description |
|---|---|
| `Entry` | Entry pattern — opens a new position |
| `Exit` | Exit pattern — closes current position |
| `Reversal` | Reversal pattern — closes and opens opposite |
| `ScaleIn` | Scale-in pattern — adds to current position |
| `ScaleOut` | Scale-out pattern — partially closes position |

### PositionState

**Namespace:** `MZpack.NT8.Algo` | `[Flags]`

| Value | Bit | Description |
|---|---|---|
| `Flat` | 1 | No position |
| `EntrySubmitting` | 4 | Entry order submitted |
| `LongLimitPending` | 8 | Pending buy limit orders, none filled |
| `ShortLimitPending` | 16 | Pending sell limit orders, none filled |
| `Long` | 32 | Buy orders filled |
| `Short` | 64 | Sell orders filled |
| `LongMarketPending` | 128 | Pending buy market order |
| `ShortMarketPending` | 256 | Pending sell market order |
| `LimitPending` | — | `LongLimitPending \| ShortLimitPending` |
| `Filled` | — | `Long \| Short` |
| `Longs` | — | `LongLimitPending \| LongMarketPending \| Long` |
| `Shorts` | — | `ShortLimitPending \| ShortMarketPending \| Short` |
| `NoDirection` | — | `Flat \| EntrySubmitting` |

### StrategyOperating

**Namespace:** `MZpack.NT8.Algo`

| Value | Description |
|---|---|
| `Auto` | Entries are made automatically |
| `Manual` | Entries must be made manually from Chart Trader |

### PositionManagement

**Namespace:** `MZpack.NT8.Algo`

| Value | Description |
|---|---|
| `MZpack` | Position managed by MZpack API |
| `NinjaTraderATM` | Position managed by NinjaTrader ATM template |

### OppositePatternAction

**Namespace:** `MZpack.NT8.Algo`

What happens when a pattern in the opposite direction is validated while a position is open.

| Value | Description |
|---|---|
| `None` | Keep current position, do nothing |
| `Close` | Close current position |
| `Reverse` | Close and open opposite position using the configured `EntryMethod` |
| `Unmanaged` | Position managed by signals — signals continue calculating after entry, enabling scale-in |

### OrdersHandlingApproach

**Namespace:** `MZpack.NT8.Algo`

| Value | Description |
|---|---|
| `Managed` | NinjaTrader managed order handling |
| `Unmanaged` | NinjaTrader unmanaged order handling |

### LogLevel

**Namespace:** `MZpack.NT8.Algo` | `[Flags]`

| Value | Bit | Description |
|---|---|---|
| `NONE` | 0 | No logging |
| `NV_PATTERN_OBC` | 1 | Log not-validated patterns on bar close (for debugging) |
| `V_PATTERN` | 8 | Log validated patterns |
| `ORDER` | 16 | Log orders (Submitted, Working, Filled, PartFilled, Cancelled, Rejected) |
| `ENTRY` | 32 | Log strategy entries |
| `POSITION` | 64 | Log position state changes |
| `PROPERTIES` | 128 | Log NinjaScriptProperty values |
| `ALL` | — | All flags combined |

### LogTarget

**Namespace:** `MZpack.NT8.Algo` | `[Flags]`

| Value | Bit | Description |
|---|---|---|
| `None` | 0 | No logging |
| `File` | 1 | Log to `\NinjaTrader 8\mzpacklog` folder |
| `NinjaScriptOutput` | 2 | Log to NinjaScript Output window |
| `All` | — | `File \| NinjaScriptOutput` |

---

## Entry / Exit

### EntryMethod

**Namespace:** `MZpack.NT8.Algo`

| Value | Description |
|---|---|
| `Market` | Enter by market order |
| `Limit` | Enter by limit order |
| `StopLimit` | Enter by stop-limit order |

### CancelLimitOrderType

**Namespace:** `MZpack.NT8.Algo`

When to cancel a pending limit order.

| Value | Description |
|---|---|
| `None` | Never auto-cancel |
| `Ticks` | Cancel after price moves N ticks away |
| `Bars` | Cancel after N bars |
| `Milliseconds` | Cancel after N milliseconds |

---

## Export

### ExportTemporality

**Namespace:** `MZpack.NT8.Algo.DataExport` | `[Flags]`

| Value | Description |
|---|---|
| `Historical` | Export historical bar data |
| `Realtime` | Export data in real time |

### ExportDataSource

**Namespace:** `MZpack.NT8.Algo.DataExport`

| Value | Description |
|---|---|
| `Level1` | Level 1 (trade/tick) data |
| `Level2` | Level 2 (market depth) data |
| `Custom` | Custom data source |

### ExportGranularity

**Namespace:** `MZpack.NT8.Algo.DataExport`

| Value | Description |
|---|---|
| `Tick` | One row per tick |
| `Bar` | One row per bar |
| `Update` | One row per update event |

### ExportMode

**Namespace:** `MZpack.NT8.Algo.DataExport`

| Value | Description |
|---|---|
| `Save` | Write data to output |
| `Load` | Read data from file |

### IndValue

**Namespace:** `MZpack.NT8.Algo.DataExport`

See [ValueDescriptor — IndValue](../data-export/value-descriptor.md#indvalue-enum) for the complete list of 100+ indicator value identifiers.

### ValueKind

**Namespace:** `MZpack.NT8.Algo.DataExport`

| Value | Description |
|---|---|
| `Feature` | Input/feature column (exported before labels) |
| `Label` | Target/label column (exported after features) |
| `Internal` | Internal column (not exported, used for intermediate calculations) |

### ValueSorce

**Namespace:** `MZpack.NT8.Algo.DataExport`

:::note
The enum name contains a typo (`ValueSorce` instead of `ValueSource`) in the source code.
:::

| Value | Description |
|---|---|
| `Indicator` | Value from an indicator |
| `DrawingObject` | Value mapped from a chart drawing object |
| `Calculate` | Value computed by a user-provided delegate |
| `DataSet` | Value referenced from another DataSet column |
