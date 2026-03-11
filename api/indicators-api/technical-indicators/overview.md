---
sidebar_position: 1
title: "Technical Indicators"
description: "Reference for StrategyPlotIndicator and built-in technical indicator wrappers (ATR, EMA, SMA, MACD, etc.) for use in MZpack strategies."
---

# Technical Indicators

MZpack provides wrapper classes around standard NinjaTrader technical indicators for use inside MZpack strategies. These wrappers extend `StrategyPlotIndicator` and integrate with the MZpack indicator lifecycle, chart rendering, and data export systems.

**Namespace:** `MZpack.NT8.Algo.Indicators`

:::tip
These indicators are wrappers for use inside MZpack strategies only. For chart-based indicators use NinjaTrader's built-in equivalents.
:::

## Base Classes

### StrategyDataSeriesIndicator

**Inheritance:** `StrategyDataSeriesIndicator : ExportedIndicator`

Abstract base for data series indicators. Provides input/output series management and bar indexing.

| Property / Method | Type | Description |
|---|---|---|
| `Input` | `ISeries<double>` | NinjaTrader input data series |
| `MZpackInput` | `Series<double>` | Alternative MZpack input series |
| `Values` | `Series<double>[]` | Output data series array (by index) |
| `GetCurrentBar()` | `int` | Current bar index adjusted for calculation mode |
| `GetAgo(int)` | `int` | Bar-ago offset adjusted for calculation mode |
| `GetInput(int)` | `double` | Input value at ago offset |

### StrategyPlotIndicator

**Inheritance:** `StrategyPlotIndicator : StrategyDataSeriesIndicator`

Abstract base that adds chart rendering capabilities — can display as overlay on the price chart or on a separate panel.

| Property | Type | Default | Description |
|---|---|---|---|
| `IsOnPanel` | `bool` | `false` | Render on a separate panel |
| `IsUpperPanel` | `bool` | `false` | Panel above the chart (vs below) |
| `PanelHeight` | `float` | 200 | Panel height in pixels |
| `PanelMargin` | `float` | 0 | Margin between chart edge and panel |
| `Strokes` | `Stroke[]` | — | Stroke styles for each plot line |
| `PlotStyles` | `PlotStyle[]` | — | Plot styles for each line |
| `BackBrush` | `Brush` | — | Panel background color |
| `BackBrushOpacity` | `int` | 20 | Background opacity (1–100) |

## Built-in Indicators

All constructors follow the pattern:

```csharp
new IndicatorName(MZpackStrategyBase strategy, ISeries<double> input, int period)
```

Output values are accessed via `Values[0]` (primary), `Values[1]`, `Values[2]` for multi-output indicators.

### Moving Averages

| Class | NinjaTrader Equivalent | Period Default | Description |
|---|---|---|---|
| `EMA` | EMA | 14 | Exponential Moving Average |
| `SMA` | SMA | 14 | Simple Moving Average |
| `WMA` | WMA | 14 | Weighted Moving Average |
| `LinReg` | LinReg | 14 | Linear Regression |

### Oscillators & Momentum

| Class | NinjaTrader Equivalent | Parameters | Description |
|---|---|---|---|
| `CCI` | CCI | Period (14) | Commodity Channel Index. Separate panel |
| `MACD` | MACD | Fast (12), Slow (26), Smooth (9) | Values[0] = MACD, Values[1] = Signal, Values[2] = Histogram. Separate panel |
| `Momentum` | Momentum | Period (14) | Rate of change of price |

### Volatility & Channels

| Class | NinjaTrader Equivalent | Period Default | Description |
|---|---|---|---|
| `ATR` | ATR | 14 | Average True Range. Separate panel |
| `DonchianChannel` | DonchianChannel | 14 | Values[0] = Mid, Values[1] = High, Values[2] = Low |

### Price Reference

| Class | Description |
|---|---|
| `CurrentDayOHL` | Values[0] = Open, Values[1] = High, Values[2] = Low. Intraday bars only |

### Series Math

| Class | NinjaTrader Equivalent | Description |
|---|---|---|
| `MAX` | MAX | Maximum of last N values |
| `MIN` | MIN | Minimum of last N values |
| `SUM` | SUM | Sum of last N values |

## Example

```csharp
// Inside OnCreateIndicators
var ema = new EMA(this, Close, 20);
var atr = new ATR(this, Close, 14);

// Access values in OnBarUpdate or signal logic
double currentEma = ema.Values[0].GetAgo(0);
double currentAtr = atr.Values[0].GetAgo(0);
```

## See Also

- [Technical Indicators sample](../../samples/technical-indicators.md) — complete working example
