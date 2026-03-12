---
sidebar_position: 21
title: "Technical Indicators"
description: "EMA, ATR, and MACD technical indicators within an MZpack strategy."
---

# Technical Indicators

Demonstrates how to use well-known technical indicators (EMA, ATR, MACD) within MZpack strategies. On bar close, prints values from all three indicators.

**Source:** `[INSTALL PATH]/API/Samples/Built-in/MZpackTechnicalSample0.cs`
**Class:** `MZpackTechnicalSample0 : MZpackStrategyBase`

## What It Covers

- EMA with configurable period, custom stroke, and `PlotStyle.Dot`
- ATR on a separate panel (`IsOnPanel`, `PanelHeight`, `IsUpperPanel`)
- MACD with 3 plot series (MACD line, signal, histogram)
- `OnBarCloseHandler` accessing indicator values via `Values[n][barIdx]`
- `WorkingStateHistorical = true` for backtesting

## Indicator Setup

```csharp
ema = new EMA(this, Close, EMA_Period);
ema.Calculate = Calculate.OnBarClose;
ema.Strokes[0] = new Stroke(System.Windows.Media.Brushes.Yellow);
ema.PlotStyle = PlotStyle.Dot;
ema.Visible = true;

atr = new ATR(this, Close, 14);
atr.Calculate = Calculate.OnBarClose;
atr.Strokes[0] = new Stroke(System.Windows.Media.Brushes.DarkCyan);
atr.IsOnPanel = true;
atr.PanelHeight = 300;
atr.IsUpperPanel = false;

macd = new MACD(this, Close);
macd.Calculate = Calculate.OnBarClose;
macd.IsUpperPanel = true;
macd.Strokes[0] = new Stroke(System.Windows.Media.Brushes.Blue);
macd.Strokes[1] = new Stroke(System.Windows.Media.Brushes.Red);
macd.Strokes[2] = new Stroke(System.Windows.Media.Brushes.Green);
```

## Accessing Values

`Values[n]` is a dictionary indexed by bar index. Check `ContainsKey` before access to avoid key-not-found errors:

```csharp
protected void StrategyOnBarCloseHandler(MarketDataEventArgs e, int currentBarIdx)
{
    Print(string.Format("{0}:  EMA = {1}  ATR = {2}  MACD = {3}, {4}, {5}",
        currentBarIdx,
        ema.Values[0].ContainsKey(currentBarIdx) ? ema.Values[0][currentBarIdx] : 0,
        atr.Values[0].ContainsKey(currentBarIdx) ? atr.Values[0][currentBarIdx] : 0,
        macd.Values[0].ContainsKey(currentBarIdx) ? macd.Values[0][currentBarIdx] : 0,
        macd.Values[1].ContainsKey(currentBarIdx) ? macd.Values[1][currentBarIdx] : 0,
        macd.Values[2].ContainsKey(currentBarIdx) ? macd.Values[2][currentBarIdx] : 0
    ));
}
```

## Key Points

- `Values[n]` is a dictionary indexed by bar index (not "ago" values)
- Check `Values[n].ContainsKey(barIdx)` before access to avoid key-not-found errors
- `WorkingStateHistorical = true` enables `OnBarCloseHandler` for historical bars (required for backtesting)

## Configurable Properties

| Property | Default | Description |
|---|---|---|
| `EMA_Period` | `14` | EMA period |
| `CCI_Period` | `14` | CCI period (indicator creation commented out) |
| `MACD_Period` | `14` | MACD period |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Custom Plots](custom-plots.md) — custom chart plots
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
