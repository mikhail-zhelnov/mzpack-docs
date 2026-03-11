---
sidebar_position: 2
title: "IIndicator"
description: "Reference for IIndicator — the root interface for all MZpack indicators, providing chart access, candle data, price utilities, and lifecycle state."
---

# IIndicator

Root interface for all MZpack indicators. Defines the contract for chart interaction, candle data access, price arithmetic, lifecycle state, and logging.

**Namespace:** `MZpack`

## Candle & Bar Data

| Method | Returns | Description |
|---|---|---|
| `GetCandle(int ago)` | `ICandle` | Get candle N bars ago (0 = current) |
| `GetCandleByBarIdx(int barIdx)` | `ICandle` | Get candle by absolute bar index |
| `GetCandleByBarIdx(int dataSeriesIdx, int barIdx)` | `ICandle` | Get candle from a specific data series |
| `GetBarHigh(int idx)` | `double` | Bar high price by index |
| `GetBarLow(int idx)` | `double` | Bar low price by index |
| `GetBarTime(int idx)` | `DateTime` | Bar time by index |
| `GetBarTime(int idx, int barsIdx)` | `DateTime` | Bar time from a specific bars series |

## Price Utilities

| Method | Returns | Description |
|---|---|---|
| `RoundToTickSize(double)` | `double` | Round price to nearest tick |
| `PriceDiffTicks(double, double)` | `int` | Difference between two prices in ticks |
| `PriceAddTicks(double, int)` | `double` | Add N ticks to a price |
| `PriceAddTick(double)` | `double` | Add one tick |
| `PriceSubtractTick(double)` | `double` | Subtract one tick |
| `Compare(double, double)` | `int` | Compare two prices (−1, 0, 1) |
| `GetCurrentBid()` | `double` | Current best bid |
| `GetCurrentAsk()` | `double` | Current best ask |

## Chart Coordinate Conversion

| Method | Returns | Description |
|---|---|---|
| `GetYByPrice(double)` | `float` | Convert price to Y pixel coordinate |
| `GetValueByY(float)` | `double` | Convert Y pixel to price value |
| `GetXByBarIdx(int)` | `float` | Convert bar index to X pixel |
| `GetBarIdxByX(float)` | `int` | Convert X pixel to bar index |
| `GetXByTime(DateTime)` | `int` | Convert time to X pixel |
| `GetTimeByX(int)` | `DateTime` | Convert X pixel to time |
| `GetBarIdXByTime(DateTime)` | `int` | Convert time to bar index |
| `GetCloseTimeByBarIdx(int)` | `DateTime` | Bar close time by index |
| `GetTickHeight()` | `float` | Height of one tick in pixels |
| `GetBarWidth()` | `float` | Width of one bar in pixels |
| `GetBarSpace()` | `float` | Spacing between bars |
| `GetChartBounds()` | `RectangleF` | Chart area bounds |

## Lifecycle State

| Property | Type | Description |
|---|---|---|
| `IsConnected` | `bool` | Data connection is active |
| `IsRealtime` | `bool` | Indicator is in real-time mode |
| `IsWorking` | `bool` | Indicator is actively processing |
| `IsTickReplay` | `bool` | Tick Replay is enabled |
| `IsOnBarClose` | `bool` | Calculate on bar close (vs each tick) |
| `IsHistoricalBidAsk` | `bool` | Historical bid/ask data available |
| `UsageMode` | `IndicatorMode` | `Chart` or `Strategy` |
| `WorkingTimeFilter` | `bool` | Working time filter is active |
| `HasInstrument` | `bool` | Instrument is assigned |

## Bar Context

| Property | Type | Description |
|---|---|---|
| `__CurrentBar` | `int` | Current bar index |
| `__BarsInProgress` | `int` | Index of the data series currently being processed |
| `__IsFirstTickOfBar` | `bool` | Current tick is the first of a new bar |
| `__IsFirstBarOfSession` | `bool` | Current bar is the first of the session |
| `__TickSize` | `double` | Instrument tick size |
| `Is1TickChart` | `bool` | Chart uses 1-tick bar type |
| `IsMinuteChart` | `bool` | Chart uses minute bar type |
| `ChartBarsPeriodSeconds` | `int` | Bar period in seconds |
| `ChartBarsValue` | `int` | Bar period value |
| `DataSeriesIndex` | `int` | Data series index for multi-series strategies |

## Data Model

| Property | Type | Description |
|---|---|---|
| `ModelIncrementRefresh` | `ModelIncrementRefresh` | How data model is refreshed: `Realtime` or `HistoricalRealtime` |
| `ModelRefreshGranularity` | `ModelRefreshGranularity` | Refresh granularity: `Tick`, `Bar`, or `ModelItem` |
| `CalcModelItemWhileCollecting` | `CalculateModelItem` | When to calculate: `OnEachTick` or `OnBarClose` |

## Rendering & UI

| Property / Method | Type | Description |
|---|---|---|
| `Visible` | `bool` | Indicator visibility on chart |
| `__IsOverlay` | `bool` | Render as overlay on price panel |
| `__MinValue` / `__MaxValue` | `double` | Y-axis range |
| `ChartRightMargin` | `int` | Right margin in pixels |
| `ForceRefreshChart()` | `void` | Force immediate chart repaint |
| `RefreshChart()` | `void` | Request chart repaint |
| `InvalidateChartVisual()` | `void` | Invalidate chart visual |
| `Sync` | `object` | Lock object for thread-safe access |

## Logging

| Method | Description |
|---|---|
| `__Print(string)` | Print to NinjaScript Output |
| `LogInformation(string)` | Log info message |
| `LogWarning(string)` | Log warning |
| `LogAlert(string)` | Log alert |
| `LogError(string)` | Log error |
| `LogException(Exception)` | Log exception |
| `DefaultAlert(string, string)` | Trigger default alert with message and sound file |
| `ShowMessage(string, MessageBoxImage)` | Show message box |

## Notification

| Method | Description |
|---|---|
| `Notify(QuoteEventArgs)` | Notify indicator of a quote update |
| `Notify(ExecutionEventArgs)` | Notify of a trade execution |
| `Notify(Trade)` | Notify of a reconstructed trade |
| `Notify(Notification)` | Send a custom notification |

## IndicatorMode Enum

| Value | Description |
|---|---|
| `Chart` | Indicator runs on a chart |
| `Strategy` | Indicator runs inside a strategy |

## Derived Interfaces

| Interface | Adds |
|---|---|
| [ITickIndicator / IOrderFlowIndicator](iorderflow-indicator.md) | Market data, order flow configuration |
| [ILevelsIndicator](ilevelsindicator.md) | Interactive horizontal price levels |
